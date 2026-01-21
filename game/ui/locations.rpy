## 地点系统 UI界面
## 从 data/world/locations.rpy 移动至此，遵循UI层分离原则

## 地图选择UI
screen map_screen():
    tag menu
    ## 使用视觉化地图作为唯一入口
    use visual_map("normal", close_action=Return())

init python:
    def discover_hotspot_clues(location_name, hotspot_name):
        """发现热点关联线索"""
        hotspot = get_hotspot_info(location_name, hotspot_name) if 'get_hotspot_info' in dir() else None
        if not hotspot:
            renpy.notify("该热点尚未配置")
            return
        clues = hotspot.get("clues", [])
        if not clues:
            renpy.notify("没有发现线索")
            return
        found_any = False
        if 'discover_clue' in dir():
            for clue_id in clues:
                if discover_clue(clue_id):
                    found_any = True
        if not found_any:
            renpy.notify("没有新线索")

    def resolve_hotspot_action(location_name, hotspot_name):
        """根据热点配置返回对应动作"""
        hotspot = get_hotspot_info(location_name, hotspot_name) if 'get_hotspot_info' in dir() else None
        if not hotspot:
            return Function(renpy.notify, "该热点尚未配置")
        hotspot_label = hotspot.get("label")
        if hotspot_label and renpy.has_label(hotspot_label):
            return Jump(hotspot_label)
        special_action = hotspot.get("special_action")
        if special_action:
            if 'run_hotspot_special_action' in dir():
                return Function(run_hotspot_special_action, special_action)
            return Function(renpy.notify, "该热点特殊动作未实现")
        if hotspot.get("clues"):
            return Function(discover_hotspot_clues, location_name, hotspot_name)
        return Function(renpy.notify, "该热点尚未实现")

## 地点探索UI
screen location_explore(location_name):
    tag location

    $ loc_info = get_location_info(location_name)
    $ bg_image = loc_info.get("background", "bg/default_bg.jpg") if loc_info else "bg/default_bg.jpg"
    if not renpy.loadable(bg_image):
        $ bg_image = "bg/default_bg.jpg"
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
            $ hotspot_action = resolve_hotspot_action(location_name, hotspot_name)

            textbutton hotspot_name:
                text_size 22
                text_idle_color ("#ffffff" if unlocked else "#666666")
                text_hover_color ("#ff3333" if unlocked else "#666666")
                action [
                    If(unlocked,
                       hotspot_action,
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
                $ talk_label = get_character_talk_label(char_name)
                $ talk_action = Jump(talk_label) if talk_label and renpy.has_label(talk_label) else Function(renpy.notify, "该角色对话未配置")

                if alive:
                    textbutton char_name:
                        text_size 22
                        text_idle_color "#ffffff"
                        text_hover_color "#ff3333"
                        action talk_action
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
        action Return()
