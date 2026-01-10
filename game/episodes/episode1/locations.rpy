# Episode 1 - 地点探索场景
# 所有 visit_* labels
#
# 重要：所有周目共享相同的label名称（不带_ep1后缀）
# 在label内部使用条件判断区分不同周目的内容
#
# 示例：
# label visit_某地点:
#     if current_episode == 1:
#         # 第一周目特有内容
#     elif current_episode == 2:
#         # 第二周目特有内容
#     # 共通内容
#

## 罗琳达宅邸（所有周目共享）
label visit_rolinda_house:
    """
    访问罗琳达的宅邸
    """

    scene bg rolinda_house with dissolve
    play music "bgm_investigation.ogg" fadein 1.0

    "你来到了小镇中最豪华的宅邸。"
    "这里是罗琳达，联邦政府社区管理负责人的住处。"

    # TODO: 添加场景描述和互动

    # 热点调查和角色对话选项
    menu visit_rolinda_house_menu:
        "你想做什么？"

        "调查书桌":
            call investigate_rolinda_house_desk
            jump visit_rolinda_house_menu

        "与罗琳达交谈" if is_character_alive("罗琳达"):
            call talk_to_rolinda_scene1
            jump visit_rolinda_house_menu

        "离开":
            return


## 叶蒂娜诊所（所有周目共享）
label visit_yedina_clinic:
    """
    访问叶蒂娜的诊所
    """

    scene bg yedina_clinic with dissolve
    play music "bgm_investigation.ogg" fadein 1.0

    "你来到了小镇唯一的医疗设施。"
    "叶蒂娜医生正在整理药柜。"

    # TODO: 添加场景内容

    menu visit_yedina_clinic_menu:
        "你想做什么？"

        "调查药柜":
            "药柜中摆放着各种药品..."
            # TODO: 添加调查逻辑
            jump visit_yedina_clinic_menu

        "与叶蒂娜交谈" if is_character_alive("叶蒂娜"):
            "TODO: 对话场景"
            jump visit_yedina_clinic_menu

        "离开":
            return


## 其他地点
## 占位符：确保游戏不会因为缺少label而崩溃
## 待剧情完成后再开发详细内容

label visit_andrea_house:
    """安德里娅的住所 - Day3后可访问（火灾现场）"""

    scene bg room with dissolve
    play music "bgm_dark.ogg" fadein 1.0

    if current_day < 3:
        "安德里娅的住所目前无法进入。"
        return

    "你来到了安德里娅曾经居住的地方。"
    "一场大火已经将这里变成了废墟。"
    "空气中仍然弥漫着焦糊的气味。"

    menu visit_andrea_house_menu:
        "你想调查什么？"

        "调查烧毁的床铺" if is_hotspot_unlocked("安德里娅住所", "烧毁的床铺"):
            "床铺已经完全烧毁，只剩下扭曲的金属框架。"
            "从残骸来看，火势是从床铺附近开始的。"
            $ discover_clue("火灾现场照片")
            jump visit_andrea_house_menu

        "调查窗户残骸" if is_hotspot_unlocked("安德里娅住所", "窗户残骸"):
            "窗框已经完全烧毁。"
            "奇怪的是，窗户似乎是从外面被打破的。"
            $ discover_clue("窗户痕迹")
            jump visit_andrea_house_menu

        "调查门锁" if is_hotspot_unlocked("安德里娅住所", "门锁"):
            "门锁有明显的撬动痕迹。"
            "这说明有人在火灾前强行进入了房间。"
            $ discover_clue("破门痕迹")
            jump visit_andrea_house_menu

        "离开":
            return

## 注意：visit_church 已在 shared/locations/church.rpy 中定义

label visit_community_center:
    """社区管理中心"""

    scene bg room with dissolve
    play music "bgm_investigation.ogg" fadein 1.0

    "你来到了社区管理中心。"
    "这里是特莉娜处理小镇日常事务的地方。"

    menu visit_community_center_menu:
        "你想做什么？"

        "调查档案柜":
            "档案柜中存放着社区居民的各种档案。"
            "有一些关于小镇历史的记录引起了你的注意。"
            $ discover_clue("居民档案")
            jump visit_community_center_menu

        "查看公告板":
            "公告板上张贴着各种社区通知。"
            "大部分是关于日常事务的通告。"
            $ discover_clue("社区通知")
            jump visit_community_center_menu

        "调查特莉娜办公桌" if is_hotspot_unlocked("社区中心", "特莉娜办公桌"):
            "办公桌上有一些关于药厂谈判的资料。"
            "看来小镇正在和某个制药公司进行某种交涉。"
            $ discover_clue("药厂谈判资料")
            jump visit_community_center_menu

        "与特莉娜交谈" if is_character_alive("特莉娜"):
            call talk_to_telina_scene1 from _call_talk_to_telina_scene1
            jump visit_community_center_menu

        "离开":
            return

label visit_badebiete_house:
    """巴德别特的家"""

    scene bg room with dissolve
    play music "bgm_investigation.ogg" fadein 1.0

    "你来到了退休警员巴德别特的住所。"
    "房间整洁而朴素，墙上挂着他警察时代的照片。"

    menu visit_badebiete_house_menu:
        "你想做什么？"

        "查看书架":
            "书架上放满了警务相关的书籍。"
            "有一本笔记本引起了你的注意。"
            $ discover_clue("警务笔记")
            jump visit_badebiete_house_menu

        "查看老照片":
            "墙上挂着巴德别特年轻时的警察照片。"
            "他看起来曾经是个严肃认真的执法者。"
            jump visit_badebiete_house_menu

        "调查抽屉" if is_hotspot_unlocked("巴德别特住所", "抽屉"):
            "抽屉里藏着一份名单。"
            "上面记录着一些人名，旁边标注着奇怪的编号。"
            $ discover_clue("实验对象名单")
            jump visit_badebiete_house_menu

        "与巴德别特交谈" if is_character_alive("巴德别特"):
            call talk_to_badebiete_scene1 from _call_talk_to_badebiete_scene1
            jump visit_badebiete_house_menu

        "离开":
            return

label visit_hafu_workshop:
    """电工哈夫的工作室"""

    scene bg room with dissolve
    play music "bgm_investigation.ogg" fadein 1.0

    "你来到了电工哈夫的工作室。"
    "到处堆满了电力设备和各种工具。"

    menu visit_hafu_workshop_menu:
        "你想做什么？"

        "查看工具台":
            "工具台上摆放着各种电工工具。"
            "哈夫似乎是个很有条理的人。"
            jump visit_hafu_workshop_menu

        "查看电路图":
            "这是小镇的电力线路图。"
            "上面标注了各个区域的供电情况。"
            $ discover_clue("电力线路图")
            jump visit_hafu_workshop_menu

        "查看维修记录":
            "记录本上记载了最近的维修工作。"
            "有一条记录显示火灾当晚曾发生停电。"
            $ discover_clue("停电记录")
            jump visit_hafu_workshop_menu

        "与哈夫交谈" if is_character_alive("哈夫"):
            call talk_to_hafu_scene1 from _call_talk_to_hafu_scene1
            jump visit_hafu_workshop_menu

        "离开":
            return

label visit_bolai_house:
    """管道工博莱斯的家"""

    scene bg room with dissolve
    play music "bgm_investigation.ogg" fadein 1.0

    "你来到了管道工博莱斯的住所。"
    "简单的房间里堆放着一些管道工具。"

    menu visit_bolai_house_menu:
        "你想做什么？"

        "查看管道图纸":
            "这是小镇地下管道的设计图。"
            "上面标注了各个管道的走向和连接点。"
            $ discover_clue("管道布局图")
            jump visit_bolai_house_menu

        "查看工作日志" if is_hotspot_unlocked("博莱斯住所", "工作日志"):
            "工作日志中有一些可疑的记录。"
            "某些维修记录的日期和实际情况似乎对不上。"
            $ discover_clue("伪造维修记录")
            jump visit_bolai_house_menu

        "与博莱斯交谈" if is_character_alive("博莱斯"):
            call talk_to_bolai_scene1 from _call_talk_to_bolai_scene1
            jump visit_bolai_house_menu

        "离开":
            return

label visit_ileina_apartment:
    """伊雷娜的公寓"""

    scene bg room with dissolve
    play music "bgm_investigation.ogg" fadein 1.0

    "你来到了伊雷娜的小公寓。"
    "陈设简单，但收拾得很整洁。"

    menu visit_ileina_apartment_menu:
        "你想做什么？"

        "查看窗户":
            "窗户面向小镇广场，视野很好。"
            "从这里可以看到广场上发生的大部分事情。"
            $ discover_clue("目击视角")
            jump visit_ileina_apartment_menu

        "查看日记" if is_hotspot_unlocked("伊雷娜公寓", "日记"):
            "伊雷娜的日记中记录了她的日常生活。"
            "有一些关于火灾当晚的记载特别引人注目。"
            $ discover_clue("伊雷娜日记")
            jump visit_ileina_apartment_menu

        "与伊雷娜交谈" if is_character_alive("伊雷娜"):
            call talk_to_ileina_scene1 from _call_talk_to_ileina_scene1
            jump visit_ileina_apartment_menu

        "离开":
            return

label visit_town_square:
    """布恰小镇广场"""

    scene bg room with dissolve
    play music "bgm_town.ogg" fadein 1.0

    "你来到了小镇的中心广场。"
    "这里是居民们聚集交流的地方。"

    menu visit_town_square_menu:
        "你想做什么？"

        "在长椅上休息":
            "你坐在长椅上观察来来往往的行人。"
            "小镇的日常生活看起来平静而普通。"
            jump visit_town_square_menu

        "查看公告栏":
            "公告栏上张贴着各种社区通知。"
            "有一张关于近期安全事项的通告。"
            $ discover_clue("小镇公告")
            jump visit_town_square_menu

        "查看喷泉":
            "这是一座已经停用的老喷泉。"
            "听说它在很多年前就不再运作了。"
            jump visit_town_square_menu

        "离开":
            return

