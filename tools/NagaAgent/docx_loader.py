from pathlib import Path  # 路径管理

try:
    import docx  # 解析docx
except ImportError:  # 缺少依赖
    docx = None  # 标记未安装


def load_docx_text(docx_path: str | Path) -> str:  # 读取docx文本
    if docx is None:  # 未安装依赖
        raise ImportError("缺少依赖 python-docx，请先安装")  # 提示安装
    path = Path(docx_path)  # 标准化路径
    if not path.exists():  # 文件不存在
        raise FileNotFoundError(f"未找到文档: {path}")  # 抛错
    document = docx.Document(path)  # 打开文档
    paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]  # 过滤空段落
    return "\n".join(paragraphs)  # 返回纯文本

