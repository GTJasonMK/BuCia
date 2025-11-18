## 时间系统 - 7天周目结构

## 时间变量定义
default current_day = 1  # 当前天数（1-7）
default current_time = "morning"  # 当前时段（morning/afternoon/evening/night）
default action_points = 3  # 每日行动点数
default max_action_points = 3  # 最大行动点数

## 时间系统函数
init python:
    ## 时段列表（按顺序）
    time_periods = ["morning", "afternoon", "evening", "night"]

    ## 时段中文名称
    time_names = {
        "morning": "清晨",
        "afternoon": "午后",
        "evening": "傍晚",
        "night": "深夜"
    }

    ## 推进时间
    def advance_time():
        global current_time, current_day, action_points

        current_index = time_periods.index(current_time)

        # 如果是夜晚，推进到第二天早晨
        if current_time == "night":
            current_day += 1
            current_time = "morning"
            action_points = max_action_points  # 恢复行动点
            return "new_day"
        else:
            # 推进到下一时段
            current_time = time_periods[current_index + 1]
            return "same_day"

    ## 获取当前时间显示文本
    def get_time_display():
        return "Day {0} - {1}".format(current_day, time_names[current_time])

    ## 消耗行动点
    def use_action_point():
        global action_points
        if action_points > 0:
            action_points -= 1
            return True
        return False

    ## 检查是否有行动点
    def has_action_points():
        return action_points > 0

    ## 重置时间（用于新周目开始）
    def reset_time():
        global current_day, current_time, action_points
        current_day = 1
        current_time = "morning"
        action_points = max_action_points

    ## 跳转到指定天数和时段
    def jump_to_time(day, time):
        global current_day, current_time, action_points
        current_day = day
        current_time = time
        action_points = max_action_points

    ## 检查是否是特定天数和时段
    def is_time(day, time):
        return current_day == day and current_time == time

    ## 检查是否在指定天数之后
    def is_day_after(day):
        return current_day >= day

    ## 检查是否在指定时段之后
    def is_time_after(time):
        current_index = time_periods.index(current_time)
        target_index = time_periods.index(time)
        return current_index >= target_index

## 关键时间节点（剧情触发）
init python:
    ## 节点1：第1天 - 主角醒来
    EVENT_DAY1_START = (1, "morning")

    ## 节点2：第3天凌晨 - 安德里娅死亡
    EVENT_DAY3_FIRE = (3, "morning")

    ## 节点3：第4天夜晚 - 巴德别特失踪
    EVENT_DAY4_DISAPPEAR = (4, "night")

    ## 节点4：第6天 - 调查强制结束，审判开始
    EVENT_DAY6_TRIAL = (6, "evening")

    ## 节点5：第7天 - 结局揭示
    EVENT_DAY7_ENDING = (7, "morning")

    ## 检查是否到达关键节点
    def check_event_trigger(event_tuple):
        day, time = event_tuple
        return current_day == day and current_time == time

    ## 自动触发的事件（无法跳过）
    def trigger_automatic_events():
        # 第3天凌晨自动触发火灾
        if check_event_trigger(EVENT_DAY3_FIRE):
            return "andrea_fire"

        # 第4天夜晚自动触发失踪
        if check_event_trigger(EVENT_DAY4_DISAPPEAR):
            return "badebiete_disappear"

        # 第6天傍晚强制进入审判
        if check_event_trigger(EVENT_DAY6_TRIAL):
            return "trial_start"

        # 第7天早晨进入结局
        if check_event_trigger(EVENT_DAY7_ENDING):
            return "ending"

        return None

## 时间显示UI已移至 game/ui/time.rpy
## 保持系统层和UI层分离
