## 线索系统 UI界面
## 从 data/clues.rpy 移动至此，遵循UI层分离原则

## 线索簿UI
screen clue_book():
    tag menu

    ## 背景
    add "gui/overlay/main_menu.png"

    ## 标题
    frame:
        xalign 0.5
        yalign 0.05
        background Frame(Solid("#00000080"), 10, 10)
        padding (30, 15)

        hbox:
            spacing 20

            text "线索簿" size 40 color "#ffffff"
            text "{size=24}完成度: [get_clue_completion()]%{/size}" color "#ffcc00"

    ## 分类标签
    default clue_category = "all"

    hbox:
        xalign 0.5
        yalign 0.15
        spacing 15

        textbutton "全部":
            text_size 24
            text_idle_color ("#ffcc00" if clue_category == "all" else "#cccccc")
            text_hover_color "#ff3333"
            action SetScreenVariable("clue_category", "all")
            background Frame(Solid("#00000080"), 10, 10)
            hover_background Frame(Solid("#1a1a1ab0"), 10, 10)
            padding (20, 8)

        textbutton "物证":
            text_size 24
            text_idle_color ("#ffcc00" if clue_category == "物证" else "#cccccc")
            text_hover_color "#ff3333"
            action SetScreenVariable("clue_category", "物证")
            background Frame(Solid("#00000080"), 10, 10)
            hover_background Frame(Solid("#1a1a1ab0"), 10, 10)
            padding (20, 8)

        textbutton "档案":
            text_size 24
            text_idle_color ("#ffcc00" if clue_category == "档案" else "#cccccc")
            text_hover_color "#ff3333"
            action SetScreenVariable("clue_category", "档案")
            background Frame(Solid("#00000080"), 10, 10)
            hover_background Frame(Solid("#1a1a1ab0"), 10, 10)
            padding (20, 8)

        textbutton "证词":
            text_size 24
            text_idle_color ("#ffcc00" if clue_category == "证词" else "#cccccc")
            text_hover_color "#ff3333"
            action SetScreenVariable("clue_category", "证词")
            background Frame(Solid("#00000080"), 10, 10)
            hover_background Frame(Solid("#1a1a1ab0"), 10, 10)
            padding (20, 8)

    ## 线索列表
    viewport:
        xalign 0.5
        yalign 0.55
        xsize 1400
        ysize 600
        scrollbars "vertical"
        mousewheel True

        vbox:
            spacing 10

            if clue_category == "all":
                $ clues_to_show = get_discovered_clues()
            else:
                $ clues_to_show = get_clues_by_type(clue_category)

            if len(clues_to_show) == 0:
                text "暂无线索" size 28 color "#666666" xalign 0.5

            for clue in clues_to_show:
                button:
                    xsize 1350
                    background Frame(Solid("#00000080"), 10, 10)
                    hover_background Frame(Solid("#1a1a1ab0"), 10, 10)
                    padding (20, 15)
                    action Show("clue_detail", clue=clue)

                    hbox:
                        spacing 20

                        ## 线索图标
                        if clue.get("image"):
                            add clue.get("image") size (80, 80)
                        else:
                            frame:
                                xsize 80
                                ysize 80
                                background Solid("#333333")

                        vbox:
                            spacing 5

                            ## 线索名称和类型
                            hbox:
                                spacing 15

                                text clue.get("name", "未知线索") size 28 color "#ffffff"

                                text "{size=20}[" + clue.get("type", "未分类") + "]{/size}" color "#ffcc00"

                                # 重要性标记
                                if clue.get("importance") == "critical":
                                    text "{size=20}[关键]{/size}" color "#ff3333"
                                elif clue.get("importance") == "high":
                                    text "{size=20}[重要]{/size}" color "#ff8833"

                            ## 线索描述
                            text clue.get("description", "") size 20 color "#cccccc" xmaximum 1000

                            ## 关联角色
                            if clue.get("relates_to"):
                                text "{size=18}相关: " + ", ".join(clue.get("relates_to", [])) + "{/size}" color "#8888ff"

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

## 线索详情UI
screen clue_detail(clue):
    modal True

    ## 半透明背景
    add Solid("#000000cc")

    ## 详情框
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1000
        ysize 700
        background Frame(Solid("#1a1a1aee"), 15, 15)
        padding (40, 30)

        vbox:
            spacing 20

            ## 线索名称
            hbox:
                spacing 15

                text clue.get("name", "未知线索") size 36 color "#ffffff"

                text "{size=24}[" + clue.get("type", "未分类") + "]{/size}" color "#ffcc00"

            ## 线索图片
            if clue.get("image"):
                add Transform(clue.get("image"), xalign=0.5, fit="contain", xysize=(600, 300))

            ## 详细描述
            text clue.get("detail", clue.get("description", "")) size 22 color "#ffffff" xmaximum 900

            ## 发现信息
            hbox:
                spacing 30

                text "{size=20}发现地点: " + clue.get("location", "未知") + "{/size}" color "#cccccc"

                if clue.get("day_found", 0) > 0:
                    text "{size=20}发现日期: Day " + str(clue.get("day_found")) + "{/size}" color "#cccccc"

            ## 关联角色
            if clue.get("relates_to"):
                text "{size=20}相关角色: " + ", ".join(clue.get("relates_to", [])) + "{/size}" color "#8888ff"

            ## 矛盾线索
            if clue.get("contradicts"):
                text "{size=20}矛盾: " + ", ".join(clue.get("contradicts", [])) + "{/size}" color "#ff3333"

        ## 关闭按钮
        textbutton "关闭":
            xalign 0.5
            yalign 0.95
            background Frame(Solid("#00000080"), 10, 10)
            hover_background Frame(Solid("#330000b0"), 10, 10)
            padding (30, 10)
            text_size 24
            text_color "#ffffff"
            action Hide("clue_detail")
