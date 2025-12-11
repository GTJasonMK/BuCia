## 摄像机对话框缩放比例
define CAMERA_DIALOGUE_SCALE = 0.7036
define CAMERA_TEXTBOX_HEIGHT = 339

screen say(who, what):

    ## 根据 camera_ui 状态选择对话框样式
    $ _use_camera_style = getattr(store, 'camera_ui_enabled', True)

    if _use_camera_style:
        ## 摄像机风格对话框 - 直接定义所有属性
        window:
            id "window"
            xalign 0.5
            xfill True
            yalign 1.0
            ysize CAMERA_TEXTBOX_HEIGHT
            background Transform("camera_ui/对话框.png", zoom=CAMERA_DIALOGUE_SCALE)

            if who is not None:
                window:
                    id "namebox"
                    style "namebox"
                    text who id "who":
                        font "fonts/lolita.ttf"

            text what id "what":
                style "say_dialogue"
                font "fonts/lolita.ttf"
                ypos 85

    else:
        ## 默认对话框样式
        window:
            id "window"

            if who is not None:

                window:
                    id "namebox"
                    style "namebox"
                    text who id "who"

            text what id "what"


    ## 如果有对话框头像，会将其显示在文本之上。请不要在手机界面下显示这个，因为
    ## 没有空间。
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## 通过 Character 对象使名称框可用于样式化。
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False


## 输入屏幕 ########################################################################
##
## 此屏幕用于显示 renpy.input。prompt 参数用于传递文本提示。
##
## 此屏幕必须创建一个 id 为 input 的输入可视控件来接受各种输入参数。
##
## https://doc.renpy.cn/zh-CN/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## 选择屏幕 ########################################################################
##
## 此屏幕用于显示由 menu 语句生成的游戏内选项。参数 items 是一个对象列表，每个对
## 象都有字幕和动作字段。
##
## https://doc.renpy.cn/zh-CN/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## 快捷菜单屏幕 ######################################################################
##
## 快捷菜单显示于游戏内，以便于访问游戏外的菜单。

screen quick_menu():

    ## 确保该菜单出现在其他屏幕之上，
    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"
            style "quick_menu"

            textbutton _("回退") action Rollback()
            textbutton _("历史") action ShowMenu('history')
            textbutton _("快进") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("自动") action Preference("auto-forward", "toggle")
            textbutton _("保存") action ShowMenu('save')
            textbutton _("快存") action QuickSave()
            textbutton _("快读") action QuickLoad()
            textbutton _("设置") action ShowMenu('preferences')


## 此代码确保只要用户没有主动隐藏界面，就会在游戏中显示相关屏幕。
## default_background: 默认背景（最底层，zorder -100）
## camera_ui: 摄像机风格UI覆盖层（最高优先级，zorder 200）
## quick_menu: 快捷菜单
## sanity_display: 精神值显示
init python:
    config.overlay_screens.append("default_background")
    config.overlay_screens.append("camera_ui")
    config.overlay_screens.append("quick_menu")
    config.overlay_screens.append("sanity_display")

default quick_menu = True

style quick_menu is hbox
style quick_button is default
style quick_button_text is button_text

style quick_menu:
    xalign 0.5
    yalign 1.0

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")


################################################################################
## 标题和游戏菜单屏幕
################################################################################

## 导航屏幕 ########################################################################
##
## 该屏幕包含在标题菜单和游戏菜单中，并提供导航到其他菜单，以及启动游戏。

## 获取精神值图标
## 注意：精神值显示现在使用动态填充效果（见 ui/time.rpy 的 sanity_display）
## 此函数保留用于向后兼容或其他用途
init python:
    def get_sanity_icon():
        return "sanity/san_eye.png"

    ## ========== 按钮动画系统核心函数 ==========

    def text_zoom_function(trans, st, at, var_name):
        """
        文字缩放函数 - 根据按钮悬停状态动态缩放文字

        参数：
            trans: Transform 对象
            st: 显示时间（秒）
            at: 动画时间（秒）
            var_name: 悬停状态变量名（如 "start_hovered"）

        返回：
            float: 下次更新的延迟时间（秒）

        工作原理：
            1. 检查对应的悬停状态变量
            2. 悬停时目标缩放为 1.1，否则为 1.0
            3. 使用线性插值平滑过渡到目标值（插值系数 0.3）
            4. 每 0.02 秒更新一次，实现平滑动画效果
        """
        # 获取全局变量的值
        is_hovered = getattr(store, var_name, False)
        target_zoom = 1.1 if is_hovered else 1.0

        # 平滑过渡到目标缩放值
        current_zoom = trans.zoom if hasattr(trans, 'zoom') else 1.0
        new_zoom = current_zoom + (target_zoom - current_zoom) * 0.3

        trans.zoom = new_zoom
        return 0.02  # 每0.02秒更新一次

    def offset_function(trans, st, at, var_names, offset_per_button):
        """
        按钮偏移函数 - 根据上方按钮的悬停状态计算累积偏移

        参数：
            trans: Transform 对象
            st: 显示时间（秒）
            at: 动画时间（秒）
            var_names: 依赖的悬停状态变量名列表（如 ["start_hovered", "config_hovered"]）
            offset_per_button: 每个悬停按钮导致的偏移量（像素）

        返回：
            float: 下次更新的延迟时间（秒）

        工作原理：
            1. 遍历所有依赖的按钮悬停状态
            2. 累加所有悬停按钮的偏移量
            3. 使用线性插值平滑过渡到目标偏移值（插值系数 0.3）
            4. 每 0.02 秒更新一次，实现平滑退避效果

        示例：
            如果 config 按钮依赖 ["start_hovered"]，offset_per_button=10
            - start 未悬停：config 偏移 0px
            - start 悬停：config 偏移 10px（向下）
        """
        # 计算总偏移量
        total_offset = 0
        for var_name in var_names:
            if getattr(store, var_name, False):
                total_offset += offset_per_button

        # 平滑过渡到目标偏移值
        current_offset = trans.yoffset if hasattr(trans, 'yoffset') else 0
        new_offset = current_offset + (total_offset - current_offset) * 0.3

        trans.yoffset = new_offset
        return 0.02  # 每0.02秒更新一次


