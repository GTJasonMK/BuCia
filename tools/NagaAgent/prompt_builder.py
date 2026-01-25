from typing import Any  # 类型提示


def build_prompt(doc_text: str, assets: dict[str, Any]) -> str:  # 构造提示词
    characters = assets.get("characters") or []  # 角色列表
    backgrounds = assets.get("backgrounds") or []  # 背景
    cgs = assets.get("cgs") or []  # CG
    music = assets.get("music") or []  # 音乐
    sfx = assets.get("sfx") or []  # 音效

    context_blocks = [
        "【可用角色】" + (", ".join(characters) if characters else "暂无登记"),
        "【背景底图】" + (", ".join(backgrounds) if backgrounds else "暂无登记"),
        "【事件CG】" + (", ".join(cgs) if cgs else "暂无登记"),
        "【背景音乐】" + (", ".join(music) if music else "暂无登记"),
        "【音效】" + (", ".join(sfx) if sfx else "暂无登记"),
    ]  # 拼装上下文

    prompt = (
        "你是视觉小说编剧，需根据用户提供的docx剧情稿生成Ren'Py友好的剧本文本。\n"
        + "\n".join(context_blocks)
        + "\n【剧情原文】\n"
        + doc_text.strip()
        + "\n【输出要求】\n"
        + "1) 保持章节顺序与原文一致；2) 标注角色立绘/场景/音乐时使用上方可用资源名；3) 遇到缺失资源时用TODO占位；4) 严禁虚构不存在的资源名。"
    )  # 生成完整提示
    return prompt  # 返回提示词

