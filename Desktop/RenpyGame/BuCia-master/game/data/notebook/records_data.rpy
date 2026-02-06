## 笔记本记录数据库
## 管理游戏中的记录条目（剧情摘要、重要事件等）

init python:
    ## ========================================
    ## 记录数据库
    ## ========================================
    ##
    ## 每条记录包含：
    ##   - id: 唯一标识符
    ##   - title: 记录标题
    ##   - content: 记录内容
    ##   - category: 分类（story/event/note）
    ##   - episode: 所属周目（1-4，0表示通用）
    ##   - day: 获取日期（1-7，0表示无日期）
    ##   - icon: 图标路径（可选）
    ##

    RECORDS_DATABASE = {
        ## === Episode 1 记录 ===
        "ep1_arrival": {
            "id": "ep1_arrival",
            "title": "抵达不查小镇",
            "content": "作为侦探齐贝拉，我接受委托来到不查小镇调查。这个偏僻的小镇似乎隐藏着许多秘密...",
            "category": "story",
            "episode": 1,
            "day": 1,
            "icon": None
        },
        "ep1_meet_mayor": {
            "id": "ep1_meet_mayor",
            "title": "会见镇长",
            "content": "与镇长进行了初次会面。他的态度似乎有些闪烁其词...",
            "category": "event",
            "episode": 1,
            "day": 1,
            "icon": None
        },
        "ep1_bolai_clue": {
            "id": "ep1_bolai_clue",
            "title": "博莱斯的线索",
            "content": "发现了关于博莱斯的重要线索。他似乎与案件有着密切关联。",
            "category": "event",
            "episode": 1,
            "day": 2,
            "icon": None
        },
        "ep1_safe_discovery": {
            "id": "ep1_safe_discovery",
            "title": "罗琳达宅邸的保险柜",
            "content": "在罗琳达宅邸发现了一个保险柜，但需要密码才能打开。",
            "category": "note",
            "episode": 1,
            "day": 3,
            "icon": None
        },

        ## === Episode 2 记录 ===
        "ep2_new_perspective": {
            "id": "ep2_new_perspective",
            "title": "新的视角",
            "content": "第二周目开始，我决定从不同的角度重新审视案件...",
            "category": "story",
            "episode": 2,
            "day": 1,
            "icon": None
        },

        ## === Episode 3 记录 ===
        "ep3_broken_reality": {
            "id": "ep3_broken_reality",
            "title": "破碎的现实",
            "content": "第三周目开始，之前的调查结果似乎开始产生矛盾...",
            "category": "story",
            "episode": 3,
            "day": 1,
            "icon": None
        },

        ## === Episode 4 记录 ===
        "ep4_truth_begins": {
            "id": "ep4_truth_begins",
            "title": "真相周目",
            "content": "所有伪书周目完成后，真相终于开始浮出水面...",
            "category": "story",
            "episode": 4,
            "day": 1,
            "icon": None
        }
    }

    ## ========================================
    ## 记录系统API
    ## ========================================

    def add_record(record_id):
        """
        添加记录到笔记本

        Args:
            record_id: 记录ID

        Returns:
            bool: 是否成功添加
        """
        if record_id not in RECORDS_DATABASE:
            return False

        if record_id not in persistent.notebook_records:
            persistent.notebook_records.append(record_id)
            renpy.notify("新记录：" + RECORDS_DATABASE[record_id]["title"])
            return True
        return False

    def has_record(record_id):
        """
        检查是否已有某条记录

        Args:
            record_id: 记录ID

        Returns:
            bool: 是否已有该记录
        """
        return record_id in persistent.notebook_records

    def get_record(record_id):
        """
        获取记录详情

        Args:
            record_id: 记录ID

        Returns:
            dict or None: 记录数据
        """
        return RECORDS_DATABASE.get(record_id, None)

    def get_all_records():
        """
        获取所有已发现的记录

        Returns:
            list: 记录数据列表
        """
        records = []
        for record_id in persistent.notebook_records:
            record = RECORDS_DATABASE.get(record_id)
            if record:
                records.append(record)
        return records

    def get_records_by_category(category):
        """
        按分类获取记录

        Args:
            category: 分类（story/event/note）

        Returns:
            list: 记录数据列表
        """
        records = []
        for record_id in persistent.notebook_records:
            record = RECORDS_DATABASE.get(record_id)
            if record and record["category"] == category:
                records.append(record)
        return records

    def get_records_by_episode(episode):
        """
        按周目获取记录

        Args:
            episode: 周目编号（1-4）

        Returns:
            list: 记录数据列表
        """
        records = []
        for record_id in persistent.notebook_records:
            record = RECORDS_DATABASE.get(record_id)
            if record and record["episode"] == episode:
                records.append(record)
        return records

    def get_record_count():
        """
        获取已发现记录数量

        Returns:
            int: 记录数量
        """
        return len(persistent.notebook_records)

    def clear_all_records():
        """
        清除所有记录（仅用于开发测试）
        """
        persistent.notebook_records = []
        renpy.notify("所有记录已清除")
