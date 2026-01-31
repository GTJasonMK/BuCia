## 渲染差异排查：GUI（Pillow 预览） vs Ren'Py（游戏内显示）
##
## 用途：
## - 当你怀疑“同一张 PNG 在 GUI 里干净，但在游戏里有缝合边缘/光晕”时，
##   用本文件的调试 label 直接在 Ren'Py 里对比渲染结果，隔离“资源问题”还是“渲染阶段问题”。
##
## 使用方式：
## - 在开发者控制台（Shift+O）输入：jump debug_render_baked_telina
## - 或者临时在任意脚本里 `jump debug_render_baked_telina`
##
## 说明：
## - 左侧：直接 show expression 文件路径（绕过 image tag 定义）
## - 右侧：正常 show 角色 tag（走项目的自动立绘/动画系统）

init -2:
    transform _debug_left:
        xalign 0.25
        yalign 1.0
        xanchor 0.5
        yanchor 1.0
        subpixel False

    transform _debug_right:
        xalign 0.75
        yalign 1.0
        xanchor 0.5
        yanchor 1.0
        subpixel False


label debug_render_baked_telina:
    scene Solid("#4a4a4a")

    ## 直接加载 baked 资源文件（不经过 image telina 的 DynamicDisplayable）
    show expression "characters_baked/telina/idle.png" as _dbg_direct at _debug_left

    ## 通过项目正常 image tag（如果这里和左侧不同，就说明“游戏端仍在二次采样/变换/走了别的资源”）
    show telina neutral as _dbg_tag at _debug_right

    "左边是直接加载文件，右边是走角色 tag。若右边有额外边缘/亮度差异，请优先检查是否仍存在运行时缩放/滤镜/缓存未更新。"
    return

