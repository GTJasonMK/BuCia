# 不查小镇 (BuCia)

基于 Ren'Py 8.5+ 的悬疑推理视觉小说项目。本仓库以 **剧情脚本 + 数据配置 + 系统逻辑 + UI** 分层组织，面向持续迭代与多周目扩展。

---

## 快速开始

1) 安装 Ren'Py SDK（推荐 8.5.0+）  
2) 打开 Ren'Py Launcher → Preferences → Project Directory 指向本仓库**父目录**  
3) Launcher 中选择 **BuCia** → Launch Project  
4) 运行前建议执行 **Lint** 检查

> 本项目无 CLI 构建脚本，调试日志在根目录 `log.txt` / `errors.txt` / `traceback.txt`。

---

## 项目结构（核心）

```
game/
├── episodes/              # 剧情与周目流程（episodeX）
├── data/                  # 数据层（角色/地点/线索/笔记本）
├── systems/               # 系统逻辑（周目/时间/弹窗/角色认知）
├── ui/                    # 业务UI（地图/笔记本/线索簿等）
├── screens/               # Ren'Py 屏幕定义（菜单/存档/设置/历史）
├── images/                # 游戏使用资源（ui/notebook/bg/clue等）
├── audio/                 # 音频资源（music/sfx/voice）
└── fonts/                 # 字体资源
asset/                     # 源素材与历史归档（不直接加载）
UI不要删QWQ/               # 旧UI归档
```

---

## 关键系统概览

- **角色数据库**：`game/data/characters/database.rpy`  
  定义角色信息、信任度、遇见记录与笔记本联动。
- **角色认知状态机**：`game/systems/character/impressions.rpy`  
  支持状态（未知/初识/中立/信任/同盟/怀疑/敌对），剧情通过 `apply_impression_event()` 触发变化，笔记本自动显示“印象”。
- **周目系统**：`game/systems/core/episode.rpy`  
  `start_episode()` 会重置时间、地点与角色认知。
- **笔记本**：`game/ui/notebook/notebook_screen.rpy`  
  人物/证物/记录/地图四页，人物页展示“印象 + 角色信息”。
- **线索系统**：`game/data/items/clues.rpy` + `game/ui/clues.rpy`  
  线索发现与弹窗提示、详情展示。
- **自动立绘**：`game/characters_images.rpy`  
  角色对白自动显示对应立绘（可按角色或句子级开关）。

---

## 资源管理规范

### 图像
- 背景：`game/images/bg/`
- 角色立绘：`game/images/characters/角色名/`
- 线索图标：`game/images/clue/`
- UI/笔记本：`game/images/ui/`、`game/images/notebook/`

### 音频
- BGM：`game/audio/music/`
- SFX：`game/audio/sfx/`
- Voice：`game/audio/voice/角色名/`

### 字体
`game/fonts/`，在 `game/gui.rpy` 中配置后使用。

---

## 开发与验证

- **运行**：Ren'Py Launcher → Launch Project  
- **检查**：Ren'Py Launcher → Lint  
- **本地清理**：`clean_all_data.bat`（会清除缓存/存档）

---

## 功能扩展与常用接口

### 1) 新增角色
- 在 `game/data/characters/database.rpy` 中添加角色数据
- 角色立绘放入 `game/images/characters/角色名/`
- 对话中用 `show 角色ID 表情` 使用

### 2) 认知状态机（印象）
- 事件定义：`impression_event_map`（`game/systems/character/impressions.rpy`）
- 触发变化：`$ apply_impression_event("事件ID")`
- 直接设置：`$ set_impression("罗琳达", "suspect")`

### 3) 角色遇见与笔记本联动
- 首次见面：`$ set_character_met("罗琳达")`
- 笔记本人物页自动显示“印象 + 基本资料”

---

## 开发守则与协作指南

### 剧情与对话编写
- 主线流程：`game/episodes/episodeX/story.rpy`
- 角色对话：`game/episodes/episodeX/dialogues.rpy`（label 以 `talk_to_角色_sceneX` 命名）
- 场景转换示例：
  ```renpy
  scene bg town_square with dissolve
  show rolinda neutral at center with dissolve
  rolinda "欢迎来到布恰小镇。"
  hide rolinda with dissolve
  ```
- 分支建议用 `menu`，结尾用 `return` 或 `jump` 回到上层标签

### 事件与线索触发
- 发现线索：`$ discover_clue("线索ID或名称")`
- 角色认知变化：`$ apply_impression_event("事件ID")`
- 角色遇见：`$ set_character_met("角色中文名")`

### 场景/地点扩展
- 地点数据：`game/data/world/locations.rpy`
- 入口 label 建议：`visit_地点_epX`
- 调查 label 建议：`investigate_地点_热点_epX`
- 记得在地点数据中配置 `characters` 与 `clues`

### 资源与路径规范
- 运行资源必须放在 `game/images/`、`game/audio/`
- `asset/` 与 `UI不要删QWQ/` 仅为源素材归档，不直接引用
- 资源命名保持小写英文或明确中文，避免同名冲突

### 协作与提交
- 小步提交，消息示例：`添加 角色对话`、`修复 存档页布局`
- UI 调整需附截图，剧情变更需注明触发节点

---

## 代码风格与命名
- `.rpy` 使用 4 空格缩进
- Label 命名：
  - 主线：`episode1_start`、`episode1_day1_morning`
  - 地点：`visit_rolinda_house_ep1`
  - 调查：`investigate_rolinda_house_desk_ep1`
  - 对话：`talk_to_rolinda_ep1_scene1`
- 数据键名使用 `snake_case`

---

## 已知配置
- 自动存档与快速存档已禁用（见 `game/options.rpy`）
- 存档位为 3x2（6 格），翻页按钮支持 1-9

---

## 常见问题
- 无法启动：检查 Ren'Py 版本是否 ≥ 8.5.0
- UI 显示异常：检查 `game/gui.rpy` 与 `game/screens/*` 中样式修改
- 资源找不到：确认资源在 `game/images/` / `game/audio/` 下并路径一致
