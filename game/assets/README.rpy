# 资产目录规划
#
# 目的：将角色立绘、场景背景、事件CG、UI素材与剧情脚本彻底分离，便于协同与替换。
#
# 推荐结构：
# assets/
# ├── characters/      # 角色立绘、表情分层
# ├── backgrounds/     # 场景背景图（bg_*）
# ├── cg/              # 事件CG、插画
# └── ui/              # UI相关素材（主菜单底图、按钮、sanity图标等）
#     └── sanity/      # 精神值显示相关图标
#
# 迁移建议：
# - 将 game/images/ 下的现有素材按类别迁移到上述子目录
# - 更新引用路径（如 gui.main_menu_background、UI屏幕 add 的图片路径、sanity 图标常量等）
# - 未来新增资源请直接放入对应的 assets 子目录，避免再次散落到 images/
#
# 注意：
# - 角色/地点/线索等数据依旧在 game/data/ 下维护
# - 剧情脚本现已归档至 game/story/episodes/

