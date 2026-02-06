# Episode 1 - 热点调查场景
# 所有 investigate_* labels
# 注意：所有周目共享相同label名称，内部用条件区分

## 罗琳达宅邸 - 书桌
label investigate_rolinda_house_desk:
    """
    调查罗琳达宅邸的书桌
    """

    "你走近整洁的办公桌。"
    "桌上摆放着一些政府文件。"

    # 发现线索
    if not is_clue_discovered("政府文件"):
        $ discover_clue("政府文件")
        "你发现了一份标题为'社区健康监测项目'的文件。"
        "这似乎是某种政府项目的说明..."
    else:
        "你已经调查过这里了。"

    return


## 罗琳达宅邸 - 保险柜
label investigate_rolinda_house_safe:
    """
    调查罗琳达宅邸的保险柜
    需要密码才能打开
    """

    "墙角有一个小型保险柜。"

    if not persistent.safe_password_found:
        "保险柜需要密码才能打开。"
        "你需要找到密码..."
        return

    "你输入了找到的密码..."
    "保险柜打开了！"

    if not is_clue_discovered("药厂资料"):
        $ discover_clue("药厂资料")
        "你发现了药厂的机密资料！"
        "这些资料详细记录了LSD药物实验的计划..."
    else:
        "保险柜已经空了。"

    return


## 叶蒂娜诊所 - 药柜
label investigate_yedina_clinic_cabinet:
    """
    调查诊所的药柜
    """

    "你检查了药柜中的药品。"
    "这里有大量镇静剂和精神类药物..."

    if not is_clue_discovered("药品清单"):
        $ discover_clue("药品清单")
        "你发现了药品进货清单。"
        "采购量似乎远超小镇人口的正常需求..."
    else:
        "你已经调查过药柜了。"

    return


## 安德莉娅住所 - 烧毁的床铺
label investigate_andrea_house_bed:
    """
    调查火灾后的床铺残骸
    只在Day 3之后可访问
    """

    "你检查了烧毁的床铺。"
    "火势很猛，几乎什么都没剩下..."

    if not is_clue_discovered("火灾现场照片"):
        $ discover_clue("火灾现场照片")
        "你拍摄了现场照片作为证据。"
    else:
        "你已经记录过现场了。"

    return


# TODO: 为其他地点的热点添加 investigate_* labels
# 每个地点有3-4个热点，总计约30-40个labels
# 建议分批实现，优先实现关键线索相关的热点
