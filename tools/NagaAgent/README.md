# 自动剧情文本生成器（LLM）

## 目标
从导入的 docx 剧情稿生成贴合项目素材的 Ren'Py 剧本文本，调用配置在 `config.json` 的 LLM 接口，并自动拼接共享素材上下文。

## 目录结构
- `config.json`：私有配置（复制 `config.example.json` 后填写真实值）
- `config.example.json`：配置模板，勿填入密钥
- `config.py`：统一加载配置
- `docx_loader.py`：解析 docx
- `context_builder.py`：读取共享素材清单 `game/episodes/shared/ai_assets.json`
- `prompt_builder.py`：拼装提示词
- `pipeline.py`：组装并发送请求

## 准备
1. 复制 `config.example.json` 为 `config.json`，填入 `base_url`、`api_key`、`model`（不要提交真实密钥）。
2. 安装依赖：`pip install python-docx`.
3. 在 `game/episodes/shared/ai_assets.json` 登记角色、背景、CG、音乐、音效名称，便于提示词引用。

## 使用示例
```powershell
python - <<'PY'
from pathlib import Path
from tools.NagaAgent.pipeline import call_llm

resp = call_llm(Path("docs/episode1_outline.docx"))  # 传入docx路径
print(resp["choices"][0]["message"]["content"])
PY
```

## 输出规范
- 保持原稿段落顺序，缺失素材以 `TODO` 标记。
- 引用资源名必须来自 `ai_assets.json`，不得虚构。
- 新增素材先更新 `ai_assets.json` 再提交给生成器。

