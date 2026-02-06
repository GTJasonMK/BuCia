#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量对 PNG 做 alpha bleed + 软边羽化。

用法示例：
  python alpha_bleed_feather.py --in "game/images/anime" --out "game/images/anime_processed" --bleed 2 --feather 0.8
  python alpha_bleed_feather.py --in "game/images/anime" --in-place --bleed 3 --feather 0.6
  python alpha_bleed_feather.py --in "game/images/anime" --out "game/images/anime_processed" --base-map "tools/alpha_bleed_map.json"
  python alpha_bleed_feather.py --in "asset/anime" --out "game/images/anime" --base-map "tools/alpha_bleed_map.json" --crop "0,0,2813,2500" --scale 0.45

依赖：Pillow（PIL）
"""

from __future__ import annotations

import argparse
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path
import os
import uuid

try:
    from PIL import Image, ImageFilter, ImageFile
except Exception as exc:  # pragma: no cover
    print("缺少 Pillow，请先安装：pip install Pillow", file=sys.stderr)
    raise


_BASE_CACHE: dict[str, Image.Image] = {}

def _parse_crop(text: str | None) -> tuple[int, int, int, int] | None:
    """
    解析裁剪参数：\"x,y,w,h\"。

    返回：(x, y, w, h)；无效/空则返回 None。
    """
    if not text:
        return None
    raw = str(text).strip()
    if not raw:
        return None
    parts = [p.strip() for p in raw.split(",")]
    if len(parts) != 4:
        raise ValueError(f"--crop 格式应为 x,y,w,h，实际为：{text}")
    x, y, w, h = (int(float(p)) for p in parts)
    if w <= 0 or h <= 0:
        raise ValueError(f"--crop 的 w/h 必须 > 0，实际为：{text}")
    return x, y, w, h


def _apply_crop_and_scale(
    image: Image.Image,
    crop: tuple[int, int, int, int] | None,
    scale: float,
) -> Image.Image:
    """对图片执行裁剪与缩放（缩放使用 LANCZOS）。"""
    out = image
    if crop:
        x, y, w, h = crop
        out = out.crop((x, y, x + w, y + h))

    if scale and float(scale) != 1.0:
        sf = float(scale)
        if sf <= 0:
            raise ValueError(f"--scale 必须 > 0，实际为：{scale}")
        w, h = out.size
        nw = max(1, int(round(w * sf)))
        nh = max(1, int(round(h * sf)))
        if (nw, nh) != out.size:
            out = out.resize((nw, nh), resample=Image.LANCZOS)
    return out


def _load_base(path: str) -> Image.Image:
    """缓存加载原立绘，避免重复读盘。"""
    if path not in _BASE_CACHE:
        _BASE_CACHE[path] = Image.open(path).convert("RGBA")
    return _BASE_CACHE[path]


def _expand_bbox(bbox: tuple[int, int, int, int], pad: int, size: tuple[int, int]) -> tuple[int, int, int, int]:
    """对 bbox 做扩张并裁剪到图片范围内。"""
    if pad <= 0:
        return bbox
    x0, y0, x1, y1 = bbox
    w, h = size
    return (
        max(0, x0 - pad),
        max(0, y0 - pad),
        min(w, x1 + pad),
        min(h, y1 + pad),
    )


def _get_alpha_bbox(image: Image.Image) -> tuple[int, int, int, int] | None:
    """返回 alpha 的非零区域 bbox。"""
    alpha = image.split()[3]
    return alpha.getbbox()


def _alpha_bleed(image: Image.Image, iterations: int) -> Image.Image:
    """对透明区域做颜色外扩，减少边缘黑边/白边。"""
    if iterations <= 0:
        return image

    img = image.copy()
    w, h = img.size
    pixels = img.load()

    bbox = _get_alpha_bbox(img)
    if not bbox:
        return img
    # 颜色外扩每次最多扩 1 像素，给足 padding 避免全图扫描
    x0, y0, x1, y1 = _expand_bbox(bbox, pad=iterations + 2, size=img.size)

    for _ in range(iterations):
        new_img = img.copy()
        new_pixels = new_img.load()

        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b, a = pixels[x, y]
                if a != 0:
                    continue

                # 从 8 邻域采样颜色
                total_r = total_g = total_b = count = 0
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if nx < 0 or ny < 0 or nx >= w or ny >= h:
                            continue
                        nr, ng, nb, na = pixels[nx, ny]
                        if na > 0:
                            total_r += nr
                            total_g += ng
                            total_b += nb
                            count += 1

                if count > 0:
                    new_pixels[x, y] = (
                        total_r // count,
                        total_g // count,
                        total_b // count,
                        0,
                    )

        img = new_img
        pixels = img.load()

    return img


def _feather_alpha(image: Image.Image, radius: float) -> Image.Image:
    """对 alpha 通道做轻度模糊，使边缘更柔和。"""
    if radius <= 0:
        return image

    r, g, b, a = image.split()
    a = a.filter(ImageFilter.GaussianBlur(radius=radius))
    return Image.merge("RGBA", (r, g, b, a))


def _unmatte_with_base(
    image: Image.Image,
    base: Image.Image,
    max_alpha: int,
    min_alpha: int,
    strength: float,
    resize_if_needed: bool,
) -> Image.Image:
    """
    基于原立绘“去底色/去光晕”（unmatte）。

    常见问题：序列帧贴片的半透明边缘像素 RGB 里混入了导出时的底色（白/黑/任意背景），
    叠到原立绘上会出现亮度不一致的“缝合边缘”。这里利用原立绘同位置像素作为 matte 背景，
    反推更接近真实前景色：C = (S - B*(1-a)) / a。
    """
    if max_alpha <= 0 or strength <= 0:
        return image

    max_alpha = max(0, min(255, int(max_alpha)))
    min_alpha = max(1, min(255, int(min_alpha)))
    strength = max(0.0, min(1.0, float(strength)))

    if image.size != base.size:
        if not resize_if_needed:
            raise ValueError(f"尺寸不一致：overlay={image.size} base={base.size}")
        base = base.resize(image.size, resample=Image.LANCZOS)

    img = image.copy()
    pixels = img.load()
    base_pixels = base.load()

    bbox = _get_alpha_bbox(img)
    if not bbox:
        return img

    x0, y0, x1, y1 = bbox
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = pixels[x, y]
            if a <= 0 or a > max_alpha:
                continue

            br, bg, bb, _ = base_pixels[x, y]

            # alpha 太小时 unmatte 会放大噪点，直接用 base 颜色兜底
            if a < min_alpha:
                pixels[x, y] = (br, bg, bb, a)
                continue

            af = a / 255.0
            inv = 1.0 - af

            cr = (r - br * inv) / af
            cg = (g - bg * inv) / af
            cb = (b - bb * inv) / af

            # clamp 到 0..255
            cr = 0.0 if cr < 0.0 else 255.0 if cr > 255.0 else cr
            cg = 0.0 if cg < 0.0 else 255.0 if cg > 255.0 else cg
            cb = 0.0 if cb < 0.0 else 255.0 if cb > 255.0 else cb

            nr = r * (1.0 - strength) + cr * strength
            ng = g * (1.0 - strength) + cg * strength
            nb = b * (1.0 - strength) + cb * strength

            pixels[x, y] = (int(round(nr)), int(round(ng)), int(round(nb)), a)

    return img


def _apply_base_color(
    image: Image.Image,
    base: Image.Image,
    threshold: int,
    resize_if_needed: bool,
    pad: int = 0,
) -> Image.Image:
    """用原立绘颜色覆盖透明/半透明边缘，减少缝合痕迹。"""
    if threshold <= 0:
        return image

    if image.size != base.size:
        if not resize_if_needed:
            raise ValueError(f"尺寸不一致：overlay={image.size} base={base.size}")
        base = base.resize(image.size, resample=Image.LANCZOS)

    img = image.copy()
    w, h = img.size
    pixels = img.load()
    base_pixels = base.load()

    alpha = img.split()[3]
    bbox = alpha.getbbox()
    if not bbox:
        return img

    x0, y0, x1, y1 = _expand_bbox(bbox, pad=pad, size=img.size)
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = pixels[x, y]
            if a <= threshold:
                br, bg, bb, _ = base_pixels[x, y]
                pixels[x, y] = (br, bg, bb, a)

    return img


def process_file(
    src: Path,
    dst: Path,
    bleed: int,
    feather: float,
    base_path: str | None,
    base_threshold: int,
    base_pad: int,
    base_resize: bool,
    unmatte: bool,
    unmatte_max_alpha: int,
    unmatte_min_alpha: int,
    unmatte_strength: float,
    crop: tuple[int, int, int, int] | None,
    scale: float,
) -> None:
    try:
        image = Image.open(src).convert("RGBA")
    except Exception as exc:
        # Pillow 在损坏/截断的 PNG 上可能抛出 struct.error/OSError 等。
        # 这里统一包装，便于上层输出具体文件路径。
        raise OSError(f"读取图片失败（可能为损坏/截断文件）：{src}") from exc

    # 先裁剪/缩放到最终分辨率（用于让游戏内渲染更接近 GUI 的 LANCZOS 预缩放效果）
    image = _apply_crop_and_scale(image, crop, scale)

    if base_path:
        base = _load_base(base_path)
        base = _apply_crop_and_scale(base, crop, scale)
        if unmatte:
            image = _unmatte_with_base(
                image,
                base,
                max_alpha=unmatte_max_alpha,
                min_alpha=unmatte_min_alpha,
                strength=unmatte_strength,
                resize_if_needed=base_resize,
            )

    # 没有透明通道时不需要做 bleed/feather/base 处理，但仍需保留裁剪/缩放结果
    if image.getextrema()[3] != (255, 255):
        image = _alpha_bleed(image, bleed)
        image = _feather_alpha(image, feather)
    if base_path:
        if image.getextrema()[3] != (255, 255):
            # feather 会让边缘产生新的低 alpha 像素，最后再用 base 覆盖一遍更稳
            auto_pad = max(bleed + 2, int(feather * 3) + 2)
            pad = auto_pad if base_pad < 0 else base_pad
            image = _apply_base_color(image, base, base_threshold, base_resize, pad=pad)

    dst.parent.mkdir(parents=True, exist_ok=True)
    # 写入使用临时文件再原子替换，避免处理中途异常导致目标文件被写坏/截断
    # Pillow 会通过文件扩展名推断格式，因此临时文件也保留 .png 后缀
    suffix = dst.suffix or ".png"
    tmp = dst.with_name(f"{dst.stem}.tmp.{os.getpid()}.{uuid.uuid4().hex}{suffix}")
    try:
        image.save(tmp, format="PNG")
        os.replace(tmp, dst)
    finally:
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass


def _process_task(
    task: tuple[str, str, int, float, str | None, int, int, bool, bool, int, int, float, tuple[int, int, int, int] | None, float]
) -> tuple[bool, str, str]:
    (
        src_str,
        dst_str,
        bleed,
        feather,
        base_path,
        base_threshold,
        base_pad,
        base_resize,
        unmatte,
        unmatte_max_alpha,
        unmatte_min_alpha,
        unmatte_strength,
        crop,
        scale,
    ) = task
    src = Path(src_str)
    dst = Path(dst_str)
    try:
        process_file(
            src,
            dst,
            bleed,
            feather,
            base_path,
            base_threshold,
            base_pad,
            base_resize,
            unmatte,
            unmatte_max_alpha,
            unmatte_min_alpha,
            unmatte_strength,
            crop,
            scale,
        )
        return True, str(dst), ""
    except Exception as exc:
        return False, str(src), f"{type(exc).__name__}: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser(description="批量 alpha bleed + 软边羽化")
    parser.add_argument("--in", dest="input_dir", required=True, help="输入目录")
    parser.add_argument("--out", dest="output_dir", help="输出目录（不传则原地覆盖）")
    parser.add_argument("--in-place", action="store_true", help="原地覆盖（优先级高于 --out）")
    parser.add_argument("--bleed", type=int, default=2, help="颜色外扩像素数（1-4 常用）")
    parser.add_argument("--feather", type=float, default=0.8, help="alpha 羽化半径（0.5-1.0 常用）")
    parser.add_argument("--glob", dest="glob_pattern", default="*.png", help="匹配规则")
    parser.add_argument("--base-image", dest="base_image", help="原立绘路径（单角色批处理）")
    parser.add_argument("--base-map", dest="base_map", help="JSON 映射：子目录名 -> 原立绘路径")
    parser.add_argument("--base-threshold", type=int, default=12, help="边缘覆盖阈值（0-255）")
    parser.add_argument("--crop", type=str, default="", help="裁剪区域：\"x,y,w,h\"（可选）")
    parser.add_argument("--scale", type=float, default=1.0, help="缩放倍率（可选，缩放使用 LANCZOS）")
    parser.add_argument(
        "--base-pad",
        type=int,
        default=-1,
        help="base 覆盖 bbox 额外 padding（像素）。-1 表示自动",
    )
    parser.add_argument(
        "--no-base-resize",
        action="store_true",
        help="当尺寸不一致时不缩放原立绘（将直接报错）",
    )
    parser.add_argument(
        "--no-unmatte",
        dest="unmatte",
        action="store_false",
        help="关闭 unmatte（默认开启，仅在提供 base 时生效）",
    )
    parser.set_defaults(unmatte=True)
    parser.add_argument(
        "--unmatte-max-alpha",
        type=int,
        default=220,
        help="unmatte 处理上限 alpha（0-255，越大影响范围越大）",
    )
    parser.add_argument(
        "--unmatte-min-alpha",
        type=int,
        default=8,
        help="unmatte 处理下限 alpha（0-255，越小越可能放大噪点）",
    )
    parser.add_argument(
        "--unmatte-strength",
        type=float,
        default=1.0,
        help="unmatte 强度（0-1）",
    )
    parser.add_argument("--workers", type=int, default=0, help="并发进程数（0 表示自动）")
    parser.add_argument(
        "--allow-truncated",
        action="store_true",
        help="允许加载被截断的 PNG（不推荐，仅用于抢救素材）",
    )
    args = parser.parse_args()

    if args.allow_truncated:
        ImageFile.LOAD_TRUNCATED_IMAGES = True

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"输入目录不存在：{input_dir}", file=sys.stderr)
        return 1

    if args.in_place:
        output_dir = input_dir
    else:
        output_dir = Path(args.output_dir) if args.output_dir else input_dir

    files = sorted(input_dir.rglob(args.glob_pattern))
    if not files:
        print("未找到任何图片文件。", file=sys.stderr)
        return 1

    base_map: dict[str, str] = {}
    if args.base_map:
        base_map = json.loads(Path(args.base_map).read_text(encoding="utf-8"))

    tasks: list[tuple[str, str, int, float, str | None, int, int, bool, bool, int, int, float, tuple[int, int, int, int] | None, float]] = []
    crop = _parse_crop(args.crop)
    for src in files:
        rel = src.relative_to(input_dir)
        dst = output_dir / rel
        base_path: str | None = None
        if args.base_image:
            base_path = args.base_image
        elif base_map:
            root_name = rel.parts[0] if rel.parts else ""
            base_path = base_map.get(root_name)

        tasks.append(
            (
                str(src),
                str(dst),
                args.bleed,
                args.feather,
                base_path,
                args.base_threshold,
                args.base_pad,
                not args.no_base_resize,
                args.unmatte,
                args.unmatte_max_alpha,
                args.unmatte_min_alpha,
                args.unmatte_strength,
                crop,
                float(args.scale),
            )
        )

    workers = args.workers if args.workers and args.workers > 0 else None
    errors: list[tuple[str, str]] = []
    with ProcessPoolExecutor(max_workers=workers) as executor:
        future_map = {executor.submit(_process_task, task): task for task in tasks}
        for future in as_completed(future_map):
            ok, path, err = future.result()
            if ok:
                print(f"处理完成: {path}")
            else:
                errors.append((path, err))
                print(f"处理失败: {path}\n  {err}", file=sys.stderr)

    if errors:
        print(f"处理结束：失败 {len(errors)} 个文件。", file=sys.stderr)
        return 1

    print("全部处理完成。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
