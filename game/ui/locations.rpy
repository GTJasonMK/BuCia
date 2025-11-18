## 地点系统 UI界面
## 从 data/locations.rpy 移动至此，遵循UI层分离原则

## 地图选择UI
screen map_screen():
    tag menu

    ## 背景
    add "bg/map_overview.jpg"

    ## 标题
    frame:
        xalign 0.5
        yalign 0.05
        background Frame(Solid("#00000080"), 10, 10)
        padding (30, 15)

        text "布恰小镇地图" size 40 color "#ffffff"

    ## 时间和行动点显示
    use time_display

    ## 地点列表
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 10

        # 动态获取并排序地点列表
        python:
            sorted_locations = sorted(
                locations_database.keys(),
                key=lambda x: locations_database[x].get("display_order", 999)
            )

        for location_name in sorted_locations:
            $ loc_info = get_location_info(location_name)
            $ unlocked = is_location_unlocked(location_name)
            $ available = is_location_available(location_name)
            $ visited = loc_info.get("visited", False) if loc_info else False
            $ label_suffix = loc_info.get("label_suffix", location_name) if loc_info else location_name

            button:
                action [
                    If(unlocked and available and has_action_points(),
                       [Function(use_action_point),
                        Function(set_location_visited, location_name),
                        Jump("visit_" + label_suffix)],
                       None)
                ]
                background Frame(Solid("#00000080"), 10, 10)
                hover_background Frame(Solid("#330000b0" if (unlocked and available) else "#00000080"), 10, 10)
                padding (30, 10)
                sensitive (unlocked and available and has_action_points())

                hbox:
                    spacing 10

                    # 地点名称
                    text location_name:
                        size 28
                        color ("#ffffff" if (unlocked and available) else "#666666")

                    # 访问标记
                    if visited:
                        text "{size=20}[[已访问]{/size}" color "#66ff66"

                    # 不可用提示
                    if unlocked and not available:
                        text "{size=20}[[当前时段不可访问]{/size}" color "#888888"
                    elif not unlocked:
                        text "{size=20}[[未解锁]{/size}" color "#666666"

    ## 返回按钮
    textbutton "返回":
        xalign 0.1
        yalign 0.9
        background Frame(Solid("#00000080"), 10, 10)
        hover_background Frame(Solid("#1a1a1ab0"), 10, 10)
        padding (30, 10)
        text_size 24
        text_color "#ffffff"
        action Return()

## 地点探索UI
screen location_explore(location_name):
    tag location

    $ loc_info = get_location_info(location_name)
    $ bg_image = loc_info.get("background", "bg/default.jpg") if loc_info else "bg/default.jpg"
    $ description = loc_info.get("description", "") if loc_info else ""
    $ hotspots = loc_info.get("hotspots", {}) if loc_info else {}
    $ characters = loc_info.get("characters", []) if loc_info else []

    ## 背景图
    add bg_image

    ## 地点名称和描述
    frame:
        xalign 0.5
        yalign 0.05
        background Frame(Solid("#00000080"), 10, 10)
        padding (30, 15)

        vbox:
            spacing 5

            text loc_info.get("name", location_name) size 35 color "#ffffff"
            text description size 20 color "#cccccc" xmaximum 800

    ## 时间显示
    use time_display

    ## 热点列表
    vbox:
        xalign 0.1
        yalign 0.5
        spacing 10

        text "可调查的地点：" size 24 color "#ffffff"

        for hotspot_name, hotspot_data in hotspots.items():
            $ unlocked = is_hotspot_unlocked(location_name, hotspot_name)

            textbutton hotspot_name:
                text_size 22
                text_idle_color ("#ffffff" if unlocked else "#666666")
                text_hover_color ("#ff3333" if unlocked else "#666666")
                action [
                    If(unlocked,
                       Jump("investigate_" + location_name.replace("·", "_") + "_" + hotspot_name),
                       None)
                ]
                background Frame(Solid("#00000080"), 10, 10)
                hover_background Frame(Solid("#330000b0" if unlocked else "#00000080"), 10, 10)
                padding (20, 8)
                sensitive unlocked

    ## 角色列表
    if characters:
        vbox:
            xalign 0.9
            yalign 0.5
            spacing 10

            text "在此的人物：" size 24 color "#ffffff"

            for char_name in characters:
                $ alive = is_character_alive(char_name)

                if alive:
                    textbutton char_name:
                        text_size 22
                        text_idle_color "#ffffff"
                        text_hover_color "#ff3333"
                        action Jump("talk_to_" + char_name)
                        background Frame(Solid("#00000080"), 10, 10)
                        hover_background Frame(Solid("#330000b0"), 10, 10)
                        padding (20, 8)

    ## 离开按钮
    textbutton "离开此地":
        xalign 0.5
        yalign 0.9
        background Frame(Solid("#00000080"), 10, 10)
        hover_background Frame(Solid("#1a1a1ab0"), 10, 10)
        padding (30, 10)
        text_size 24
        text_color "#ffffff"
        action Jump("map_screen")
