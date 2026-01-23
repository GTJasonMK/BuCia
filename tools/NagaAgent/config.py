from pathlib import Path  # 路径管理
import json  # 解析配置

CONFIG_PATH = Path(__file__).with_name("config.json")  # 默认配置路径


def load_config(path: Path | None = None) -> dict:  # 加载配置
    cfg_path = path or CONFIG_PATH  # 使用传入路径或默认
    if not cfg_path.exists():  # 缺失配置直接报错
        raise FileNotFoundError(f"缺少配置文件: {cfg_path}")  # 单行说明
    data = json.loads(cfg_path.read_text(encoding="utf-8"))  # 读取JSON
    required = ["base_url", "api_key", "model"]  # 必填字段
    missing = [k for k in required if not data.get(k)]  # 检查空值
    if missing:  # 有缺失字段
        raise ValueError(f"配置字段缺失或为空: {', '.join(missing)}")  # 抛出错误
    return data  # 返回配置

