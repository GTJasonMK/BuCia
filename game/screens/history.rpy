screen history():

    tag menu

    ## 避免预缓存此屏幕，因为它可能非常大。
    predict False

    use game_menu(_("历史"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing, show_navigation=False):

        style_prefix "history"

        for h in _history_list:

            window:

                ## 此代码可确保如果 history_height 为 None 时仍可正常显示条目。
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## 从 Character 对象中获取叙述角色的文字颜色，如果设置了
                        ## 的话。
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("尚无对话历史记录。")


## 此代码决定了允许在历史记录屏幕上显示哪些标签。

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## 帮助屏幕 ########################################################################
##
## 提供有关键盘和鼠标映射信息的屏幕。它使用其它屏幕（keyboard_help、mouse_help
## 和 gamepad_help）来显示实际的帮助内容。
