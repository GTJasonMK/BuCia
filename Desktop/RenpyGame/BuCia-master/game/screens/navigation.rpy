screen navigation():

    ## 游戏内菜单（非主菜单）
    if not main_menu:
        vbox:
            style_prefix "navigation"

            xpos gui.navigation_xpos
            yalign 0.5

            spacing gui.navigation_spacing

            textbutton _("历史") action ShowMenu("history")
            textbutton _("保存") action ShowMenu("save")
            textbutton _("读取游戏") action ShowMenu("load")
            textbutton _("设置") action ShowMenu("preferences")

            if _in_replay:
                textbutton _("结束回放") action EndReplay(confirm=True)
            else:
                textbutton _("标题菜单") action MainMenu()

            textbutton _("关于") action ShowMenu("about")

            if renpy.variant("pc"):
                textbutton _("退出") action Quit(confirm=True)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")
    activate_sound "audio/sfx/空灵点击音效.ogg"        #点击的按钮时的音效
    # hover_sound "audio/boton.mp3"           #悬浮在按钮上时的音效

style navigation_button_text:
    properties gui.text_properties("navigation_button")


## 标题菜单屏幕 ######################################################################
##
## 用于在 Ren'Py 启动时显示标题菜单。
##
## https://doc.renpy.cn/zh-CN/screen_special.html#main-menu

