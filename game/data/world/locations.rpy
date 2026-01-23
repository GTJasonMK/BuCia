## 地点系统 - 布恰小镇地图

## 地图移动目标变量
default map_target_location = None

## 地点数据库
init python:
    locations_database = {
        "罗琳达宅邸": {
            "name": "罗琳达的宅邸",
            "display_order": 1,
            "label_suffix": "rolinda_house",
            "description": "小镇中最豪华的居所，联邦政府社区管理负责人的住处。",
            "background": "bg/rolinda_house.jpg",
            "bgm": "bgm_investigation.ogg",
            "map_pos": (625, 140),
            "map_icon": "building",
            "hotspots": {
                "书桌": {
                    "description": "整洁的办公桌，上面摆放着一些文件。",
                    "label": "investigate_rolinda_house_desk",
                    "clues": ["政府文件"],
                    "unlocked": True
                },
                "保险柜": {
                    "description": "墙角的小型保险柜，需要密码。",
                    "label": "investigate_rolinda_house_safe",
                    "clues": ["药厂资料"],
                    "unlocked": False,
                    "unlock_condition": "password_found"
                },
                "窗户": {
                    "description": "可以看到小镇广场的窗户。",
                    "label": None,
                    "clues": [],
                    "unlocked": True
                }
            },
            "characters": ["罗琳达"],
            "available_times": ["morning", "afternoon", "evening"],
            "unlocked": True,
            "visited": False
        },

        "叶蒂娜诊所": {
            "name": "叶蒂娜的诊所",
            "display_order": 2,
            "label_suffix": "yedina_clinic",
            "description": "小镇唯一的医疗设施，兼具药房功能。",
            "background": "bg/yedina_clinic.jpg",
            "bgm": "bgm_investigation.ogg",
            "map_pos": (1200, 128),
            "map_icon": "building",
            "hotspots": {
                "药柜": {
                    "description": "放满各种药品的柜子，有些标签模糊。",
                    "label": "investigate_yedina_clinic_cabinet",
                    "clues": ["药品清单"],
                    "unlocked": True
                },
                "检查床": {
                    "description": "用于检查病人的病床。",
                    "label": None,
                    "clues": [],
                    "unlocked": True
                },
                "办公桌": {
                    "description": "叶蒂娜的工作台，散落着一些医疗记录。",
                    "label": None,
                    "clues": ["安德莉娅尸检报告"],
                    "unlocked": False,
                    "unlock_condition": "day3_after"
                }
            },
            "characters": ["叶蒂娜"],
            "available_times": ["morning", "afternoon", "evening"],
            "unlocked": True,
            "visited": False
        },

        "安德莉娅住所": {
            "name": "安德莉娅的住所",
            "display_order": 3,
            "label_suffix": "andrea_house",
            "description": "小镇边缘的简陋房屋，Day 3凌晨被火灾焚毁。",
            "background": "bg/andrea_house.jpg",
            "bgm": "bgm_dark.ogg",
            "map_pos": (240, 830),
            "map_icon": "house",
            "hotspots": {
                "烧毁的床铺": {
                    "description": "火灾后的残骸，能看出曾经的简陋。",
                    "label": "investigate_andrea_house_bed",
                    "clues": ["火灾现场照片"],
                    "unlocked": False,
                    "unlock_condition": "day3_after"
                },
                "窗户残骸": {
                    "description": "窗框已经完全烧毁。",
                    "label": None,
                    "clues": ["窗户痕迹"],
                    "unlocked": False,
                    "unlock_condition": "day3_after"
                },
                "门锁": {
                    "description": "门锁似乎有被撬动的痕迹。",
                    "label": None,
                    "clues": ["破门痕迹"],
                    "unlocked": False,
                    "unlock_condition": "day3_after"
                }
            },
            "characters": [],
            "available_times": ["morning", "afternoon", "evening"],
            "unlocked": False,
            "unlock_condition": "day3_after",
            "visited": False
        },

        "教堂": {
            "name": "莫洛拉瓦的家",
            "display_order": 4,
            "label_suffix": "church",
            "description": "莫洛拉瓦在小镇的居所，平日里也在此接待来访者。",
            "background": "bg/church.jpg",
            "bgm": "bgm_church.ogg",
            "map_pos": (460, 900),
            "map_icon": "church",
            "hotspots": {
                "祈祷室": {
                    "description": "安静的祈祷空间，可以在这里冥想。",
                    "clues": [],
                    "unlocked": True,
                    "special_action": "restore_sanity"
                },
                "地窖": {
                    "description": "教堂地下的避难所，战时用作庇护所。",
                    "clues": ["避难所记录"],
                    "unlocked": False,
                    "unlock_condition": "molorava_trust_high"
                },
                "忏悔室": {
                    "description": "莫洛拉瓦神父听取忏悔的地方。",
                    "clues": [],
                    "unlocked": True
                }
            },
            "characters": ["莫洛拉瓦"],
            "available_times": ["morning", "afternoon", "evening"],
            "unlocked": True,
            "visited": False
        },

        "社区中心": {
            "name": "特莉娜的家",
            "display_order": 5,
            "label_suffix": "community_center",
            "description": "特莉娜在小镇的居所，平时也会在这里处理事务。",
            "background": "bg/community_center.jpg",
            "bgm": "bgm_investigation.ogg",
            "map_pos": (911, 561),
            "map_icon": "building",
            "hotspots": {
                "档案柜": {
                    "description": "存放社区档案的文件柜。",
                    "clues": ["居民档案"],
                    "unlocked": True
                },
                "公告板": {
                    "description": "张贴各种通知的公告板。",
                    "clues": ["社区通知"],
                    "unlocked": True
                },
                "特莉娜办公桌": {
                    "description": "社区负责人的办公桌，整理得很整洁。",
                    "clues": ["药厂谈判资料"],
                    "unlocked": False,
                    "unlock_condition": "telina_trust_high"
                }
            },
            "characters": ["特莉娜"],
            "available_times": ["morning", "afternoon"],
            "unlocked": True,
            "visited": False
        },

        "巴德别特住所": {
            "name": "巴德别特的家",
            "display_order": 6,
            "label_suffix": "badebiete_house",
            "description": "退休警员的住所，整洁而朴素。",
            "background": "bg/badebiete_house.jpg",
            "bgm": "bgm_investigation.ogg",
            "map_pos": (1214, 765),
            "map_icon": "house",
            "hotspots": {
                "书架": {
                    "description": "放满警务相关书籍的书架。",
                    "clues": ["警务笔记"],
                    "unlocked": True
                },
                "老照片": {
                    "description": "墙上挂着的警察时代照片。",
                    "clues": [],
                    "unlocked": True
                },
                "抽屉": {
                    "description": "书桌的抽屉，似乎藏着什么。",
                    "clues": ["实验对象名单"],
                    "unlocked": False,
                    "unlock_condition": "badebiete_trust_high"
                }
            },
            "characters": ["巴德别特"],
            "available_times": ["evening", "night"],
            "unlocked": True,
            "visited": False
        },

        "哈夫工作室": {
            "name": "电工哈夫的工作室",
            "display_order": 7,
            "label_suffix": "hafu_workshop",
            "description": "堆满电力设备和工具的工作间。",
            "background": "bg/hafu_workshop.jpg",
            "bgm": "bgm_investigation.ogg",
            "map_pos": (800, 330),
            "map_icon": "workshop",
            "hotspots": {
                "工具台": {
                    "description": "各种电工工具整齐摆放。",
                    "clues": [],
                    "unlocked": True
                },
                "电路图": {
                    "description": "小镇的电力线路图。",
                    "clues": ["电力线路图"],
                    "unlocked": True
                },
                "维修记录": {
                    "description": "记录了最近的维修工作。",
                    "clues": ["停电记录"],
                    "unlocked": True
                }
            },
            "characters": ["哈夫"],
            "available_times": ["morning", "afternoon", "evening"],
            "unlocked": True,
            "visited": False
        },

        "博莱斯住所": {
            "name": "管道工博莱斯的家",
            "display_order": 8,
            "label_suffix": "bolai_house",
            "description": "简单的居所，靠近地下管道入口。",
            "background": "bg/bolai_house.jpg",
            "bgm": "bgm_investigation.ogg",
            "map_pos": (980, 120),
            "map_icon": "house",
            "hotspots": {
                "管道图纸": {
                    "description": "小镇地下管道的设计图。",
                    "clues": ["管道布局图"],
                    "unlocked": True
                },
                "工作日志": {
                    "description": "记录管道维修工作的日志。",
                    "clues": ["伪造维修记录"],
                    "unlocked": False,
                    "unlock_condition": "bolai_confronted"
                }
            },
            "characters": ["博莱斯"],
            "available_times": ["evening", "night"],
            "unlocked": True,
            "visited": False
        },

        "伊蕾娜公寓": {
            "name": "伊蕾娜的公寓",
            "display_order": 9,
            "label_suffix": "ileina_apartment",
            "description": "租金低廉的小公寓，陈设简单。",
            "background": "bg/ileina_apartment.jpg",
            "bgm": "bgm_investigation.ogg",
            "map_pos": (1350, 460),
            "map_icon": "house",
            "hotspots": {
                "窗户": {
                    "description": "面向小镇广场的窗户，视野很好。",
                    "clues": ["目击视角"],
                    "unlocked": True
                },
                "日记": {
                    "description": "伊蕾娜的私人日记。",
                    "clues": ["伊蕾娜日记"],
                    "unlocked": False,
                    "unlock_condition": "ileina_trust_high"
                }
            },
            "characters": ["伊蕾娜"],
            "available_times": ["afternoon", "evening", "night"],
            "unlocked": True,
            "visited": False
        },

        "小镇广场": {
            "name": "布恰小镇广场",
            "display_order": 10,
            "label_suffix": "town_square",
            "description": "小镇的中心区域，居民们的聚集地。",
            "background": "bg/town_square.jpg",
            "bgm": "bgm_town.ogg",
            "map_pos": None,
            "map_icon": "square",
            "hotspots": {
                "长椅": {
                    "description": "广场上的长椅，可以观察人来人往。",
                    "clues": [],
                    "unlocked": True
                },
                "公告栏": {
                    "description": "张贴各种通知的地方。",
                    "clues": ["小镇公告"],
                    "unlocked": True
                },
                "喷泉": {
                    "description": "已经停用的老喷泉。",
                    "clues": [],
                    "unlocked": True
                }
            },
            "characters": [],  # 随机遇到角色
            "available_times": ["morning", "afternoon", "evening"],
            "unlocked": True,
            "visited": False
        }
    }

    ## 地点默认解锁状态快照（用于周目重置）
    default_location_unlocks = {}
    for loc_name, loc_data in locations_database.items():
        default_location_unlocks[loc_name] = loc_data.get("unlocked", False)

    ## 当前所在地点
    current_location = None

    ## 获取地点信息
    def get_location_info(location_name):
        if location_name in locations_database:
            return locations_database[location_name]
        return None

    ## 重置地点解锁状态（周目初始化用）
    def reset_locations_unlock_state():
        for loc_name, default_unlocked in default_location_unlocks.items():
            if loc_name in locations_database:
                locations_database[loc_name]["unlocked"] = default_unlocked
        persistent.unlocked_locations = []

    ## 检查地点是否解锁
    def is_location_unlocked(location_name):
        location = get_location_info(location_name)
        if not location:
            return False

        # 如果地点本身已解锁，返回True
        if location.get("unlocked", False):
            return True

        # 检查解锁条件
        unlock_condition = location.get("unlock_condition", None)
        if unlock_condition:
            return check_unlock_condition(unlock_condition)

        return False

    ## 解锁条件映射表（新增条件只需添加映射）
    unlock_condition_checks = {
        "day3_after": lambda: current_day >= 3,
        "molorava_trust_high": lambda: get_character_trust("莫洛拉瓦") >= 60,
        "telina_trust_high": lambda: get_character_trust("特莉娜") >= 60,
        "badebiete_trust_high": lambda: get_character_trust("巴德别特") >= 60,
        "ileina_trust_high": lambda: get_character_trust("伊蕾娜") >= 60,
        "bolai_confronted": lambda: persistent.bolai_confronted if hasattr(persistent, 'bolai_confronted') else False,
        "password_found": lambda: persistent.safe_password_found if hasattr(persistent, 'safe_password_found') else False
    }

    ## 检查解锁条件
    def check_unlock_condition(condition):
        checker = unlock_condition_checks.get(condition)
        if not checker:
            return False
        return checker()

    ## 检查热点是否解锁
    def is_hotspot_unlocked(location_name, hotspot_name):
        location = get_location_info(location_name)
        if not location:
            return False

        hotspot = location.get("hotspots", {}).get(hotspot_name, None)
        if not hotspot:
            return False

        # 如果热点本身已解锁，返回True
        if hotspot.get("unlocked", False):
            return True

        # 检查解锁条件
        unlock_condition = hotspot.get("unlock_condition", None)
        if unlock_condition:
            return check_unlock_condition(unlock_condition)

        return False

    ## 检查地点在当前时段是否可访问
    def is_location_available(location_name):
        location = get_location_info(location_name)
        if not location:
            return False

        available_times = location.get("available_times", [])
        return current_time in available_times

    ## 标记地点为已访问（持久化存储）
    def set_location_visited(location_name):
        if location_name in locations_database:
            ## 使用持久化存储
            if location_name not in persistent.visited_locations:
                persistent.visited_locations.append(location_name)

    ## 检查地点是否已访问
    def is_location_visited(location_name):
        return location_name in persistent.visited_locations

    ## 获取地点的角色列表
    def get_location_characters(location_name):
        location = get_location_info(location_name)
        if not location:
            return []
        return location.get("characters", [])

    ## 角色对话标签映射
    character_talk_labels = {
        "罗琳达": "talk_to_rolinda_scene1",
        "叶蒂娜": "talk_to_yedina_scene1",
        "巴德别特": "talk_to_badebiete_scene1",
        "特莉娜": "talk_to_telina_scene1",
        "哈夫": "talk_to_hafu_scene1",
        "博莱斯": "talk_to_bolai_scene1",
        "伊蕾娜": "talk_to_ileina_scene1"
    }

    def get_character_talk_label(char_name):
        """获取角色对话label，未配置返回None"""
        return character_talk_labels.get(char_name)

    def get_hotspot_label(location_name, hotspot_name):
        """获取热点label，未配置返回None"""
        location = get_location_info(location_name)
        if not location:
            return None
        hotspot = location.get("hotspots", {}).get(hotspot_name, None)
        if not hotspot:
            return None
        return hotspot.get("label")

    def get_hotspot_info(location_name, hotspot_name):
        """获取热点完整数据，未配置返回None"""
        location = get_location_info(location_name)
        if not location:
            return None
        return location.get("hotspots", {}).get(hotspot_name, None)

    def run_hotspot_special_action(action_name):
        """
        执行热点特殊动作

        Args:
            action_name: 特殊动作名称

        Returns:
            bool: 是否成功执行
        """
        if action_name == "restore_sanity":
            if hasattr(renpy.store, "set_sanity"):
                renpy.store.set_sanity(100)
            else:
                persistent.sanity = 100
                renpy.notify("精神值已恢复")
            return True
        return False

    ## 获取所有已解锁的地点列表
    def get_unlocked_locations():
        unlocked = []
        for loc_name in locations_database:
            if is_location_unlocked(loc_name):
                unlocked.append(loc_name)
        return unlocked

    ## ========================================
    ## 地图系统API
    ## ========================================

    def get_current_location():
        """获取当前所在地点"""
        return current_location

    def set_current_location(location_name):
        """设置当前所在地点"""
        global current_location
        if location_name in locations_database or location_name is None:
            current_location = location_name
            return True
        return False

    def get_location_map_pos(location_name):
        """获取地点的地图坐标"""
        location = get_location_info(location_name)
        if location:
            return location.get("map_pos", None)
        return None

    def get_all_map_locations():
        """获取所有有地图坐标的地点"""
        result = []
        for loc_name, loc_data in locations_database.items():
            if loc_data.get("map_pos"):
                result.append({
                    "name": loc_name,
                    "display_name": loc_data.get("name", loc_name),
                    "pos": loc_data["map_pos"],
                    "icon": loc_data.get("map_icon", "default"),
                    "unlocked": is_location_unlocked(loc_name),
                    "available": is_location_available(loc_name),
                    "visited": is_location_visited(loc_name)  ## 使用持久化检查
                })
        return result

    def travel_to_location(location_name):
        """
        前往指定地点（消耗行动点）

        Returns:
            bool: 是否成功前往
        """
        if not is_location_unlocked(location_name):
            renpy.notify("该地点尚未解锁")
            return False

        if not is_location_available(location_name):
            renpy.notify("当前时段无法前往该地点")
            return False

        if not has_action_points():
            renpy.notify("行动点不足")
            return False

        # 消耗行动点
        use_action_point()
        # 设置当前位置
        set_current_location(location_name)
        # 标记已访问
        set_location_visited(location_name)

        return True

    def get_visited_locations():
        """获取所有已访问的地点（从持久化存储读取）"""
        return persistent.visited_locations[:]  ## 返回副本避免直接修改

    ## ========================================
    ## 地点解锁API（带弹窗通知）
    ## ========================================

    def unlock_location(location_name):
        """
        解锁指定地点并显示弹窗通知

        Args:
            location_name: 地点名称

        Returns:
            bool: True=新解锁, False=已解锁或地点不存在
        """
        if location_name not in locations_database:
            renpy.log("错误：尝试解锁不存在的地点 - '{}'".format(location_name))
            return False

        ## 检查是否已经解锁过（使用持久化存储）
        if location_name in persistent.unlocked_locations:
            return False  ## 已经解锁过

        ## 设置地点为解锁状态
        locations_database[location_name]["unlocked"] = True

        ## 添加到持久化解锁列表
        persistent.unlocked_locations.append(location_name)

        ## 显示弹窗通知
        display_name = locations_database[location_name].get("name", location_name)
        if hasattr(renpy.store, "popup_location"):
            renpy.store.popup_location(display_name)
        else:
            renpy.notify("新地点已解锁：" + display_name)

        return True

    def is_location_first_unlock(location_name):
        """
        检查地点是否已被解锁过（持久化）

        Args:
            location_name: 地点名称

        Returns:
            bool: True=已解锁过
        """
        return location_name in persistent.unlocked_locations

    def get_unlocked_location_count():
        """
        获取已解锁地点数量

        Returns:
            int: 已解锁地点数量
        """
        return len(persistent.unlocked_locations)

    ## ========================================
    ## 地图移动API（带场景跳转）
    ## ========================================

    def get_location_label(location_name):
        """
        获取地点对应的visit label名称

        Args:
            location_name: 地点名称

        Returns:
            str: label名称（如 "visit_rolinda_house"），地点不存在返回None
        """
        loc_data = locations_database.get(location_name)
        if loc_data:
            label_suffix = loc_data.get("label_suffix", "")
            if label_suffix:
                return "visit_" + label_suffix
        return None

    def do_travel_to_location(location_name):
        """
        前往指定地点并跳转到场景（从地图UI调用）

        这个函数会：
        1. 调用 travel_to_location() 检查条件并消耗行动点
        2. 如果成功，关闭笔记本界面
        3. 跳转到对应的 visit_* 场景

        Args:
            location_name: 地点名称

        Returns:
            无返回值（成功时会跳转场景）
        """
        ## 先确认地点场景可用，避免消耗行动点后无处可去
        target_label = get_location_label(location_name)
        if not target_label:
            renpy.notify("错误：找不到地点场景")
            return

        if not renpy.has_label(target_label):
            renpy.notify("该地点场景尚未实现")
            return

        ## 调用 travel_to_location 检查条件并消耗行动点
        if not travel_to_location(location_name):
            ## 失败时 travel_to_location 已经显示了提示
            return

        ## 关闭相关界面并清理选择状态
        store.map_selected_location = None
        renpy.hide_screen("notebook")
        renpy.hide_screen("visual_map")
        renpy.hide_screen("map_screen")

        ## 跳转到地点场景
        renpy.jump(target_label)

    def prepare_map_travel(location_name):
        """
        准备地图移动（设置目标地点变量）
        配合 Jump("process_map_travel") 使用

        Args:
            location_name: 目标地点名称
        """
        store.map_target_location = location_name

## 地图和地点探索UI已移至 game/ui/locations.rpy
## 保持数据层和UI层分离

## ============================================================================
## 地图移动处理 Label
## ============================================================================

label process_map_travel:
    ## 处理从地图UI发起的位置移动
    ## 由 prepare_map_travel() + Jump("process_map_travel") 触发

    ## 检查目标地点是否设置
    if map_target_location is None:
        $ renpy.notify("错误：未指定目标地点")
        return

    ## 获取目标 label
    $ target_label = get_location_label(map_target_location)

    if target_label is None:
        $ renpy.notify("错误：找不到地点场景")
        $ map_target_location = None
        return

    ## 检查 label 是否存在
    if not renpy.has_label(target_label):
        $ renpy.notify("该地点场景尚未实现")
        $ map_target_location = None
        return

    ## 调用 travel_to_location 检查条件并消耗行动点
    $ travel_success = travel_to_location(map_target_location)

    if not travel_success:
        ## 失败时 travel_to_location 已经显示了提示
        $ map_target_location = None
        return

    ## 清理变量
    $ map_target_location = None

    ## 跳转到目标场景
    jump expression target_label
