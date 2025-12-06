# 不查小镇 (BuCia) 开发者指南

本文档面向有 Python 背景但不熟悉 Ren'Py 的开发者，帮助你快速理解项目并参与开发。

---

## 目录

1. [Ren'Py 语法速成](#1-renpy-语法速成)
2. [项目架构与代码规范](#2-项目架构与代码规范)
3. [开发工作流程](#3-开发工作流程)
4. [常见开发场景](#4-常见开发场景)
5. [调试与测试](#5-调试与测试)
6. [提交规范](#6-提交规范)

---

## 1. Ren'Py 语法速成

### 1.1 Ren'Py 是什么？

Ren'Py 是一个视觉小说引擎，使用一种**混合语言**：
- **Ren'Py 脚本语言**：用于对话、场景控制、UI 定义
- **Python**：用于游戏逻辑、数据处理、复杂运算

作为 Python 开发者，你会发现 Ren'Py 的 Python 部分非常熟悉，只需要学习 Ren'Py 特有的语法。

### 1.2 文件结构

所有游戏文件放在 `game/` 目录下，扩展名为 `.rpy`：

```
game/
├── script.rpy          # 游戏入口
├── options.rpy         # 全局配置
├── gui.rpy             # GUI 样式
└── ...
```

**重要**：`.rpy` 文件会被编译为 `.rpyc` 二进制文件，`.rpyc` 是缓存文件，不要提交到 Git。

### 1.3 基础语法

#### 1.3.1 Label（标签）- 代码块入口

Label 是 Ren'Py 中的"函数入口点"，用于组织代码：

```renpy
## 定义一个 label
label my_scene:
    "这是一段旁白文字。"
    "可以有多行。"
    return

## 从其他地方跳转
label another_scene:
    jump my_scene      # 跳转到 my_scene（不返回）
    # 或者
    call my_scene      # 调用 my_scene（执行后返回继续）
    "my_scene 执行完毕，继续这里的代码"
    return
```

**类比 Python**：
- `label xxx:` 类似于 `def xxx():`
- `jump xxx` 类似于 `xxx()` 但不返回（类似 goto）
- `call xxx` 类似于 `xxx()` 会返回
- `return` 类似于函数的 `return`

#### 1.3.2 对话与角色

```renpy
## 定义角色（通常在 database.rpy 中）
define tsibela = Character("茨贝拉", color="#ffffff")
define rolinda = Character("罗琳达", color="#cc0000")

## 使用角色说话
label dialogue_example:
    ## 旁白（无角色名）
    "你走进了房间。"

    ## 角色对话
    tsibela "你好，我是茨贝拉。"
    rolinda "欢迎来到布查小镇。"

    ## 带表情的对话
    tsibela happy "太好了！"
    rolinda angry "你在说什么？"

    return
```

#### 1.3.3 Python 代码块

在 Ren'Py 中嵌入 Python 有三种方式：

```renpy
## 方式1：单行 Python 语句（用 $ 前缀）
label python_example:
    $ current_day = 1
    $ player_name = "茨贝拉"
    $ trust_level = get_character_trust("罗琳达")

    ## 方式2：多行 Python 代码块
    python:
        for i in range(3):
            print(i)
        result = some_function()

    return

## 方式3：初始化时执行的 Python（文件顶层）
init python:
    ## 这里定义全局函数和变量
    def my_function():
        return "hello"

    my_dict = {"key": "value"}
```

**init 优先级**：
```renpy
init -1 python:
    ## 优先级 -1，最先执行
    pass

init python:
    ## 默认优先级 0
    pass

init 1 python:
    ## 优先级 1，后执行
    pass
```

#### 1.3.4 变量类型

Ren'Py 有三种变量声明方式，对应不同的生命周期：

```renpy
## 1. define - 常量（不可在游戏中修改）
define GAME_VERSION = "0.1.0"
define tsibela = Character("茨贝拉")

## 2. default - 存档变量（每个存档独立，会被存档保存）
default current_day = 1
default player_health = 100
default inventory = []

## 3. persistent - 跨存档变量（所有存档共享，存在用户配置文件中）
## 通常在 init python 中初始化
init python:
    if persistent.episode_1_unlocked is None:
        persistent.episode_1_unlocked = True
```

**使用场景**：
| 类型 | 用途示例 | 是否存档 |
|------|----------|----------|
| `define` | 角色定义、常量配置 | 否 |
| `default` | 当前天数、行动点、临时状态 | 是（存档内） |
| `persistent` | 周目解锁、成就、全局设置 | 是（跨存档） |

#### 1.3.5 条件分支

```renpy
label branch_example:
    ## if 语句
    if current_day >= 3:
        "已经是第三天了。"
    elif current_day == 2:
        "今天是第二天。"
    else:
        "还是第一天。"

    ## 带条件的对话选项
    menu:
        "你想做什么？"

        "调查现场":
            jump investigate_scene

        "与罗琳达交谈" if is_character_alive("罗琳达"):
            ## 只有罗琳达存活时才显示此选项
            jump talk_to_rolinda

        "休息":
            $ player_health += 10
            "你休息了一会儿。"

    return
```

#### 1.3.6 场景与立绘

```renpy
label visual_example:
    ## 切换背景（scene 会清除所有立绘）
    scene bg church with dissolve

    ## 显示角色立绘
    show tsibela normal at center
    show rolinda angry at left

    ## 隐藏立绘
    hide rolinda

    ## 更换表情（无需 hide 再 show）
    show tsibela happy

    ## 播放音乐
    play music "music/bgm_investigation.ogg" fadein 1.0

    ## 播放音效
    play sound "sfx/door_open.ogg"

    ## 停止音乐
    stop music fadeout 1.0

    return
```

**位置关键字**：
- `at left` / `at right` / `at center`
- `at truecenter`（完全居中）
- 也可以自定义 transform

#### 1.3.7 Screen（屏幕/界面）

Screen 是 Ren'Py 的 UI 系统，类似于 HTML/CSS：

```renpy
## 定义一个屏幕
screen my_hud():
    ## frame 是一个容器
    frame:
        xpos 10
        ypos 10

        ## vbox 垂直排列子元素
        vbox:
            spacing 10

            text "Day [current_day]" size 24
            text "HP: [player_health]"

            ## 按钮
            textbutton "保存" action ShowMenu("save")
            textbutton "设置" action ShowMenu("preferences")

## 显示屏幕
label show_hud_example:
    show screen my_hud
    "现在屏幕上显示了 HUD。"
    hide screen my_hud
    return

## 等待用户点击屏幕按钮（阻塞式）
label blocking_screen_example:
    call screen map_screen
    ## 用户选择后继续
    return
```

**常用 Screen 组件**：
| 组件 | 用途 |
|------|------|
| `text` | 显示文本 |
| `textbutton` | 文本按钮 |
| `imagebutton` | 图片按钮 |
| `vbox` / `hbox` | 垂直/水平布局 |
| `frame` | 带背景的容器 |
| `fixed` | 绝对定位容器 |
| `viewport` | 可滚动区域 |

#### 1.3.8 Transform（变换/动画）

```renpy
## 定义一个变换
transform fade_in:
    alpha 0.0
    linear 0.5 alpha 1.0

transform slide_left:
    xoffset 100
    ease 0.3 xoffset 0

## 使用变换
screen animated_button():
    textbutton "点击我":
        at fade_in
        action NullAction()

## 复杂变换（带状态）
transform button_hover:
    zoom 1.0
    on hover:
        linear 0.15 zoom 1.1
    on idle:
        linear 0.15 zoom 1.0
```

### 1.4 Ren'Py 与 Python 的交互

```renpy
init python:
    ## 定义 Python 函数
    def calculate_damage(base, modifier):
        return base * modifier

    ## 访问 Ren'Py 变量
    def check_day():
        ## store 是存放所有 Ren'Py 变量的命名空间
        return store.current_day >= 3

    ## 使用 Ren'Py API
    def show_notification(message):
        renpy.notify(message)  # 显示通知

    def log_debug(message):
        renpy.log(message)     # 写入日志

label use_python:
    ## 调用 Python 函数
    $ damage = calculate_damage(10, 1.5)
    "造成了 [damage] 点伤害。"

    ## 使用返回值做条件判断
    if check_day():
        "已经是第三天了。"

    return
```

### 1.5 关键 Ren'Py API

```python
## 显示通知（右上角弹出）
renpy.notify("发现新线索！")

## 写入日志文件
renpy.log("调试信息")

## 跳转到 label（从 Python 中）
renpy.jump("some_label")

## 调用 label（从 Python 中）
renpy.call("some_label")

## 刷新界面交互
renpy.restart_interaction()

## 检查是否是安卓/iOS
renpy.android  # True/False
renpy.ios      # True/False

## 显示/隐藏屏幕
renpy.show_screen("screen_name")
renpy.hide_screen("screen_name")
```

---

## 2. 项目架构与代码规范

### 2.1 三层架构

本项目采用**数据-系统-表现**分离架构：

```
game/
├── data/           # 数据层：纯数据定义，无逻辑
│   ├── characters/database.rpy   # 角色数据
│   ├── items/clues.rpy           # 线索数据
│   └── world/locations.rpy       # 地点数据
│
├── systems/        # 系统层：游戏逻辑和 API
│   └── core/
│       ├── episode.rpy           # 周目管理
│       └── time.rpy              # 时间系统
│
├── ui/             # 表现层：UI 逻辑
│   ├── time.rpy
│   ├── locations.rpy
│   └── clues.rpy
│
├── screens/        # 屏幕定义（UI 组件）
│   ├── main_menu.rpy
│   ├── dialogue.rpy
│   └── ...
│
└── episodes/       # 剧情内容
    ├── episode1/
    │   ├── story.rpy
    │   ├── dialogues.rpy
    │   └── ...
    └── shared/     # 多周目共享内容
```

### 2.2 命名规范

#### 文件命名
- 全小写，下划线分隔
- 示例：`time.rpy`, `main_menu.rpy`, `database.rpy`

#### Label 命名
```renpy
## 地点访问
label visit_church:
label visit_town_square:

## 调查热点
label investigate_church_altar:
label investigate_rolinda_desk:

## 角色对话
label talk_to_rolinda_scene1:
label talk_to_tsibela_scene2:

## 事件
label event_fire:
label event_discovery:

## 周目流程
label ep1_day1_morning:
label ep2_day3_evening:
```

#### 变量命名
```renpy
## Persistent（跨存档）
persistent.episode_1_unlocked
persistent.discovered_clues
persistent.sanity

## Default（存档内）
default current_day = 1
default action_points = 3

## Define（常量）
define GAME_VERSION = "0.1.0"
define tsibela = Character("茨贝拉")
```

#### 函数命名
```python
## 获取类
def get_character_trust(char_name):
def get_clue_info(clue_id):

## 检查类
def is_character_alive(char_name):
def is_location_unlocked(loc_name):
def has_action_points():

## 修改类
def modify_character_trust(char_name, amount):
def set_character_dead(char_name):

## 操作类
def advance_time():
def discover_clue(clue_id):
def use_action_point():
```

### 2.3 代码格式

#### 缩进
- **必须使用 4 个空格**（不能用 Tab）
- Ren'Py 对缩进非常敏感，错误的缩进会导致语法错误

```renpy
## 正确
label example:
    if condition:
        "文本"
    return

## 错误（使用了 Tab 或 2 空格）
label example:
  if condition:      # 2空格，错误！
    "文本"
  return
```

#### 注释
```renpy
## 使用 ## 进行注释（推荐）
## 这是一个重要的场景

# 单个 # 也可以，但项目统一使用 ##

## 禁止在 screen 定义后使用 Python docstring
screen my_screen():
    """这样会报错！"""   # ❌ 错误
    pass

screen my_screen():
    ## 正确的注释方式
    pass
```

#### 禁止使用 Emoji
```renpy
## ❌ 错误 - 会导致编码问题
text "欢迎！😊"

## ✅ 正确
text "欢迎！"
```

### 2.4 数据库结构

#### 角色数据库 (`data/characters/database.rpy`)
```python
character_database = {
    "角色名": {
        "full_name": "完整名称",
        "role": "角色职业",
        "faction": "阵营",        # 主角/共谋者/受害者等
        "trust": 50,              # 信任度 0-100
        "alive": True,            # 是否存活
        "sprite": "sprite_name",  # 立绘文件夹名
        "color": "#ffffff",       # 对话颜色
        "bio": "简介",
        "secrets": ["秘密1", "秘密2"],
        "background": "背景故事",
        "first_meet": False       # 是否已见过
    }
}
```

#### 线索数据库 (`data/items/clues.rpy`)
```python
clues_database = {
    "线索名称": {
        "id": "clue_id",
        "name": "显示名称",
        "type": "物证",           # 物证/档案/证词
        "description": "简短描述",
        "detail": "详细内容",
        "location": "发现地点",
        "day_found": 3,           # 可发现的天数
        "relates_to": ["角色1"],  # 关联角色
        "contradicts": ["矛盾线索"],
        "image": "clue/xxx.png",
        "importance": "high"      # high/medium/low/critical
    }
}
```

#### 地点数据库 (`data/world/locations.rpy`)
```python
locations_database = {
    "地点名": {
        "name": "显示名称",
        "display_order": 1,       # 显示顺序
        "label_suffix": "xxx",    # 用于生成 visit_xxx
        "description": "描述",
        "background": "bg/xxx.jpg",
        "bgm": "bgm_xxx.ogg",
        "hotspots": {
            "热点名": {
                "description": "热点描述",
                "clues": ["可发现的线索"],
                "unlocked": True,
                "unlock_condition": "条件名"
            }
        },
        "characters": ["可遇见的角色"],
        "available_times": ["morning", "afternoon"],
        "unlocked": True,
        "visited": False
    }
}
```

### 2.5 Persistent 变量管理

**所有 persistent 变量必须在 `init_persistent.rpy` 中声明**：

```python
init -1 python:
    ## 使用 getattr 检查，兼容旧存档
    if getattr(persistent, 'new_variable', None) is None:
        persistent.new_variable = default_value
```

添加新 persistent 变量的步骤：
1. 在 `init_persistent.rpy` 中添加初始化代码
2. 添加对应的重置逻辑到 `reset_all_persistent()` 函数
3. 在 `show_persistent_status()` 中添加状态显示

---

## 3. 开发工作流程

### 3.1 环境搭建

1. **安装 Ren'Py SDK**
   - 下载：https://www.renpy.org/latest.html
   - 推荐版本：8.5.0+（最低 8.3.6）

2. **克隆项目**
   ```bash
   git clone https://github.com/GTJasonMK/BuCia.git
   ```

3. **配置 Ren'Py Launcher**
   - 打开 Ren'Py Launcher
   - Preferences → Project Directory → 选择项目的**父目录**
   - 返回主界面，选择 BuCia 项目

4. **推荐编辑器**
   - VSCode + Ren'Py Language 插件
   - 项目已配置 `.vscode/settings.json`

### 3.2 开发前检查清单

开始写代码前，请确认：

- [ ] 已阅读相关模块的现有代码
- [ ] 查阅了 Ren'Py 官方文档确认 API 用法
- [ ] 检查是否有可复用的现有代码/函数
- [ ] 了解修改会影响的其他模块

### 3.3 分支策略

```
master（主分支）
  └── dev（开发分支，如有）
        ├── feature/功能名
        └── bugfix/修复名
```

```bash
## 创建功能分支
git checkout master
git checkout -b feature/add-new-character

## 开发完成后
git add .
git commit -m "feat: 添加新角色XXX及其对话"
git push origin feature/add-new-character
## 然后创建 Pull Request
```

### 3.4 代码审查要点

PR 审查时会关注：

1. **架构一致性** - 代码放在正确的层级吗？
2. **命名规范** - label/变量/函数命名符合规范吗？
3. **复用原则** - 是否复用了现有代码？
4. **数据完整性** - 新增数据添加到了正确的数据库吗？
5. **Persistent 管理** - 新 persistent 变量声明在 `init_persistent.rpy` 了吗？

---

## 4. 常见开发场景

### 4.1 添加新角色

**步骤 1**：在 `data/characters/database.rpy` 添加角色定义

```renpy
## 顶层添加角色对象
define new_char = Character("新角色", color="#ff8800", image="new_char")

## 在 character_database 中添加数据
init python:
    character_database["新角色"] = {
        "full_name": "新角色全名",
        "role": "角色职业",
        "faction": "neutral",
        "trust": 50,
        "alive": True,
        "sprite": "new_char",
        "color": "#ff8800",
        "bio": "角色简介...",
        "secrets": ["秘密"],
        "background": "背景故事...",
        "first_meet": False
    }
```

**步骤 2**：准备立绘资源

```
game/images/characters/new_char/
├── normal.png    # 默认表情
├── happy.png     # 开心
├── sad.png       # 难过
└── angry.png     # 生气
```

**步骤 3**：编写对话场景

```renpy
## 在 episodes/episode1/dialogues.rpy
label talk_to_new_char_scene1:
    scene bg location_name with dissolve
    show new_char normal at center

    if is_first_meet("新角色"):
        new_char "你好，我们第一次见面。"
        $ set_character_met("新角色")
    else:
        new_char "又见面了。"

    menu:
        "友好交谈":
            $ modify_character_trust("新角色", 5)
            new_char happy "谢谢你的关心。"

        "质问":
            $ modify_character_trust("新角色", -10)
            new_char angry "你这是什么意思？"

    return
```

**步骤 4**：添加到地点

```python
## 在 data/world/locations.rpy 的对应地点
"某地点": {
    ...
    "characters": ["原有角色", "新角色"],  # 添加
    ...
}
```

### 4.2 添加新线索

**步骤 1**：在 `data/items/clues.rpy` 添加线索数据

```python
clues_database["新线索"] = {
    "id": "new_clue",
    "name": "新线索名称",
    "type": "物证",
    "description": "简短描述",
    "detail": "详细内容...",
    "location": "发现地点",
    "day_found": 1,
    "relates_to": ["相关角色"],
    "contradicts": [],
    "image": "clue/new_clue.png",
    "importance": "medium"
}
```

**步骤 2**：准备图标

- 规格：80x80 像素，PNG 透明背景
- 路径：`game/images/clue/new_clue.png`

**步骤 3**：在调查场景中触发发现

```renpy
label investigate_some_hotspot:
    "你仔细检查了这里..."

    if not is_clue_discovered("新线索"):
        $ discover_clue("新线索")
        "你发现了一条重要线索！"
        ## 可选：显示线索详情
        "【新线索】"
        "[clues_database['新线索']['detail']]"
    else:
        "你已经调查过这里了。"

    return
```

### 4.3 添加新地点

**步骤 1**：在 `data/world/locations.rpy` 添加地点数据

```python
locations_database["新地点"] = {
    "name": "新地点名称",
    "display_order": 11,
    "label_suffix": "new_location",
    "description": "地点描述...",
    "background": "bg/new_location.jpg",
    "bgm": "bgm_investigation.ogg",
    "hotspots": {
        "热点1": {
            "description": "热点描述",
            "clues": ["可发现的线索ID"],
            "unlocked": True
        },
        "热点2": {
            "description": "需要解锁的热点",
            "clues": ["线索ID"],
            "unlocked": False,
            "unlock_condition": "day3_after"
        }
    },
    "characters": ["可遇见的角色"],
    "available_times": ["morning", "afternoon", "evening"],
    "unlocked": True,
    "visited": False
}
```

**步骤 2**：准备背景图

- 规格：1920x1080，JPG 或 PNG
- 路径：`game/images/bg/new_location.jpg`

**步骤 3**：编写访问场景

```renpy
## 在 episodes/episode1/locations.rpy
label visit_new_location:
    $ set_location_visited("新地点")

    scene bg new_location with dissolve
    play music "music/bgm_investigation.ogg" fadein 1.0

    "你来到了新地点..."

    menu visit_new_location_menu:
        "调查热点1":
            call investigate_new_location_hotspot1
            jump visit_new_location_menu

        "与角色交谈" if "角色名" in get_location_characters("新地点") and is_character_alive("角色名"):
            call talk_to_character_scene1
            jump visit_new_location_menu

        "离开":
            return
```

**步骤 4**：在地图 UI 中添加（如需要）

参考 `ui/locations.rpy` 中的现有实现。

### 4.4 添加分支选项

```renpy
label branching_example:
    tsibela "我该怎么做？"

    menu:
        ## 无条件选项
        "选项A":
            $ choice = "A"
            "你选择了A。"

        ## 带条件的选项（条件不满足时隐藏）
        "选项B（需要高信任度）" if get_character_trust("罗琳达") >= 60:
            $ choice = "B"
            "你选择了B。"

        ## 带条件的选项（条件不满足时显示但不可点击）
        "选项C（需要线索）":
            if is_clue_discovered("关键线索"):
                $ choice = "C"
                "你选择了C。"
            else:
                "你还没有足够的证据支持这个选项。"
                ## 返回菜单重新选择
                jump branching_example

    ## 根据选择分支
    if choice == "A":
        jump branch_a
    elif choice == "B":
        jump branch_b
    else:
        jump branch_c
```

### 4.5 使用时间系统

```renpy
label time_usage_example:
    ## 显示当前时间
    $ time_text = get_time_display()
    "现在是 [time_text]"

    ## 消耗行动点
    if has_action_points():
        $ use_action_point()
        "你决定调查这里。（消耗1行动点）"
        "剩余行动点：[action_points]"
    else:
        "你已经没有行动点了，需要休息。"
        $ advance_time()

    ## 推进时间
    $ result = advance_time()
    if result == "new_day":
        "新的一天开始了。"
        "你恢复了精力。（行动点已恢复）"
    else:
        "时间流逝..."

    ## 检查关键时间节点
    if check_event_trigger(EVENT_DAY3_FIRE):
        "突然，你听到了火警声！"
        call event_fire

    return
```

### 4.6 修改精神值

```renpy
label sanity_example:
    ## 降低精神值
    $ persistent.sanity -= 10
    $ persistent.sanity = max(0, persistent.sanity)  # 确保不低于0

    "你感到一阵眩晕...（精神值-10）"

    ## 根据精神值触发不同效果
    if persistent.sanity <= 20:
        "你的视野开始模糊，似乎看到了不存在的东西..."
        ## 触发幻觉场景
        call hallucination_scene
    elif persistent.sanity <= 50:
        "你感到不安..."

    ## 恢复精神值（例如在教堂祈祷）
    $ persistent.sanity += 20
    $ persistent.sanity = min(100, persistent.sanity)  # 确保不超过100
    "你的心情平静了一些。（精神值+20）"

    return
```

---

## 5. 调试与测试

### 5.1 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Shift+D` | 打开开发者菜单 |
| `Shift+R` | 重新加载脚本（热重载） |
| `Shift+O` | 打开控制台 |
| `Shift+I` | 检查元素（调试 Screen） |
| `F1` | 显示 persistent 状态 |
| `F2` | 重置周目解锁 |

### 5.2 控制台命令

按 `Shift+O` 打开控制台后可执行：

```python
## 解锁所有周目
unlock_all_episodes()

## 重置所有 persistent
reset_all_persistent()

## 设置精神值
set_sanity(50)

## 跳转到指定 label
renpy.jump("episode1_day3")

## 显示 persistent 状态
show_persistent_status()

## 发现指定线索
discover_clue("打火机")

## 修改角色信任度
modify_character_trust("罗琳达", 30)

## 查看变量值
print(current_day)
print(persistent.episode_2_unlocked)
```

### 5.3 清除缓存

当代码修改后不生效时：

```bash
## 删除编译缓存
rm -rf game/cache/
rm -rf game/**/*.rpyc

## Windows PowerShell
Remove-Item -Recurse -Force game\cache\
Get-ChildItem -Path game -Filter *.rpyc -Recurse | Remove-Item
```

然后重启游戏。

### 5.4 重置 Persistent 数据

1. **游戏内**：按 `F2`
2. **手动删除**：
   - Windows: `%APPDATA%\RenPy\HaiTangYiGuZhiShi-1763360452\`
   - macOS: `~/Library/RenPy/HaiTangYiGuZhiShi-1763360452/`
   - Linux: `~/.renpy/HaiTangYiGuZhiShi-1763360452/`

### 5.5 测试检查清单

提交代码前请验证：

- [ ] 游戏可以正常启动
- [ ] 主菜单正常显示
- [ ] 新增/修改的功能正常运行
- [ ] 没有控制台报错
- [ ] 所有按钮可以点击
- [ ] 文本正确显示（无乱码）
- [ ] 图片和音频正常加载
- [ ] 存档可以保存和加载
- [ ] 已用 `Shift+R` 测试热重载

---

## 6. 提交规范

### 6.1 提交信息格式

```
<类型>: <简短描述>

[可选：详细说明]
```

**类型列表**：
| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复 bug |
| `docs` | 文档更新 |
| `style` | 代码格式（不影响功能） |
| `refactor` | 重构（不是新功能也不是修复） |
| `test` | 测试相关 |
| `chore` | 构建/工具/配置 |

**示例**：
```
feat: 添加新角色"哈夫"及其对话场景

- 在 database.rpy 中添加角色定义
- 添加角色立绘（4种表情）
- 编写初次见面和后续对话场景
- 将角色添加到电工工作室地点
```

### 6.2 提交前检查清单

- [ ] 代码格式正确（4空格缩进）
- [ ] 没有使用 emoji
- [ ] 注释使用 `##`
- [ ] 变量命名符合规范
- [ ] 新 persistent 变量已在 `init_persistent.rpy` 声明
- [ ] 没有将 `.rpyc` 文件加入提交
- [ ] 通过本地测试
- [ ] 提交信息符合规范

### 6.3 Pull Request 模板

```markdown
## 变更说明
简要描述这个 PR 做了什么。

## 变更类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 重构
- [ ] 文档

## 测试情况
描述你如何测试这些变更。

## 截图（如有 UI 变更）
贴上相关截图。

## 检查清单
- [ ] 代码符合项目规范
- [ ] 已进行本地测试
- [ ] 已更新相关文档（如需要）
```

---

## 附录：快速参考卡

### Ren'Py 基础语法

```renpy
## 定义
define const = "value"           # 常量
default var = 1                  # 存档变量

## 流程控制
label name:                      # 定义入口
    jump other_label             # 跳转（不返回）
    call other_label             # 调用（返回）
    return                       # 返回

## 对话
"旁白文字"
character "对话文字"
character expression "带表情对话"

## 条件
if condition:
    pass
elif other:
    pass
else:
    pass

## 选项菜单
menu:
    "选项1":
        pass
    "选项2" if condition:
        pass

## Python
$ var = value                    # 单行
python:                          # 多行
    pass
init python:                     # 初始化时执行
    pass

## 视觉
scene bg name with dissolve      # 切换背景
show char at position            # 显示立绘
hide char                        # 隐藏立绘
play music "file" fadein 1.0     # 播放音乐
play sound "file"                # 播放音效
```

### 项目 API 速查

```python
## 角色
get_character_trust("角色名")      # 获取信任度
modify_character_trust("角色名", 10)  # 修改信任度
is_character_alive("角色名")       # 检查存活

## 线索
discover_clue("线索ID")            # 发现线索
is_clue_discovered("线索ID")       # 检查发现

## 地点
is_location_unlocked("地点名")     # 检查解锁
is_hotspot_unlocked("地点", "热点")  # 检查热点

## 时间
advance_time()                    # 推进时间
use_action_point()                # 消耗行动点
has_action_points()               # 检查行动点
get_time_display()                # 获取时间文本

## 周目
get_current_episode()             # 获取当前周目
is_episode(1)                     # 检查周目
start_episode(1)                  # 开始周目
```

---

**文档版本**：v1.0
**最后更新**：2025-11-26
**适用 Ren'Py 版本**：8.3.6+
