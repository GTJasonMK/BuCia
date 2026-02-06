screen game_menu(title, scroll=None, yinitial=0.0, spacing=0, show_navigation=True, show_return=True, show_label=True, show_header=False, header_title=None, background_override=None):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        if background_override:
            add background_override
        else:
            add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        if show_navigation:
            hbox:

                ## 导航部分的预留空间。
                frame:
                    style "game_menu_navigation_frame"

                frame:
                    style "game_menu_content_frame"

                    if scroll == "viewport":

                        viewport:
                            yinitial yinitial
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            pagekeys True

                            side_yfill True

                            vbox:
                                spacing spacing

                                transclude

                    elif scroll == "vpgrid":

                        vpgrid:
                            cols 1
                            yinitial yinitial

                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            pagekeys True

                            side_yfill True

                            spacing spacing

                            transclude

                    else:

                        transclude
        else:
            frame:
                style "game_menu_content_frame_full"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    if show_navigation:
        use navigation

    if show_return:
        if show_navigation:
            textbutton _("返回"):
                style "return_button"
                action Return()
        else:
            textbutton _("返回"):
                style "return_button_full"
                action Return()

    if show_label and title:
        label title

    if show_header:
        $ _header_title = header_title if header_title is not None else title
        if _header_title:
            text _header_title:
                style "menu_header_title"
        imagebutton:
            style "menu_header_close"
            idle im.FactorScale("images/notebook/关闭UI（未选中）.png", 1.2)
            hover im.FactorScale("images/notebook/关闭UI（未选中）.png", 1.2)
            action Return()

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text
style return_button_full is navigation_button
style return_button_full_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 60
    top_padding 120

    background None

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_content_frame_full:
    xfill True
    left_margin 60
    right_margin 60
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xalign 0.5
    ysize 140

style game_menu_label_text:
    size 60
    color gui.accent_color
    yalign 0.5
    xalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45

style return_button_full:
    xalign 1.0
    yalign 0.0
    xoffset -40
    yoffset 20

style menu_header_title is gui_text
style menu_header_close is gui_button
style menu_header_close_text is gui_button_text

style menu_header_title:
    xalign 0.03
    yalign 0.03
    xoffset -15  # 向左平移约11像素（从-4改为-15）
    yoffset -8
    size 46
    color "#111111"

style menu_header_close:
    xalign 0.98
    yalign 0.03
    xoffset 8
    yoffset -6
    background None
    xpadding 6
    ypadding 2

style menu_header_close_text:
    size 28
    color "#111111"

style menu_center_panel is frame

style menu_center_panel:
    xsize 1420
    ysize 760
    xpadding 60
    ypadding 40
    background Solid("#d6d6d6")


## 关于屏幕 ########################################################################
##
## 此屏幕提供有关游戏和 Ren'Py 的制作人员和版权信息。
##
## 此屏幕没有什么特别之处，因此它也可以作为一个例子来说明如何制作一个自定义屏
## 幕。

screen about():

    tag menu

    ## 此 use 语句将 game_menu 屏幕包含到了这个屏幕内。子级 vbox 将包含在
    ## game_menu 屏幕的 viewport 内。
    use game_menu(_("关于"), scroll="viewport", show_navigation=False, show_return=False, show_label=False, show_header=True):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("版本 [config.version!t]\n")

            ## gui.about 通常在 options.rpy 中设置。
            if gui.about:
                text "[gui.about!t]\n"

            text _("引擎：{a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only]\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## 读取和保存屏幕 #####################################################################
##
## 这些屏幕负责让用户保存游戏并能够再次读取。由于它们几乎完全一样，因此这两个屏
## 幕都是以第三个屏幕 file_slots 来实现的。
##
## https://doc.renpy.cn/zh-CN/screen_special.html#save https://doc.renpy.cn/zh-
## CN/screen_special.html#load
