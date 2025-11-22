################################################################################
## Screens 索引文件
################################################################################
##
## 此文件作为所有 UI screens 的索引，所有 screen 定义已拆分到 screens/ 子目录
##
## 拆分后的结构：
## - screens/main_menu.rpy      # 主菜单（包含配置、transforms、主菜单）
## - screens/dialogue.rpy       # 对话相关（say, input, choice, quick_menu）
## - screens/navigation.rpy     # 导航和快捷菜单
## - screens/game_menu.rpy      # 游戏菜单框架
## - screens/save_load.rpy      # 存档读档界面
## - screens/preferences.rpy    # 设置界面
## - screens/history.rpy        # 历史记录
## - screens/common.rpy         # 通用组件（help, confirm, notify等）
##
## Ren'Py 会自动加载 screens/ 目录下的所有 .rpy 文件
## 此索引文件仅用于文档说明，实际的 screens 已经通过子文件加载
##
## 添加新 screen 的步骤：
## 1. 确定新 screen 属于哪个类别
## 2. 在对应的 screens/xxx.rpy 文件中添加定义
## 3. 如果需要新类别，在 screens/ 中创建新文件
##
################################################################################

## 注意：
## screens/ 目录中的文件会按字母顺序加载
## main_menu.rpy 包含了通用配置和初始化，会首先被加载
