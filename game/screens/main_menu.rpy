################################################################################
## 初始化
################################################################################

init offset = -1

## 控制Start按钮展开状态的变量
default show_episodes = False

## 左下文本框提示信息
default button_hint_text = ""

## 按钮悬停状态变量（用于相邻按钮退避）
default start_hovered = False
default config_hovered = False
default official_hovered = False
default exit_hovered = False
default episode1_hovered = False
default episode2_hovered = False
default episode3_hovered = False
default load_hovered = False

## 周目按钮下拉动画
transform episodes_slide_down:
    on show:
        yoffset -50
        alpha 0.0
        easein 0.4 yoffset 0 alpha 1.0
    on hide:
        easeout 0.3 yoffset -30 alpha 0.0

## 周目按钮从右侧滑入动画
transform slide_in_1:
    alpha 0.0 xoffset 500
    ease 0.3 alpha 1.0 xoffset 0

transform slide_in_2:
    alpha 0.0 xoffset 500
    pause 0.1
    ease 0.3 alpha 1.0 xoffset 0

transform slide_in_3:
    alpha 0.0 xoffset 500
    pause 0.2
    ease 0.3 alpha 1.0 xoffset 0

transform slide_in_4:
    alpha 0.0 xoffset 500
    pause 0.3
    ease 0.3 alpha 1.0 xoffset 0

## 主按钮从右侧滑入动画（用于关闭周目选择后）
transform main_slide_in_1:
    alpha 0.0 xoffset 500
    ease 0.3 alpha 1.0 xoffset 0

transform main_slide_in_2:
    alpha 0.0 xoffset 500
    pause 0.1
    ease 0.3 alpha 1.0 xoffset 0

transform main_slide_in_3:
    alpha 0.0 xoffset 500
    pause 0.2
    ease 0.3 alpha 1.0 xoffset 0

## 按钮悬停放大效果 - 主按钮
transform main_button_hover:
    zoom 0.346 alpha 1.0
    on hover:
        linear 0.15 zoom 0.3806 alpha 0.85
    on idle:
        linear 0.15 zoom 0.346 alpha 1.0

## 按钮悬停放大效果 - 周目按钮
transform episode_button_hover:
    zoom 0.25 alpha 1.0
    on hover:
        linear 0.15 zoom 0.275 alpha 0.85
    on idle:
        linear 0.15 zoom 0.25 alpha 1.0

################################################################################
## 按钮动画系统
################################################################################
##
## 系统说明：
## 此系统为主菜单按钮提供动态的悬停效果，包括：
## 1. 文字缩放：悬停时文字放大到1.1倍
## 2. 按钮退避：悬停时下方相邻按钮自动向下偏移，保持间距不变
##
## 如何添加新按钮：
## 1. 在下方的 BUTTON_GROUPS 配置中添加按钮名称
## 2. 在对应位置添加 default xxx_hovered = False 变量定义
## 3. 在下方的 Transform 定义区添加对应的 transform
##
## 配置项说明：
## - buttons: 按钮名称列表，顺序很重要（决定依赖关系）
## - offset_per_button: 每个悬停按钮导致下方按钮偏移的像素数
##

init python:
    ## ====== 按钮分组配置 ======
    BUTTON_GROUPS = {
        "main": {
            "buttons": ["start", "config", "official", "exit"],
            "offset_per_button": 10
        },
        "episode": {
            "buttons": ["episode1", "episode2", "episode3", "load"],
            "offset_per_button": 8
        }
    }

    ## ====== 文字样式配置 ======
    ## 集中管理所有文字的字体、大小、颜色等样式
    ## 使用方式：text "xxx": properties TEXT_STYLES["样式名"]
    TEXT_STYLES = {
        "hint": {
            # 左下角提示文字样式
            "size": 32,
            "color": "#ffffff",
            "font": "fonts/Holy-Union-2.ttf"
        },
        "main_button": {
            # 主按钮文字样式 (Start, Config, Official Web, Exit)
            "size": 85,
            "color": "#ffffff",
            "font": "fonts/Holy-Union-2.ttf",
            "outlines": [(2, "#00000080", 0, 0)]
        },
        "episode_status": {
            # 周目状态文字样式 (Locked)
            "size": 45,
            "color": "#ffffff",
            "font": "fonts/Holy-Union-2.ttf",
            "outlines": [(2, "#00000080", 0, 0)]
        },
        "episode_button": {
            # 周目按钮文字样式 (Episode 1/2/3, Load Game)
            # 注意：color 属性由各按钮根据解锁状态单独设置
            "size": 60,
            "font": "fonts/Holy-Union-2.ttf",
            "outlines": [(2, "#00000080", 0, 0)]
        }
    }

    ## ====== 自动生成包装函数 ======
    ## 根据配置自动为每个按钮创建文字缩放和偏移函数
    for group_name, group_config in BUTTON_GROUPS.items():
        buttons = group_config["buttons"]
        offset = group_config["offset_per_button"]

        for i, button_name in enumerate(buttons):
            var_name = button_name + "_hovered"

            # 创建文字缩放函数（所有按钮都需要）
            # 使用闭包捕获 var_name，避免后期绑定问题
            func = (lambda vn: lambda trans, st, at: text_zoom_function(trans, st, at, vn))(var_name)
            setattr(store, button_name + "_text_zoom_func", func)

            # 为非首个按钮创建偏移函数（首个按钮不需要偏移）
            # 每个按钮依赖组内所有上方按钮的悬停状态
            if i > 0:
                dependencies = [buttons[j] + "_hovered" for j in range(i)]
                func = (lambda deps, off: lambda trans, st, at: offset_function(trans, st, at, deps, off))(dependencies, offset)
                setattr(store, button_name + "_offset_func", func)



################################################################################
## Transform 定义
################################################################################
##
## 注意：Transform 必须静态定义，无法通过 Python 循环动态生成
## 每个按钮需要一个 xxx_text_zoom transform
## 非首个按钮需要额外的 xxx_offset transform
##

## 主按钮组 Transforms
transform start_text_zoom:
    function start_text_zoom_func

transform config_text_zoom:
    function config_text_zoom_func

transform config_offset:
    function config_offset_func

transform official_text_zoom:
    function official_text_zoom_func

transform official_offset:
    function official_offset_func

transform exit_text_zoom:
    function exit_text_zoom_func

transform exit_offset:
    function exit_offset_func

## 周目按钮组 Transforms
transform episode1_text_zoom:
    function episode1_text_zoom_func

transform episode2_text_zoom:
    function episode2_text_zoom_func

transform episode2_offset:
    function episode2_offset_func

transform episode3_text_zoom:
    function episode3_text_zoom_func

transform episode3_offset:
    function episode3_offset_func

transform load_text_zoom:
    function load_text_zoom_func

transform load_offset:
    function load_offset_func


################################################################################
## 样式
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## 游戏内屏幕
################################################################################


## 对话屏幕 ########################################################################
##
## 对话屏幕用于向用户显示对话。它需要两个参数，who 和 what，分别是叙述角色的名字
## 和所叙述的文本。（如果没有名字，参数 who 可以是 None。）
##
## 此屏幕必须创建一个 id 为 what 的文本可视控件，因为 Ren'Py 使用它来管理文本显
## 示。它还可以创建 id 为 who 和 id 为 window 的可视控件来应用样式属性。
##
## https://doc.renpy.cn/zh-CN/screen_special.html#say

screen main_menu():
    ## 主菜单屏幕 - 按原始设计5543×3227缩放到1920×1080
    ## 缩放比例：x=0.34633, y=0.33471

    tag menu

    ## 开发者快捷键
    key "K_F1" action Function(show_persistent_status)
    key "K_F2" action Function(force_reset_episodes)

    ## 背景图（缩放到1920x1080）
    add "ui/main_menu_bg.png":
        size (1920, 1080)

    ## 标题logo（坐标：12, 262）
    add "ui/title_logo.png":
        xpos 4
        ypos 88
        zoom 0.346

    ## 角色图（坐标：1617, 186）
    add "ui/title_character.png":
        xpos 560
        ypos 62
        zoom 0.346

    ## 左下文本框（坐标：208, 1533）- 只在有提示文字时显示
    if button_hint_text:
        add "gui/text_frame.png":
            xpos 72
            ypos 513
            zoom 0.346

        ## 左下文本框内的提示文字
        text button_hint_text:
            xpos 120
            ypos 580
            xmaximum 750
            properties TEXT_STYLES["hint"]
            text_align 0.0
            line_spacing 8

    ## 右侧按钮区域（x坐标：3610 → 1250）
    fixed:
        ## Start按钮（y坐标：1138 → 381）
        imagebutton:
            idle "gui/button_bar.png"
            hover "gui/button_bar.png"
            action ToggleVariable("show_episodes")
            hovered [SetVariable("button_hint_text", "Choose an episode to begin your journey in the town of Bucha"), SetVariable("start_hovered", True)]
            unhovered [SetVariable("button_hint_text", ""), SetVariable("start_hovered", False)]
            xpos 1250
            ypos 381
            at main_button_hover

        text "Start":
            xpos 1584
            ypos 433
            properties TEXT_STYLES["main_button"]
            xanchor 0.5
            yanchor 0.5
            at start_text_zoom

        ## 初始状态：显示Config、Exit、Official Web
        if not show_episodes:
            ## Config按钮（y坐标：1533 → 513）
            imagebutton:
                idle "gui/button_bar.png"
                hover "gui/button_bar.png"
                action ShowMenu("preferences")
                hovered [SetVariable("button_hint_text", "Adjust game settings, display, audio, and preferences"), SetVariable("config_hovered", True)]
                unhovered [SetVariable("button_hint_text", ""), SetVariable("config_hovered", False)]
                xpos 1250
                ypos 513
                at [main_button_hover, main_slide_in_1, config_offset]

            text "Config":
                xpos 1584
                ypos 565
                properties TEXT_STYLES["main_button"]
                xanchor 0.5
                yanchor 0.5
                at [main_slide_in_1, config_text_zoom, config_offset]

            ## Official Web按钮（y坐标：1928 → 645）
            imagebutton:
                idle "gui/button_bar.png"
                hover "gui/button_bar.png"
                action OpenURL("https://your-official-website.com")
                hovered [SetVariable("button_hint_text", "Visit our official website for more information and updates"), SetVariable("official_hovered", True)]
                unhovered [SetVariable("button_hint_text", ""), SetVariable("official_hovered", False)]
                xpos 1250
                ypos 645
                at [main_button_hover, main_slide_in_2, official_offset]

            text "Official Web":
                xpos 1584
                ypos 697
                properties TEXT_STYLES["main_button"]
                xanchor 0.5
                yanchor 0.5
                at [main_slide_in_2, official_text_zoom, official_offset]

            ## Exit按钮（y坐标：2323 → 777）
            imagebutton:
                idle "gui/button_bar.png"
                hover "gui/button_bar.png"
                action Quit(confirm=True)
                hovered [SetVariable("button_hint_text", "Exit the game and return to desktop"), SetVariable("exit_hovered", True)]
                unhovered [SetVariable("button_hint_text", ""), SetVariable("exit_hovered", False)]
                xpos 1250
                ypos 777
                at [main_button_hover, main_slide_in_3, exit_offset]

            text "Exit":
                xpos 1584
                ypos 829
                properties TEXT_STYLES["main_button"]
                xanchor 0.5
                yanchor 0.5
                at [main_slide_in_3, exit_text_zoom, exit_offset]

        ## 展开状态：显示周目选择
        if show_episodes:
            ## Episode 1按钮（zoom=0.25，右对齐，间隔80px，无延迟）
            imagebutton:
                idle "gui/button_bar.png"
                hover "gui/button_bar.png"
                action [SetVariable("show_episodes", False), Start("episode_1")]
                hovered [SetVariable("button_hint_text", "Episode 1: The Beginning\nExperience the first chapter of mysteries in Bucha. Uncover hidden secrets and make crucial choices that will shape your journey."), SetVariable("episode1_hovered", True)]
                unhovered [SetVariable("button_hint_text", ""), SetVariable("episode1_hovered", False)]
                sensitive persistent.episode_1_unlocked
                xpos 1436
                ypos 513
                at [episode_button_hover, slide_in_1]

            # Episode 1 - 左侧状态文字
            text ("" if persistent.episode_1_unlocked else "(Locked)"):
                xpos 1450
                ypos 551
                properties TEXT_STYLES["episode_status"]
                yanchor 0.5
                at [slide_in_1, episode1_text_zoom]

            # Episode 1 - 右侧主文字
            text "Episode 1":
                xpos 1905
                ypos 551
                properties TEXT_STYLES["episode_button"]
                color ("#ffffff" if persistent.episode_1_unlocked else "#888888")
                xanchor 1.0
                yanchor 0.5
                at [slide_in_1, episode1_text_zoom]

            ## Episode 2按钮（zoom=0.25，右对齐，间隔80px，延迟0.3s）
            imagebutton:
                idle "gui/button_bar.png"
                hover "gui/button_bar.png"
                action [SetVariable("show_episodes", False), Start("episode_2")]
                hovered [SetVariable("button_hint_text", "Episode 2: Deeper Into Darkness\nContinue your investigation as the mystery deepens. New challenges await as you delve further into the town's secrets."), SetVariable("episode2_hovered", True)]
                unhovered [SetVariable("button_hint_text", ""), SetVariable("episode2_hovered", False)]
                sensitive persistent.episode_2_unlocked
                xpos 1436
                ypos 593
                at [episode_button_hover, slide_in_2, episode2_offset]

            # Episode 2 - 左侧状态文字
            text ("" if persistent.episode_2_unlocked else "(Locked)"):
                xpos 1450
                ypos 631
                properties TEXT_STYLES["episode_status"]
                yanchor 0.5
                at [slide_in_2, episode2_text_zoom, episode2_offset]

            # Episode 2 - 右侧主文字
            text "Episode 2":
                xpos 1905
                ypos 631
                properties TEXT_STYLES["episode_button"]
                color ("#ffffff" if persistent.episode_2_unlocked else "#888888")
                xanchor 1.0
                yanchor 0.5
                at [slide_in_2, episode2_text_zoom, episode2_offset]

            ## Episode 3按钮（zoom=0.25，右对齐，间隔80px，延迟0.6s）
            imagebutton:
                idle "gui/button_bar.png"
                hover "gui/button_bar.png"
                action [SetVariable("show_episodes", False), Start("episode_3")]
                hovered [SetVariable("button_hint_text", "Episode 3: The Final Truth\nFace the ultimate revelation in the concluding chapter. All mysteries converge as you discover the shocking truth behind Bucha."), SetVariable("episode3_hovered", True)]
                unhovered [SetVariable("button_hint_text", ""), SetVariable("episode3_hovered", False)]
                sensitive persistent.episode_3_unlocked
                xpos 1436
                ypos 673
                at [episode_button_hover, slide_in_3, episode3_offset]

            # Episode 3 - 左侧状态文字
            text ("" if persistent.episode_3_unlocked else "(Locked)"):
                xpos 1450
                ypos 711
                properties TEXT_STYLES["episode_status"]
                yanchor 0.5
                at [slide_in_3, episode3_text_zoom, episode3_offset]

            # Episode 3 - 右侧主文字
            text "Episode 3":
                xpos 1905
                ypos 711
                properties TEXT_STYLES["episode_button"]
                color ("#ffffff" if persistent.episode_3_unlocked else "#888888")
                xanchor 1.0
                yanchor 0.5
                at [slide_in_3, episode3_text_zoom, episode3_offset]

            ## Load Game按钮（zoom=0.25，右对齐，间隔80px，延迟0.9s）
            imagebutton:
                idle "gui/button_bar.png"
                hover "gui/button_bar.png"
                action ShowMenu("load")
                hovered [SetVariable("button_hint_text", "Continue your adventure from a previously saved game"), SetVariable("load_hovered", True)]
                unhovered [SetVariable("button_hint_text", ""), SetVariable("load_hovered", False)]
                xpos 1436
                ypos 753
                at [episode_button_hover, slide_in_4, load_offset]

            text "Load Game":
                xpos 1677
                ypos 791
                properties TEXT_STYLES["episode_button"]
                xanchor 0.5
                yanchor 0.5
                at [slide_in_4, load_text_zoom, load_offset]


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 420
    yfill True

    background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## 游戏菜单屏幕 ######################################################################
##
## 此屏幕列出了游戏菜单的基本共同结构。可使用屏幕标题调用，并显示背景、标题和导
## 航菜单。
##
## scroll 参数可以是 None，也可以是 viewport 或 vpgrid。此屏幕旨在与一个或多个子
## 屏幕同时使用，这些子屏幕将被嵌入（放置）在其中。
