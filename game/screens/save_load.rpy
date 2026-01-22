screen save():

    tag menu

    use file_slots(_("保存"))


screen load():

    tag menu

    use file_slots(_("读取"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("第 {} 页"))

    use game_menu("", show_navigation=False, show_return=False, show_label=False, show_header=True, header_title=title):
        ## 存档位网格（3x2）
        grid gui.file_slot_cols gui.file_slot_rows:
            xalign 0.5
            yalign 0.50
            spacing 45

            for i in range(gui.file_slot_cols * gui.file_slot_rows):

                $ slot = i + 1

                button:
                    xsize 520
                    ysize 280
                    action FileAction(slot)
                    key "save_delete" action FileDelete(slot)

                    background Frame(Solid("#6f6f6f"), 10, 10)
                    hover_background Frame(Solid("#7a7a7a"), 10, 10)

                    fixed:
                        xsize 520
                        ysize 280

                        add FileScreenshot(slot):
                            xalign 0.5
                            yalign 0.0
                            xsize 520
                            ysize 230

                        text FileTime(slot, format=_("{#file_time}%Y-%m-%d %H:%M"), empty=_("空存档位")):
                            xalign 0.5
                            yalign 1.0
                            yoffset -8
                            size 20
                            color "#4d4d4d"

        ## 翻页按钮
        hbox:
            xalign 0.5
            yalign 0.93
            spacing 18

            textbutton "<":
                style "save_page_button"
                action [FilePagePrevious(), With(dissolve)]

            for i in range(1, 10):
                $ _page_id = str(i)
                vbox:
                    spacing 0
                    xalign 0.5

                    textbutton str(i):
                        style "save_page_button"
                        text_style "save_page_button_text"
                        action [FilePage(_page_id), With(dissolve)]

                    if FilePageName() == _page_id:
                        frame:
                            xalign 0.5
                            yoffset -4
                            background Solid("#000000")
                            xsize 12
                            ysize 2

            textbutton ">":
                style "save_page_button"
                action [FilePageNext(), With(dissolve)]

        if config.has_sync and CurrentScreenName() != "save":
            textbutton _("下载同步"):
                xalign 0.5
                yalign 0.97
                style "save_sync_button"
                action DownloadSync()
        elif config.has_sync and CurrentScreenName() == "save":
            textbutton _("上传同步"):
                xalign 0.5
                yalign 0.97
                style "save_sync_button"
                action UploadSync()


style save_page_button is gui_button
style save_page_button_text is gui_button_text
style save_sync_button is gui_button
style save_sync_button_text is gui_button_text

style save_page_button:
    background None
    xpadding 6
    ypadding 2

style save_page_button_text:
    size 22
    color "#222222"
    hover_color "#000000"
    outlines [(1, "#ffffff", 0, 0)]
    textalign 0.5

style save_page_indicator_text is gui_text

style save_page_indicator_text:
    size 22
    color "#000000"
    xalign 0.5
    outlines [(1, "#ffffff", 0, 0)]

style save_sync_button:
    background None
    xpadding 10
    ypadding 4

style save_sync_button_text:
    size 22
    color "#222222"


## 设置屏幕 ########################################################################
##
## 设置屏幕允许用户配置游戏，使其更适合自己。
##
## https://doc.renpy.cn/zh-CN/screen_special.html#preferences
