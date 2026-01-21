## 弹窗提示UI屏幕
## 显示事件通知的弹窗界面

## ============================================================================
## 弹窗图片资源
## ============================================================================

image popup_bg = "popup/popup_bg.png"

## ============================================================================
## 弹窗动画变换
## ============================================================================

## 弹窗进入动画（从上方滑入 + 淡入）
transform popup_enter:
    alpha 0.0
    yoffset -50
    easein 0.3 alpha 1.0 yoffset 0

## 弹窗退出动画（向上滑出 + 淡出）
transform popup_exit:
    alpha 1.0
    yoffset 0
    easeout 0.3 alpha 0.0 yoffset -30

## 弹窗闪烁效果（用于强调）
transform popup_pulse:
    alpha 1.0
    linear 0.5 alpha 0.8
    linear 0.5 alpha 1.0
    repeat

## ============================================================================
## 弹窗通知屏幕
## ============================================================================

screen popup_notification():
    ## 层级设置，确保显示在最上层
    zorder 200
    modal False  ## 不阻塞其他交互

    ## 点击任意位置关闭弹窗
    button:
        xfill True
        yfill True
        action Function(close_popup)
        background None

    ## 弹窗背景框（屏幕正上方居中）
    frame:
        at popup_enter
        anchor (0.5, 0.0)
        xpos 960
        ypos 80
        background "popup_bg"
        xsize 1148
        ysize 399
        xpadding 80
        ypadding 60

        ## 内容区域
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20

            ## 标题
            if popup_current:
                $ title_color = POPUP_COLORS.get(popup_current.get("type", "info"), "#ffffff")

                text popup_current.get("title", ""):
                    xalign 0.5
                    size 42
                    color title_color
                    font "fonts/lolita.ttf"
                    outlines [(2, "#000000", 0, 0)]

                ## 分隔线效果
                null height 10

                ## 内容
                text popup_current.get("content", ""):
                    xalign 0.5
                    size 36
                    color "#ffffff"
                    font "fonts/lolita.ttf"
                    outlines [(1, "#000000", 0, 0)]

    ## 点击提示（底部）
    text "点击任意位置关闭":
        xalign 0.5
        ypos 500
        size 18
        color "#888888"
        font "fonts/lolita.ttf"

## ============================================================================
## 简化版弹窗（用于快速提示）
## ============================================================================

screen popup_simple(message, popup_type="info"):
    ## 简化版弹窗，只显示一行文字
    zorder 200
    modal False

    timer 2.0 action Hide("popup_simple")

    frame:
        at popup_enter
        xalign 0.5
        yalign 0.1
        xpadding 40
        ypadding 20
        background Solid("#000000cc")

        $ msg_color = POPUP_COLORS.get(popup_type, "#ffffff")

        text message:
            size 28
            color msg_color
            font "fonts/lolita.ttf"

## ============================================================================
## 成就/解锁弹窗（带图标）
## ============================================================================

screen popup_unlock(title, content, icon_type="info"):
    ## 带图标的解锁弹窗
    zorder 200
    modal False

    button:
        xfill True
        yfill True
        action Hide("popup_unlock")
        background None

        frame:
            at popup_enter
            xalign 0.5
            yalign 0.15
            background "popup_bg"
            xsize 1148
            ysize 399
            xpadding 80
            ypadding 60

            hbox:
                xalign 0.5
                yalign 0.5
                spacing 40

                ## 图标区域（预留）
                ## add "popup/icon_{}.png".format(icon_type):
                ##     yalign 0.5

                ## 文字区域
                vbox:
                    yalign 0.5
                    spacing 15

                    $ title_color = POPUP_COLORS.get(icon_type, "#ffffff")

                    text title:
                        size 42
                        color title_color
                        font "fonts/lolita.ttf"
                        outlines [(2, "#000000", 0, 0)]

                    text content:
                        size 32
                        color "#ffffff"
                        font "fonts/lolita.ttf"
                        outlines [(1, "#000000", 0, 0)]

## ============================================================================
## 测试用标签
## ============================================================================

label test_popup:
    ## 测试弹窗系统
    "准备测试弹窗系统..."

    $ popup_clue("火灾现场照片")
    "测试线索弹窗"

    $ popup_location("安德莉娅住所")
    "测试地点弹窗"

    $ popup_character("罗琳达")
    "测试角色弹窗"

    $ popup_event("火灾发生")
    "测试事件弹窗"

    $ popup_trust("罗琳达", 10)
    "测试信任度弹窗"

    "弹窗测试完成！"
    return
