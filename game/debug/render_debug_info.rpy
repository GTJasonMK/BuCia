## 渲染信息调试（用于定位：GUI 预览 vs 游戏内显示差异）
##
## 快捷键：
## - F10：显示/隐藏调试信息
##
## 关注点：
## - virtual(基准分辨率) 与 physical(窗口/屏幕实际像素) 是否一致
##   若不一致，Ren'Py 会对整帧进行缩放，可能放大半透明边缘问题。
## - config.mipmap 是否启用（缩放时可能影响半透明边缘的观感）

default render_debug_info_enabled = False

screen render_debug_info():
    ## 即使未显示信息，也保留按键入口
    key "K_F10" action ToggleVariable("render_debug_info_enabled")

    if render_debug_info_enabled:
        $ _vw = int(config.screen_width)
        $ _vh = int(config.screen_height)
        $ _pw, _ph = renpy.get_physical_size()
        $ _sx = (float(_pw) / float(_vw)) if _vw else 0.0
        $ _sy = (float(_ph) / float(_vh)) if _vh else 0.0
        python:
            try:
                _mipmap_str = str(config.mipmap)
            except Exception:
                _mipmap_str = "N/A (8.5+)"

        frame:
            xalign 0.0
            yalign 0.0
            xpadding 12
            ypadding 10
            background Solid("#00000088")

            vbox:
                spacing 4
                text "Render Debug (F10)" size 18 color "#ffffff"
                text "virtual: %dx%d" % (_vw, _vh) size 16 color "#ffffff"
                text "physical: %dx%d" % (int(_pw), int(_ph)) size 16 color "#ffffff"
                text "scale: %.3f x %.3f" % (_sx, _sy) size 16 color "#ffffff"
                text "mipmap: %s" % _mipmap_str size 16 color "#ffffff"

