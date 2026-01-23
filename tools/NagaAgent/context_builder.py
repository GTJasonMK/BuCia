from pathlib import Path  # 路径管理
import json  # 解析JSON

SHARED_ASSETS_PATH = Path(__file__).resolve().parents[2] / "game" / "episodes" / "shared" / "ai_assets.json"  # 共享清单


def load_shared_assets(path: Path | None = None) -> dict:  # 读取共享资源
    target = path or SHARED_ASSETS_PATH  # 使用传入或默认
    if not target.exists():  # 未提供清单则返回空壳
        return {"characters": [], "backgrounds": [], "cgs": [], "music": [], "sfx": []}  # 保持结构
    data = json.loads(target.read_text(encoding="utf-8"))  # 读取JSON
    return {
        "characters": data.get("characters", []),  # 角色列表
        "backgrounds": data.get("backgrounds", []),  # 背景图
        "cgs": data.get("cgs", []),  # CG列表
        "music": data.get("music", []),  # 音乐
        "sfx": data.get("sfx", [])  # 音效
    }  # 返回标准结构

