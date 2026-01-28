# 周目剧情文件组织说明
#
# 此目录用于组织游戏的周目剧情内容，避免script.rpy文件过于庞大
#
# ## 目录结构
#
# episodes/
# ├── README.rpy                    # 本说明文件
# ├── episode1/                     # 第一周目（伪书·陷阱与迷雾）
# │   ├── story.rpy                # 主线剧情流程
# │   ├── locations.rpy            # 地点探索场景 (label visit_*)
# │   ├── investigations.rpy       # 热点调查场景 (label investigate_*)
# │   ├── dialogues.rpy            # 角色对话场景 (label talk_to_*)
# │   └── events.rpy               # 特殊事件和cutscene
# ├── episode2/                     # 第二周目（伪书·真相的碎片）
# ├── episode3/                     # 第三周目（伪书·破碎的现实）
# ├── episode4/                     # 第四周目（真相周目）
# └── shared/                       # 周目间共享的内容
#     └── common_scenes.rpy        # 可复用的场景片段
#
# ## 命名规范
#
# ### Label命名
# - 主线剧情: label episode1_start, label episode1_day1_morning
# - 地点探索: label visit_rolinda_house_ep1
# - 热点调查: label investigate_rolinda_house_desk_ep1
# - 角色对话: label talk_to_rolinda_ep1_scene1
# - 特殊事件: label event_fire_ep1, label event_trial_ep1
#
# ### 文件拆分原则
# - story.rpy: 周目的主要流程和关键剧情节点
# - locations.rpy: 所有 visit_* labels，每个地点一个label
# - investigations.rpy: 所有 investigate_* labels，每个热点一个label
# - dialogues.rpy: 所有 talk_to_* labels，按角色和场景组织
# - events.rpy: 自动触发的事件，cutscene，审判场景等
#
# ## 开发建议
#
# 1. 先在story.rpy中编写主线流程框架
# 2. 使用jump或call连接到其他文件中的具体场景
# 3. 周目间相似的场景可以放在shared/中复用
# 4. 使用条件判断实现周目差异：
#    if persistent.episode_1_unlocked:
#        # 第一周目特有内容
#    elif persistent.episode_2_unlocked:
#        # 第二周目特有内容
#
# ## 示例
#
# ### story.rpy
# ```python
# label episode1_start:
#     "第一周目开始..."
#     call visit_rolinda_house_ep1
#     jump episode1_day2
# ```
#
# ### locations.rpy
# ```python
# label visit_rolinda_house_ep1:
#     scene bg rolinda_house with dissolve
#     "你来到了罗琳达的宅邸。"
#     # 热点调查选项
#     menu:
#         "调查书桌":
#             call investigate_rolinda_house_desk_ep1
#         "离开":
#             return
# ```
#
# ### dialogues.rpy
# ```python
# label talk_to_rolinda_ep1_scene1:
#     show rolinda neutral
#     rolinda "欢迎来到布恰小镇。"
#     # 对话选项和信任度变化
#     menu:
#         "表示感谢":
#             $ modify_character_trust("罗琳达", 5)
#         "保持警惕":
#             $ modify_character_trust("罗琳达", -5)
#     return
# ```
