# Episode 1 - 伪书·陷阱与迷雾
# 第一周目主线剧情流程

## 周目主入口
label episode1_start:
    """
    第一周目开始
    从这里进入主线剧情
    """

    # 设置当前周目
    $ start_episode(1)

    scene bg room with fade

    "第一周目：陷阱与迷雾"

    "你在一个陌生的房间中醒来..."
    "头很痛，记忆模糊不清..."

    # TODO: 添加开场剧情

    # 进入第一天
    jump episode1_day1


## Day 1 流程
label episode1_day1:
    """
    第一天的主线流程
    """

    # 显示时间UI
    show screen time_display

    "Day 1 - 清晨"

    # TODO: 第一天的剧情内容

    # 开放地图探索
    call screen map_screen

    return


## Day 2 流程
label episode1_day2:
    """
    第二天的主线流程
    """

    "Day 2 - 清晨"

    # TODO: 第二天的剧情内容

    call screen map_screen

    return


## Day 3 - 安德里娅火灾事件
label episode1_day3:
    """
    第三天 - 关键事件日
    """

    # 自动触发火灾事件
    call event_fire

    # 调查开始
    call screen map_screen

    return


## 周目结局
label episode1_ending:
    """
    第一周目结局
    根据玩家选择指认凶手
    """

    # TODO: 审判场景

    scene bg black with fade

    "第一周目完成"

    # 解锁第二周目
    $ persistent.episode_2_unlocked = True

    return


## 示例：连接到其他文件的场景
# 这些label的具体实现在对应的文件中
# label visit_rolinda_house: 在 locations.rpy 中
# label talk_to_rolinda_scene1: 在 dialogues.rpy 中
# label investigate_rolinda_house_desk: 在 investigations.rpy 中
# label event_fire: 在 events.rpy 中
