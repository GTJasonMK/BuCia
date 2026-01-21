## Episode系统 - 周目管理
## 负责追踪当前周目，提供周目初始化功能

## 当前周目追踪变量
default current_episode = 1  # 当前正在进行的周目(1-4)

## Episode系统函数
init python:
    def start_episode(episode_num):
        """
        开始一个新周目

        Args:
            episode_num: 周目编号(1-4)
        """
        global current_episode

        current_episode = episode_num

        # 重置时间系统
        reset_time()

        # 重置地点访问状态(可选)
        for loc_name in locations_database:
            locations_database[loc_name]["visited"] = False
        # 同步重置持久化访问记录，避免周目间残留
        persistent.visited_locations = []
        # 重置地点解锁状态，避免周目间解锁残留
        if 'reset_locations_unlock_state' in dir():
            reset_locations_unlock_state()
        store.current_location = None

        renpy.notify(f"开始第{episode_num}周目")

    def get_current_episode():
        """获取当前周目编号"""
        return current_episode

    def is_episode(episode_num):
        """检查是否为指定周目"""
        return current_episode == episode_num

    def is_first_episode():
        """检查是否为第一周目"""
        return current_episode == 1

    def is_final_episode():
        """检查是否为第四周目(真相周目)"""
        return current_episode == 4
