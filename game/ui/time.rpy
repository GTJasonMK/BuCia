## 时间系统 UI界面
## 从 systems/time_system.rpy 移动至此，遵循UI层分离原则

## 时间显示UI（叠加在游戏画面上）
screen time_display():
    zorder 100

    frame:
        xalign 0.98
        yalign 0.02
        background Frame(Solid("#00000080"), 10, 10)
        padding (15, 10)

        vbox:
            spacing 5

            # 日期显示
            text "[current_day!s] / 7" size 24 color "#ffffff"

            # 时段显示
            text "{size=18}[time_names[current_time]]{/size}" color "#cccccc"

            # 行动点显示
            if has_action_points():
                text "{size=16}行动点: [action_points]/[max_action_points]{/size}" color "#ffcc00"
            else:
                text "{size=16}行动点: 0/[max_action_points]{/size}" color "#666666"

## 时间推进按钮（调查地图时使用）
screen time_advance_button():
    zorder 100

    if has_action_points() and current_time != "night":
        textbutton "推进时间":
            xalign 0.98
            yalign 0.15
            background Frame(Solid("#00000080"), 10, 10)
            hover_background Frame(Solid("#1a1a1ab0"), 10, 10)
            padding (20, 10)
            text_size 20
            text_color "#ffffff"
            action Function(advance_time)

## 休息按钮（跳过到下一天）
screen rest_button():
    zorder 100

    if current_time == "night":
        textbutton "休息到明天":
            xalign 0.98
            yalign 0.15
            background Frame(Solid("#00000080"), 10, 10)
            hover_background Frame(Solid("#330000b0"), 10, 10)
            padding (20, 10)
            text_size 20
            text_color "#ffffff"
            action [Function(advance_time), Jump("day_start")]

## 精神值显示UI（叠加在游戏画面左上角）
screen sanity_display():
    """
    精神值指示器
    根据 persistent.sanity 显示对应的eye图标
    点击打开设置菜单
    """
    zorder 100

    # 仅在非主菜单时显示
    if not main_menu:
        imagebutton:
            xalign 0.02
            yalign 0.02
            idle Transform(get_sanity_icon(), zoom=0.5)
            hover Transform(get_sanity_icon(), zoom=0.5, alpha=0.8)
            action ShowMenu("preferences")
            tooltip "精神值: {}%\n点击打开设置".format(persistent.sanity if persistent.sanity is not None else 100)

        # 显示tooltip
        $ tooltip_text = GetTooltip()
        if tooltip_text:
            nearrect:
                focus "tooltip"
                prefer_top True

                frame:
                    xalign 0.0
                    yalign 0.0
                    xoffset 10
                    yoffset 80
                    background Frame(Solid("#000000cc"), 10, 10)
                    padding (12, 8)

                    text tooltip_text:
                        size 16
                        color "#ffffff"
