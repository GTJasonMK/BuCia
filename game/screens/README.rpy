## Screens 目录结构说明
##
## 此目录包含游戏所有UI屏幕定义，已从原始的2094行单文件模块化拆分为8个文件
##
## 目录结构：
##
## screens/
## ├── main_menu.rpy        # 主菜单和周目选择（582行）
## ├── dialogue.rpy         # 对话、选择、输入屏幕（275行）
## ├── game_menu.rpy        # 游戏菜单框架（168行）
## ├── save_load.rpy        # 存档和读档界面（143行）
## ├── preferences.rpy      # 设置/偏好界面（159行）
## ├── history.rpy          # 对话历史记录（87行）
## ├── navigation.rpy       # 导航菜单（45行）
## └── common.rpy           # 通用UI组件（635行）
##
## 文件详细说明：
##
## main_menu.rpy - 主菜单和周目选择系统
##   包含内容：
##   - screen main_menu: 主菜单界面
##   - 按钮动画系统（文字缩放、偏移函数）
##   - TEXT_STYLES 配置（统一文字样式）
##   - BUTTON_GROUPS 配置（按钮组管理）
##   - 周目按钮展开/折叠逻辑
##   - 精神值图标显示
##   重要修复：周目按钮颜色逻辑（已从TEXT_STYLES中移除color属性）
##
## dialogue.rpy - 对话相关屏幕
##   包含内容：
##   - screen say: 对话显示屏幕
##   - screen input: 文本输入屏幕
##    --下属有对话与名字对齐（第36行的dialogue_x_offset）
##   - screen choice: 选项选择屏幕
##   - screen quick_menu: 快捷菜单（自动前进、快进、历史等）
##   - screen bubble: 气泡对话（可选）
##   - 角色名框配置
##
## game_menu.rpy - 游戏内菜单框架
##   包含内容：
##   - screen game_menu: 游戏菜单基础框架
##   - screen about: 关于界面
##   - 菜单背景和标题
##
## save_load.rpy - 存档系统界面
##   包含内容：
##   - screen save: 保存界面
##   - screen load: 加载界面
##   - screen file_slots: 存档槽位显示
##   - 存档缩略图和时间显示
##
## preferences.rpy - 游戏设置界面
##   包含内容：
##   - screen preferences: 设置/偏好界面
##   - 显示、音量、文字速度等设置
##   - 测试语音功能
##
## history.rpy - 对话历史
##   包含内容：
##   - screen history: 历史记录界面
##   - 对话回看功能
##
## navigation.rpy - 导航菜单
##   包含内容：
##   - screen navigation: 导航按钮组
##   - 历史、保存、读档、设置、主菜单等按钮
##
## common.rpy - 通用UI组件
##   包含内容：
##   - screen help: 帮助界面（键盘、鼠标、手柄）
##   - screen confirm: 确认对话框
##   - screen notify: 通知提示
##   - screen nvl: NVL模式对话
##   - screen skip_indicator: 快进指示器
##   - 各种通用transform和style定义
##
## 如何添加新屏幕：
##
## 1. 确定屏幕用途，选择合适的文件
##    - 主菜单相关 → main_menu.rpy
##    - 对话相关 → dialogue.rpy
##    - 设置相关 → preferences.rpy
##    - 通用组件 → common.rpy
##
## 2. 如果是全新类型，创建新文件（如 minigame.rpy）
##
## 3. 添加 screen 定义：
##    screen my_new_screen():
##        ## 屏幕功能说明
##        tag menu  # 如果是菜单类屏幕
##
##        frame:
##            # UI元素
##            pass
##
## 4. 添加样式定义（如需要）：
##    style my_screen_frame:
##        background "#000000aa"
##        padding (20, 20)
##
## 屏幕设计原则：
##
## - 单一职责：每个screen只负责一个界面功能
## - 样式分离：使用style定义样式，不在screen中硬编码
## - 复用优先：相似的UI组件应该抽取为独立screen
## - 响应式：考虑不同分辨率的显示效果
##
## 重要注意事项：
##
## 1. 周目按钮颜色问题：
##    - TEXT_STYLES["episode_button"] 中不应包含 color 属性
##    - 颜色应由各按钮根据 persistent.episode_X_unlocked 状态单独设置
##    - 示例：color ("#ffffff" if persistent.episode_1_unlocked else "#888888")
##
## 2. 文字样式使用：
##    - 使用 properties TEXT_STYLES["样式名"] 应用预定义样式
##    - 如需覆盖某个属性，在 properties 之后单独设置
##
## 3. Transform 和动画：
##    - 按钮悬停效果使用 transform 实现
##    - 文字缩放使用 text_zoom_function
##    - 位置偏移使用 offset_function
##
## 示例：添加成就界面
##
## 创建 screens/achievements.rpy：
##
## screen achievements():
##     """成就界面"""
##     tag menu
##
##     use game_menu("成就"):
##         viewport:
##             scrollbars "vertical"
##             mousewheel True
##
##             vbox:
##                 spacing 20
##
##                 for achievement in achievements_list:
##                     hbox:
##                         spacing 10
##
##                         if achievement.unlocked:
##                             add achievement.icon
##                             text achievement.name
##                         else:
##                             add "locked.png"
##                             text "未解锁"
##
## 最后更新：2026/2/7