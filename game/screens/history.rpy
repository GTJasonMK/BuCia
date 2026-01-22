screen history():

    tag menu

    ## 避免预缓存此屏幕，因为它可能非常大。
    predict False

    use game_menu("", show_navigation=False, show_return=False, show_label=False, show_header=True, header_title=_("历史")):

        ## 内容区域
        viewport:
            xalign 0.5
            yalign 0.55
            xsize 1250
            ysize 760
            mousewheel True
            draggable True

            vbox:
                spacing 18

                for h in _history_list:
                    frame:
                        xfill True
                        background Solid("#ffffff00")

                        vbox:
                            spacing 6

                            if h.who:
                                text h.who:
                                    style "history_name_text"
                                    substitute False
                                    if "color" in h.who_args:
                                        color h.who_args["color"]

                            $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                            text what:
                                style "history_body_text"
                                substitute False

                if not _history_list:
                    text _("尚无对话历史记录。"):
                        style "history_empty_text"


## 此代码决定了允许在历史记录屏幕上显示哪些标签。

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_name_text is gui_text
style history_body_text is gui_text
style history_empty_text is gui_text

style history_name_text:
    size 26
    color "#111111"

style history_body_text:
    size 22
    color "#1f1f1f"
    xmaximum 1200

style history_empty_text:
    xalign 0.5
    size 24
    color "#555555"



## 帮助屏幕 ########################################################################
##
## 提供有关键盘和鼠标映射信息的屏幕。它使用其它屏幕（keyboard_help、mouse_help
## 和 gamepad_help）来显示实际的帮助内容。
