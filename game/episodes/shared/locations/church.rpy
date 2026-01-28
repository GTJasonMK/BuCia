## 共享地点场景 - 教堂（架构示例）
## 此文件展示如何使用周目复用机制避免代码重复

## 教堂 - 通用访问场景
label visit_church:
    """
    教堂通用场景示例
    展示共享基础内容 + 周目特有内容的架构模式
    """

    scene bg church with dissolve
    "古老的东正教教堂。"  # 共同描述，只写一次

    # 根据当前周目调用特有内容
    if is_episode(1):
        call visit_church_ep1_unique from _call_visit_church_ep1
    elif is_episode(2):
        call visit_church_ep2_unique from _call_visit_church_ep2
    # 其他周目类似...

    # 共同的交互选项示例
    menu:
        "调查祭坛":
            "你调查了祭坛..."
            # 实际内容待开发

        "离开":
            return

    jump visit_church  # 循环回到菜单


## 注释：
## - 共享场景放在 shared/locations/ 中
## - 周目特有内容定义在 episodeX/unique_scenes.rpy 中
## - 使用 is_episode(n) 判断当前周目
## - 实际剧情内容待剧本完成后开发

