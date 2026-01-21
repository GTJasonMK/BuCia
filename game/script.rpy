## 游戏的主脚本文件
## 此文件作为游戏入口，负责路由到各个周目的实际剧情内容

## persistent变量初始化已移至 game/init_persistent.rpy
## 所有跨存档的变量在那里统一管理

## 角色定义已移至 game/data/characters/database.rpy
## 此处不再重复定义

## 游戏从这里开始
label start:
    # 默认从Episode 1开始
    jump episode_1

## Episode 1 - 伪书·陷阱与迷雾
label episode_1:
    if not persistent.episode_1_unlocked:
        "此章节尚未解锁。"
        return

    # 跳转到 game/episodes/episode1/story.rpy 中的实际剧情
    jump episode1_start

## Episode 2 - 伪书·真相的碎片
label episode_2:
    if not persistent.episode_2_unlocked:
        "此章节尚未解锁。"
        "请先完成第一周目。"
        return

    # 跳转到 game/episodes/episode2/story.rpy 中的实际剧情
    # 当前尚未开发，显示提示信息
    jump episode2_placeholder

## Episode 3 - 伪书·破碎的现实
label episode_3:
    if not persistent.episode_3_unlocked:
        "此章节尚未解锁。"
        "请先完成第二周目。"
        return

    # 跳转到 game/episodes/episode3/story.rpy 中的实际剧情
    # 当前尚未开发，显示提示信息
    jump episode3_placeholder

## Episode 4 - 真相周目
label episode_4:
    if not persistent.episode_4_unlocked:
        "此章节尚未解锁。"
        "请先完成第三周目。"
        return

    # 跳转到 game/episodes/episode4/story.rpy 中的实际剧情
    # 当前尚未开发，显示提示信息
    jump episode4_placeholder

## Episodes 5-8（第二部，开发中）
label episodes_5_8:
    if not persistent.episodes_5_8_unlocked:
        "此章节尚未解锁。"
        "请先完成第四周目。"
        return

    scene bg room with dissolve

    "Episodes 5-8: 开发中"
    "敬请期待..."

    return

## 开发者测试场景 - 精神值图标测试
label sanity_test:
    """
    精神值图标显示测试
    用于验证不同精神值档位的图标显示效果

    使用方法：
    1. 在主菜单按 Shift+O 打开控制台
    2. 输入: renpy.call_in_new_context("sanity_test")
    或
    3. 在游戏中直接 jump sanity_test
    """

    scene bg room with dissolve

    show screen time_display
    show screen sanity_display

    "精神值图标测试场景"
    "左上角显示的eye图标会根据精神值变化而改变。"
    "当前精神值: [persistent.sanity]"

    menu:
        "请选择要测试的精神值档位："

        "100 - 正常状态（图标1）":
            $ persistent.sanity = 100
            "精神值已设置为100 - 正常状态"

        "75 - 轻度幻觉（图标2）":
            $ persistent.sanity = 75
            "精神值已设置为75 - 轻度幻觉"

        "58 - 中度幻觉（图标3）":
            $ persistent.sanity = 58
            "精神值已设置为58 - 中度幻觉"

        "42 - 重度幻觉（图标4）":
            $ persistent.sanity = 42
            "精神值已设置为42 - 重度幻觉"

        "25 - 极度混乱（图标5）":
            $ persistent.sanity = 25
            "精神值已设置为25 - 极度混乱"

        "8 - 崩溃边缘（图标6）":
            $ persistent.sanity = 8
            "精神值已设置为8 - 崩溃边缘"

        "退出测试":
            $ persistent.sanity = 100
            "精神值已恢复为100"
            return

    "观察左上角的eye图标，它应该已经改变。"
    "鼠标悬停在图标上可以看到当前精神值。"
    "点击图标可以打开设置菜单。"

    jump sanity_test

## 周目占位符（待开发）
label episode2_placeholder:
    scene bg room with dissolve
    "Episode 2: 伪书·真相的碎片"
    "此周目正在开发中，敬请期待..."
    return

label episode3_placeholder:
    scene bg room with dissolve
    "Episode 3: 伪书·破碎的现实"
    "此周目正在开发中，敬请期待..."
    return

label episode4_placeholder:
    scene bg room with dissolve
    "Episode 4: 真相周目"
    "此周目正在开发中，敬请期待..."
    return

