# 统一persistent变量初始化文件
# 所有跨存档的persistent变量在此统一管理和初始化
# 使用 init -1 确保在其他初始化代码之前执行

init -1 python:
    """
    persistent变量初始化

    persistent变量会在所有存档间共享，主要用于：
    - 周目解锁状态
    - 线索收集进度
    - 游戏全局状态
    - 特殊解锁标志

    注意：使用 getattr 检查以兼容旧存档中可能存在的 None 值
    """

    # ========================================
    # 周目系统 - Episode解锁状态
    # ========================================

    # 第一周目（伪书·陷阱与迷雾）- 默认解锁
    if getattr(persistent, 'episode_1_unlocked', None) is None:
        persistent.episode_1_unlocked = True

    # 第二周目（伪书·真相的碎片）- 完成周目1后解锁
    if getattr(persistent, 'episode_2_unlocked', None) is None:
        persistent.episode_2_unlocked = False

    # 第三周目（伪书·破碎的现实）- 完成周目2后解锁
    if getattr(persistent, 'episode_3_unlocked', None) is None:
        persistent.episode_3_unlocked = False

    # 第四周目（真相周目）- 完成所有伪书周目后解锁
    if getattr(persistent, 'episode_4_unlocked', None) is None:
        persistent.episode_4_unlocked = False

    # 第二部（Episodes 5-8）- 开发中
    if getattr(persistent, 'episodes_5_8_unlocked', None) is None:
        persistent.episodes_5_8_unlocked = False

    # ========================================
    # 线索系统 - 已发现的线索
    # ========================================

    # 已发现线索的ID列表
    if getattr(persistent, 'discovered_clues', None) is None:
        persistent.discovered_clues = []

    # ========================================
    # 游戏状态 - 全局变量
    # ========================================

    # 精神值（0-100，100为正常，0为崩溃）
    # 影响角色认知和幻觉触发
    if getattr(persistent, 'sanity', None) is None:
        persistent.sanity = 100

    # ========================================
    # 特殊标志 - 剧情解锁条件
    # ========================================

    # 博莱斯对质标志 - 解锁特定线索和热点
    if getattr(persistent, 'bolai_confronted', None) is None:
        persistent.bolai_confronted = False

    # 保险柜密码发现标志 - 解锁罗琳达宅邸保险柜
    if getattr(persistent, 'safe_password_found', None) is None:
        persistent.safe_password_found = False

    # ========================================
    # 笔记本系统 - 角色档案和记录
    # ========================================

    # 已遇见的角色列表（角色名）
    if getattr(persistent, 'met_characters', None) is None:
        persistent.met_characters = []

    # 笔记本记录列表（记录ID）
    if getattr(persistent, 'notebook_records', None) is None:
        persistent.notebook_records = []

    # ========================================
    # 地点系统 - 已访问的地点
    # ========================================

    # 已访问地点的名称列表
    if getattr(persistent, 'visited_locations', None) is None:
        persistent.visited_locations = []

    # 已解锁地点的名称列表（用于弹窗通知）
    if getattr(persistent, 'unlocked_locations', None) is None:
        persistent.unlocked_locations = []

    # ========================================
    # 开发者工具函数
    # ========================================

    def reset_all_persistent():
        """
        重置所有persistent变量到初始状态
        仅用于开发和测试
        """
        persistent.episode_1_unlocked = True
        persistent.episode_2_unlocked = False
        persistent.episode_3_unlocked = False
        persistent.episode_4_unlocked = False
        persistent.episodes_5_8_unlocked = False
        persistent.discovered_clues = []
        persistent.sanity = 100
        persistent.bolai_confronted = False
        persistent.safe_password_found = False
        persistent.met_characters = []
        persistent.notebook_records = []
        persistent.visited_locations = []
        persistent.unlocked_locations = []
        renpy.notify("所有persistent变量已重置")

    def unlock_all_episodes():
        """
        解锁所有周目
        仅用于开发和测试
        """
        persistent.episode_1_unlocked = True
        persistent.episode_2_unlocked = True
        persistent.episode_3_unlocked = True
        persistent.episode_4_unlocked = True
        persistent.episodes_5_8_unlocked = True
        renpy.notify("所有周目已解锁")

    def set_sanity(value):
        """
        设置精神值
        仅用于开发和测试

        Args:
            value: 精神值（0-100）
        """
        persistent.sanity = max(0, min(100, value))
        renpy.notify("精神值已设置为: {}".format(persistent.sanity))

    def test_sanity_levels():
        """
        循环测试所有精神值档位的图标显示
        仅用于开发和测试
        """
        levels = [100, 75, 58, 42, 25, 8]
        names = ["正常", "轻度幻觉", "中度幻觉", "重度幻觉", "极度混乱", "崩溃边缘"]

        for i, level in enumerate(levels):
            persistent.sanity = level
            renpy.notify("精神值: {} - {}".format(level, names[i]))

    def show_persistent_status():
        """
        显示当前 persistent 变量状态
        用于调试周目解锁问题
        """
        status = "=== Persistent 状态 ===\n"
        status += "Episode 1: {}\n".format("解锁" if persistent.episode_1_unlocked else "锁定")
        status += "Episode 2: {}\n".format("解锁" if persistent.episode_2_unlocked else "锁定")
        status += "Episode 3: {}\n".format("解锁" if persistent.episode_3_unlocked else "锁定")
        status += "Episode 4: {}\n".format("解锁" if persistent.episode_4_unlocked else "锁定")
        status += "Episodes 5-8: {}\n".format("解锁" if persistent.episodes_5_8_unlocked else "锁定")
        status += "精神值: {}\n".format(persistent.sanity)
        status += "已发现线索: {}个".format(len(persistent.discovered_clues))
        renpy.notify(status)
        return status

    def force_reset_episodes():
        """
        强制重置周目解锁状态
        在主菜单按 Shift+D -> Console -> force_reset_episodes() 调用
        """
        persistent.episode_1_unlocked = True
        persistent.episode_2_unlocked = False
        persistent.episode_3_unlocked = False
        persistent.episode_4_unlocked = False
        persistent.episodes_5_8_unlocked = False
        renpy.notify("周目已强制重置！只有Episode 1解锁")
        # 强制刷新主菜单
        renpy.restart_interaction()

