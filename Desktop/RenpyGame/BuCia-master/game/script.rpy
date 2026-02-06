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

