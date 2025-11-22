## 地点系统 - 布恰小镇地图

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
            "hotspots": {
                "书桌": {
                    "description": "整洁的办公桌，上面摆放着一些文件。",
                    "clues": ["政府文件"],
                    "unlocked": True
                },
                "保险柜": {
                    "description": "墙角的小型保险柜，需要密码。",
                    "clues": ["药厂资料"],
                    "unlocked": False,
                    "unlock_condition": "password_found"
                },
                "窗户": {
                    "description": "可以看到小镇广场的窗户。",
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
            "hotspots": {
                "药柜": {
                    "description": "放满各种药品的柜子，有些标签模糊。",
                    "clues": ["药品清单"],
                    "unlocked": True
                },
                "检查床": {
                    "description": "用于检查病人的病床。",
                    "clues": [],
                    "unlocked": True
                },
                "办公桌": {
                    "description": "叶蒂娜的工作台，散落着一些医疗记录。",
                    "clues": ["安德里娅尸检报告"],
                    "unlocked": False,
                    "unlock_condition": "day3_after"
                }
            },
            "characters": ["叶蒂娜"],
            "available_times": ["morning", "afternoon", "evening"],
            "unlocked": True,
            "visited": False
        },

        "安德里娅住所": {
            "name": "安德里娅的住所",
            "display_order": 3,
            "label_suffix": "andrea_house",
            "description": "小镇边缘的简陋房屋，Day 3凌晨被火灾焚毁。",
            "background": "bg/andrea_house.jpg",
            "bgm": "bgm_dark.ogg",
            "hotspots": {
                "烧毁的床铺": {
                    "description": "火灾后的残骸，能看出曾经的简陋。",
                    "clues": ["火灾现场照片"],
                    "unlocked": False,
                    "unlock_condition": "day3_after"
                },
                "窗户残骸": {
                    "description": "窗框已经完全烧毁。",
                    "clues": ["窗户痕迹"],
                    "unlocked": False,
                    "unlock_condition": "day3_after"
                },
                "门锁": {
                    "description": "门锁似乎有被撬动的痕迹。",
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
            "name": "圣母升天教堂",
            "display_order": 4,
            "label_suffix": "church",
            "description": "小镇的东正教教堂，莫洛拉瓦神父工作的地方。",
            "background": "bg/church.jpg",
            "bgm": "bgm_church.ogg",
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
            "name": "社区管理中心",
            "display_order": 5,
            "label_suffix": "community_center",
            "description": "特莉娜的办公场所，处理小镇日常事务。",
            "background": "bg/community_center.jpg",
            "bgm": "bgm_investigation.ogg",
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

        "伊雷娜公寓": {
            "name": "伊雷娜的公寓",
            "display_order": 9,
            "label_suffix": "ileina_apartment",
            "description": "租金低廉的小公寓，陈设简单。",
            "background": "bg/ileina_apartment.jpg",
            "bgm": "bgm_investigation.ogg",
            "hotspots": {
                "窗户": {
                    "description": "面向小镇广场的窗户，视野很好。",
                    "clues": ["目击视角"],
                    "unlocked": True
                },
                "日记": {
                    "description": "伊雷娜的私人日记。",
                    "clues": ["伊雷娜日记"],
                    "unlocked": False,
                    "unlock_condition": "ileina_trust_high"
                }
            },
            "characters": ["伊雷娜"],
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

    ## 当前所在地点
    current_location = None

    ## 获取地点信息
    def get_location_info(location_name):
        if location_name in locations_database:
            return locations_database[location_name]
        return None

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

    ## 检查解锁条件
    def check_unlock_condition(condition):
        if condition == "day3_after":
            return current_day >= 3
        elif condition == "molorava_trust_high":
            return get_character_trust("莫洛拉瓦") >= 60
        elif condition == "telina_trust_high":
            return get_character_trust("特莉娜") >= 60
        elif condition == "badebiete_trust_high":
            return get_character_trust("巴德别特") >= 60
        elif condition == "ileina_trust_high":
            return get_character_trust("伊雷娜") >= 60
        elif condition == "bolai_confronted":
            return persistent.bolai_confronted if hasattr(persistent, 'bolai_confronted') else False
        elif condition == "password_found":
            return persistent.safe_password_found if hasattr(persistent, 'safe_password_found') else False
        return False

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

    ## 标记地点为已访问
    def set_location_visited(location_name):
        if location_name in locations_database:
            locations_database[location_name]["visited"] = True

    ## 获取地点的角色列表
    def get_location_characters(location_name):
        location = get_location_info(location_name)
        if not location:
            return []
        return location.get("characters", [])

    ## 获取所有已解锁的地点列表
    def get_unlocked_locations():
        unlocked = []
        for loc_name in locations_database:
            if is_location_unlocked(loc_name):
                unlocked.append(loc_name)
        return unlocked

## 地图和地点探索UI已移至 game/ui/locations.rpy
## 保持数据层和UI层分离
