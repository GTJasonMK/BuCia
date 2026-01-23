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
        "undiscovered_6": "notebook/未发现 6.png"
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
    ## 全屏地图显示（覆盖笔记本背景，使用原始1920x1080尺寸）
    ## 所有坐标严格按照坐标.txt文件

    ## ========== 图层17: 背景 (0, 0) ==========
    add "map/背景.png":
        pos (0, 0)

    ## ========== 图层16: 泥地 (237, 77) ==========
    add "map/泥地.png":
        pos (237, 77)

    ## ========== 图层15: 填充 (36, 4) ==========
    add "map/填充.png":
        pos (36, 4)

    ## ========== 图层14: 路 (147, 43) ==========
    add "map/路.png":
        pos (147, 43)

    ## ========== 图层13: 描边 (39, 2) ==========
    add "map/描边.png":
        pos (39, 2)

    ## ========== 图层1: 粉色碎片 (985, 171) ==========
    add "map/粉色碎片.png":
        pos (985, 171)

    ## ========== 图层2: 蓝色碎片 (1245, 782) ==========
    add "map/蓝色碎片.png":
        pos (1245, 782)

    ## ========== 动态地点标记 ==========
    $ all_locations = renpy.store.get_all_map_locations() if hasattr(renpy.store, "get_all_map_locations") else []
    for loc in all_locations:
        $ loc_pos = loc["pos"]
        $ is_visited = loc["visited"]
        $ is_unlocked = loc["unlocked"]
        if is_visited or is_unlocked:
            if is_unlocked and loc.get("available", True):
                imagebutton:
                    pos loc_pos
                    idle "map/粉色碎片.png"
                    hover Transform("map/粉色碎片.png", zoom=1.1)
                    action SetVariable("notebook_selected_item", loc)
            else:
                imagebutton:
                    pos loc_pos
                    idle "map/蓝色碎片.png"
                    hover Transform("map/蓝色碎片.png", zoom=1.1)
                    action SetVariable("notebook_selected_item", loc)

    ## ========== 图层3: 我的位置 (1535, 189) ==========
    add "map/我的位置.png":
        pos (1535, 189)

    ## ========== 图层4: 我的位置标签 (1494, 160) ==========
    add "map/我的位置标签.png":
        pos (1494, 160)
    text "我的位置":
        pos (1574, 205)
        size 28
        color "#4a3728"
        font "fonts/lolita.ttf"

    ## ========== 图层5: 住址 (1663, 433) ==========
    add "map/住址.png":
        pos (1663, 433)

    ## ========== 图层6: 住址标签 (1572, 392) ==========
    add "map/住址标签.png":
        pos (1572, 392)
    text "住址":
        pos (1692, 437)
        size 28
        color "#4a3728"
        font "fonts/lolita.ttf"

    ## ========== 图层7: 清除 (1648, 632) ==========
    imagebutton:
        pos (1648, 632)
        idle "map/清除.png"
        hover Transform("map/清除.png", zoom=1.05)
        action SetVariable("notebook_selected_item", None)

    ## ========== 图层8: 清除标签 (1572, 604) ==========
    add "map/清除标签.png":
        pos (1572, 604)
    text "清除":
        pos (1692, 649)
        size 28
        color "#4a3728"
        font "fonts/lolita.ttf"

    ## ========== 图层9: 返回 (792, 337) ==========
    imagebutton:
        pos (792, 337)
        idle "map/返回.png"
        hover Transform("map/返回.png", zoom=1.05)
        action Hide("notebook")

    ## ========== 图层10: 返回标签 (1572, 808) ==========
    add "map/返回标签.png":
        pos (1572, 808)
    text "返回":
        pos (1692, 853)
        size 28
        color "#4a3728"
        font "fonts/lolita.ttf"

    ## ========== 图层11: 现在 (753, 434) ==========
    add "map/现在.png":
        pos (753, 434)

    ## ========== 图层12: 现在标签 (724, 331) ==========
    add "map/现在标签.png":
        pos (724, 331)
    text "现在":
        pos (820, 450)
        size 32
        color "#4a3728"
        font "fonts/lolita.ttf"

    ## ========== 返回笔记本按钮（右上角） ==========
    textbutton "返回笔记本":
        pos (1750, 20)
        text_size 18
        text_color "#ffffff"
        background Solid("#2a221880")
        hover_background Solid("#4a3728c0")
        xpadding 15
        ypadding 8
        action Function(switch_notebook_tab, NOTEBOOK_TAB_EVIDENCE)

    ## ========== 结果显示面板（选中地点时显示） ==========
    if notebook_selected_item and isinstance(notebook_selected_item, dict) and "display_name" in notebook_selected_item:
        frame:
            pos (1100, 300)
            xsize 380
            ysize 300
            background "map/结果.png"
            xpadding 30
            ypadding 25

            vbox:
                spacing 12

                ## 地点名称
                text notebook_selected_item.get("display_name", "???"):
                    size 28
                    color "#4a3728"
                    font "fonts/lolita.ttf"

                ## 状态标签
                hbox:
                    spacing 10
                    if notebook_selected_item.get("visited"):
                        text "已访问":
                            size 18
                            color "#8bc34a"
                    if notebook_selected_item.get("unlocked"):
                        text "已解锁":
                            size 18
                            color "#64b5f6"

                null height 5

                ## 描述
                $ loc_info = renpy.store.get_location_info(notebook_selected_item["name"]) if hasattr(renpy.store, "get_location_info") else None
                if loc_info:
                    text loc_info.get("description", ""):
                        size 18
                        color "#5a4a38"
                        font "fonts/lolita.ttf"
                        xmaximum 320

                null height 10

                ## 前往按钮
                if notebook_selected_item.get("unlocked") and notebook_selected_item.get("available", True):
                    textbutton "前往此处":
                        xalign 0.5
                        text_size 20
                        text_color "#ffffff"
                        background Solid("#4a7c4e")
                        hover_background Solid("#5a9c5e")
                        xpadding 25
                        ypadding 8
                        ## 使用 prepare_map_travel + Jump 处理移动和场景跳转
                        action [
                            Function(prepare_map_travel, notebook_selected_item["name"]),
                            Hide("notebook"),
                            Jump("process_map_travel")
                        ]

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
