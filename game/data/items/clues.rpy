## 线索系统 - 证据与证词收集

## 线索数据库
init python:
    clues_database = {
        ## 物证类线索
        "打火机": {
            "id": "lighter",
            "name": "打火机",
            "type": "物证",
            "description": "在火灾现场附近发现的打火机。",
            "detail": "一个普通的金属打火机，表面有使用痕迹。打火机底部刻有字母'M'。这可能是纵火者留下的关键证据。",
            "location": "安德莉娅住所",
            "day_found": 3,
            "relates_to": ["莫洛拉瓦", "安德莉娅"],
            "contradicts": ["莫洛拉瓦不吸烟证词"],
            "image": "clue/lighter.png",
            "importance": "high"
        },

        "安德莉娅尸检报告": {
            "id": "autopsy_report",
            "name": "安德莉娅尸检报告",
            "type": "档案",
            "description": "叶蒂娜完成的尸检报告。",
            "detail": "死因：烟雾吸入导致窒息死亡。死亡时间：Day 3凌晨2:30-3:00之间。体内检测出异常药物残留，但报告中未详细说明。",
            "location": "叶蒂娜诊所",
            "day_found": 3,
            "relates_to": ["安德莉娅", "叶蒂娜"],
            "contradicts": [],
            "image": "clue/autopsy_report.png",
            "importance": "critical"
        },

        "火灾现场照片": {
            "id": "fire_scene_photo",
            "name": "火灾现场照片",
            "type": "物证",
            "description": "火灾后的现场照片。",
            "detail": "房屋内部严重烧毁，起火点似乎在窗户附近。窗户玻璃从外侧破碎，暗示有人从外部扔入燃烧物。",
            "location": "安德莉娅住所",
            "day_found": 3,
            "relates_to": ["安德莉娅"],
            "contradicts": ["安德莉娅自杀说"],
            "image": "clue/fire_scene.png",
            "importance": "high"
        },

        "破门痕迹": {
            "id": "door_marks",
            "name": "破门痕迹",
            "type": "物证",
            "description": "安德莉娅住所门锁的异常痕迹。",
            "detail": "门锁有被撬动的痕迹，但不明显。似乎有人试图从外部打开门锁，但最终使用了其他方法进入。",
            "location": "安德莉娅住所",
            "day_found": 3,
            "relates_to": ["安德莉娅"],
            "contradicts": [],
            "image": "clue/door_marks.png",
            "importance": "medium"
        },

        "窗户痕迹": {
            "id": "window_marks",
            "name": "窗户痕迹",
            "type": "物证",
            "description": "火灾现场窗户的破碎痕迹。",
            "detail": "窗户玻璃碎片散落在房间内侧，说明玻璃是从外向内破碎的。这与有人从外部投掷燃烧物的推测一致。",
            "location": "安德莉娅住所",
            "day_found": 3,
            "relates_to": ["安德莉娅"],
            "contradicts": ["内部起火说"],
            "image": "clue/window_marks.png",
            "importance": "high"
        },

        "药品清单": {
            "id": "medicine_list",
            "name": "药品清单",
            "type": "档案",
            "description": "诊所的药品进货清单。",
            "detail": "清单中记录了大量镇静剂和精神类药物的采购。采购量远超小镇人口的正常需求。供应商标注为'联邦药厂'。",
            "location": "叶蒂娜诊所",
            "day_found": 1,
            "relates_to": ["叶蒂娜", "罗琳达"],
            "contradicts": [],
            "image": "clue/medicine_list.png",
            "importance": "critical"
        },

        "政府文件": {
            "id": "government_files",
            "name": "政府文件",
            "type": "档案",
            "description": "罗琳达办公桌上的政府文件。",
            "detail": "标题为'社区健康监测项目'的官方文件。文件中提到定期向居民提供'健康补充剂'，但未说明具体成分。",
            "location": "罗琳达宅邸",
            "day_found": 1,
            "relates_to": ["罗琳达"],
            "contradicts": [],
            "image": "clue/government_files.png",
            "importance": "critical"
        },

        "药厂资料": {
            "id": "pharma_data",
            "name": "药厂资料",
            "type": "档案",
            "description": "保险柜中的药厂机密资料。",
            "detail": "详细记录了LSD药物实验的计划。目标是测试精神控制药物在小规模社区中的效果。布恰小镇被选为实验点。",
            "location": "罗琳达宅邸",
            "day_found": 0,  # 需要解锁保险柜
            "relates_to": ["罗琳达", "叶蒂娜"],
            "contradicts": ["健康监测说"],
            "image": "clue/pharma_data.png",
            "importance": "critical"
        },

        "居民档案": {
            "id": "resident_files",
            "name": "居民档案",
            "type": "档案",
            "description": "社区中心的居民档案。",
            "detail": "记录了小镇所有居民的基本信息。安德莉娅的档案标注为'特殊监测对象'，茨贝拉的档案则标注为'实验对象-主要'。",
            "location": "社区中心",
            "day_found": 1,
            "relates_to": ["特莉娜", "安德莉娅", "茨贝拉"],
            "contradicts": [],
            "image": "clue/resident_files.png",
            "importance": "critical"
        },

        "社区通知": {
            "id": "community_notice",
            "name": "社区通知",
            "type": "档案",
            "description": "社区中心公告栏上的通知。",
            "detail": "通知居民定期领取'健康补充剂'。强调这是联邦政府的福利项目，所有居民必须按时服用。",
            "location": "社区中心",
            "day_found": 1,
            "relates_to": ["罗琳达", "特莉娜"],
            "contradicts": [],
            "image": "clue/community_notice.png",
            "importance": "medium"
        },

        "药厂谈判资料": {
            "id": "negotiation_files",
            "name": "药厂谈判资料",
            "type": "档案",
            "description": "特莉娜暗中收集的资料。",
            "detail": "特莉娜收集的药厂机密文件副本。她打算用这些资料与罗琳达谈判，作为进入市区工作的筹码。",
            "location": "社区中心",
            "day_found": 0,  # 需要高信任度
            "relates_to": ["特莉娜", "罗琳达"],
            "contradicts": [],
            "image": "clue/negotiation_files.png",
            "importance": "high"
        },

        "警务笔记": {
            "id": "police_notes",
            "name": "警务笔记",
            "type": "档案",
            "description": "巴德别特的警务笔记。",
            "detail": "记录了巴德别特在国家警察期间参与的'特殊搜寻任务'。任务内容是抓捕流浪汉和醉酒者，交付给'研究所'。",
            "location": "巴德别特住所",
            "day_found": 1,
            "relates_to": ["巴德别特"],
            "contradicts": [],
            "image": "clue/police_notes.png",
            "importance": "high"
        },

        "实验对象名单": {
            "id": "subject_list",
            "name": "实验对象名单",
            "type": "档案",
            "description": "实验对象的详细名单。",
            "detail": "巴德别特保存的机密名单。记录了数十名'实验对象'的姓名和下落。安德莉娅和茨贝拉都在名单上，标注为'战俘来源'。",
            "location": "巴德别特住所",
            "day_found": 0,  # 需要高信任度
            "relates_to": ["巴德别特", "安德莉娅", "茨贝拉"],
            "contradicts": [],
            "image": "clue/subject_list.png",
            "importance": "critical"
        },

        "电力线路图": {
            "id": "power_map",
            "name": "电力线路图",
            "type": "档案",
            "description": "小镇的电力线路图。",
            "detail": "详细标注了小镇的电力系统布局。安德莉娅住所的电力线路在Day 3凌晨被人为切断。",
            "location": "哈夫工作室",
            "day_found": 3,
            "relates_to": ["哈夫", "安德莉娅"],
            "contradicts": [],
            "image": "clue/power_map.png",
            "importance": "high"
        },

        "停电记录": {
            "id": "blackout_record",
            "name": "停电记录",
            "type": "档案",
            "description": "最近的停电维修记录。",
            "detail": "Day 3凌晨2:00，安德莉娅住所片区发生'线路故障'。哈夫的记录显示这是一次'例行维护'，但时间非常可疑。",
            "location": "哈夫工作室",
            "day_found": 3,
            "relates_to": ["哈夫", "安德莉娅"],
            "contradicts": ["例行维护说"],
            "image": "clue/blackout_record.png",
            "importance": "critical"
        },

        "管道布局图": {
            "id": "pipe_map",
            "name": "管道布局图",
            "type": "档案",
            "description": "小镇地下管道的设计图。",
            "detail": "显示了小镇完整的地下管道系统。某些管道可以用作秘密通道，连接不同的建筑物。",
            "location": "博莱斯住所",
            "day_found": 1,
            "relates_to": ["博莱斯"],
            "contradicts": [],
            "image": "clue/pipe_map.png",
            "importance": "medium"
        },

        "伪造维修记录": {
            "id": "fake_maintenance",
            "name": "伪造维修记录",
            "type": "档案",
            "description": "博莱斯伪造的维修记录。",
            "detail": "博莱斯承认受人指使，伪造了某些日期的管道维修记录。这些记录可以为某些人提供不在场证明。",
            "location": "博莱斯住所",
            "day_found": 0,  # 需要对质
            "relates_to": ["博莱斯", "罗琳达"],
            "contradicts": ["维修时间线"],
            "image": "clue/fake_maintenance.png",
            "importance": "high"
        },

        "伊蕾娜日记": {
            "id": "ileina_diary",
            "name": "伊蕾娜日记",
            "type": "证词",
            "description": "伊蕾娜的私人日记。",
            "detail": "日记中记录了伊蕾娜对小镇的观察。她多次提到'那个女人（罗琳达）很可怕'，以及'我必须听她的话，否则...'",
            "location": "伊蕾娜公寓",
            "day_found": 0,  # 需要高信任度
            "relates_to": ["伊蕾娜", "罗琳达"],
            "contradicts": [],
            "image": "clue/ileina_diary.png",
            "importance": "high"
        },

        "目击视角": {
            "id": "witness_view",
            "name": "目击视角",
            "type": "证词",
            "description": "从伊蕾娜公寓窗户看到的视角。",
            "detail": "伊蕾娜的窗户正对小镇广场，可以看到大部分居民的活动。她可能目击了关键事件，但需要信任才会说出真相。",
            "location": "伊蕾娜公寓",
            "day_found": 1,
            "relates_to": ["伊蕾娜"],
            "contradicts": [],
            "image": "clue/witness_view.png",
            "importance": "high"
        },

        "避难所记录": {
            "id": "shelter_record",
            "name": "避难所记录",
            "type": "档案",
            "description": "教堂地窖避难所的使用记录。",
            "detail": "战争期间的避难所使用记录。记录显示莫洛拉瓦曾在战线缓冲区提供庇护，但他极力否认这段经历。",
            "location": "教堂",
            "day_found": 0,  # 需要高信任度
            "relates_to": ["莫洛拉瓦"],
            "contradicts": ["莫洛拉瓦的隐瞒"],
            "image": "clue/shelter_record.png",
            "importance": "medium"
        },

        "小镇公告": {
            "id": "town_notice",
            "name": "小镇公告",
            "type": "档案",
            "description": "广场公告栏上的通知。",
            "detail": "通知居民遵守宵禁时间，夜间不要外出。同时提醒定期领取'健康补充剂'。",
            "location": "小镇广场",
            "day_found": 1,
            "relates_to": [],
            "contradicts": [],
            "image": "clue/town_notice.png",
            "importance": "low"
        }
    }

    ## 已发现的线索列表（初始化已移至init_persistent.rpy）

    def resolve_clue_key(clue_id):
        """
        解析线索键名（支持中文名称或英文ID）

        Args:
            clue_id: 线索ID（中文名称或英文ID）

        Returns:
            str or None: 线索键名
        """
        if clue_id in clues_database:
            return clue_id
        for key, clue in clues_database.items():
            if clue.get("id") == clue_id:
                return key
        return None

    ## 发现线索
    def discover_clue(clue_id):
        """
        发现线索并添加到已发现列表

        Args:
            clue_id: 线索ID（中文名称或英文ID）

        Returns:
            True: 新发现的线索
            False: 已发现过或ID无效
        """
        # 检查线索ID是否存在
        clue_key = resolve_clue_key(clue_id)
        if not clue_key:
            renpy.log(f"警告：尝试发现不存在的线索ID '{clue_id}'")
            return False

        # 检查是否已发现过
        if clue_key in persistent.discovered_clues:
            return False  # 已发现过

        # 添加到已发现列表
        persistent.discovered_clues.append(clue_key)

        # 显示弹窗通知
        clue_name = clues_database[clue_key]["name"]
        if 'popup_clue' in dir():
            popup_clue(clue_name)
        else:
            renpy.notify(f"发现新线索：{clue_name}")

        return True  # 新发现

    ## 检查线索是否已发现
    def is_clue_discovered(clue_id):
        clue_key = resolve_clue_key(clue_id)
        if not clue_key:
            return False
        return clue_key in persistent.discovered_clues

    ## 获取线索信息
    def get_clue_info(clue_id):
        clue_key = resolve_clue_key(clue_id)
        if clue_key:
            return clues_database[clue_key]
        return None

    ## 获取所有已发现的线索
    def get_discovered_clues():
        discovered = []
        for clue_id in persistent.discovered_clues:
            if clue_id in clues_database:
                discovered.append(clues_database[clue_id])
        return discovered

    ## 按类型获取线索
    def get_clues_by_type(clue_type):
        result = []
        for clue_id in persistent.discovered_clues:
            if clue_id in clues_database:
                clue = clues_database[clue_id]
                if clue.get("type") == clue_type:
                    result.append(clue)
        return result

    ## 获取与角色相关的线索
    def get_clues_related_to(character_name):
        result = []
        for clue_id in persistent.discovered_clues:
            if clue_id in clues_database:
                clue = clues_database[clue_id]
                if character_name in clue.get("relates_to", []):
                    result.append(clue)
        return result

    ## 检查两个线索是否矛盾
    def check_clues_contradiction(clue_id1, clue_id2):
        clue1 = get_clue_info(clue_id1)
        clue2 = get_clue_info(clue_id2)

        if clue1 and clue2:
            # 检查clue1是否与clue2的名称矛盾
            if clue2.get("name") in clue1.get("contradicts", []):
                return True
            # 检查clue2是否与clue1的名称矛盾
            if clue1.get("name") in clue2.get("contradicts", []):
                return True

        return False

    ## 获取线索完成度百分比
    def get_clue_completion():
        total = len(clues_database)
        discovered = len(persistent.discovered_clues)
        return int((discovered / total) * 100) if total > 0 else 0

## 线索簿UI已移至 game/ui/clues.rpy
## 保持数据层和UI层分离
