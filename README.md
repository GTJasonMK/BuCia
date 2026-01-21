# 不查小镇 (BuCia)

基于 Ren'Py 引擎的悬疑推理视觉小说游戏。

---

## 目录

- [快速开始](#快速开始)
- [项目架构](#项目架构)
- [资源管理](#资源管理)
- [功能扩展](#功能扩展)
- [代码规范](#代码规范)
- [开发流程](#开发流程)
- [常见问题](#常见问题)

---

## 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/GTJasonMK/BuCia.git
```

假设克隆到了 `D:\Projects\BuCia`

### 2. 配置 Ren'Py Launcher

1. 下载并安装 [Ren'Py SDK](https://www.renpy.org/latest.html)（推荐 8.5.0+）
2. 打开 Ren'Py Launcher
3. 点击左下角 **preferences**
4. 在 **General** 一栏，点击 **Project Dictionary** 更换为克隆仓库的**父目录**（本例中选择 `D:\Projects`）
5. 返回主界面

### 3. 启动项目

Ren'Py 会自动检索到 `BuCia` 项目并显示在列表中，选择后点击 **Launch Project** 即可运行。

**引擎版本要求**：Ren'Py 8.3.6 或更高

---

## 项目架构

### 根目录结构

```
.
├── game/        # 运行时脚本与资源（Ren'Py 实际加载）
├── asset/       # 设计源素材与历史归档（不直接加载）
├── docs/        # 项目说明文档
├── UI不要删QWQ/ # 历史UI归档包
└── log.txt / traceback.txt # 本地排查用日志
```

### 三层架构设计

项目采用**数据层 → 系统层 → 表现层**的分离架构：

```
game/
├── data/                    # 数据层 - 游戏数据
│   ├── characters/          # 角色相关数据
│   │   └── database.rpy     # 角色定义和数据库
│   ├── world/               # 世界设定数据
│   │   └── locations.rpy    # 地点数据
│   ├── items/               # 物品相关数据
│   │   └── clues.rpy        # 线索数据
│   └── config/              # 配置数据（预留）
├── systems/                 # 系统层 - 游戏逻辑
│   ├── core/                # 核心游戏系统
│   │   ├── episode.rpy      # 周目管理系统
│   │   └── time.rpy         # 时间系统
│   ├── gameplay/            # 游戏玩法系统（预留）
│   ├── character/           # 角色系统（预留）
│   ├── progress/            # 进度追踪系统（预留）
│   └── extras/              # 额外功能系统（预留）
├── ui/                      # 表现层 - 用户界面
│   ├── time.rpy             # 时间UI
│   ├── locations.rpy        # 地图UI
│   └── clues.rpy            # 线索簿UI
├── screens/                 # UI屏幕定义（模块化）
│   ├── main_menu.rpy        # 主菜单和周目选择
│   ├── dialogue.rpy         # 对话、选择、输入屏幕
│   ├── game_menu.rpy        # 游戏菜单框架
│   ├── save_load.rpy        # 存档和读档界面
│   ├── preferences.rpy      # 设置界面
│   ├── history.rpy          # 历史记录
│   ├── navigation.rpy       # 导航菜单
│   └── common.rpy           # 通用UI组件
└── fonts/                   # 字体资源
    ├── lolita.ttf           # 标题字体
    ├── SourceHanSansLite.ttf # 对话字体
    └── Holy-Union-2.ttf     # UI字体
```

### 周目复用机制

支持多周目共享场景和周目特有场景：

```
game/episodes/
├── shared/              # 多周目共享内容
│   ├── locations/       # 共享地点（3+周目使用）
│   └── common_scenes.rpy
└── episode1/            # 周目1特有内容
    ├── story.rpy        # 主线剧情
    ├── locations.rpy    # 特有地点
    └── ...
```

**使用规则**：
- 场景在**3个及以上周目**出现 → 放在 `shared/`
- 场景是**周目特有** → 放在 `episodeX/`

---

## 资源管理

### 图像资源

#### 背景图 (Background)
- **位置**：`game/images/bg/`
- **规格**：1920x1080，JPG或PNG
- **命名**：`town_square.jpg`, `church_interior.jpg`
- **使用**：`scene bg town_square with dissolve`

#### 角色立绘 (Character Sprites)
- **位置**：`game/images/characters/角色名/`
- **规格**：高度1080px，PNG透明背景
- **命名**：`normal.png`, `happy.png`, `sad.png`
- **使用**：`show tsibela happy at center`

#### CG图 (Event CG)
- **位置**：`game/images/cg/`
- **规格**：1920x1080，JPG
- **命名**：`ep1_fire.jpg`, `ending_good.jpg`
- **使用**：`scene cg ep1_fire with dissolve`

#### 线索图标
- **位置**：`game/images/clue/`
- **规格**：80x80像素，PNG透明背景
- **命名**：`lighter.png`, `diary.png`
- **使用**：在 `clues_database` 中引用

#### 精神值图标
- **位置**：`game/images/sanity/`
- **文件**：`1.png`（正常）至 `6.png`（崩溃）
- **自动调用**：根据 `persistent.sanity` 值自动选择

### 音频资源

#### BGM (背景音乐)
- **位置**：`game/audio/music/`
- **格式**：OGG（推荐）或MP3，128-192kbps
- **命名**：`bgm_investigation.ogg`, `bgm_tension.ogg`
- **使用**：`play music "music/bgm_investigation.ogg" fadein 1.0`

#### 音效 (SFX)
- **位置**：`game/audio/sfx/`
- **格式**：OGG，时长≤5秒
- **命名**：`door_open.ogg`, `footstep.ogg`
- **使用**：`play sound "sfx/door_open.ogg"`

#### 语音 (Voice)
- **位置**：`game/audio/voice/角色名/`
- **格式**：OGG
- **命名**：`ep1_line001.ogg`, `ep1_line002.ogg`
- **使用**：`voice "voice/tsibela/ep1_line001.ogg"`

### 字体资源
- **位置**：`game/fonts/`
- **当前字体**：
  - `Holy-Union-2.ttf` - UI和周目按钮字体
  - `lolita.ttf` - 界面标题字体
  - `SourceHanSansLite.ttf` - 对话和正文字体（思源黑体）

**添加新字体：**
1. 将字体文件放入 `game/fonts/` 目录
2. 在 `gui.rpy` 中定义字体：
   ```python
   define gui.new_font = "fonts/your_font.ttf"
   ```
3. 在需要的地方使用：
   ```renpy
   text "示例文字" font "fonts/your_font.ttf"
   ```

### GUI界面资源
- **位置**：`game/gui/`
- **包含**：按钮、对话框、菜单遮罩等UI元素

---

## 功能扩展

### 添加新角色

**1. 注册角色数据**（`game/data/characters/database.rpy`）
```python
## 定义角色对象
define new_character = Character("新角色", color="#ffffff")

## 添加数据库条目
character_database = {
    "新角色": {
        "full_name": "新角色的全名",
        "role": "角色职业",
        "faction": "neutral",
        "trust": 50,
        "alive": True,
        "secrets": ["秘密1", "秘密2"],
        "background": "背景故事..."
    }
}
```

**2. 准备立绘**
- 创建 `game/images/characters/new_character/`
- 放入 `normal.png`, `happy.png`, `sad.png` 等

**3. 编写对话**（`game/episodes/episode1/dialogues.rpy`）
```renpy
label talk_to_new_character_scene1:
    scene bg location_name
    show new_character normal at center

    new_character "你好，我是新角色。"

    menu:
        "对话选项1":
            $ modify_character_trust("新角色", 5)
        "对话选项2":
            $ modify_character_trust("新角色", -10)

    return
```

**4. 添加到地点**（`game/data/world/locations.rpy`）
```python
"地点名称": {
    "characters": ["罗琳达", "新角色"],  # 添加新角色
    # ...
}
```

---

### 添加新线索

**1. 注册线索数据**（`game/data/items/clues.rpy`）
```python
clues_database = {
    "new_clue_id": {
        "name": "线索名称",
        "type": "物证",  # 物证/档案/证词
        "description": "简短描述",
        "detail": "详细内容",
        "location": "发现地点",
        "relates_to": ["角色1", "角色2"],
        "contradicts": ["矛盾线索id"],
        "importance": "high",
        "icon": "clue/new_clue.png"
    }
}
```

**2. 准备图标**
- 创建 80x80 PNG 图标
- 保存到 `game/images/clue/new_clue.png`

**3. 在调查场景中发现**（`game/episodes/episode1/investigations.rpy`）
```renpy
label investigate_location_hotspot:
    "你仔细检查了这里..."
    $ discover_clue("new_clue_id")
    "发现了重要线索！"
    return
```

---

### 添加新地点

**1. 注册地点数据**（`game/data/world/locations.rpy`）
```python
locations_database = {
    "新地点ID": {
        "name": "地点名称",
        "description": "地点描述",
        "background": "bg/new_location.jpg",
        "label": "visit_new_location",
        "hotspots": [
            {
                "name": "热点1",
                "label": "investigate_new_location_hotspot1",
                "clue_id": "相关线索id",
                "unlock_condition": "day2_afternoon"
            }
        ],
        "characters": ["角色1", "角色2"],
        "available_times": ["morning", "afternoon", "evening"],
        "unlock_condition": "day1_morning",
        "action_cost": 1
    }
}
```

**2. 准备背景图**
- 创建 1920x1080 背景图
- 保存到 `game/images/bg/new_location.jpg`

**3. 编写访问场景**（`game/episodes/episode1/locations.rpy`）
```renpy
label visit_new_location:
    scene bg new_location with dissolve
    play music "music/bgm_investigation.ogg" fadein 1.0

    "你来到了新地点..."

    menu visit_new_location_menu:
        "调查热点1":
            call investigate_new_location_hotspot1
            jump visit_new_location_menu

        "与角色1交谈" if is_character_alive("角色1"):
            call talk_to_character1
            jump visit_new_location_menu

        "离开":
            return
```

**4. 编写调查场景**（`game/episodes/episode1/investigations.rpy`）
```renpy
label investigate_new_location_hotspot1:
    "你调查了热点1..."

    if is_hotspot_unlocked("新地点ID", "热点1"):
        $ discover_clue("相关线索id")
    else:
        "现在无法调查这里。"

    return
```

**5. 在地图UI中添加按钮**（`game/ui/locations.rpy`）
```renpy
## 在 screen map_screen() 中添加
if is_location_unlocked("新地点ID"):
    textbutton "新地点名称":
        action [Function(use_action_point), Jump("visit_new_location")]
        sensitive has_action_points()
else:
    textbutton "新地点名称 [[未解锁]":
        action None
        text_color "#666666"
```

---

### 添加新周目

**1. 创建周目目录**
```bash
game/episodes/episode2/
├── story.rpy
├── locations.rpy
├── unique_scenes.rpy
├── dialogues.rpy
├── investigations.rpy
└── events.rpy
```

**2. 编写周目入口**（`game/script.rpy`）
```renpy
label episode_2:
    ## 初始化周目状态
    $ current_episode = 2
    $ current_day = 1
    $ current_time = "morning"
    $ action_points = 3

    ## 显示标题
    scene black with fade
    centered "{size=60}Episode 2{/size}\n{size=40}伪书·真相的碎片{/size}"
    pause 2.0

    ## 调用主线
    call ep2_story_start

    ## 解锁下一周目
    $ persistent.episode_3_unlocked = True
    return
```

**3. 编写主线剧情**（`game/episodes/episode2/story.rpy`）
```renpy
label ep2_story_start:
    scene bg town_square with fade
    "又是一个轮回的开始..."
    call ep2_day1_morning
    return

label ep2_day1_morning:
    $ current_day = 1
    $ current_time = "morning"

    # 剧情内容...
    call free_investigation

    $ advance_time()
    call ep2_day1_afternoon
    return
```

**4. 在主菜单添加按钮**（`game/screens/main_menu.rpy`）
```renpy
## 在展开状态中添加周目按钮
imagebutton:
    idle "gui/button_bar.png"
    hover "gui/button_bar.png"
    action [SetVariable("show_episodes", False), Start("episode_2")]
    sensitive persistent.episode_2_unlocked
    hovered [SetVariable("button_hint_text", "Episode 2描述"), SetVariable("episode2_hovered", True)]
    unhovered [SetVariable("button_hint_text", ""), SetVariable("episode2_hovered", False)]

text "Episode 2":
    properties TEXT_STYLES["episode_button"]
    color ("#ffffff" if persistent.episode_2_unlocked else "#888888")
```

**注意**：周目按钮的颜色通过 persistent 变量控制，解锁为白色，锁定为灰色。

---

## 代码规范

### 命名规范

#### 文件命名
- 全小写，使用下划线分隔
- 示例：`time.rpy`, `database.rpy`, `main_menu.rpy`

#### 目录命名
- 全小写，使用下划线分隔（如需要）
- 示例：`save_load/`, `characters/`, `core/`

#### Label命名
```renpy
visit_地点名              # visit_church, visit_town_square
investigate_地点_热点     # investigate_church_altar
talk_to_角色_sceneX      # talk_to_tsibela_scene1
event_描述               # event_fire_discovery
epX_dayY_时段            # ep1_day1_morning
```

#### 变量命名
```python
persistent.episode_1_unlocked    # Persistent变量（跨存档）
default current_day = 1          # Default变量（存档内）
define tsibela = Character(...)  # Define变量（常量）
$ temp_value = 10                # 临时变量
```

### 代码格式

#### 缩进
- 使用 **4个空格**（不使用Tab）
- Ren'Py脚本对缩进敏感

```renpy
label example:
    scene bg room

    if condition:
        "文本内容"

    return
```

#### 注释
- 使用 `##` 进行注释
- 重要逻辑必须添加注释

```renpy
## 这是一个重要场景
label important_scene:
    ## 显示背景
    scene bg church with dissolve

    ## 角色登场
    show tsibela normal at center

    return
```

#### 禁止使用
- ❌ Screen定义后的 `"""docstring"""` （8.3.6不支持）
- ✅ 始终使用 `##` 注释

---

## 开发流程

### Git工作流

#### 分支策略
```
main（主分支）
  ├── dev（开发分支）
  │     ├── feature/功能名（功能分支）
  │     └── bugfix/修复名（修复分支）
  └── release/版本号（发布分支）
```

#### 提交流程
```bash
## 1. 创建功能分支
git checkout dev
git checkout -b feature/add-new-character

## 2. 进行开发并提交
git add .
git commit -m "feat: 添加新角色XXX及其对话场景"

## 3. 推送并创建PR
git push origin feature/add-new-character
```

#### 提交信息规范
```
<类型>: <简短描述>

类型：
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式
- refactor: 重构
- test: 测试相关
- chore: 构建/工具

示例：
feat: 添加新角色"哈夫"及其初始对话场景
fix: 修复线索簿显示错误
docs: 更新README中的资源管理章节
```

---

### 本地测试

#### 测试前准备
```bash
## 清除缓存
rm -rf game/cache/
rm game/**/*.rpyc

## 重置persistent数据（如果需要）
## 方法1: 游戏中按 F2
## 方法2: 删除 %APPDATA%\RenPy\HaiTangYiGuZhiShi-1763360452\
```

#### 测试检查清单
- [ ] 游戏可以正常启动
- [ ] 主菜单正常显示
- [ ] 新增内容正常运行
- [ ] 所有按钮可以点击
- [ ] 文本和图片正确显示
- [ ] 音频正常播放
- [ ] 时间系统正常
- [ ] 存档可以保存和加载

#### 调试工具
- `Shift+D`：开发者菜单
- `Shift+R`：重新加载脚本
- `Shift+O`：控制台
- `F1`：显示Persistent状态
- `F2`：重置周目解锁
- `log.txt`：查看错误日志

---

## 常见问题

### 资源相关

**Q: 图片不显示？**

A: 检查文件路径、文件名（区分大小写）、扩展名是否正确。
```renpy
## 错误
scene bg church.jpg  # ❌

## 正确
scene bg church      # ✅ 自动查找.jpg或.png
```

**Q: 音频无法播放？**

A: 确认格式为OGG或MP3，检查文件路径包含子目录。
```renpy
play music "music/bgm_investigation.ogg"  # ✅
play music "bgm_investigation.ogg"        # ❌
```

---

### 代码相关

**Q: 修改代码后游戏没变化？**

A:
1. 按 `Shift+R` 重新加载脚本
2. 删除 `.rpyc` 缓存后重启
3. 确认修改的是正确的文件

**Q: 出现"label已定义"错误？**

A: 检查是否有重复的label定义，使用 `grep -r "label xxx" game/` 查找所有定义。

**Q: Persistent变量修改后没生效？**

A:
1. Persistent数据存储在系统AppData
2. 使用 `F2` 快捷键强制重置
3. 或删除 `%APPDATA%\RenPy\HaiTangYiGuZhiShi-1763360452\`

**Q: Screen定义报错"expected a keyword argument"？**

A: 检查screen定义后是否有`"""`docstring，8.3.6不支持，改为`##`注释。

---

### 开发流程相关

**Q: 如何测试周目解锁？**

A:
1. 在代码中设置：`$ persistent.episode_2_unlocked = True`
2. 使用 `F1` 查看状态，`F2` 重置
3. 调用 `unlock_all_episodes()` 函数

**Q: 如何回退版本？**

A:
```bash
git log --oneline              # 查看历史
git checkout <commit-hash>     # 回退
git checkout -b rollback-xxx   # 保存状态
```

---

## 常用API参考

### 角色系统
```python
get_character_trust("角色名")           # 获取信任度
modify_character_trust("角色名", 10)    # 修改信任度
is_character_alive("角色名")           # 检查存活
```

### 线索系统
```python
discover_clue("线索id")                # 发现线索
is_clue_discovered("线索id")           # 检查是否已发现
get_clues_by_type("物证")              # 按类型获取
```

### 地点系统
```python
is_location_unlocked("地点id")         # 检查解锁
is_location_available("地点id")        # 检查开放
is_hotspot_unlocked("地点id", "热点")  # 检查热点
```

### 时间系统
```python
advance_time()                         # 推进时间
use_action_point()                     # 消耗行动点
has_action_points()                    # 检查行动点
```

### 周目系统
```python
get_current_episode()                  # 获取周目编号
is_episode(X)                          # 检查指定周目
is_first_episode()                     # 检查第一周目
is_truth_episode()                     # 检查真相周目
```

---

## 联系与支持

- **GitHub**: https://github.com/GTJasonMK/BuCia
- **Ren'Py官方文档**: https://www.renpy.org/doc/html/
- **项目维护**: 在GitHub提交Issue

---

**文档版本**：v2.0
**最后更新**：2025-11-23
**维护者**：项目开发团队

## 更新日志

### v2.0 (2025-11-23)
- 重构项目结构：systems/ 和 data/ 目录采用子目录分类
- 新增 screens/ 目录：将 screens.rpy 模块化拆分为8个文件
- 新增 fonts/ 目录：统一管理字体资源
- 修复周目按钮颜色逻辑问题
- 更新所有文档以反映新的目录结构

### v1.0 (2025-11-18)
- 初始版本发布
- 建立三层架构设计
- 实现周目系统基础功能
