## 角色认知状态机 - 主角对角色印象
## 用于记录每个周目内主角对角色的认知变化，并提供笔记本展示所需接口

## 角色印象（随存档保存）
default character_impressions = {}

init python:
    ## 状态机定义（可按剧情扩展）
    impression_states = [
        "unknown",   ## 未知
        "met",       ## 初识
        "neutral",   ## 中立
        "trust",     ## 信任
        "ally",      ## 同盟
        "suspect",   ## 怀疑
        "hostile"    ## 敌对
    ]

    ## 状态显示文案（用于UI）
    impression_display = {
        "unknown": "未知",
        "met": "初识",
        "neutral": "中立",
        "trust": "信任",
        "ally": "同盟",
        "suspect": "怀疑",
        "hostile": "敌对"
    }

    ## 周目默认印象（可按周目定制）
    ## 结构：{episode_num: {"default": "unknown", "角色名": "state"}}
    impression_episode_defaults = {
        1: {"default": "unknown"},
        2: {"default": "unknown"},
        3: {"default": "unknown"},
        4: {"default": "unknown"}
    }

    ## 事件驱动的印象变化（按剧情调用）
    ## 结构：{"event_id": {"角色名": "state"}}
    impression_event_map = {
        ## Episode 1 - 示例事件
        "ep1_meet_rolinda": {"罗琳达": "met"},
        "ep1_supplement_doubt": {"罗琳达": "suspect"},
        "ep1_meet_yedina": {"叶蒂娜": "met"},
        "ep1_autopsy_doubt": {"叶蒂娜": "suspect"}
    }

    def resolve_character_name(char_name):
        """
        解析角色名称（支持中文名/全名/立绘ID）
        """
        if not char_name:
            return None
        if 'character_database' not in globals():
            return char_name
        if char_name in character_database:
            return char_name
        for key, data in character_database.items():
            if data.get("full_name") == char_name:
                return key
        for key, data in character_database.items():
            if data.get("sprite") == char_name:
                return key
        return char_name

    def _get_impression_default(episode_num, char_name):
        defaults = impression_episode_defaults.get(episode_num, {})
        if char_name in defaults:
            return defaults[char_name]
        return defaults.get("default", "unknown")

    def reset_impressions(episode_num=None, silent=True):
        """
        重置当前周目的角色印象
        """
        if episode_num is None:
            if hasattr(renpy.store, "get_current_episode"):
                episode_num = renpy.store.get_current_episode()
            else:
                episode_num = 1

        if hasattr(renpy.store, "get_all_character_names"):
            names = renpy.store.get_all_character_names()
        elif 'character_database' in globals():
            names = list(character_database.keys())
        else:
            names = []

        store.character_impressions = {}
        for name in names:
            store.character_impressions[name] = _get_impression_default(episode_num, name)

        if not silent:
            renpy.notify("角色认知已重置")

    def get_impression(char_name, episode_num=None):
        """
        获取角色当前印象状态
        """
        if not char_name:
            return "unknown"

        resolved = resolve_character_name(char_name)
        if resolved in store.character_impressions:
            state = store.character_impressions[resolved]
            if state == "unknown":
                met_list = getattr(persistent, "met_characters", [])
                if resolved in met_list:
                    return "met"
            return state

        if episode_num is None:
            if hasattr(renpy.store, "get_current_episode"):
                episode_num = renpy.store.get_current_episode()
            else:
                episode_num = 1

        state = _get_impression_default(episode_num, resolved)
        if state == "unknown":
            met_list = getattr(persistent, "met_characters", [])
            if resolved in met_list:
                return "met"
        return state

    def get_impression_display(char_name, episode_num=None):
        """
        获取角色印象显示文案
        """
        state_id = get_impression(char_name, episode_num)
        return impression_display.get(state_id, "未知")

    def set_impression(char_name, state_id, reason=None, silent=False):
        """
        设置角色印象状态
        """
        if not char_name:
            return False
        if state_id not in impression_display:
            renpy.log(f"错误：未知的印象状态 - '{state_id}'")
            return False
        resolved = resolve_character_name(char_name)
        if 'character_database' in globals() and resolved not in character_database:
            renpy.log(f"错误：尝试设置不存在角色印象 - '{char_name}'")
            return False

        ## 初识状态同步解锁角色
        if state_id == "met" and reason != "meet":
            if hasattr(renpy.store, "meet_character"):
                renpy.store.meet_character(resolved)

        old_state = store.character_impressions.get(resolved)
        store.character_impressions[resolved] = state_id

        if (not silent) and (old_state != state_id):
            state_text = impression_display.get(state_id, state_id)
            if hasattr(renpy.store, "popup_impression"):
                renpy.store.popup_impression(resolved, state_text)
            else:
                msg = f"{resolved}印象变为：{state_text}"
                renpy.notify(msg)
        return True

    def apply_impression_event(event_id, silent=False):
        """
        通过事件批量更新角色印象
        """
        changes = impression_event_map.get(event_id)
        if not changes:
            return False
        for char_name, new_state in changes.items():
            set_impression(char_name, new_state, reason=event_id, silent=silent)
        return True
