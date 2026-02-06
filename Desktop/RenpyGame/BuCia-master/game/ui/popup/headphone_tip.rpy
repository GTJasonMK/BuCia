## 开局耳机提示

screen headphone_tip():
    modal True
    zorder 200

    ## 中心提示面板
    frame:
        xalign 0.5
        yalign 0.30
        xsize 900
        ysize 480
        background Solid("#000000AA")

        add Transform("ui/向日葵耳麦.png", zoom=0.56):
            xalign 0.5
            yalign 0.85

    text "“听”十分重要，佩戴耳机以获得更佳听觉体验":
        xalign 0.5
        yalign 0.80
        size 40
        color "#ffffff"
        outlines [(2, "#000000", 0, 0)]

    ## 任意点击关闭
    button:
        xfill True
        yfill True
        background None
        action Return()

    key "dismiss" action Return()
    key "K_ESCAPE" action Return()
