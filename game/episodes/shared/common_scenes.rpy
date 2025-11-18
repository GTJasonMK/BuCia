# 共享场景文件
# 周目间可复用的场景片段

## 通用场景：时间推进提示
label common_time_advance:
    """
    显示时间推进的通用提示
    """
    centered "时间流逝..."
    return


## 通用场景：发现重要线索
label common_clue_discovered:
    """
    发现重要线索时的通用表现

    使用方法：
        $ temp_clue_name = "线索名称"
        call common_clue_discovered

    注意：调用前需要设置 temp_clue_name 变量
    """
    with hpunch
    play sound "sfx_discover.ogg"
    centered "{color=#ff3333}发现关键线索：[temp_clue_name]{/color}"
    return


## 通用场景：角色死亡
label common_character_death:
    """
    角色死亡的通用场景

    使用方法：
        $ temp_char_name = "角色名称"
        call common_character_death

    注意：调用前需要设置 temp_char_name 变量
    """
    scene bg black with fade
    centered "{color=#ff0000}[temp_char_name] 死亡{/color}"
    return


## 通用场景：精神值警告
label common_sanity_warning:
    """
    精神值过低时的警告
    """
    if persistent.sanity < 34:
        scene bg distorted with dissolve
        centered "{color=#ff3333}你感到意识模糊...{/color}"
        centered "{color=#ff3333}现实与幻觉的边界开始模糊...{/color}"
        scene bg black with fade
    return


## 通用场景：周目结束茶会
label common_teaparty_transition:
    """
    周目间的茶会场景
    与AI娜杰日达的对话
    """
    scene bg teaparty with dissolve
    play music "bgm_mysterious.ogg" fadein 1.0

    show najezhida neutral at center

    najezhida "又一次失败了呢。"
    najezhida "你离真相还很远..."

    # TODO: 根据周目数量显示不同的对话

    scene bg black with fade

    return


# 这个文件中的场景可以被所有周目调用
# 避免重复编写相同的场景内容
