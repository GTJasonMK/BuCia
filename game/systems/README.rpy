## Systems 目录结构说明
##
## 此目录用于组织游戏的各种系统逻辑
##
## 目录结构：
##
## systems/
## ├── core/         # 核心游戏系统
## │   ├── episode.rpy      # 周目管理系统
## │   └── time.rpy         # 时间系统
## ├── gameplay/     # 游戏玩法系统
## │   └── (未来扩展：investigation, deduction, evidence等)
## ├── character/    # 角色相关系统
## │   └── (未来扩展：relationship, trust, dialogue_tree等)
## ├── progress/     # 进度追踪系统
## │   └── (未来扩展：achievement, quest, statistics等)
## └── extras/       # 额外功能系统
##     └── (未来扩展：gallery, music_room, minigames等)
##
## 如何添加新系统：
## 1. 确定系统属于哪个类别（core/gameplay/character/progress/extras）
## 2. 在对应子目录中创建 .rpy 文件
## 3. 使用清晰的命名，如 investigation.rpy, achievement.rpy 等
## 4. 在文件顶部添加注释说明系统用途和主要功能
##
## 命名规范：
## - 使用小写字母和下划线
## - 文件名应简洁明确，反映系统功能
## - 每个系统一个文件，避免文件过大
