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
## 现有系统说明：
##
## core/episode.rpy - 周目管理系统
##   - 管理当前周目（current_episode）
##   - 提供周目检查函数（is_episode, is_first_episode等）
##
## core/time.rpy - 时间系统
##   - 管理游戏内时间（current_day, current_time）
##   - 行动点系统（action_points）
##   - 时间推进函数（advance_time）
##
## 如何添加新系统：
## 1. 确定系统属于哪个类别（core/gameplay/character/progress/extras）
## 2. 在对应子目录中创建 .rpy 文件
## 3. 使用清晰的命名，如 investigation.rpy, achievement.rpy 等
## 4. 在文件顶部添加注释说明系统用途和主要功能
##
## 系统设计原则：
## - 单一职责：每个系统文件只负责一个核心功能
## - 接口清晰：提供明确的函数接口供其他模块调用
## - 数据分离：数据定义应放在 data/ 目录，系统只负责逻辑
## - 文档完善：关键函数必须添加注释说明参数和返回值
##
## 命名规范：
## - 使用小写字母和下划线
## - 文件名应简洁明确，反映系统功能
## - 每个系统一个文件，避免文件过大（建议<500行）
##
## 示例：添加调查系统
##
## 1. 创建 systems/gameplay/investigation.rpy
## 2. 定义调查相关的函数和变量：
##
## default investigation_mode = False
##
## init python:
##     def start_investigation(location_id):
##         """开始调查指定地点"""
##         global investigation_mode
##         investigation_mode = True
##         # 调查逻辑
##
##     def discover_evidence(evidence_id):
##         """发现证据"""
##         # 证据收集逻辑
##
## 最后更新：2025-11-23
