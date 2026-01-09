## 时间系统 UI界面
## 从 systems/time_system.rpy 移动至此，遵循UI层分离原则

## 时间显示UI（叠加在游戏画面上）
## 位置在 REC 指示灯下方
screen time_display():
    zorder 100

    frame:
        xalign 0.98
        yalign 0.12  ## 从 0.02 改为 0.12，避免和 REC 重叠
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
## 实现动态填充效果：红色圆球覆盖眼球，根据精神值从底部向上填充

## ========== 精神值图标配置 ==========
## 整体缩放（调整这个值会同时缩放眼睛和圆球，保持相对位置）
## 调小以匹配 REC 指示灯大小
define SANITY_ZOOM = 0.45

## 眼睛图标（固定参数）
define SANITY_ICON = "sanity/san_eye.png"
define SANITY_ICON_WIDTH = 313
define SANITY_ICON_HEIGHT = 204

## 红色圆球（相对于眼睛的比例参数，已固定）
define SANITY_CIRCLE = "sanity/red_circle.png"
define SANITY_CIRCLE_SIZE = 200
define SANITY_CIRCLE_SCALE = 0.484       # 圆球相对眼睛的缩放比例
define SANITY_CIRCLE_X_RATIO = 0.351     # X偏移占眼睛宽度的比例
define SANITY_CIRCLE_Y_RATIO = 0.237     # Y偏移占眼睛高度的比例
## =====================================

screen sanity_display():
    ## 精神值指示器
    ## 红色圆球根据精神值从底部向上填充
    ## 点击打开设置菜单
    zorder 100

    ## 仅在非主菜单且摄像机UI启用时显示
    if not main_menu and camera_ui_enabled:
        ## 计算尺寸参数（基于统一缩放）
        $ sanity = persistent.sanity if persistent.sanity is not None else 100
        $ fill_ratio = sanity / 100.0

        ## 根据摄像机UI状态调整位置
        ## camera_ui 启用时使用摄像机配套位置，否则使用默认位置
        $ _camera_mode = getattr(store, 'camera_ui_enabled', True)
        ## 摄像机模式：与 REC 平行，设计坐标 (79, 69) → 缩放后约 (55, 48)
        ## 调整 Y 位置让眼睛和 REC 在同一水平线
        $ sanity_xpos = 55 if _camera_mode else int(1920 * 0.02)
        $ sanity_ypos = 35 if _camera_mode else int(1080 * 0.02)

        ## 眼睛显示尺寸
        $ icon_width = int(SANITY_ICON_WIDTH * SANITY_ZOOM)
        $ icon_height = int(SANITY_ICON_HEIGHT * SANITY_ZOOM)

        ## 圆球参数（相对于眼睛自动计算）
        $ circle_zoom = SANITY_ZOOM * SANITY_CIRCLE_SCALE
        $ circle_xpos = int(SANITY_ICON_WIDTH * SANITY_CIRCLE_X_RATIO * SANITY_ZOOM)
        $ circle_ypos = int(SANITY_ICON_HEIGHT * SANITY_CIRCLE_Y_RATIO * SANITY_ZOOM)
        $ circle_visible_height = int(SANITY_CIRCLE_SIZE * fill_ratio)
        $ circle_crop_y = SANITY_CIRCLE_SIZE - circle_visible_height

        ## 可点击的精神值图标容器
        button:
            xpos sanity_xpos
            ypos sanity_ypos
            xsize icon_width
            ysize icon_height
            action ShowMenu("preferences")
            tooltip "精神值: {}%\n点击打开设置".format(sanity)

            fixed:
                xsize icon_width
                ysize icon_height

                ## 底层：红色圆球（从底部向上填充）
                if circle_visible_height > 0:
                    add Transform(
                        Crop((0, circle_crop_y, SANITY_CIRCLE_SIZE, circle_visible_height), SANITY_CIRCLE),
                        zoom=circle_zoom
                    ):
                        xpos circle_xpos
                        ypos circle_ypos + int(circle_crop_y * circle_zoom)

                ## 顶层：眼睛图标（覆盖在圆球上方）
                add Transform(SANITY_ICON, zoom=SANITY_ZOOM)

        ## 显示tooltip
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
