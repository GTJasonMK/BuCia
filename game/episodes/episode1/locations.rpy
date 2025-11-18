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
    """安德里娅的住所（占位符）"""
    scene bg room with dissolve
    "安德里娅的住所"
    "此地点剧情正在开发中..."
    return

## 注意：visit_church 已在 shared/locations/church.rpy 中定义

label visit_community_center:
    """社区管理中心（占位符）"""
    scene bg room with dissolve
    "社区管理中心"
    "此地点剧情正在开发中..."
    return

label visit_badebiete_house:
    """巴德别特的家（占位符）"""
    scene bg room with dissolve
    "巴德别特的家"
    "此地点剧情正在开发中..."
    return

label visit_hafu_workshop:
    """电工哈夫的工作室（占位符）"""
    scene bg room with dissolve
    "电工哈夫的工作室"
    "此地点剧情正在开发中..."
    return

label visit_bolai_house:
    """管道工博莱斯的家（占位符）"""
    scene bg room with dissolve
    "管道工博莱斯的家"
    "此地点剧情正在开发中..."
    return

label visit_ileina_apartment:
    """伊雷娜的公寓（占位符）"""
    scene bg room with dissolve
    "伊雷娜的公寓"
    "此地点剧情正在开发中..."
    return

label visit_town_square:
    """布恰小镇广场（占位符）"""
    scene bg room with dissolve
    "布恰小镇广场"
    "此地点剧情正在开发中..."
    return

