## 弹窗提示系统
## 用于显示事件通知（线索发现、地点解锁、角色遇见等）

## 弹窗队列和状态
default popup_queue = []  ## 弹窗队列
default popup_showing = False  ## 是否正在显示弹窗
default popup_current = None  ## 当前显示的弹窗数据
default popup_sequence = 0  ## 弹窗序列号（用于避免定时器错关）

## 弹窗类型图标映射
define POPUP_ICONS = {
    "clue": "clue",           ## 线索发现
    "location": "location",   ## 地点解锁
    "character": "character", ## 角色遇见
    "event": "event",         ## 剧情事件
    "item": "item",           ## 物品获得
    "trust": "trust",         ## 信任度变化
    "impression": "impression", ## 角色印象变化
    "warning": "warning",     ## 警告提示
    "info": "info"            ## 一般信息
}

## 弹窗类型颜色映射
define POPUP_COLORS = {
    "clue": "#ffd700",        ## 金色 - 线索
    "location": "#64b5f6",    ## 蓝色 - 地点
    "character": "#81c784",   ## 绿色 - 角色
    "event": "#ff8a65",       ## 橙色 - 事件
    "item": "#ba68c8",        ## 紫色 - 物品
    "trust": "#f48fb1",       ## 粉色 - 信任度
    "impression": "#ffd54f",  ## 黄色 - 印象变化
    "warning": "#ef5350",     ## 红色 - 警告
    "info": "#ffffff"         ## 白色 - 信息
}

## 弹窗显示时长（秒）
define POPUP_DURATION = 2.5

init python:
    import time

    def show_popup(title, content, popup_type="info", duration=None):
        """
        显示弹窗提示

        Args:
            title: 弹窗标题（如"发现新线索"）
            content: 弹窗内容（如"火灾现场照片"）
            popup_type: 弹窗类型（clue/location/character/event/item/trust/warning/info）
            duration: 显示时长（秒），默认使用POPUP_DURATION
        """
        popup_data = {
            "title": title,
            "content": content,
            "type": popup_type,
            "duration": duration if duration else POPUP_DURATION,
            "timestamp": time.time()
        }

        ## 添加到队列
        store.popup_queue.append(popup_data)

        ## 如果当前没有显示弹窗，立即显示
        if not store.popup_showing:
            _show_next_popup()

    def _show_next_popup():
        """显示队列中的下一个弹窗"""
        if not store.popup_queue:
            store.popup_showing = False
            store.popup_current = None
            return

        ## 取出队列中的第一个弹窗
        store.popup_current = store.popup_queue.pop(0)
        store.popup_showing = True
        store.popup_sequence += 1
        store.popup_current["id"] = store.popup_sequence

        ## 显示弹窗屏幕
        renpy.show_screen("popup_notification")

        ## 设置定时器，自动关闭弹窗
        duration = store.popup_current.get("duration", POPUP_DURATION)
        renpy.invoke_in_thread(_popup_timer, store.popup_current["id"], duration)

    def _popup_timer(popup_id, duration):
        """弹窗定时器（在后台线程运行）"""
        import time
        time.sleep(duration)
        ## 回到主线程关闭弹窗
        renpy.invoke_in_main_thread(_close_current_popup, popup_id)

    def _close_current_popup(popup_id=None):
        """关闭当前弹窗并显示下一个"""
        if popup_id is not None:
            if not store.popup_current or store.popup_current.get("id") != popup_id:
                return
        if renpy.get_screen("popup_notification"):
            renpy.hide_screen("popup_notification")

        store.popup_showing = False
        store.popup_current = None

        ## 如果队列中还有弹窗，显示下一个
        if store.popup_queue:
            _show_next_popup()

    def close_popup():
        """手动关闭弹窗（点击时调用）"""
        _close_current_popup()

    def clear_popup_queue():
        """清空弹窗队列"""
        store.popup_queue = []
        if renpy.get_screen("popup_notification"):
            renpy.hide_screen("popup_notification")
        store.popup_showing = False
        store.popup_current = None

    ## ========================================
    ## 便捷弹窗函数
    ## ========================================

    def popup_clue(clue_name):
        """线索发现弹窗"""
        show_popup("发现新线索", clue_name, "clue")

    def popup_location(location_name):
        """地点解锁弹窗"""
        show_popup("新地点已解锁", location_name, "location")

    def popup_character(char_name):
        """角色遇见弹窗（已禁用）"""
        pass  # 弹窗功能已移除

    def popup_event(event_name):
        """剧情事件弹窗"""
        show_popup("事件发生", event_name, "event")

    def popup_item(item_name):
        """物品获得弹窗"""
        show_popup("获得物品", item_name, "item")

    def popup_trust(char_name, change):
        """信任度变化弹窗"""
        if change > 0:
            show_popup("信任度提升", "{} +{}".format(char_name, change), "trust")
        elif change < 0:
            show_popup("信任度下降", "{} {}".format(char_name, change), "trust")

    def popup_impression(char_name, state_text):
        """角色印象变化弹窗"""
        show_popup("印象变化", "{}：{}".format(char_name, state_text), "impression")

    def popup_warning(message):
        """警告弹窗"""
        show_popup("警告", message, "warning")

    def popup_info(title, message):
        """一般信息弹窗"""
        show_popup(title, message, "info")

