# Episode 1 - 角色对话场景
# 所有 talk_to_* labels

## 罗琳达 - 场景1：初次见面
label talk_to_rolinda_scene1:
    """
    第一次与罗琳达对话
    """

    show rolinda neutral at center with dissolve

    if is_first_meet("罗琳达"):
        $ set_character_met("罗琳达")
        rolinda "你好，欢迎来到布恰小镇。"
        rolinda "我是罗琳达，负责这里的社区管理工作。"
    else:
        rolinda "有什么可以帮你的吗？"

    menu talk_rolinda_menu1:
        "你想说什么？"

        "询问小镇情况":
            rolinda "这是个安静祥和的小镇。"
            rolinda "战后的生活虽然艰难，但大家都在努力重建。"
            $ modify_character_trust("罗琳达", 5)
            jump talk_rolinda_menu1

        "询问健康补充剂":
            rolinda "那是联邦政府的福利项目。"
            rolinda "为了帮助战后居民恢复健康..."
            # 罗琳达似乎有所隐瞒
            jump talk_rolinda_menu1

        "结束对话":
            rolinda "有需要随时找我。"
            hide rolinda with dissolve
            return


## 叶蒂娜 - 场景1：关于药品
label talk_to_yedina_scene1:
    """
    与叶蒂娜讨论药品问题
    """

    show yedina neutral at center with dissolve

    yedina "你好，需要什么医疗帮助吗？"

    menu talk_yedina_menu1:
        "询问药品来源":
            yedina "药品都是从联邦药厂统一配送的。"
            yedina "质量有保证，你不用担心。"
            $ modify_character_trust("叶蒂娜", 5)

        "询问安德里娅的情况" if is_day_after(3):
            yedina "安德里娅...是个悲剧。"
            yedina "我完成了尸检，死因是烟雾吸入导致窒息。"
            # 叶蒂娜似乎欲言又止
            $ modify_character_trust("叶蒂娜", 10)

        "告辞":
            hide yedina with dissolve
            return


## 巴德别特 - 场景1：警察经历
label talk_to_badebiete_scene1:
    """
    与巴德别特交谈，了解他的过去
    """

    show badebiete serious at center with dissolve

    badebiete "年轻人，有什么事吗？"

    menu talk_badebiete_menu1:
        "询问警察经历":
            badebiete "我曾是国家警察...做过很多任务。"
            badebiete "但有些事情，我不想再提起。"
            $ modify_character_trust("巴德别特", 5)

        "询问小镇的秘密":
            badebiete "..."
            badebiete "有些事情知道了反而不好。"
            badebiete "小心点，年轻人。"
            $ modify_character_trust("巴德别特", 10)

        "告辞":
            hide badebiete with dissolve
            return


# TODO: 为其余角色添加对话场景
# 每个角色至少需要2-3个场景，随着剧情推进和信任度提升解锁更多对话
# label talk_to_telina_ep1_scene1:
# label talk_to_molorava_ep1_scene1:
# label talk_to_hafu_ep1_scene1:
# label talk_to_bolai_ep1_scene1:
# label talk_to_ileina_ep1_scene1:
