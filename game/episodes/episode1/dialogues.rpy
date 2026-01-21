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

        "询问安德莉娅的情况" if is_day_after(3):
            yedina "安德莉娅...是个悲剧。"
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

## 特莉娜 - 场景1：社区事务
label talk_to_telina_scene1:
    """
    与特莉娜交谈，了解社区情况
    """

    show telina neutral at center with dissolve

    if is_first_meet("特莉娜"):
        $ set_character_met("特莉娜")
        telina "你好，我是特莉娜，社区事务负责人。"
        telina "有什么需要帮忙的吗？"
    else:
        telina "又见面了，有什么事吗？"

    menu talk_telina_menu1:
        "你想说什么？"

        "询问社区情况":
            telina "社区运作一切正常。"
            telina "居民们都在努力适应战后的新生活。"
            $ modify_character_trust("特莉娜", 5)
            jump talk_telina_menu1

        "询问药厂谈判" if get_character_trust("特莉娜") >= 40:
            telina "...你是怎么知道这件事的？"
            telina "这是机密事项，我不方便透露。"
            jump talk_telina_menu1

        "告辞":
            telina "好的，有事再来找我。"
            hide telina with dissolve
            return


## 哈夫 - 场景1：电力系统
label talk_to_hafu_scene1:
    """
    与电工哈夫交谈
    """

    show hafu neutral at center with dissolve

    if is_first_meet("哈夫"):
        $ set_character_met("哈夫")
        hafu "你好，我是哈夫，小镇的电工。"
    else:
        hafu "什么事？"

    menu talk_hafu_menu1:
        "你想说什么？"

        "询问小镇电力情况":
            hafu "电力系统老化得厉害。"
            hafu "我每天都在做维修工作。"
            $ modify_character_trust("哈夫", 5)
            jump talk_hafu_menu1

        "询问火灾当晚的停电" if is_day_after(3):
            hafu "那天晚上确实停电了..."
            hafu "但只是例行的线路检修，没什么特别的。"
            # 哈夫似乎有些紧张
            $ modify_character_trust("哈夫", 10)
            jump talk_hafu_menu1

        "告辞":
            hafu "好的。"
            hide hafu with dissolve
            return


## 博莱斯 - 场景1：管道系统
label talk_to_bolai_scene1:
    """
    与管道工博莱斯交谈
    """

    show bolai neutral at center with dissolve

    if is_first_meet("博莱斯"):
        $ set_character_met("博莱斯")
        bolai "嗯？你找我？"
        bolai "我是博莱斯，负责小镇的管道维护。"
    else:
        bolai "又是你啊。"

    menu talk_bolai_menu1:
        "你想说什么？"

        "询问管道情况":
            bolai "地下管道很复杂。"
            bolai "有些地方我都不太清楚通向哪里。"
            $ modify_character_trust("博莱斯", 5)
            jump talk_bolai_menu1

        "质问维修记录的问题" if is_clue_discovered("伪造维修记录"):
            bolai "你...你在说什么？"
            bolai "我只是做我的工作而已！"
            # 博莱斯明显变得慌张
            $ persistent.bolai_confronted = True
            $ modify_character_trust("博莱斯", -20)
            jump talk_bolai_menu1

        "告辞":
            bolai "...再见。"
            hide bolai with dissolve
            return


## 伊蕾娜 - 场景1：日常生活
label talk_to_ileina_scene1:
    """
    与伊蕾娜交谈
    """

    show ileina neutral at center with dissolve

    if is_first_meet("伊蕾娜"):
        $ set_character_met("伊蕾娜")
        ileina "你好...我是伊蕾娜。"
        ileina "你是新来的调查员吗？"
    else:
        ileina "有什么事吗？"

    menu talk_ileina_menu1:
        "你想说什么？"

        "询问日常生活":
            ileina "生活很平淡..."
            ileina "每天都在想办法度日。"
            $ modify_character_trust("伊蕾娜", 5)
            jump talk_ileina_menu1

        "询问火灾当晚看到了什么" if is_day_after(3):
            ileina "那天晚上..."
            ileina "我从窗户看到了一些奇怪的东西。"
            ileina "但我不确定自己看到的是什么。"
            $ modify_character_trust("伊蕾娜", 10)
            jump talk_ileina_menu1

        "告辞":
            ileina "好的...再见。"
            hide ileina with dissolve
            return
