## 视觉化地图系统
## 提供可交互的布恰小镇地图界面

## ============================================================================
## 配置参数
## ============================================================================

## 地图缩放比例（素材已为1920x1080，保持全屏显示）
define MAP_SCALE = 1.0

## 地图素材路径
init python:
    MAP_IMAGES = {
        ## 地图层级（从下到上）
        "background": "map/背景.png",
        "dirt": "map/泥地.png",
        "fill": "map/填充.png",
        "road": "map/路.png",
        "outline": "map/描边.png",

        ## 位置标记
        "marker_pink": "map/粉色碎片.png",
        "marker_blue": "map/蓝色碎片.png",
        "marker_current": "map/现在.png",
        "marker_current_label": "map/现在标签.png",
        "marker_location": "map/我的位置.png",
        "marker_location_label": "map/我的位置标签.png",
        "marker_residence": "map/住址.png",
        "marker_residence_label": "map/住址标签.png",

        ## 控制按钮
        "btn_return": "map/返回.png",
        "btn_return_label": "map/返回标签.png",
        "btn_clear": "map/清除.png",
        "btn_clear_label": "map/清除标签.png"
    }

    ## 地图层级位置（基于坐标.txt）
    MAP_LAYER_POSITIONS = {
        "background": (0, 0),
        "dirt": (36, 4),
        "fill": (237, 77),
        "road": (147, 43),
        "outline": (39, 2)
    }

## 当前选中的地点（用于显示详情）
default map_selected_location = None
## 当前悬停地点（用于显示标签）
default map_hover_label = ""
default map_hover_pos = None

## 地图模式：normal（正常导航）或 view（仅查看，用于笔记本）
default map_mode = "normal"

## ============================================================================
## 地图主屏幕
## ============================================================================

screen visual_map(mode="normal", close_action=Hide("visual_map")):
    tag menu
    modal True

    $ map_mode = mode

    ## 显示时隐藏摄像机UI，关闭时恢复
    on "show" action SetVariable("camera_ui_enabled", False)
    on "hide" action SetVariable("camera_ui_enabled", True)

    ## 快捷键
    key "m" action close_action
    key "K_ESCAPE" action close_action

    ## ========== 地图背景层 ==========
    fixed:
        ## 背景
        add MAP_IMAGES["background"]:
            pos (0, 0)
            zoom MAP_SCALE

        ## 泥地层
        add MAP_IMAGES["dirt"]:
            pos (int(36 * MAP_SCALE), int(4 * MAP_SCALE))
            zoom MAP_SCALE

        ## 填充层
        add MAP_IMAGES["fill"]:
            pos (int(237 * MAP_SCALE), int(77 * MAP_SCALE))
            zoom MAP_SCALE

        ## 道路层
        add MAP_IMAGES["road"]:
            pos (int(147 * MAP_SCALE), int(43 * MAP_SCALE))
            zoom MAP_SCALE

        ## 描边层
        add MAP_IMAGES["outline"]:
            pos (int(39 * MAP_SCALE), int(2 * MAP_SCALE))
            zoom MAP_SCALE

    ## ========== 地点标记 ==========
    fixed:
        $ all_locations = get_all_map_locations()

        for loc in all_locations:
            $ loc_name = loc["name"]
            $ loc_pos = loc["pos"]
            $ is_unlocked = loc["unlocked"]
            $ is_available = loc["available"]
            $ is_visited = loc["visited"]
            $ is_current = (get_current_location() == loc_name)
            $ is_revealed = loc_name in getattr(persistent, "unlocked_locations", [])

            ## 计算缩放后的位置
            $ scaled_x = int(loc_pos[0] * MAP_SCALE)
            $ scaled_y = int(loc_pos[1] * MAP_SCALE)

            ## 地点标记按钮
            if is_current:
                ## 当前所在位置 - 特殊标记
                fixed:
                    pos (scaled_x - 20, scaled_y - 20)
                    add MAP_IMAGES["marker_current"]:
                        zoom MAP_SCALE * 1.2
                    ## 当前位置标签
                    add MAP_IMAGES["marker_current_label"]:
                        pos (40, -30)
                        zoom MAP_SCALE * 0.8
            else:
                ## 其他地点
                imagebutton:
                    pos (scaled_x - 15, scaled_y - 15)
                    idle Transform(MAP_IMAGES["marker_pink"] if is_revealed else MAP_IMAGES["marker_blue"], zoom=MAP_SCALE)
                    hover Transform(MAP_IMAGES["marker_pink"] if is_revealed else MAP_IMAGES["marker_blue"], zoom=MAP_SCALE * 1.2)
                    action SetVariable("map_selected_location", loc)
                    hovered [
                        SetVariable("map_hover_label", loc["display_name"]),
                        SetVariable("map_hover_pos", loc["pos"])
                    ]
                    unhovered [
                        SetVariable("map_hover_label", ""),
                        SetVariable("map_hover_pos", None)
                    ]
                    sensitive True

    ## ========== 当前位置标记 ==========
    if get_current_location():
        $ current_loc = get_current_location()
        $ current_pos = get_location_map_pos(current_loc)
        if current_pos:
            fixed:
                pos (int(current_pos[0] * MAP_SCALE) - 25, int(current_pos[1] * MAP_SCALE) - 50)
                add MAP_IMAGES["marker_location"]:
                    zoom MAP_SCALE
                add MAP_IMAGES["marker_location_label"]:
                    pos (30, -25)
                    zoom MAP_SCALE * 0.7

    ## ========== 悬浮地点标签 ==========
    if map_hover_label and map_hover_pos:
        $ hover_pos = map_hover_pos
        $ hover_x = int(hover_pos[0] * MAP_SCALE)
        $ hover_y = int(hover_pos[1] * MAP_SCALE)
        frame:
            xanchor 0.5
            yanchor 1.0
            xpos hover_x
            ypos hover_y - int(30 * MAP_SCALE)
            background Solid("#1a1510cc")
            xpadding 12
            ypadding 6

            text map_hover_label:
                size 20
                color "#f5e6c8"
                font "fonts/lolita.ttf"

    ## ========== 地点信息面板 ==========
    if map_selected_location:
        frame:
            xalign 1.0
            yalign 0.0
            xoffset -20
            yoffset 20
            xsize 380
            ypadding 20
            xpadding 20
            background Solid("#2a2218e0")

            vbox:
                spacing 12

                ## 地点名称
                text map_selected_location["display_name"]:
                    size 28
                    color "#f5e6c8"
                    font "fonts/lolita.ttf"

                ## 状态信息
                hbox:
                    spacing 15
                    if map_selected_location["unlocked"]:
                        text "已解锁":
                            size 18
                            color "#8bc34a"
                    else:
                        text "未解锁":
                            size 18
                            color "#f44336"

                    if map_selected_location["available"]:
                        text "可前往":
                            size 18
                            color "#8bc34a"
                    else:
                        text "当前时段不可":
                            size 18
                            color "#ff9800"

                    if map_selected_location["visited"]:
                        text "已访问":
                            size 18
                            color "#9e9e9e"

                null height 10

                ## 地点描述
                $ loc_info = get_location_info(map_selected_location["name"])
                if loc_info:
                    text loc_info.get("description", ""):
                        size 18
                        color "#d4c4a8"
                        font "fonts/lolita.ttf"
                        xmaximum 340

                null height 15

                ## 操作按钮
                if mode == "normal":
                    hbox:
                        spacing 20
                        xalign 0.5

                        ## 前往按钮
                        if map_selected_location["unlocked"] and map_selected_location["available"]:
                            textbutton "前往此处":
                                text_size 22
                                text_color "#ffffff"
                                background Solid("#4a7c4e")
                                hover_background Solid("#5a9c5e")
                                xpadding 25
                                ypadding 10
                                action Function(do_travel_to_location, map_selected_location["name"])
                        else:
                            textbutton "无法前往":
                                text_size 22
                                text_color "#888888"
                                background Solid("#444444")
                                xpadding 25
                                ypadding 10
                                sensitive False

                        ## 关闭按钮
                        textbutton "关闭":
                            text_size 22
                            text_color "#ffffff"
                            background Solid("#5a4a3a")
                            hover_background Solid("#7a6a5a")
                            xpadding 25
                            ypadding 10
                            action SetVariable("map_selected_location", None)

    ## ========== 控制按钮区域 ==========
    fixed:
        ## 返回按钮
        imagebutton:
            pos (int(792 * MAP_SCALE), int(900 * MAP_SCALE))
            idle Transform(MAP_IMAGES["btn_return"], zoom=MAP_SCALE)
            hover Transform(MAP_IMAGES["btn_return"], zoom=MAP_SCALE * 1.1)
            action close_action

        ## 返回标签
        add MAP_IMAGES["btn_return_label"]:
            pos (int(724 * MAP_SCALE), int(870 * MAP_SCALE))
            zoom MAP_SCALE * 0.8

    ## ========== 顶部信息栏 ==========
    frame:
        xalign 0.5
        yalign 0.0
        yoffset 10
        xpadding 30
        ypadding 10
        background Solid("#1a1510c0")

        hbox:
            spacing 40

            text "布恰小镇地图":
                size 32
                color "#f5e6c8"
                font "fonts/lolita.ttf"

            if mode == "normal":
                ## 显示行动点（正常模式）
                hbox:
                    spacing 10
                    text "行动点:":
                        size 22
                        color "#d4c4a8"
                    $ ap = renpy.store.get_action_points() if hasattr(renpy.store, "get_action_points") else 3
                    text "[ap]":
                        size 22
                        color "#8bc34a"

    ## ========== 图例 ==========
    frame:
        xalign 0.0
        yalign 1.0
        xoffset 20
        yoffset -20
        xpadding 15
        ypadding 15
        background Solid("#1a1510c0")

        vbox:
            spacing 8

            text "图例":
                size 20
                color "#f5e6c8"

            hbox:
                spacing 8
                add MAP_IMAGES["marker_pink"]:
                    zoom MAP_SCALE * 0.6
                text "已解锁":
                    size 16
                    color "#d4c4a8"
                    yalign 0.5

            hbox:
                spacing 8
                add MAP_IMAGES["marker_blue"]:
                    zoom MAP_SCALE * 0.6
                text "未解锁":
                    size 16
                    color "#d4c4a8"
                    yalign 0.5

            hbox:
                spacing 8
                add MAP_IMAGES["marker_current"]:
                    zoom MAP_SCALE * 0.5
                text "当前位置":
                    size 16
                    color "#ffd700"
                    yalign 0.5

## ============================================================================
## 简化版地图（用于笔记本标签页）
## ============================================================================

screen notebook_map_view():
    ## 缩小版地图，嵌入笔记本
    $ mini_scale = 0.45

    fixed:
        xsize int(config.screen_width * mini_scale)
        ysize int(config.screen_height * mini_scale)

        ## 地图背景层（与主地图一致）
        add MAP_IMAGES["background"]:
            pos (0, 0)
            zoom mini_scale

        add MAP_IMAGES["dirt"]:
            pos (int(MAP_LAYER_POSITIONS["dirt"][0] * mini_scale), int(MAP_LAYER_POSITIONS["dirt"][1] * mini_scale))
            zoom mini_scale

        add MAP_IMAGES["fill"]:
            pos (int(MAP_LAYER_POSITIONS["fill"][0] * mini_scale), int(MAP_LAYER_POSITIONS["fill"][1] * mini_scale))
            zoom mini_scale

        add MAP_IMAGES["road"]:
            pos (int(MAP_LAYER_POSITIONS["road"][0] * mini_scale), int(MAP_LAYER_POSITIONS["road"][1] * mini_scale))
            zoom mini_scale

        add MAP_IMAGES["outline"]:
            pos (int(MAP_LAYER_POSITIONS["outline"][0] * mini_scale), int(MAP_LAYER_POSITIONS["outline"][1] * mini_scale))
            zoom mini_scale

        ## 地点标记
        $ all_locations = get_all_map_locations()

        for loc in all_locations:
            $ loc_pos = loc["pos"]
            $ is_current = (get_current_location() == loc["name"])
            $ is_revealed = loc["name"] in getattr(persistent, "unlocked_locations", [])

            $ mini_x = int(loc_pos[0] * mini_scale)
            $ mini_y = int(loc_pos[1] * mini_scale)

            imagebutton:
                pos (mini_x - 8, mini_y - 8)
                idle Transform(MAP_IMAGES["marker_pink"] if is_revealed else MAP_IMAGES["marker_blue"], zoom=mini_scale)
                hover Transform(MAP_IMAGES["marker_pink"] if is_revealed else MAP_IMAGES["marker_blue"], zoom=mini_scale * 1.2)
                action SetVariable("notebook_selected_item", loc)
                hovered [
                    SetVariable("map_hover_label", loc["display_name"]),
                    SetVariable("map_hover_pos", loc["pos"])
                ]
                unhovered [
                    SetVariable("map_hover_label", ""),
                    SetVariable("map_hover_pos", None)
                ]

            if is_current:
                add MAP_IMAGES["marker_current"]:
                    pos (mini_x - 8, mini_y - 8)
                    zoom mini_scale * 0.8

        ## 悬浮标签
        if map_hover_label and map_hover_pos:
            $ hover_pos = map_hover_pos
            $ hover_x = int(hover_pos[0] * mini_scale)
            $ hover_y = int(hover_pos[1] * mini_scale)
            frame:
                xanchor 0.5
                yanchor 1.0
                xpos hover_x
                ypos hover_y - int(20 * mini_scale)
                background Solid("#1a1510cc")
                xpadding 10
                ypadding 5

                text map_hover_label:
                    size 18
                    color "#f5e6c8"
                    font "fonts/lolita.ttf"

        ## 提示文字
        text "点击地点查看详情":
            xalign 0.5
            yalign 1.0
            yoffset -10
            size 18
            color "#4a3728"
            font "fonts/lolita.ttf"

## ============================================================================
## 使用示例
## ============================================================================
##
## 打开地图（正常导航模式）:
##   show screen visual_map
##   或
##   show screen visual_map("normal")
##
## 打开地图（仅查看模式）:
##   show screen visual_map("view")
##
## 快捷键:
##   M - 打开/关闭地图
##   ESC - 关闭地图
##
