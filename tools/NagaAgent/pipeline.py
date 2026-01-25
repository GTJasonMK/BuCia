import json  # 序列化请求体
from pathlib import Path  # 路径管理
from urllib import request  # HTTP请求

from .config import load_config  # 配置加载
from .docx_loader import load_docx_text  # 文档读取
from .context_builder import load_shared_assets  # 资源清单
from .prompt_builder import build_prompt  # 提示词构建


def build_payload(docx_path: str | Path, config_path: Path | None = None, assets_path: Path | None = None) -> tuple[str, dict, bytes, float]:  # 构造请求
    cfg = load_config(config_path)  # 读取配置
    doc_text = load_docx_text(docx_path)  # 提取剧情
    assets = load_shared_assets(assets_path)  # 载入共享素材
    prompt = build_prompt(doc_text, assets)  # 生成提示词

    url = cfg["base_url"].rstrip("/") + "/chat/completions"  # 组合接口地址
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",  # 认证
        "Content-Type": "application/json"  # JSON请求
    }  # 请求头
    body = {
        "model": cfg["model"],  # 模型名
        "messages": [
            {"role": "system", "content": "你是严谨的视觉小说编剧，负责将原始剧情转化为Ren'Py脚本。"},  # 系统提示
            {"role": "user", "content": prompt}  # 用户内容
        ],
        "temperature": cfg.get("temperature", 0.6),  # 可选温度
        "max_tokens": cfg.get("max_tokens", 2000)  # 可选长度
    }  # 请求体
    timeout = float(cfg.get("timeout_seconds", 60))  # 超时时间
    return url, headers, json.dumps(body, ensure_ascii=False).encode("utf-8"), timeout  # 返回四元组


def call_llm(docx_path: str | Path, config_path: Path | None = None, assets_path: Path | None = None) -> dict:  # 执行请求
    url, headers, body, timeout = build_payload(docx_path, config_path, assets_path)  # 获取请求要素
    req = request.Request(url, data=body, headers=headers, method="POST")  # 构造请求
    with request.urlopen(req, timeout=timeout) as resp:  # 发送并等待响应
        content = resp.read().decode("utf-8")  # 读取响应
        return json.loads(content)  # 返回解析后的JSON

