## 笔记本UI系统
## 提供证物、人物、记录、地图四个标签页的笔记本界面

## ============================================================================
## 配置参数
## ============================================================================

## 笔记本缩放比例（所有素材已按1920x1080设计，无需缩放）
define NOTEBOOK_SCALE = 1.0

## 标签页类型
define NOTEBOOK_TAB_EVIDENCE = "evidence"    ## 证物
define NOTEBOOK_TAB_CHARACTERS = "characters" ## 人物
define NOTEBOOK_TAB_RECORDS = "records"      ## 记录
define NOTEBOOK_TAB_MAP = "map"              ## 地图

## 当前选中的标签页
default notebook_current_tab = NOTEBOOK_TAB_EVIDENCE

## 当前选中的项目索引（用于详情显示）
default notebook_selected_item = None

## 当前页码（每页6个项目）
default notebook_current_page = 0

## ============================================================================
## 笔记本图片路径
## ============================================================================

init python:
    NOTEBOOK_IMAGES = {
        ## 背景
        "background": "notebook/背景纸.png",
        "paper": "notebook/褶皱笔记纸.png",

        ## 标签按钮（选中/未选中）
        "tab_evidence_selected": "notebook/证物(选中）.png",
        "tab_evidence_idle": "notebook/证物(未选中）.png",
        "tab_characters_selected": "notebook/人物(选中）.png",
        "tab_characters_idle": "notebook/人物(未选中）.png",
        "tab_records_selected": "notebook/记录(选中）.png",
        "tab_records_idle": "notebook/记录(未选中）.png",
        "tab_map_selected": "notebook/地图(选中）.png",
        "tab_map_idle": "notebook/地图(未选中）.png",

        ## 标签图标（装饰用）
        "icon_evidence": "notebook/证物.png",
        "icon_characters": "notebook/人物.png",
        "icon_records": "notebook/记录.png",
        "icon_map": "notebook/地图.png",

        ## 导航
        "arrow_left": "notebook/向左.png",
        "arrow_right": "notebook/向右.png",

        ## 关闭/返回
        "close_selected": "notebook/关闭UI（选中）.png",
        "close_idle": "notebook/关闭UI（未选中）.png",
        "return_selected": "notebook/返回（选中）.png",
        "return_idle": "notebook/返回（未选中）.png",

        ## 内容区域
        "grid": "notebook/六宫格.png",
        "dialogue": "notebook/对话框.png",
        "tape": "notebook/胶带.png",

        ## 装饰元素
        "closing_tear": "notebook/关闭的撕纸.png",

        ## 未发现占位图
        "undiscovered_1": "notebook/未发现 1.png",
        "undiscovered_2": "notebook/未发现 2.png",
        "undiscovered_3": "notebook/未发现 3.png",
        "undiscovered_4": "notebook/未发现 4.png",
        "undiscovered_5": "notebook/未发现 5.png",
        "undiscovered_6": "notebook/未发现 6.png",
    }
    MAP_IMAGES = {
        ## 地图元素
        "background":"map/背景.png",
        "dirt":"map/泥地.png",
        "fill":"map/填充.png",
        "road":"map/路.png",
        "outline":"map/描边.png",
        "marker_pink":"map/粉色碎片.png",
        "marker_blue":"map/蓝色碎片.png",
        "marker_current":"map/现在.png",
        "marker_current_label":"map/现在标签.png",
        "marker_location":"map/我的位置.png",
        "marker_location_label":"map/我的位置标签.png",
        "btn_return":"map/返回.png",
        "btn_return_label":"map/返回标签.png",

    }

    ## UI元素坐标（基于坐标.txt，已按游戏分辨率1920x1080设计）
    ## 所有坐标直接使用，无需缩放
    NOTEBOOK_POSITIONS = {
        ## 箭头导航
        "arrow_right": (639, 827),
        "arrow_left": (134, 827),

        ## 六宫格内容位置
        "grid": (26, 89),

        ## 返回按钮（详情页用）
        "return": (1779, 933),

        ## 对话框（底部）
        "dialogue": (0, 907),

        ## 关闭UI按钮
        "close": (1830, 11),

        ## 装饰元素
        "closing_tear": (1757, 0),
        "tape": (959, 0),
        "paper": (1016, 44),

        ## 标签图标位置（装饰用，与按钮位置对应）
        ## 顺序：证物→地图→记录→人物（从上到下）
        "icon_evidence": (1743, 215),
        "icon_map": (1748, 405),
        "icon_records": (1741, 588),
        "icon_characters": (1749, 775),

        ## 标签按钮位置
        ## 顺序：证物→地图→记录→人物（从上到下）
        "tab_evidence": (1612, 185),
        "tab_map": (1612, 375),
        "tab_records": (1612, 555),
        "tab_characters": (1611, 747),
    }

    ## 六宫格位置（基于坐标.txt）
    NOTEBOOK_GRID_POSITIONS = [
        (65, 67),    ## 位置1
        (357, 67),   ## 位置2
        (661, 67),   ## 位置3
        (65, 439),   ## 位置4
        (357, 439),  ## 位置5
        (661, 439)   ## 位置6
    ]

    ## 获取当前标签页的项目列表
    def get_notebook_items(tab):
        """获取指定标签页的项目列表"""
        if tab == NOTEBOOK_TAB_EVIDENCE:
            ## 返回已发现的线索
            return renpy.store.get_discovered_clues() if hasattr(renpy.store, "get_discovered_clues") else []
        elif tab == NOTEBOOK_TAB_CHARACTERS:
            ## 返回已遇见的角色
            return renpy.store.get_met_characters() if hasattr(renpy.store, "get_met_characters") else []
        elif tab == NOTEBOOK_TAB_RECORDS:
            ## 返回所有记录
            return renpy.store.get_all_records() if hasattr(renpy.store, "get_all_records") else []
        elif tab == NOTEBOOK_TAB_MAP:
            ## 地图标签页不使用此函数获取数据
            ## 地图内容由 notebook_map_content() 直接调用 get_all_map_locations() 渲染
            return []
        return []

    ## 获取指定页的项目
    def get_notebook_page_items(tab, page):
        """获取指定标签页指定页码的项目（每页6个）"""
        items = get_notebook_items(tab)
        start = page * 6
        end = start + 6
        return items[start:end]

    ## 获取总页数
    def get_notebook_total_pages(tab):
        """获取指定标签页的总页数"""
        items = get_notebook_items(tab)
        total = len(items)
        if total == 0:
            return 1
        return (total + 5) // 6  ## 向上取整

    ## 切换标签页
    def switch_notebook_tab(tab):
        """切换到指定标签页"""
        store.notebook_current_tab = tab
        store.notebook_current_page = 0
        store.notebook_selected_item = None

    ## 翻页
    def notebook_prev_page():
        """上一页"""
        if store.notebook_current_page > 0:
            store.notebook_current_page -= 1

    def notebook_next_page():
        """下一页"""
        total = get_notebook_total_pages(store.notebook_current_tab)
        if store.notebook_current_page < total - 1:
            store.notebook_current_page += 1

## ============================================================================
## 笔记本主屏幕
## ============================================================================

screen notebook():
    ## 笔记本界面
    tag menu
    modal True

    ## 显示时隐藏摄像机UI，关闭时恢复
    on "show" action SetVariable("camera_ui_enabled", False)
    on "hide" action SetVariable("camera_ui_enabled", True)

    ## 快捷键
    key "n" action Hide("notebook")
    key "K_ESCAPE" action Hide("notebook")

    ## 半透明背景遮罩
    add Solid("#00000080")

    ## 笔记本主体
    fixed:
        ## ========== 地图标签页特殊处理（全屏显示） ==========
        if notebook_current_tab == NOTEBOOK_TAB_MAP:
            ## 地图内容全屏显示
            use notebook_map_content
        else:
            ## ========== 其他标签页：显示笔记本背景 ==========
            ## 底层：背景纸
            add NOTEBOOK_IMAGES["background"]:
                pos (0, 0)

            ## 装饰层：胶带
            add NOTEBOOK_IMAGES["tape"]:
                pos NOTEBOOK_POSITIONS["tape"]

            ## 装饰层：褶皱笔记纸
            add NOTEBOOK_IMAGES["paper"]:
                pos NOTEBOOK_POSITIONS["paper"]

            ## 内容区域：六宫格背景（仅证物和人物）
            if notebook_current_tab in [NOTEBOOK_TAB_EVIDENCE, NOTEBOOK_TAB_CHARACTERS]:
                add NOTEBOOK_IMAGES["grid"]:
                    pos NOTEBOOK_POSITIONS["grid"]

            ## 装饰层：关闭的撕纸
            add NOTEBOOK_IMAGES["closing_tear"]:
                pos NOTEBOOK_POSITIONS["closing_tear"]

            ## 底部：对话框装饰
            add NOTEBOOK_IMAGES["dialogue"]:
                pos NOTEBOOK_POSITIONS["dialogue"]

            ## 根据当前标签页显示内容
            if notebook_current_tab == NOTEBOOK_TAB_EVIDENCE:
                use notebook_evidence_content
            elif notebook_current_tab == NOTEBOOK_TAB_CHARACTERS:
                use notebook_characters_content
            elif notebook_current_tab == NOTEBOOK_TAB_RECORDS:
                use notebook_records_content

            ## 翻页按钮
            $ total_pages = get_notebook_total_pages(notebook_current_tab)

            ## 左箭头（上一页）
            if notebook_current_page > 0:
                imagebutton:
                    idle NOTEBOOK_IMAGES["arrow_left"]
                    hover Transform(NOTEBOOK_IMAGES["arrow_left"], zoom=1.1)
                    action Function(notebook_prev_page)
                    pos NOTEBOOK_POSITIONS["arrow_left"]
            else:
                add Transform(NOTEBOOK_IMAGES["arrow_left"], alpha=0.3):
                    pos NOTEBOOK_POSITIONS["arrow_left"]

            ## 右箭头（下一页）
            if notebook_current_page < total_pages - 1:
                imagebutton:
                    idle NOTEBOOK_IMAGES["arrow_right"]
                    hover Transform(NOTEBOOK_IMAGES["arrow_right"], zoom=1.1)
                    action Function(notebook_next_page)
                    pos NOTEBOOK_POSITIONS["arrow_right"]
            else:
                add Transform(NOTEBOOK_IMAGES["arrow_right"], alpha=0.3):
                    pos NOTEBOOK_POSITIONS["arrow_right"]

            ## 页码显示
            $ page_center_x = int((NOTEBOOK_POSITIONS["arrow_left"][0] + NOTEBOOK_POSITIONS["arrow_right"][0]) / 2)
            $ page_y = NOTEBOOK_POSITIONS["arrow_left"][1] + 20
            text "[notebook_current_page + 1]/[total_pages]":
                xpos page_center_x
                ypos page_y
                xanchor 0.5
                size 24
                color "#4a3728"
                font "fonts/lolita.ttf"

        ## ========== 笔记本UI元素（仅非地图标签页显示） ==========
        if notebook_current_tab != NOTEBOOK_TAB_MAP:
            ## 右侧标签图标
            add NOTEBOOK_IMAGES["icon_evidence"]:
                pos NOTEBOOK_POSITIONS["icon_evidence"]

            add NOTEBOOK_IMAGES["icon_map"]:
                pos NOTEBOOK_POSITIONS["icon_map"]

            add NOTEBOOK_IMAGES["icon_records"]:
                pos NOTEBOOK_POSITIONS["icon_records"]

            add NOTEBOOK_IMAGES["icon_characters"]:
                pos NOTEBOOK_POSITIONS["icon_characters"]

            ## 右侧标签按钮
            ## 证物标签
            $ tab_evidence_img = NOTEBOOK_IMAGES["tab_evidence_selected"] if notebook_current_tab == NOTEBOOK_TAB_EVIDENCE else NOTEBOOK_IMAGES["tab_evidence_idle"]
            imagebutton:
                idle tab_evidence_img
                hover NOTEBOOK_IMAGES["tab_evidence_selected"]
                action Function(switch_notebook_tab, NOTEBOOK_TAB_EVIDENCE)
                pos NOTEBOOK_POSITIONS["tab_evidence"]

            ## 地图标签
            $ tab_map_img = NOTEBOOK_IMAGES["tab_map_selected"] if notebook_current_tab == NOTEBOOK_TAB_MAP else NOTEBOOK_IMAGES["tab_map_idle"]
            imagebutton:
                idle tab_map_img
                hover NOTEBOOK_IMAGES["tab_map_selected"]
                action Function(switch_notebook_tab, NOTEBOOK_TAB_MAP)
                pos NOTEBOOK_POSITIONS["tab_map"]

            ## 记录标签
            $ tab_records_img = NOTEBOOK_IMAGES["tab_records_selected"] if notebook_current_tab == NOTEBOOK_TAB_RECORDS else NOTEBOOK_IMAGES["tab_records_idle"]
            imagebutton:
                idle tab_records_img
                hover NOTEBOOK_IMAGES["tab_records_selected"]
                action Function(switch_notebook_tab, NOTEBOOK_TAB_RECORDS)
                pos NOTEBOOK_POSITIONS["tab_records"]

            ## 人物标签
            $ tab_characters_img = NOTEBOOK_IMAGES["tab_characters_selected"] if notebook_current_tab == NOTEBOOK_TAB_CHARACTERS else NOTEBOOK_IMAGES["tab_characters_idle"]
            imagebutton:
                idle tab_characters_img
                hover NOTEBOOK_IMAGES["tab_characters_selected"]
                action Function(switch_notebook_tab, NOTEBOOK_TAB_CHARACTERS)
                pos NOTEBOOK_POSITIONS["tab_characters"]

            ## 关闭按钮
            imagebutton:
                idle NOTEBOOK_IMAGES["close_idle"]
                hover NOTEBOOK_IMAGES["close_selected"]
                action Hide("notebook")
                pos NOTEBOOK_POSITIONS["close"]

            ## 返回按钮
            if notebook_selected_item is not None:
                imagebutton:
                    idle NOTEBOOK_IMAGES["return_idle"]
                    hover NOTEBOOK_IMAGES["return_selected"]
                    action SetVariable("notebook_selected_item", None)
                    pos NOTEBOOK_POSITIONS["return"]
            else:
                imagebutton:
                    idle NOTEBOOK_IMAGES["return_idle"]
                    hover NOTEBOOK_IMAGES["return_selected"]
                    action Hide("notebook")
                    pos NOTEBOOK_POSITIONS["return"]

## ============================================================================
## 证物标签页内容
## ============================================================================

screen notebook_evidence_content():
    $ items = get_notebook_page_items(NOTEBOOK_TAB_EVIDENCE, notebook_current_page)

    for i in range(6):
        $ slot_pos = NOTEBOOK_GRID_POSITIONS[i]

        if i < len(items):
            ## 显示线索图标
            $ clue = items[i]
            button:
                pos slot_pos
                action SetVariable("notebook_selected_item", clue)
                if clue.get("icon"):
                    add clue["icon"]
                else:
                    ## 默认图标
                    add Solid("#8b7355"):
                        size (250, 277)
                    text clue.get("name", "???"):
                        xalign 0.5
                        yalign 0.5
                        size 20
                        color "#ffffff"
        else:
            ## 未发现占位图
            $ undiscovered_key = "undiscovered_{}".format((i % 6) + 1)
            add NOTEBOOK_IMAGES[undiscovered_key]:
                pos slot_pos

    ## 详情显示区域（如果选中了项目）
    if notebook_selected_item:
        use notebook_detail_panel(notebook_selected_item, "evidence")

## ============================================================================
## 人物标签页内容
## ============================================================================

screen notebook_characters_content():
    $ items = get_notebook_page_items(NOTEBOOK_TAB_CHARACTERS, notebook_current_page)

    for i in range(6):
        $ slot_pos = NOTEBOOK_GRID_POSITIONS[i]

        if i < len(items):
            ## 显示角色头像
            $ char = items[i]
            $ char_name = char.get("full_name", char.get("name", "???"))
            button:
                pos slot_pos
                action SetVariable("notebook_selected_item", char)
                ## 角色头像或默认显示
                add Solid(char.get("color", "#888888")):
                    size (250, 277)
                $ impression_text = renpy.store.get_impression_display(char_name) if hasattr(renpy.store, "get_impression_display") else "未知"
                text "印象：" + impression_text:
                    xalign 0.5
                    yalign 0.78
                    size 18
                    color "#ffffff"
                    outlines [(2, "#000000", 0, 0)]
                text char_name:
                    xalign 0.5
                    yalign 0.9
                    size 24
                    color "#ffffff"
                    outlines [(2, "#000000", 0, 0)]
        else:
            ## 未发现占位图
            $ undiscovered_key = "undiscovered_{}".format((i % 6) + 1)
            add NOTEBOOK_IMAGES[undiscovered_key]:
                pos slot_pos

    ## 详情显示区域
    if notebook_selected_item:
        use notebook_detail_panel(notebook_selected_item, "character")

## ============================================================================
## 记录标签页内容
## ============================================================================

screen notebook_records_content():
    $ items = get_notebook_page_items(NOTEBOOK_TAB_RECORDS, notebook_current_page)

    ## 记录列表（垂直排列）
    vbox:
        xpos 80
        ypos 120
        spacing 20

        if len(items) == 0:
            text "暂无记录":
                size 28
                color "#4a3728"
                font "fonts/lolita.ttf"
        else:
            for record in items:
                button:
                    xsize 600
                    ysize 80
                    action SetVariable("notebook_selected_item", record)
                    background Solid("#d4c4a8" if notebook_selected_item == record else "#e8dcc8")
                    hbox:
                        spacing 20
                        xalign 0.0
                        yalign 0.5
                        xoffset 20

                        ## 分类图标
                        $ category = record.get("category", "note")
                        if category == "story":
                            text "[故事]":
                                size 20
                                color "#8b0000"
                        elif category == "event":
                            text "[事件]":
                                size 20
                                color "#006400"
                        else:
                            text "[笔记]":
                                size 20
                                color "#4a3728"

                        text record.get("title", "无标题"):
                            size 24
                            color "#4a3728"
                            font "fonts/lolita.ttf"

    ## 详情显示区域
    if notebook_selected_item:
        use notebook_detail_panel(notebook_selected_item, "record")

## ============================================================================
## 地图标签页内容（全屏显示，使用原始坐标）
## ============================================================================
##
## UI组件坐标（基于坐标.txt，设计尺寸1920x1080）：
##   背景: (0, 0)
##   泥地: (36, 4)
##   填充: (237, 77)
##   路: (147, 43)
##   描边: (39, 2)
##   粉色碎片: (985, 171) - 示例位置
##   蓝色碎片: (1245, 782) - 示例位置
##   我的位置: (1535, 189)
##   我的位置 标签: (1494, 160)
##   住址: (1663, 433)
##   住址 标签: (1572, 392)
##   现在: (1648, 632)
##   现在 标签: (1572, 604)
##   返回: (792, 337)
##   返回 标签: (724, 331)
##   清除: (753, 434)
##   清除 标签: (1572, 808)
##
## ============================================================================

screen notebook_map_content():
    ## 全屏地图显示（与主地图同一套图层、坐标与缩放）
    $ map_scale = MAP_SCALE

    ## ========== 地图背景层 ==========
    fixed:
        add MAP_IMAGES["background"]:
            pos (0, 0)
            zoom map_scale

        add MAP_IMAGES["dirt"]:
            pos (int(MAP_LAYER_POSITIONS["dirt"][0] * map_scale), int(MAP_LAYER_POSITIONS["dirt"][1] * map_scale))
            zoom map_scale

        add MAP_IMAGES["fill"]:
            pos (int(MAP_LAYER_POSITIONS["fill"][0] * map_scale), int(MAP_LAYER_POSITIONS["fill"][1] * map_scale))
            zoom map_scale

        add MAP_IMAGES["road"]:
            pos (int(MAP_LAYER_POSITIONS["road"][0] * map_scale), int(MAP_LAYER_POSITIONS["road"][1] * map_scale))
            zoom map_scale

        add MAP_IMAGES["outline"]:
            pos (int(MAP_LAYER_POSITIONS["outline"][0] * map_scale), int(MAP_LAYER_POSITIONS["outline"][1] * map_scale))
            zoom map_scale

    ## ========== 地点标记 ==========
    fixed:
        $ all_locations = renpy.store.get_all_map_locations() if hasattr(renpy.store, "get_all_map_locations") else []

        for loc in all_locations:
            $ loc_pos = loc["pos"]
            $ is_current = (renpy.store.get_current_location() if hasattr(renpy.store, "get_current_location") else None) == loc["name"]
            $ is_revealed = loc["name"] in getattr(persistent, "unlocked_locations", [])

            $ map_x = int(loc_pos[0] * map_scale)
            $ map_y = int(loc_pos[1] * map_scale)

            if is_current:
                fixed:
                    pos (map_x - 20, map_y - 20)
                    add MAP_IMAGES["marker_current"]:
                        zoom map_scale * 1.2
                    add MAP_IMAGES["marker_current_label"]:
                        pos (40, -30)
                        zoom map_scale * 0.8
            else:
                imagebutton:
                    pos (map_x - 5, map_y - 5)
                    idle Transform(MAP_IMAGES["marker_pink"] if is_revealed else MAP_IMAGES["marker_blue"], zoom=map_scale * 0.4)
                    hover Transform(MAP_IMAGES["marker_pink"] if is_revealed else MAP_IMAGES["marker_blue"], zoom=map_scale * 0.4 * 1.2)
                    action SetVariable("notebook_selected_item", loc)
                    hovered [
                        SetVariable("map_hover_label", loc["display_name"]),
                        SetVariable("map_hover_pos", loc["pos"])
                    ]
                    unhovered [
                        SetVariable("map_hover_label", ""),
                        SetVariable("map_hover_pos", None)
                    ]

    ## ========== 当前位置标记 ==========
    if hasattr(renpy.store, "get_current_location"):
        $ current_loc = renpy.store.get_current_location()
        $ current_pos = renpy.store.get_location_map_pos(current_loc) if hasattr(renpy.store, "get_location_map_pos") else None
        if current_pos:
            fixed:
                pos (int(current_pos[0] * map_scale) - 25, int(current_pos[1] * map_scale) - 50)
                add MAP_IMAGES["marker_location"]:
                    zoom map_scale
                add MAP_IMAGES["marker_location_label"]:
                    pos (30, -25)
                    zoom map_scale * 0.7

    ## ========== 悬浮地点标签 ==========
    if map_hover_label and map_hover_pos:
        $ hover_pos = map_hover_pos
        $ hover_x = int(hover_pos[0] * map_scale)
        $ hover_y = int(hover_pos[1] * map_scale)
        frame:
            xanchor 0.5
            yanchor 1.0
            xpos hover_x
            ypos hover_y - int(30 * map_scale)
            background Solid("#1a1510cc")
            xpadding 12
            ypadding 6

            text map_hover_label:
                size 20
                color "#f5e6c8"
                font "fonts/lolita.ttf"

    ## ========== 选中地点信息 ==========
    if notebook_selected_item and isinstance(notebook_selected_item, dict) and "display_name" in notebook_selected_item:
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

                text notebook_selected_item.get("display_name", "???"):
                    size 28
                    color "#f5e6c8"
                    font "fonts/lolita.ttf"

                hbox:
                    spacing 15
                    if notebook_selected_item.get("unlocked"):
                        text "已解锁":
                            size 18
                            color "#8bc34a"
                    else:
                        text "未解锁":
                            size 18
                            color "#f44336"

                    if notebook_selected_item.get("available"):
                        text "可前往":
                            size 18
                            color "#8bc34a"
                    else:
                        text "当前时段不可":
                            size 18
                            color "#ff9800"

                    if notebook_selected_item.get("visited"):
                        text "已访问":
                            size 18
                            color "#9e9e9e"

                null height 10

                $ loc_info = renpy.store.get_location_info(notebook_selected_item["name"]) if hasattr(renpy.store, "get_location_info") else None
                if loc_info:
                    text loc_info.get("description", ""):
                        size 18
                        color "#d4c4a8"
                        font "fonts/lolita.ttf"
                        xmaximum 340

                null height 15

                if notebook_selected_item.get("unlocked") and notebook_selected_item.get("available", True):
                    textbutton "前往此处":
                        xalign 0.5
                        text_size 20
                        text_color "#ffffff"
                        background Solid("#4a7c4e")
                        hover_background Solid("#5a9c5e")
                        xpadding 25
                        ypadding 8
                        action [
                            Function(prepare_map_travel, notebook_selected_item["name"]),
                            Hide("notebook"),
                            Jump("process_map_travel")
                        ]
                else:
                    textbutton "关闭":
                        xalign 0.5
                        text_size 20
                        text_color "#ffffff"
                        background Solid("#5a4a3a")
                        hover_background Solid("#7a6a5a")
                        xpadding 25
                        ypadding 8
                        action SetVariable("notebook_selected_item", None)

    ## ========== 返回笔记本 ==========
    fixed:
        add MAP_IMAGES["btn_return_label"]:
            pos (int(792 * map_scale), int(870 * map_scale))
            zoom map_scale * 0.8 
               
        imagebutton:
            pos (int(845 * map_scale), int(870 * map_scale))
            idle Transform(MAP_IMAGES["btn_return"], zoom=map_scale * 0.8)
            hover Transform(MAP_IMAGES["btn_return"], zoom=map_scale * 0.8 * 1.1)
            action Function(switch_notebook_tab, NOTEBOOK_TAB_EVIDENCE)




## ============================================================================
## 详情面板
## ============================================================================

screen notebook_detail_panel(item, item_type):
    ## 右侧详情面板
    frame:
        xpos 750
        ypos 100
        xsize 450
        ysize 600
        background Solid("#f5f0e6")

        vbox:
            spacing 15
            xalign 0.5
            yalign 0.0
            yoffset 20

            ## 返回按钮
            imagebutton:
                idle Transform(NOTEBOOK_IMAGES["return_idle"], zoom=0.8)
                hover Transform(NOTEBOOK_IMAGES["return_selected"], zoom=0.8)
                action SetVariable("notebook_selected_item", None)
                xalign 1.0

            ## 根据类型显示不同内容
            if item_type == "evidence":
                ## 线索详情
                text item.get("name", "未知线索"):
                    size 32
                    color "#4a3728"
                    font "fonts/lolita.ttf"
                    xalign 0.5

                null height 10

                text item.get("description", "无描述"):
                    size 22
                    color "#5a4a38"
                    font "fonts/lolita.ttf"
                    xmaximum 400
                    text_align 0.0

            elif item_type == "character":
                ## 角色详情
                $ char_name = item.get("full_name", "???")
                text char_name:
                    size 36
                    color item.get("color", "#4a3728")
                    font "fonts/lolita.ttf"
                    xalign 0.5

                text item.get("role", ""):
                    size 24
                    color "#666666"
                    font "fonts/lolita.ttf"
                    xalign 0.5

                text "印象: [renpy.store.get_impression_display(char_name) if hasattr(renpy.store, 'get_impression_display') else '未知']":
                    size 22
                    color "#4a3728"
                    font "fonts/lolita.ttf"
                    xalign 0.5

                null height 10

                text "简介:":
                    size 20
                    color "#4a3728"
                    font "fonts/lolita.ttf"

                text item.get("bio", "无信息"):
                    size 20
                    color "#5a4a38"
                    font "fonts/lolita.ttf"
                    xmaximum 400
                    text_align 0.0

                null height 10

                ## 信任度显示
                hbox:
                    spacing 10
                    text "信任度:":
                        size 20
                        color "#4a3728"
                    $ trust = item.get("trust", 0)
                    bar:
                        value trust
                        range 100
                        xsize 200
                        ysize 20
                        left_bar Solid("#4a9c4a")
                        right_bar Solid("#cccccc")

            elif item_type == "record":
                ## 记录详情
                text item.get("title", "无标题"):
                    size 32
                    color "#4a3728"
                    font "fonts/lolita.ttf"
                    xalign 0.5

                $ category = item.get("category", "note")
                $ category_text = {"story": "故事", "event": "事件", "note": "笔记"}.get(category, "笔记")
                text "分类: [category_text]":
                    size 20
                    color "#666666"
                    font "fonts/lolita.ttf"
                    xalign 0.5

                $ day = item.get("day", 0)
                if day > 0:
                    text "Day [day]":
                        size 18
                        color "#888888"
                        font "fonts/lolita.ttf"
                        xalign 0.5

                null height 15

                text item.get("content", "无内容"):
                    size 22
                    color "#5a4a38"
                    font "fonts/lolita.ttf"
                    xmaximum 400
                    text_align 0.0

## ============================================================================
## 使用示例
## ============================================================================
##
## 打开笔记本:
##   show screen notebook
##
## 关闭笔记本:
##   hide screen notebook
##
## 快捷键:
##   N - 打开/关闭笔记本
##   ESC - 关闭笔记本
##
