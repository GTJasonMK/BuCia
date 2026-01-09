## 摄像机UI系统
## 提供摄像机风格的游戏界面覆盖层
## 设计原则：配置驱动、高扩展性、元素可独立控制

## ============================================================================
## 设计参数
## ============================================================================

## 原始设计尺寸（UI素材的设计基准）
define CAMERA_UI_DESIGN_WIDTH = 2729
define CAMERA_UI_DESIGN_HEIGHT = 1535

## 游戏目标尺寸
define CAMERA_UI_GAME_WIDTH = 1920
define CAMERA_UI_GAME_HEIGHT = 1080

## 自动计算缩放比例
define CAMERA_UI_SCALE = 1920.0 / 2729.0  # ≈ 0.7036

## ============================================================================
## UI元素配置
## ============================================================================
##
## 每个元素包含：
##   - image: 图片路径
##   - pos: 原始设计坐标 (x, y)
##   - zorder: 层级（数值越大越靠前）
##   - visible_key: 控制显示的变量键名
##   - description: 元素描述（用于调试）
##
## 添加新元素只需在此字典中添加配置即可
## ============================================================================

init python:
    CAMERA_UI_ELEMENTS = {
        ## === 底层元素 ===
        "day": {
            "image": "camera_ui/天数.png",
            "pos": (1201, 46),
            "zorder": 0,
            "description": "天数显示"
        },
        "time": {
            "image": "camera_ui/小时：分钟.png",
            "pos": (1372, 46),
            "zorder": 1,
            "description": "时间显示"
        },
        ## "dialogue_box" 已移至对话系统联动
        ## 对话框只在有对话时显示，与 Ren'Py 的 say screen 集成
        ## 详见 screens/dialogue.rpy 中的实现
        "rec": {
            "image": "camera_ui/红点REC.png",
            "pos": (2292, 69),
            "zorder": 3,
            "description": "录制指示灯"
        },
        ## "sanity_eye" 已由独立的 sanity_display 系统处理
        ## 如需使用此UI中的眼睛图片，取消下方注释
        # "sanity_eye": {
        #     "image": "camera_ui/SAN值-眼睛.png",
        #     "pos": (79, 69),
        #     "zorder": 4,
        #     "description": "精神值眼睛"
        # },

        ## === 中层元素（左下角控制区） ===
        "auto": {
            "image": "camera_ui/AUTO.png",
            "pos": (316, 1410),
            "zorder": 5,
            "description": "AUTO标签"
        },
        "slash": {
            "image": "camera_ui/_.png",
            "pos": (404, 1456),
            "zorder": 6,
            "description": "斜杠分隔符"
        },
        "on": {
            "image": "camera_ui/ON.png",
            "pos": (444, 1456),
            "zorder": 7,
            "description": "ON标签"
        },
        "off": {
            "image": "camera_ui/OFF.png",
            "pos": (293, 1456),
            "zorder": 8,
            "description": "OFF标签"
        },
        "battery": {
            "image": "camera_ui/电池UI.png",
            "pos": (53, 1413),
            "zorder": 9,
            "description": "电池图标"
        },

        ## === 上层元素（装饰） ===
        "sunflower": {
            "image": "camera_ui/向日葵.png",
            "pos": (2395, 1123),
            "zorder": 10,
            "description": "向日葵装饰"
        },
        "town_name": {
            "image": "camera_ui/右下 不查小镇.png",
            "pos": (2187, 1358),
            "zorder": 11,
            "description": "右下角镇名"
        },

        ## === 最顶层（边框） ===
        "frame": {
            "image": "camera_ui/边框.png",
            "pos": (13, 16),
            "zorder": 12,
            "description": "摄像机边框"
        }
    }

    ## 坐标转换函数：将设计坐标转换为游戏坐标
    def camera_ui_scale_pos(x, y):
        """
        将原始设计坐标转换为游戏实际坐标

        Args:
            x: 原始X坐标
            y: 原始Y坐标

        Returns:
            tuple: (scaled_x, scaled_y)
        """
        return (int(x * CAMERA_UI_SCALE), int(y * CAMERA_UI_SCALE))

    ## 获取元素配置
    def get_camera_ui_element(name):
        """获取指定UI元素的配置"""
        return CAMERA_UI_ELEMENTS.get(name, None)

    ## 获取所有元素名称
    def get_camera_ui_element_names():
        """获取所有UI元素的名称列表"""
        return list(CAMERA_UI_ELEMENTS.keys())

    ## 设置单个元素可见性
    def set_camera_ui_visible(name, visible=True):
        """
        设置单个UI元素的可见性

        Args:
            name: 元素名称
            visible: 是否可见
        """
        if name in CAMERA_UI_ELEMENTS:
            store.camera_ui_visibility[name] = visible

    ## 设置多个元素可见性
    def set_camera_ui_group_visible(names, visible=True):
        """
        批量设置UI元素的可见性

        Args:
            names: 元素名称列表
            visible: 是否可见
        """
        for name in names:
            set_camera_ui_visible(name, visible)

    ## 显示所有元素
    def show_all_camera_ui():
        """显示所有UI元素"""
        for name in CAMERA_UI_ELEMENTS:
            store.camera_ui_visibility[name] = True

    ## 隐藏所有元素
    def hide_all_camera_ui():
        """隐藏所有UI元素"""
        for name in CAMERA_UI_ELEMENTS:
            store.camera_ui_visibility[name] = False

    ## 重置为默认可见性
    def reset_camera_ui_visibility():
        """重置所有元素为默认可见状态"""
        store.camera_ui_visibility = {name: True for name in CAMERA_UI_ELEMENTS}

## ============================================================================
## 可见性控制变量
## ============================================================================

## 每个元素的可见性状态（默认全部显示）
## 注意：dialogue_box 已移至对话系统，不在此处控制
default camera_ui_visibility = {
    "day": True,
    "time": True,
    "rec": True,
    "auto": True,
    "slash": True,
    "on": True,
    "off": True,
    "battery": True,
    "sunflower": True,
    "town_name": True,
    "frame": True
}

## 整体UI开关
default camera_ui_enabled = True

## 默认背景图片
define DEFAULT_BACKGROUND = "bg/default_bg.jpg"

## ============================================================================
## 默认背景屏幕
## ============================================================================
## 在没有其他背景时显示的默认场景背景
## 使用负 zorder 确保显示在所有其他内容之下

screen default_background():
    ## 最底层，在所有其他 screen 之下
    zorder -100

    ## 仅在游戏进行中显示（不在主菜单显示）
    if not main_menu:
        add DEFAULT_BACKGROUND

## ============================================================================
## 摄像机UI屏幕
## ============================================================================

screen camera_ui():
    ## 摄像机风格UI覆盖层
    ## 仅在游戏进行中且启用时显示（不在主菜单显示）
    ## 使用高zorder确保显示在其他UI之上（sanity_display使用100）
    zorder 200

    ## 快捷键：A 键切换自动播放
    key "a" action Preference("auto-forward", "toggle")

    ## 快捷键：N 键打开/关闭笔记本
    key "n" action ToggleScreen("notebook")

    ## 快捷键：M 键打开/关闭地图
    key "m" action ToggleScreen("visual_map")

    ## 主菜单时不显示
    if not main_menu and camera_ui_enabled:
        ## 自动播放控制区需要特殊处理的元素
        $ _auto_control_elements = ["auto", "slash", "on", "off"]

        ## 渲染普通元素（排除自动播放控制区）
        for name in sorted(CAMERA_UI_ELEMENTS.keys(), key=lambda n: CAMERA_UI_ELEMENTS[n]["zorder"]):
            if name not in _auto_control_elements and camera_ui_visibility.get(name, True):
                $ elem = CAMERA_UI_ELEMENTS[name]
                $ scaled_x, scaled_y = camera_ui_scale_pos(elem["pos"][0], elem["pos"][1])

                add Transform(elem["image"], zoom=CAMERA_UI_SCALE):
                    pos (scaled_x, scaled_y)

        ## ========== 自动播放控制区 ==========
        ## AUTO 标签（静态显示）
        if camera_ui_visibility.get("auto", True):
            $ auto_elem = CAMERA_UI_ELEMENTS["auto"]
            $ auto_x, auto_y = camera_ui_scale_pos(auto_elem["pos"][0], auto_elem["pos"][1])
            add Transform(auto_elem["image"], zoom=CAMERA_UI_SCALE):
                pos (auto_x, auto_y)

        ## 斜杠分隔符（静态显示）
        if camera_ui_visibility.get("slash", True):
            $ slash_elem = CAMERA_UI_ELEMENTS["slash"]
            $ slash_x, slash_y = camera_ui_scale_pos(slash_elem["pos"][0], slash_elem["pos"][1])
            add Transform(slash_elem["image"], zoom=CAMERA_UI_SCALE):
                pos (slash_x, slash_y)

        ## OFF 按钮（点击关闭自动播放）
        if camera_ui_visibility.get("off", True):
            $ off_elem = CAMERA_UI_ELEMENTS["off"]
            $ off_x, off_y = camera_ui_scale_pos(off_elem["pos"][0], off_elem["pos"][1])
            ## 当自动播放关闭时高亮显示
            if not preferences.afm_enable:
                imagebutton:
                    idle Transform(off_elem["image"], zoom=CAMERA_UI_SCALE)
                    hover Transform(off_elem["image"], zoom=CAMERA_UI_SCALE * 1.1)
                    action Preference("auto-forward", "disable")
                    pos (off_x, off_y)
            else:
                ## 自动播放开启时，OFF 变暗
                imagebutton:
                    idle Transform(off_elem["image"], zoom=CAMERA_UI_SCALE, alpha=0.4)
                    hover Transform(off_elem["image"], zoom=CAMERA_UI_SCALE)
                    action Preference("auto-forward", "disable")
                    pos (off_x, off_y)

        ## ON 按钮（点击开启自动播放）
        if camera_ui_visibility.get("on", True):
            $ on_elem = CAMERA_UI_ELEMENTS["on"]
            $ on_x, on_y = camera_ui_scale_pos(on_elem["pos"][0], on_elem["pos"][1])
            ## 当自动播放开启时高亮显示
            if preferences.afm_enable:
                imagebutton:
                    idle Transform(on_elem["image"], zoom=CAMERA_UI_SCALE)
                    hover Transform(on_elem["image"], zoom=CAMERA_UI_SCALE * 1.1)
                    action Preference("auto-forward", "enable")
                    pos (on_x, on_y)
            else:
                ## 自动播放关闭时，ON 变暗
                imagebutton:
                    idle Transform(on_elem["image"], zoom=CAMERA_UI_SCALE, alpha=0.4)
                    hover Transform(on_elem["image"], zoom=CAMERA_UI_SCALE)
                    action Preference("auto-forward", "enable")
                    pos (on_x, on_y)

## ============================================================================
## 预定义的UI组合（便捷函数）
## ============================================================================

init python:
    ## 定义常用的元素组
    CAMERA_UI_GROUPS = {
        ## 信息显示组（顶部）
        "info": ["day", "time", "rec"],

        ## 控制区组（左下角）
        "controls": ["auto", "slash", "on", "off", "battery"],

        ## 装饰组（右侧）
        "decoration": ["sunflower", "town_name"],

        ## 框架组（仅边框，对话框已移至对话系统）
        "frame_group": ["frame"],

        ## 全部元素
        "all": list(CAMERA_UI_ELEMENTS.keys())
    }

    def show_camera_ui_group(group_name):
        """
        显示预定义的元素组

        Args:
            group_name: 组名（info/controls/decoration/frame_group/all）
        """
        if group_name in CAMERA_UI_GROUPS:
            set_camera_ui_group_visible(CAMERA_UI_GROUPS[group_name], True)

    def hide_camera_ui_group(group_name):
        """
        隐藏预定义的元素组

        Args:
            group_name: 组名（info/controls/decoration/frame_group/all）
        """
        if group_name in CAMERA_UI_GROUPS:
            set_camera_ui_group_visible(CAMERA_UI_GROUPS[group_name], False)

## ============================================================================
## 使用示例（注释）
## ============================================================================
##
## 基本使用：
##   show screen camera_ui           # 显示摄像机UI
##   hide screen camera_ui           # 隐藏摄像机UI
##
## 控制整体开关：
##   $ camera_ui_enabled = False     # 禁用整个UI
##   $ camera_ui_enabled = True      # 启用整个UI
##
## 控制单个元素：
##   $ set_camera_ui_visible("rec", False)      # 隐藏录制指示灯
##   $ set_camera_ui_visible("frame", True)     # 显示边框
##
## 控制元素组：
##   $ hide_camera_ui_group("controls")         # 隐藏左下角控制区
##   $ show_camera_ui_group("info")             # 显示顶部信息区
##
## 批量控制：
##   $ set_camera_ui_group_visible(["rec", "battery"], False)  # 隐藏多个
##   $ hide_all_camera_ui()                     # 隐藏全部
##   $ show_all_camera_ui()                     # 显示全部
##   $ reset_camera_ui_visibility()             # 重置为默认
##
## ============================================================================
