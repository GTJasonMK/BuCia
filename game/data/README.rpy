## Data 目录结构说明
##
## 此目录用于组织游戏的所有数据定义
##
## 目录结构：
##
## data/
## ├── characters/   # 角色相关数据
## │   └── database.rpy     # 角色定义和数据库
## ├── world/        # 世界设定数据
## │   └── locations.rpy    # 地点数据
## ├── items/        # 物品相关数据
## │   └── clues.rpy        # 线索数据
## └── config/       # 配置数据
##     └── (未来扩展：constants, settings, balancing等)
##
## 现有数据说明：
##
## characters/database.rpy - 角色系统数据
##   - 角色对象定义（define tsibela, rolinda等13个角色）
##   - 角色数据库（character_database字典）
##   - 角色关系和信任度系统
##
## world/locations.rpy - 地点系统数据
##   - 地点数据库（locations_database字典）
##   - 地点热点和调查点定义
##   - 地点解锁条件
##
## items/clues.rpy - 线索系统数据
##   - 线索数据库（clues_database字典）
##   - 线索类型：物证、档案、证词
##   - 线索关联和矛盾关系
##
## 如何添加新数据：
## 1. 确定数据类型属于哪个类别
## 2. 在对应子目录中创建或修改 .rpy 文件
## 3. 使用 Python 字典或 Ren'Py define 定义数据
## 4. 在文件顶部添加注释说明数据结构
##
## 数据组织原则：
## - characters/: 所有角色相关信息（属性、对话、关系等）
## - world/: 游戏世界设定（地点、事件、时间线等）
## - items/: 可收集或使用的物品（线索、道具、证据等）
## - config/: 游戏配置和常量（难度、数值平衡等）
##
## 数据定义规范：
## - 使用 init python: 块定义数据库字典
## - 使用 define 定义游戏常量和角色对象
## - 数据结构保持一致性，便于系统层调用
## - 添加充分的注释说明每个字段的含义
##
## 命名规范：
## - 使用小写字母和下划线
## - 文件名应清晰反映数据类型
## - 每种数据类型一个文件，保持模块化
##
## 示例：添加道具数据
##
## 1. 创建 data/items/props.rpy
## 2. 定义道具数据库：
##
## init python:
##     props_database = {
##         "钥匙": {
##             "id": "key_church",
##             "name": "教堂钥匙",
##             "type": "key",
##             "description": "打开教堂大门的钥匙",
##             "icon": "props/key.png",
##             "unlock_location": "church_main_hall"
##         },
##         "日记": {
##             "id": "diary_rolinda",
##             "name": "罗琳达的日记",
##             "type": "document",
##             "description": "记录了重要线索的日记本",
##             "icon": "props/diary.png",
##             "related_clues": ["clue_1", "clue_2"]
##         }
##     }
##
## 最后更新：2025-11-23
