# Episode 1 - 特殊事件场景
# 自动触发的事件、cutscene、审判场景等

## Day 3 - 火灾事件
label event_fire:
    """
    Day 3凌晨自动触发
    安德里娅的房屋发生火灾
    """

    scene bg black with fade

    "凌晨2:30，一阵骚动将你惊醒..."

    scene bg andrea_house with hpunch

    play sound "sfx_fire.ogg"

    "安德里娅的房屋燃起熊熊大火！"

    scene bg town_square with dissolve

    "居民们聚集在广场上..."

    show yedina sad at left
    show rolinda serious at right

    rolinda "是安德里娅的房子...快叫人灭火！"

    "等火势扑灭时，一切都太迟了..."

    yedina "安德里娅...她没能逃出来。"

    scene bg black with fade

    "第一起死亡事件发生了。"
    "调查开始..."

    # 解锁安德里娅住所
    $ locations_database["安德里娅住所"]["unlocked"] = True

    return


## Day 4 - 巴德别特失踪
label event_disappear:
    """
    Day 4夜晚自动触发
    巴德别特失踪/死亡
    """

    scene bg night with fade

    "夜幕降临..."

    "你注意到巴德别特的房子一片漆黑。"

    scene bg badebiete_house with dissolve

    "敲门没有回应..."
    "巴德别特不见了。"

    # 标记巴德别特死亡
    $ set_character_dead("巴德别特")

    scene bg black with fade

    "又一起离奇事件..."
    "真相越来越扑朔迷离。"

    return


## Day 6 - 审判开始
label event_trial_start:
    """
    Day 6傍晚强制触发
    调查结束，审判开始
    """

    scene bg black with fade

    "第六天傍晚，调查时间结束。"

    scene bg trial_hall with dissolve
    play music "bgm_trial.ogg" fadein 1.0

    show azov stern at center

    azov "现在开始审判。"
    azov "根据你收集的证据，指出真正的凶手。"

    # 进入审判界面
    call trial_phase

    return


## 审判阶段
label trial_phase:
    """
    第一周目的审判阶段
    玩家根据线索指认凶手
    """

    show azov stern at center

    azov "你认为凶手是谁？"

    menu trial_suspect_menu:
        "根据你的调查，凶手是..."

        "莫洛拉瓦神父":
            jump trial_accuse_molorava

        "哈夫电工":
            jump trial_accuse_hafu

        "我还不确定":
            azov "时间不多了，你必须做出选择。"
            jump trial_suspect_menu


## 指认莫洛拉瓦
label trial_accuse_molorava:
    """
    指认莫洛拉瓦为凶手
    """

    show azov stern at center

    "你列举了打火机、隐瞒过去等证据..."

    azov "审判结束。"
    azov "莫洛拉瓦神父，被判有罪。"

    scene bg black with fade

    "但是...真的是这样吗？"
    "有什么地方不对劲..."

    jump episode1_ending


## 指认哈夫
label trial_accuse_hafu:
    """
    指认哈夫为凶手
    """

    show azov stern at center

    "你列举了停电记录、电力线路图等证据..."

    azov "审判结束。"
    azov "哈夫电工，被判有罪。"

    scene bg black with fade

    "但是...这真的是真相吗？"
    "疑云并未散去..."

    jump episode1_ending


# TODO: 添加其他特殊事件
# label event_teaparty_ep1:  # 周目间的茶会场景
# label event_revelation_ep1:  # 真相揭示的cutscene
