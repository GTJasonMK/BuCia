## 角色定义文件 - 布恰小镇的居民

## 定义角色（用于对话）
define narrator = Character(None, what_color="#ffffff")
define tsibela = Character("茨贝拉", color="#ffffff", image="tsibela")
define rolinda = Character("罗琳达", color="#cc0000", image="rolinda")
define yedina = Character("叶蒂娜", color="#66cc66", image="yedina")
define andrea = Character("安德里娅", color="#8888ff", image="andrea")
define telina = Character("特莉娜", color="#ffaa00", image="telina")
define molorava = Character("莫洛拉瓦", color="#aa88ff", image="molorava")
define badebiete = Character("巴德别特", color="#888888", image="badebiete")
define hafu = Character("哈夫", color="#ffcc66", image="hafu")
define bolai = Character("博莱斯", color="#996633", image="bolai")
define ileina = Character("伊雷娜", color="#ff88aa", image="ileina")
define najezhida = Character("娜杰日达", color="#00ccff", image="najezhida")
define azov = Character("审判亚速", color="#ff0000", image="azov")

## 角色数据库（存储角色信息）
init python:
    character_database = {
        "茨贝拉": {
            "full_name": "茨贝拉",
            "role": "失忆的主角",
            "faction": "主角",
            "trust": 0,  # 自己对自己的信任（精神值相关）
            "alive": True,
            "sprite": "tsibela",
            "color": "#ffffff",
            "bio": "曾作为顿巴斯民兵，以失忆状态出现于布恰镇。身上只有刻有姓名的军牌。",
            "secrets": ["顿涅茨克人民军第114旅", "北顿涅茨克战役幸存者", "真正的凶手（三周目揭示）"],
            "background": "隶属于顿涅茨克人民军第114旅，活跃于马里乌波尔地区。后被派遣至北顿涅茨克-利西昌斯克战役，以突击班组班长身份负责袭扰阻滞。班组转移过程中收编了安德里娅，以班组全灭代价完成任务后被俘。",
            "first_meet": True
        },
        "罗琳达": {
            "full_name": "罗琳达",
            "role": "小镇话事人",
            "faction": "主谋",
            "trust": 50,
            "alive": True,
            "sprite": "rolinda",
            "color": "#cc0000",
            "bio": "布查小镇的实际管理者，拥有极高威望。以联邦政府社区管理负责人身份进入小镇。",
            "secrets": ["CIA特工", "LSD项目监督者", "伪书创作者（审判层）"],
            "background": "中情局特勤干员，负责监督LSD精神控制项目推进。在伪书层将侦探权交给茨贝拉，在审判层可指挥审判亚速。",
            "first_meet": False
        },
        "叶蒂娜": {
            "full_name": "叶蒂娜",
            "role": "医生/科研职员",
            "faction": "被迫共谋",
            "trust": 30,
            "alive": True,
            "sprite": "yedina",
            "color": "#66cc66",
            "bio": "布查小镇原住民，药厂派遣的科研职员。对LSD项目认知被限制在'社区健康监测'范畴。",
            "secrets": ["知道药物来源", "被要求隐瞒尸检报告细节", "私下溯源调查"],
            "background": "药厂特派职员，协助罗琳达工作。为罗琳达处理慢性胃病，承担小镇基础医疗。安德里娅死后负责尸检，被要求隐瞒药物残留信息。",
            "first_meet": False
        },
        "安德里娅": {
            "full_name": "安德里娅",
            "role": "第一受害者",
            "faction": "受害者",
            "trust": 0,
            "alive": False,  # Day 3凌晨死亡
            "sprite": "andrea",
            "color": "#8888ff",
            "bio": "前顿巴斯民兵，卢甘斯克人民军黎明营成员。因外貌特征和'应激性戒备凝视'被镇上居民排斥。",
            "secrets": ["过量药物实验对象", "与茨贝拉曾是战友"],
            "background": "曾参加北顿涅茨克-利西昌斯克战役，班组全歼后被俘。转交给CIA后被安排至布查镇作为过量药物实验对象。第3天凌晨房屋被纵火，死于火场。",
            "first_meet": False
        },
        "特莉娜": {
            "full_name": "特莉娜",
            "role": "社区负责人",
            "faction": "共谋者",
            "trust": 40,
            "alive": True,
            "sprite": "telina",
            "color": "#ffaa00",
            "bio": "布恰小镇社区负责人。野心勃勃，希望进入市区生活并获得更好的工作。",
            "secrets": ["收集药厂资料作为谈判筹码", "协助伪造证据"],
            "background": "不满足于社区负责人职位，察觉'健康监测'异常。暗中收集药厂资料想与罗琳达谈判，作为进入市区的政治筹码。",
            "first_meet": False
        },
        "莫洛拉瓦": {
            "full_name": "莫洛拉瓦",
            "role": "神父",
            "faction": "一周目被陷害者",
            "trust": 20,
            "alive": True,
            "sprite": "molorava",
            "color": "#aa88ff",
            "bio": "曾在战线缓冲区教会担任神职人员。害怕被清算，逃离原城市隐居于布查小镇。",
            "secrets": ["隐瞒顿巴斯经历", "害怕亚速营清算", "误以为安德里娅是亚速分子"],
            "background": "战争期间教堂地窖改造成避难所，害怕承担'分离主义支持者'罪名。假借探病逃离，在布查小镇居住，日常乘城郊巴士上下班。",
            "first_meet": False
        },
        "巴德别特": {
            "full_name": "巴德别特",
            "role": "退休警员",
            "faction": "赎罪者",
            "trust": 60,
            "alive": False,  # Day 4夜失踪/死亡
            "sprite": "badebiete",
            "color": "#888888",
            "bio": "前国家警察，主动申请调至领土社区警察。退休后居住于布查小镇。",
            "secrets": ["曾参与抓捕实验对象", "知道药物实验内情", "试图拯救居民被灭口"],
            "background": "国家警察期间多次签下实验对象搜寻任务，抓捕流浪汉/醉酒者交付研究所获取奖金。得知实验细节后被罪恶感压垮，申请调离逃避罪恶。第4天夜试图联系旧下属放行居民被灭口。",
            "first_meet": False
        },
        "哈夫": {
            "full_name": "哈夫",
            "role": "电工",
            "faction": "一周目被陷害者",
            "trust": 30,
            "alive": True,
            "sprite": "hafu",
            "color": "#ffcc66",
            "bio": "电力公司技术人员，市政紧急抢修队成员。战后PTSD，在布查小镇休养。",
            "secrets": ["掌控电力系统", "战后恐惧症", "可能被利用制造监控空窗"],
            "background": "战争期间负责市中心电网恢复，轰炸区心理创伤导致恐惧症。为休养来到布查小镇当社区电力修理工。",
            "first_meet": False
        },
        "博莱斯": {
            "full_name": "博莱斯",
            "role": "管道工",
            "faction": "共谋者",
            "trust": 35,
            "alive": True,
            "sprite": "bolai",
            "color": "#996633",
            "bio": "曾居住市区，收入微薄。负责城郊地下管道翻新项目后定居布查小镇。",
            "secrets": ["可控制管道/检修记录", "伪造维修记录", "为金钱被收买"],
            "background": "因收入微薄难以维持市区生活，被调至城郊管道翻新项目。完成布查小镇给水管网改造后，被低廉租金吸引定居。",
            "first_meet": False
        },
        "伊雷娜": {
            "full_name": "伊雷娜",
            "role": "少女",
            "faction": "脆弱证人",
            "trust": 25,
            "alive": True,
            "sprite": "ileina",
            "color": "#ff88aa",
            "bio": "刚成年的青少女，脱离原生家庭独自生活。曾遭受家暴，极度缺乏安全感。",
            "secrets": ["易被操纵", "可被包装成'脆弱目击'", "渴望庇护"],
            "background": "因房租低廉留在布查小镇。家暴经历导致极度缺乏安全感，容易被威胁或利诱提供虚假证词。",
            "first_meet": False
        },
        "娜杰日达": {
            "full_name": "娜杰日达",
            "role": "AI助手/场务",
            "faction": "上位层",
            "trust": 100,  # 第四周目后
            "alive": True,  # 作为AI不受生死影响
            "sprite": "najezhida",
            "color": "#00ccff",
            "bio": "维护游戏剧本运行的AI角色。目睹玩家被罗琳达剧本逼入绝境后，产生情感决定协助。",
            "secrets": ["知晓所有真相", "可以回溯时间", "第四周目成为玩家盟友"],
            "background": "上位层的AI，负责维护舞台运作。在故事层以引导系统出现，提示回溯/存档操作。周目1-3后的茶会以冰冷口吻点评，周目3后产生情感决定反抗罗琳达。",
            "first_meet": False
        },
        "审判亚速": {
            "full_name": "审判亚速",
            "role": "权威象征",
            "faction": "审判层",
            "trust": 0,  # 无意识的代理
            "alive": True,
            "sprite": "azov",
            "color": "#ff0000",
            "bio": "罗琳达在审判层的代理，骑士形象。象征权威，维持审判秩序。",
            "secrets": ["无自主意识", "听命于罗琳达", "只在线索梳理环节出现"],
            "background": "审判层的具象化存在，罗琳达权能的体现。可对指认的凶手执行逮捕，维持线索梳理过程的秩序。只能被主角和罗琳达所见。",
            "first_meet": False
        }
    }

    ## 角色关系网络（影响对话和线索获取）
    character_relations = {
        "茨贝拉": {
            "安德里娅": "战友",
            "罗琳达": "侦探权授予者",
            "巴德别特": "协助调查"
        },
        "罗琳达": {
            "叶蒂娜": "上下级",
            "特莉娜": "利益交换",
            "审判亚速": "控制者"
        },
        "安德里娅": {
            "茨贝拉": "战友",
            "莫洛拉瓦": "误会（被当作亚速）"
        }
        # 更多关系待补充
    }

    ## 获取角色信任度
    def get_character_trust(char_name):
        """
        获取角色的信任度

        Args:
            char_name: 角色名称

        Returns:
            int: 信任度(0-100)，角色不存在时返回0
        """
        if char_name not in character_database:
            renpy.log(f"警告：尝试获取不存在的角色信任度 - '{char_name}'")
            return 0
        return character_database[char_name]["trust"]

    ## 修改角色信任度
    def modify_character_trust(char_name, amount):
        """
        修改角色信任度

        Args:
            char_name: 角色名称
            amount: 变化量（正数增加，负数减少）

        Returns:
            bool: 是否成功修改
        """
        if char_name not in character_database:
            renpy.log(f"错误：尝试修改不存在的角色信任度 - '{char_name}'")
            return False

        if not isinstance(amount, (int, float)):
            renpy.log(f"错误：信任度变化量必须是数字 - 得到: {type(amount)}")
            return False

        old_trust = character_database[char_name]["trust"]
        character_database[char_name]["trust"] += amount
        character_database[char_name]["trust"] = max(0, min(100, character_database[char_name]["trust"]))
        new_trust = character_database[char_name]["trust"]

        # 显示信任度变化通知（仅当实际发生变化时）
        actual_change = new_trust - old_trust
        if actual_change > 0:
            renpy.notify(f"{char_name}信任度 +{actual_change}")
        elif actual_change < 0:
            renpy.notify(f"{char_name}信任度 {actual_change}")

        return True

    ## 检查角色是否存活
    def is_character_alive(char_name):
        """
        检查角色是否存活

        Args:
            char_name: 角色名称

        Returns:
            bool: 是否存活，角色不存在时返回False
        """
        if char_name not in character_database:
            renpy.log(f"警告：尝试检查不存在的角色存活状态 - '{char_name}'")
            return False
        return character_database[char_name]["alive"]

    ## 标记角色死亡
    def set_character_dead(char_name):
        """
        标记角色为死亡状态

        Args:
            char_name: 角色名称

        Returns:
            bool: 是否成功标记
        """
        if char_name not in character_database:
            renpy.log(f"错误：尝试标记不存在的角色死亡 - '{char_name}'")
            return False

        character_database[char_name]["alive"] = False
        renpy.log(f"角色 '{char_name}' 已标记为死亡")
        return True

    ## 标记角色初次见面（推荐使用 meet_character）
    def set_character_met(char_name):
        """
        标记与角色初次见面
        内部调用 meet_character 以保持一致性

        Args:
            char_name: 角色名称

        Returns:
            bool: 是否成功标记
        """
        ## 调用 meet_character 来处理持久化和弹窗
        return meet_character(char_name)

    ## 检查是否初次见面
    def is_first_meet(char_name):
        """
        检查是否是与角色的初次见面

        Args:
            char_name: 角色名称

        Returns:
            bool: True=初次见面(first_meet=False), False=已经见过(first_meet=True)，角色不存在时返回False
        """
        if char_name not in character_database:
            renpy.log(f"警告：尝试检查不存在的角色见面状态 - '{char_name}'")
            return False
        return not character_database[char_name].get("first_meet", False)

    ## ========================================
    ## 笔记本系统集成API
    ## ========================================

    def meet_character(char_name):
        """
        记录与角色相遇（添加到笔记本人物页）

        Args:
            char_name: 角色名称

        Returns:
            bool: 是否成功添加（首次相遇返回True）
        """
        if char_name not in character_database:
            renpy.log(f"错误：尝试记录与不存在的角色相遇 - '{char_name}'")
            return False

        if char_name not in persistent.met_characters:
            persistent.met_characters.append(char_name)
            character_database[char_name]["first_meet"] = True
            ## 显示弹窗通知
            if 'popup_character' in dir():
                popup_character(char_name)
            else:
                renpy.notify("遇见了 " + char_name)
            return True
        return False

    def has_met_character(char_name):
        """
        检查是否已遇见某角色

        Args:
            char_name: 角色名称

        Returns:
            bool: 是否已遇见
        """
        return char_name in persistent.met_characters

    def get_met_characters():
        """
        获取所有已遇见的角色数据

        Returns:
            list: 角色数据列表
        """
        characters = []
        for char_name in persistent.met_characters:
            char_data = character_database.get(char_name)
            if char_data:
                characters.append(char_data)
        return characters

    def get_character_data(char_name):
        """
        获取角色完整数据

        Args:
            char_name: 角色名称

        Returns:
            dict or None: 角色数据
        """
        return character_database.get(char_name, None)

    def get_all_character_names():
        """
        获取所有角色名称列表

        Returns:
            list: 角色名称列表
        """
        return list(character_database.keys())

    def get_met_character_count():
        """
        获取已遇见角色数量

        Returns:
            int: 已遇见角色数量
        """
        return len(persistent.met_characters)

    def clear_met_characters():
        """
        清除所有已遇见角色记录（仅用于开发测试）
        """
        persistent.met_characters = []
        renpy.notify("已遇见角色记录已清除")
