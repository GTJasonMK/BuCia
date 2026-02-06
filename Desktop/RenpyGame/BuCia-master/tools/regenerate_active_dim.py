#!/usr/bin/env python3
"""
重新生成 active 和 dim 版本：从 normal 版本复制，只调整亮度（不缩放）
"""
import sys
from pathlib import Path
from PIL import Image
import numpy as np

def apply_dim_brightness(image: Image.Image, brightness: float = 0.75) -> Image.Image:
    """降低亮度（仅 RGB，保留 Alpha）"""
    if brightness >= 0.999:
        return image.copy()
    arr = np.array(image, dtype=np.float32)
    arr[:, :, :3] *= brightness
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def regenerate_versions(baked_dir: Path, dim_brightness: float = 0.75):
    """为每个角色重新生成 active 和 dim 版本"""
    baked_dir = Path(baked_dir)
    if not baked_dir.exists():
        print(f"目录不存在: {baked_dir}", file=sys.stderr)
        return 1
    
    total_processed = 0
    
    # 遍历每个角色目录
    for char_dir in baked_dir.iterdir():
        if not char_dir.is_dir():
            continue
        
        char_name = char_dir.name
        print(f"处理角色: {char_name}")
        
        # 跳过已经是 active 或 dim 的目录
        if char_name in ("active", "dim"):
            continue
        
        # 创建 active 和 dim 目录
        active_dir = char_dir / "active"
        dim_dir = char_dir / "dim"
        active_dir.mkdir(exist_ok=True)
        dim_dir.mkdir(exist_ok=True)
        
        # 处理所有 PNG 文件（包括 idle.png）
        for png_file in char_dir.glob("*.png"):
            if png_file.name.startswith("."):
                continue
            
            try:
                img = Image.open(png_file).convert("RGBA")
                
                # active 版本：直接复制（不缩放）
                active_path = active_dir / png_file.name
                img.save(active_path)
                total_processed += 1
                
                # dim 版本：应用亮度调整
                dim_img = apply_dim_brightness(img, dim_brightness)
                dim_path = dim_dir / png_file.name
                dim_img.save(dim_path)
                total_processed += 1
                
            except Exception as e:
                print(f"  警告: 处理 {png_file.name} 时出错: {e}", file=sys.stderr)
    
    print(f"\n完成！共处理 {total_processed} 个文件")
    return 0

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="重新生成 active 和 dim 版本（不缩放，只调整亮度）")
    parser.add_argument("--baked-dir", default="game/images/characters_baked", help="baked 目录路径")
    parser.add_argument("--dim-brightness", type=float, default=0.75, help="dim 版本亮度倍率（0-1）")
    args = parser.parse_args()
    
    repo_root = Path(__file__).resolve().parent.parent
    baked_dir = repo_root / args.baked_dir
    
    sys.exit(regenerate_versions(baked_dir, args.dim_brightness))
