#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
离线"先拼接再缩放（LANCZOS）"烘焙角色说话立绘。

目的：
- 游戏里如果交给 Ren'Py/GPU 做大倍率缩放，会再次放大半透明边缘的缝合痕迹。
- 因此把"拼接 + 缩放"离线完成，游戏内只做帧切换（几乎不再二次采样）。

合成方式：
- 使用标准的 PIL alpha_composite，与 alpha_bleed_gui.py 保持一致。
- 前提：序列帧已经由 alpha_bleed_feather.py 做了预处理（unmatte、bleed、feather），
  修复了边缘颜色污染问题。

输出规范：
- 所有变体（normal/active/dim）输出相同尺寸的画布
- active/dim 在画布内居中缩放，避免切换时画布大小跳变

输入：
- 已处理好的贴片帧：game/images/anime/**.png（alpha_bleed_feather.py 的输出）
- 原角色立绘：game/images/characters/*.png
- 映射：tools/alpha_bleed_map.json（子目录名 -> 原立绘路径）

输出：
- game/images/characters_baked/<tag>/
  - 有眼睛+嘴巴帧：生成 e{ei}_m{mi}.png，并额外生成 idle.png（等同 e0_m0）
  - 只有"表情序列"：保留原文件名输出，并额外生成 idle.png（等同第一帧）

用法示例：
  python tools/bake_character_composites.py
  python tools/bake_character_composites.py --scale 0.32 --crop "0,0,2813,2500"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
except Exception as exc:  # pragma: no cover
    print("缺少依赖，请先安装：pip install Pillow numpy", file=sys.stderr)
    raise


def _parse_crop(text: str) -> tuple[int, int, int, int]:
    raw = str(text or "").strip()
    if not raw:
        raise ValueError("--crop 不能为空，格式应为 x,y,w,h")
    parts = [p.strip() for p in raw.split(",")]
    if len(parts) != 4:
        raise ValueError(f"--crop 格式应为 x,y,w,h，实际为：{text}")
    x, y, w, h = (int(float(p)) for p in parts)
    if w <= 0 or h <= 0:
        raise ValueError(f"--crop 的 w/h 必须 > 0，实际为：{text}")
    return x, y, w, h


def _save_atomic(image: Image.Image, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(f"{dst.stem}.tmp.{os.getpid()}.{uuid.uuid4().hex}{dst.suffix or '.png'}")
    try:
        image.save(tmp, format="PNG")
        os.replace(tmp, dst)
    finally:
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass


def _crop_half(image: Image.Image, crop: tuple[int, int, int, int]) -> Image.Image:
    x, y, w, h = crop
    return image.crop((x, y, x + w, y + h))


def _standard_composite(
    base: Image.Image,
    overlay: Image.Image,
) -> Image.Image:
    """
    标准 alpha 合成：与 GUI 工具保持一致。

    使用 PIL 的 alpha_composite，前提是 alpha_bleed_feather.py 已经对序列帧
    做了预处理（unmatte、bleed、feather），修复了边缘颜色污染问题。
    """
    if base.size != overlay.size:
        raise ValueError(f"尺寸不一致：base={base.size} overlay={overlay.size}")

    return Image.alpha_composite(base, overlay)


def _scale(image: Image.Image, scale: float) -> Image.Image:
    sf = float(scale)
    if sf <= 0:
        raise ValueError(f"--scale 必须 > 0，实际为：{scale}")
    if sf == 1.0:
        return image
    w, h = image.size
    nw = max(1, int(round(w * sf)))
    nh = max(1, int(round(h * sf)))
    if (nw, nh) == image.size:
        return image
    return image.resize((nw, nh), resample=Image.LANCZOS)


def _scale_centered(image: Image.Image, target_size: tuple[int, int], content_scale: float) -> Image.Image:
    """
    缩放图像内容并居中放置在目标尺寸的画布中。

    用于 active/dim 变体：在统一尺寸的画布中，内容做缩放但画布大小不变。
    """
    target_w, target_h = target_size

    if content_scale == 1.0:
        # 不缩放，直接返回（如果尺寸匹配）或裁剪/填充到目标尺寸
        if image.size == target_size:
            return image
        # 居中裁剪或填充
        result = Image.new("RGBA", target_size, (0, 0, 0, 0))
        paste_x = (target_w - image.width) // 2
        paste_y = (target_h - image.height) // 2
        result.paste(image, (paste_x, paste_y))
        return result

    # 缩放内容
    scaled_w = int(round(image.width * content_scale))
    scaled_h = int(round(image.height * content_scale))
    scaled = image.resize((scaled_w, scaled_h), resample=Image.LANCZOS)

    # 创建目标尺寸画布，居中放置缩放后的内容
    result = Image.new("RGBA", target_size, (0, 0, 0, 0))
    paste_x = (target_w - scaled_w) // 2
    paste_y = (target_h - scaled_h) // 2
    result.paste(scaled, (paste_x, paste_y))

    return result


def _infer_input_scale(
    sample_size: tuple[int, int],
    base_full_size: tuple[int, int],
    crop: tuple[int, int, int, int],
) -> tuple[str, float]:
    """
    推断贴片帧输入形态与相对 half-body 的缩放倍率。

    返回：(mode, input_scale)
    - mode=full_canvas：贴片与原立绘同尺寸（2813x5000），需要先裁剪半身。
    - mode=half_body：贴片已是半身尺寸（可能已缩放），无需再裁剪。
    """
    _, _, crop_w, crop_h = crop
    if sample_size == base_full_size:
        return "full_canvas", 1.0
    if sample_size == (crop_w, crop_h):
        return "half_body", 1.0

    sx = float(sample_size[0]) / float(crop_w)
    sy = float(sample_size[1]) / float(crop_h)
    if abs(sx - sy) > 0.01:
        raise ValueError(
            f"无法推断输入缩放倍率：sample={sample_size} crop={(crop_w, crop_h)} scale_x={sx:.4f} scale_y={sy:.4f}"
        )
    return "half_body", (sx + sy) * 0.5


def main() -> int:
    parser = argparse.ArgumentParser(description="烘焙角色组合帧：先拼接再缩放（LANCZOS）")
    parser.add_argument("--anime-dir", default="game/images/anime", help="已处理贴片帧目录")
    parser.add_argument("--base-map", default="tools/alpha_bleed_map.json", help="子目录名 -> 原立绘路径")
    parser.add_argument("--out-dir", default="game/images/characters_baked", help="输出目录")
    parser.add_argument("--crop", default="0,0,2813,2500", help="裁剪区域：x,y,w,h（默认取上半身）")
    parser.add_argument("--scale", type=float, default=0.32, help="缩放倍率（LANCZOS）")
    parser.add_argument("--active-zoom", type=float, default=1.05, help="说话角色额外放大倍率（相对 --scale）")
    parser.add_argument("--dim-zoom", type=float, default=0.9, help="非说话角色额外缩小倍率（相对 --scale）")
    parser.add_argument("--dim-brightness", type=float, default=0.75, help="非说话角色亮度倍率（0-1，越小越暗）")
    parser.add_argument("--skip-existing", action="store_true", help="跳过已存在文件（断点续跑）")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    anime_dir = (repo_root / args.anime_dir).resolve()
    base_map_path = (repo_root / args.base_map).resolve()
    out_dir = (repo_root / args.out_dir).resolve()
    crop = _parse_crop(args.crop)
    scale = float(args.scale)
    active_zoom = float(args.active_zoom)
    dim_zoom = float(args.dim_zoom)
    dim_brightness = float(args.dim_brightness)

    if active_zoom <= 0 or dim_zoom <= 0:
        print("--active-zoom/--dim-zoom 必须 > 0", file=sys.stderr)
        return 1
    if dim_brightness < 0 or dim_brightness > 1.0:
        print("--dim-brightness 必须在 0..1 范围内", file=sys.stderr)
        return 1

    if not anime_dir.exists():
        print(f"找不到 anime-dir：{anime_dir}", file=sys.stderr)
        return 1
    if not base_map_path.exists():
        print(f"找不到 base-map：{base_map_path}", file=sys.stderr)
        return 1

    base_map = json.loads(base_map_path.read_text(encoding="utf-8"))
    if not isinstance(base_map, dict) or not base_map:
        print("base-map 内容无效（应为非空 JSON 对象）。", file=sys.stderr)
        return 1

    total_out = 0

    def _apply_dim_brightness(image: Image.Image) -> Image.Image:
        """离线降低亮度（仅 RGB，保留 Alpha），避免运行时 alpha 变化带来的边缘问题。"""
        if dim_brightness >= 0.999:
            return image
        arr = np.array(image, dtype=np.float32)
        arr[:, :, :3] *= dim_brightness
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        return Image.fromarray(arr, "RGBA")

    for subdir_name, base_path_text in base_map.items():
        src_dir = anime_dir / str(subdir_name)
        if not src_dir.exists():
            print(f"[跳过] 找不到序列帧目录：{src_dir}")
            continue

        base_path = Path(str(base_path_text))
        if not base_path.is_absolute():
            base_path = (repo_root / base_path).resolve()
        if not base_path.exists():
            print(f"[跳过] 找不到原立绘：{base_path}（来自 {subdir_name}）")
            continue

        tag = base_path.stem
        out_tag_dir = out_dir / tag
        out_tag_dir.mkdir(parents=True, exist_ok=True)
        out_active_dir = out_tag_dir / "active"
        out_dim_dir = out_tag_dir / "dim"
        out_active_dir.mkdir(parents=True, exist_ok=True)
        out_dim_dir.mkdir(parents=True, exist_ok=True)

        base_full = Image.open(base_path).convert("RGBA")
        base_half_raw = _crop_half(base_full, crop)

        eye_files = sorted(src_dir.glob("e*.png"))
        mouth_files = sorted(src_dir.glob("m*.png"))

        # 推断输入贴片是否已裁剪/缩放
        sample_path: Path | None = None
        if eye_files:
            sample_path = eye_files[0]
        elif mouth_files:
            sample_path = mouth_files[0]
        else:
            any_png = sorted(src_dir.glob("*.png"))
            sample_path = any_png[0] if any_png else None

        if sample_path is None:
            print(f"[跳过] 目录没有 png：{src_dir}")
            continue

        sample_img = Image.open(sample_path).convert("RGBA")
        input_mode, input_scale = _infer_input_scale(sample_img.size, base_full.size, crop)
        # 用于后续所有合成的 base（与贴片同尺寸）
        base_half = base_half_raw if input_scale == 1.0 else _scale(base_half_raw, input_scale)

        # 计算统一的输出画布尺寸（基于 normal 尺寸）
        normal_factor = (scale / input_scale) if input_scale else scale
        canvas_w = int(round(base_half.width * normal_factor))
        canvas_h = int(round(base_half.height * normal_factor))
        canvas_size = (canvas_w, canvas_h)

        # 眼睛+嘴巴：生成组合帧
        if eye_files and mouth_files:
            if input_mode == "full_canvas":
                eye_imgs = [_crop_half(Image.open(p).convert("RGBA"), crop) for p in eye_files]
                mouth_imgs = [_crop_half(Image.open(p).convert("RGBA"), crop) for p in mouth_files]
            else:
                eye_imgs = [Image.open(p).convert("RGBA") for p in eye_files]
                mouth_imgs = [Image.open(p).convert("RGBA") for p in mouth_files]

            idle_out: Image.Image | None = None
            idle_active: Image.Image | None = None
            idle_dim: Image.Image | None = None
            for ei, eye_img in enumerate(eye_imgs):
                for mi, mouth_img in enumerate(mouth_imgs):
                    if eye_img.size != base_half.size or mouth_img.size != base_half.size:
                        raise ValueError(
                            f"尺寸不一致：base={base_half.size} eye={eye_img.size} mouth={mouth_img.size}（{tag}）"
                        )
                    # 标准合成（与 GUI 一致）
                    composed = _standard_composite(base_half, eye_img)
                    composed = _standard_composite(composed, mouth_img)

                    # normal：直接缩放到画布尺寸
                    normal = _scale(composed, normal_factor)

                    # active/dim：缩放内容但保持画布尺寸不变
                    active = _scale_centered(composed, canvas_size, normal_factor * active_zoom)
                    dim = _apply_dim_brightness(
                        _scale_centered(composed, canvas_size, normal_factor * dim_zoom)
                    )

                    dst = out_tag_dir / f"e{ei}_m{mi}.png"
                    if not (args.skip_existing and dst.exists()):
                        _save_atomic(normal, dst)
                        total_out += 1
                    dst_active = out_active_dir / f"e{ei}_m{mi}.png"
                    if not (args.skip_existing and dst_active.exists()):
                        _save_atomic(active, dst_active)
                        total_out += 1
                    dst_dim = out_dim_dir / f"e{ei}_m{mi}.png"
                    if not (args.skip_existing and dst_dim.exists()):
                        _save_atomic(dim, dst_dim)
                        total_out += 1

                    if idle_out is None and ei == 0 and mi == 0:
                        idle_out = normal
                        idle_active = active
                        idle_dim = dim

            # 生成 idle.png（等同 e0_m0）
            if idle_out is None:
                idle_out = _scale(base_half, normal_factor)
                idle_active = _scale_centered(base_half, canvas_size, normal_factor * active_zoom)
                idle_dim = _apply_dim_brightness(
                    _scale_centered(base_half, canvas_size, normal_factor * dim_zoom)
                )

            idle_path = out_tag_dir / "idle.png"
            if not (args.skip_existing and idle_path.exists()):
                _save_atomic(idle_out, idle_path)
                total_out += 1
            idle_active_path = out_active_dir / "idle.png"
            if not (args.skip_existing and idle_active_path.exists()):
                _save_atomic(idle_active or idle_out, idle_active_path)
                total_out += 1
            idle_dim_path = out_dim_dir / "idle.png"
            if not (args.skip_existing and idle_dim_path.exists()):
                _save_atomic(idle_dim or idle_out, idle_dim_path)
                total_out += 1

            print(f"[完成] {tag}: eye={len(eye_imgs)} mouth={len(mouth_imgs)} -> {out_tag_dir}")
            continue

        # 只有表情序列：保留文件名输出
        overlay_files = sorted([p for p in src_dir.glob("*.png") if p.is_file()])
        if not overlay_files:
            print(f"[跳过] 目录没有 png：{src_dir}")
            continue

        first_out: Image.Image | None = None
        first_active: Image.Image | None = None
        first_dim: Image.Image | None = None
        for p in overlay_files:
            overlay_img = Image.open(p).convert("RGBA")
            overlay_half = _crop_half(overlay_img, crop) if input_mode == "full_canvas" else overlay_img
            if overlay_half.size != base_half.size:
                raise ValueError(f"尺寸不一致：base={base_half.size} overlay={overlay_half.size}（{tag} {p.name}）")

            # 标准合成（与 GUI 一致）
            composed = _standard_composite(base_half, overlay_half)

            normal = _scale(composed, normal_factor)
            active = _scale_centered(composed, canvas_size, normal_factor * active_zoom)
            dim = _apply_dim_brightness(
                _scale_centered(composed, canvas_size, normal_factor * dim_zoom)
            )

            dst = out_tag_dir / p.name
            if not (args.skip_existing and dst.exists()):
                _save_atomic(normal, dst)
                total_out += 1
            dst_active = out_active_dir / p.name
            if not (args.skip_existing and dst_active.exists()):
                _save_atomic(active, dst_active)
                total_out += 1
            dst_dim = out_dim_dir / p.name
            if not (args.skip_existing and dst_dim.exists()):
                _save_atomic(dim, dst_dim)
                total_out += 1

            if first_out is None:
                first_out = normal
                first_active = active
                first_dim = dim

        idle_path = out_tag_dir / "idle.png"
        if first_out is None:
            first_out = _scale(base_half, normal_factor)
            first_active = _scale_centered(base_half, canvas_size, normal_factor * active_zoom)
            first_dim = _apply_dim_brightness(
                _scale_centered(base_half, canvas_size, normal_factor * dim_zoom)
            )

        if not (args.skip_existing and idle_path.exists()):
            _save_atomic(first_out, idle_path)
            total_out += 1
        idle_active_path = out_active_dir / "idle.png"
        if not (args.skip_existing and idle_active_path.exists()):
            _save_atomic(first_active or first_out, idle_active_path)
            total_out += 1
        idle_dim_path = out_dim_dir / "idle.png"
        if not (args.skip_existing and idle_dim_path.exists()):
            _save_atomic(first_dim or first_out, idle_dim_path)
            total_out += 1

        print(f"[完成] {tag}: frames={len(overlay_files)} -> {out_tag_dir}")

    print(f"全部烘焙完成，共输出 {total_out} 个文件：{out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
