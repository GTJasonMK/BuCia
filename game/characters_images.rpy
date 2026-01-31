## 角色立绘绑定（来自 asset/charcater2）
## 说明：当前仅有单张立绘，所有表情/状态复用同一图片

## 自动立绘显示开关与一次性抑制
default auto_sprite_enabled = True
default auto_sprite_suppress_next = False
default auto_sprite_suppress_next_tag = None
default auto_sprite_pair = []
default auto_sprite_active = None
default auto_sprite_force_side = {}
default auto_sprite_last_side = None
default auto_sprite_tag_enabled = {
    "andrea": True,
    "tsibela": True,
    "telina": True,
    "molorava": True,
    "badebiete": True,
    "hafu": True,
    "bolai": True,
    "ileina": True,
    "rolinda": True,
    "yedina": True,
}
default auto_sprite_talk_start = {}
default auto_sprite_talk_until = {}
default auto_sprite_talk_cycles = {}

init -2:
    ## 立绘尺寸较大（约 2813x5000），直接显示会超出常见纹理上限
    ## 显示半身立绘：离线已“先拼接再缩放（LANCZOS）”烘焙到最终尺寸，游戏内不再做大倍率缩放
    $ _character_offline_scale = 0.45
    $ _character_sprite_scale = 1.0
    $ _character_sprite_crop_ratio = 0.5  # 裁剪上半部分（50%高度），显示半身
    $ _character_half_raw_size = (2813, 2500)
    $ _character_half_size = (int(round(_character_half_raw_size[0] * _character_offline_scale)), int(round(_character_half_raw_size[1] * _character_offline_scale)))
    ## 说话动画控制（按句子时长计算循环次数）
    $ _character_talk_min_duration = 0.3
    $ _character_talk_max_duration = 12.0
    ## 眨眼周期：1.0 秒完成一个眨眼循环（25字以上的句子会有眨眼）
    $ _character_eye_cycle_seconds = 0.8
    ## 嘴巴周期：说话时嘴巴快速开合，0.3 秒一个循环（约 3.3 次/秒）
    $ _character_mouth_cycle_seconds = 0.3

    ## 双人对话立绘位置（以屏幕中线为对称轴）
    $ _character_pair_offset = 0.18
    $ _character_dim_alpha = 0.6
    $ _character_dim_scale = 0.9
    $ _character_active_scale = 1.05

    ## 统一角色显示位置（对话框左侧，与左侧高亮一致）
    transform character_center:
        subpixel False
        xalign (0.5 - _character_pair_offset)
        yalign 1.0
        xanchor 0.5
        yanchor 1.0

    ## 左侧-高亮
    transform character_left_active:
        subpixel False
        xalign (0.5 - _character_pair_offset)
        yalign 1.0
        xanchor 0.5
        yanchor 1.0

    ## 左侧-变暗缩小
    transform character_left_dim:
        subpixel False
        xalign (0.5 - _character_pair_offset)
        yalign 1.0
        xanchor 0.5
        yanchor 1.0

    ## 右侧-高亮
    transform character_right_active:
        subpixel False
        xalign (0.5 + _character_pair_offset)
        yalign 1.0
        xanchor 0.5
        yanchor 1.0

    ## 右侧-变暗缩小
    transform character_right_dim:
        subpixel False
        xalign (0.5 + _character_pair_offset)
        yalign 1.0
        xanchor 0.5
        yanchor 1.0

    ## 创建半身立绘的辅助函数（裁剪上半部分；缩放在最终 Composite 外层做）
    python:
        def create_half_body_sprite(image_path, scale):
            """创建半身立绘：优先直接返回（已离线烘焙）；否则裁剪上半身做兜底。"""
            if isinstance(image_path, str) and image_path.startswith("characters_baked/"):
                return image_path
            # im.Crop 语法: (x, y, width, height)
            return im.Crop(image_path, (0, 0, _character_half_size[0], _character_half_size[1]))

        def _calc_talk_cycles_by_duration(duration, cycle_seconds):
            """按时长估算动画循环次数（余数超过半周期则进一）"""
            safe_cycle = max(0.001, float(cycle_seconds))
            if float(duration) < safe_cycle:
                return 0
            base_cycles = int(float(duration) / safe_cycle)
            remainder = float(duration) - (base_cycles * safe_cycle)
            if remainder >= (safe_cycle * 0.5):
                base_cycles += 1
            return max(0, base_cycles)

        def _get_text_cps():
            """获取当前文本流式输出速度（每秒字符数）"""
            cps = getattr(renpy.store.preferences, "text_cps", None)
            if cps is None:
                cps = getattr(renpy.config, "default_text_cps", 30)
            return cps

        def _get_now():
            """获取当前时间（兼容不同 Ren'Py 版本）"""
            fn = getattr(renpy, "get_time", None)
            if callable(fn):
                return fn()
            core = getattr(renpy, "display", None)
            if core is not None and hasattr(core, "core"):
                fn = getattr(core.core, "get_time", None)
                if callable(fn):
                    return fn()
            iface = getattr(getattr(renpy, "game", None), "interface", None)
            if iface is not None and hasattr(iface, "get_time"):
                return iface.get_time()
            import time
            return time.time()

        def start_sprite_talk(tag, what):
            """开始说话：计算持续时间与循环次数"""
            if not what:
                what = getattr(renpy.store, "last_say_what", None)
            if not what:
                return
            if tag not in _auto_sprite_tags:
                return
            try:
                plain = renpy.filter_text_tags(what, allow=[])
            except Exception:
                plain = what
            text_len = len(plain)
            cps = _get_text_cps()
            if cps is None or cps <= 0:
                duration = _character_talk_min_duration
            else:
                duration = max(_character_talk_min_duration, float(text_len) / float(cps))
                duration = min(duration, _character_talk_max_duration)
            now = _get_now()
            store.auto_sprite_talk_start[tag] = now
            store.auto_sprite_talk_until[tag] = now + duration
            store.auto_sprite_talk_cycles[tag] = {
                "eye": _calc_talk_cycles_by_duration(
                    duration,
                    _character_eye_cycle_seconds
                ),
                "mouth": _calc_talk_cycles_by_duration(
                    duration,
                    _character_mouth_cycle_seconds
                ),
            }

        def stop_sprite_talk(tag):
            """结束说话：立即停止动画"""
            if tag not in _auto_sprite_tags:
                return
            now = _get_now()
            store.auto_sprite_talk_until[tag] = now

        def build_talking_layer(tag, idle_path, frame_paths, scale, part):
            """说话时按文本时长播放 n 个周期，不说话显示静态首帧"""
            def _apply_mask(img):
                return img
            frames = [_apply_mask(create_half_body_sprite(path, scale)) for path in frame_paths]
            idle_frame = frames[0] if frames else _apply_mask(create_half_body_sprite(idle_path, scale))

            def _talk_anim(st, at):
                end_time = store.auto_sprite_talk_until.get(tag, 0.0)
                start_time = store.auto_sprite_talk_start.get(tag, 0.0)
                now = _get_now()
                if (end_time <= start_time) or (now >= end_time) or not frames:
                    return idle_frame, 0.1
                duration = max(0.001, end_time - start_time)
                progress = (now - start_time) / duration
                progress = max(0.0, min(1.0, progress))
                cycles = store.auto_sprite_talk_cycles.get(tag, {}).get(part, 1)
                if cycles <= 0:
                    return idle_frame, 0.1
                phase = progress * cycles
                frame_index = int(phase * len(frames)) % len(frames)
                return frames[frame_index], 0

            return DynamicDisplayable(_talk_anim)

        def build_baked_combo_sprite(tag, baked_dir, eye_count, mouth_count):
            """
            使用离线烘焙后的“组合帧”显示说话动画。

            组合帧文件命名：
            - idle: <baked_dir>/idle.png（等同 e0_m0）
            - combo: <baked_dir>/e{ei}_m{mi}.png
            """
            idle_frame = create_half_body_sprite(f"{baked_dir}/idle.png", 1.0)
            frames = []
            for ei in range(int(eye_count)):
                for mi in range(int(mouth_count)):
                    frames.append(create_half_body_sprite(f"{baked_dir}/e{ei}_m{mi}.png", 1.0))

            def _combo_anim(st, at):
                end_time = store.auto_sprite_talk_until.get(tag, 0.0)
                start_time = store.auto_sprite_talk_start.get(tag, 0.0)
                now = _get_now()
                if (end_time <= start_time) or (now >= end_time) or not frames:
                    return idle_frame, 0.1

                duration = max(0.001, end_time - start_time)
                progress = (now - start_time) / duration
                progress = max(0.0, min(1.0, progress))

                eye_cycles = store.auto_sprite_talk_cycles.get(tag, {}).get("eye", 0)
                mouth_cycles = store.auto_sprite_talk_cycles.get(tag, {}).get("mouth", 0)

                # 两个分量都不播放时：直接停在 idle
                if (eye_cycles <= 0) and (mouth_cycles <= 0):
                    return idle_frame, 0.1

                ei = 0
                mi = 0
                if eye_cycles > 0 and int(eye_count) > 0:
                    phase = progress * eye_cycles
                    ei = int(phase * int(eye_count)) % int(eye_count)
                if mouth_cycles > 0 and int(mouth_count) > 0:
                    phase = progress * mouth_cycles
                    mi = int(phase * int(mouth_count)) % int(mouth_count)

                idx = ei * int(mouth_count) + mi
                if idx < 0 or idx >= len(frames):
                    return idle_frame, 0.1
                return frames[idx], 0

            return DynamicDisplayable(_combo_anim)

    ## 安德莉娅（文件名来源：1.png）
    image andrea = build_baked_combo_sprite("andrea", "characters_baked/andrea", 3, 2)
    image andrea active = build_baked_combo_sprite("andrea", "characters_baked/andrea/active", 3, 2)
    image andrea dim = build_baked_combo_sprite("andrea", "characters_baked/andrea/dim", 3, 2)
    image andrea neutral = "andrea"

    ## 茨贝拉（2.png）
    image tsibela = build_baked_combo_sprite("tsibela", "characters_baked/tsibela", 3, 4)
    image tsibela active = build_baked_combo_sprite("tsibela", "characters_baked/tsibela/active", 3, 4)
    image tsibela dim = build_baked_combo_sprite("tsibela", "characters_baked/tsibela/dim", 3, 4)
    image tsibela neutral = "tsibela"

    ## 特莉娜（3.png）
    image telina = build_baked_combo_sprite("telina", "characters_baked/telina", 4, 4)
    image telina active = build_baked_combo_sprite("telina", "characters_baked/telina/active", 4, 4)
    image telina dim = build_baked_combo_sprite("telina", "characters_baked/telina/dim", 4, 4)
    image telina neutral = "telina"

    ## 莫洛拉瓦（4.png）
    image molorava = build_talking_layer(
        "molorava",
        "characters_baked/molorava/idle.png",
        [
            "characters_baked/molorava/molorava-1.png",
            "characters_baked/molorava/molorava-2.png",
            "characters_baked/molorava/molorava-3.png",
            "characters_baked/molorava/molorava-4.png",
            "characters_baked/molorava/molorava-5.png"
        ],
        _character_sprite_scale,
        "mouth"
    )
    image molorava active = build_talking_layer(
        "molorava",
        "characters_baked/molorava/active/idle.png",
        [
            "characters_baked/molorava/active/molorava-1.png",
            "characters_baked/molorava/active/molorava-2.png",
            "characters_baked/molorava/active/molorava-3.png",
            "characters_baked/molorava/active/molorava-4.png",
            "characters_baked/molorava/active/molorava-5.png"
        ],
        _character_sprite_scale,
        "mouth"
    )
    image molorava dim = build_talking_layer(
        "molorava",
        "characters_baked/molorava/dim/idle.png",
        [
            "characters_baked/molorava/dim/molorava-1.png",
            "characters_baked/molorava/dim/molorava-2.png",
            "characters_baked/molorava/dim/molorava-3.png",
            "characters_baked/molorava/dim/molorava-4.png",
            "characters_baked/molorava/dim/molorava-5.png"
        ],
        _character_sprite_scale,
        "mouth"
    )
    image molorava neutral = "molorava"

    ## 巴德别特（5.png）
    image badebiete = build_baked_combo_sprite("badebiete", "characters_baked/badebiete", 4, 4)
    image badebiete active = build_baked_combo_sprite("badebiete", "characters_baked/badebiete/active", 4, 4)
    image badebiete dim = build_baked_combo_sprite("badebiete", "characters_baked/badebiete/dim", 4, 4)
    image badebiete neutral = "badebiete"
    image badebiete serious = "badebiete"

    ## 哈夫（6.png）
    image hafu = build_baked_combo_sprite("hafu", "characters_baked/hafu", 4, 4)
    image hafu active = build_baked_combo_sprite("hafu", "characters_baked/hafu/active", 4, 4)
    image hafu dim = build_baked_combo_sprite("hafu", "characters_baked/hafu/dim", 4, 4)
    image hafu neutral = "hafu"

    ## 博莱斯（7.png）
    image bolai = build_baked_combo_sprite("bolai", "characters_baked/bolai", 4, 4)
    image bolai active = build_baked_combo_sprite("bolai", "characters_baked/bolai/active", 4, 4)
    image bolai dim = build_baked_combo_sprite("bolai", "characters_baked/bolai/dim", 4, 4)
    image bolai neutral = "bolai"

    ## 伊蕾娜（8.png）
    image ileina = build_baked_combo_sprite("ileina", "characters_baked/ileina", 3, 3)
    image ileina active = build_baked_combo_sprite("ileina", "characters_baked/ileina/active", 3, 3)
    image ileina dim = build_baked_combo_sprite("ileina", "characters_baked/ileina/dim", 3, 3)
    image ileina neutral = "ileina"

    ## 罗琳达（9.png）
    image rolinda = build_talking_layer(
        "rolinda",
        "characters_baked/rolinda/idle.png",
        [
            "characters_baked/rolinda/rolinda-2.png",
            "characters_baked/rolinda/rolinda-3.png",
            "characters_baked/rolinda/rolinda-4.png",
            "characters_baked/rolinda/rolinda-5.png",
            "characters_baked/rolinda/rolinda-6.png"
        ],
        _character_sprite_scale,
        "mouth"
    )
    image rolinda active = build_talking_layer(
        "rolinda",
        "characters_baked/rolinda/active/idle.png",
        [
            "characters_baked/rolinda/active/rolinda-2.png",
            "characters_baked/rolinda/active/rolinda-3.png",
            "characters_baked/rolinda/active/rolinda-4.png",
            "characters_baked/rolinda/active/rolinda-5.png",
            "characters_baked/rolinda/active/rolinda-6.png"
        ],
        _character_sprite_scale,
        "mouth"
    )
    image rolinda dim = build_talking_layer(
        "rolinda",
        "characters_baked/rolinda/dim/idle.png",
        [
            "characters_baked/rolinda/dim/rolinda-2.png",
            "characters_baked/rolinda/dim/rolinda-3.png",
            "characters_baked/rolinda/dim/rolinda-4.png",
            "characters_baked/rolinda/dim/rolinda-5.png",
            "characters_baked/rolinda/dim/rolinda-6.png"
        ],
        _character_sprite_scale,
        "mouth"
    )
    image rolinda neutral = "rolinda"
    image rolinda serious = "rolinda"

    ## 叶蒂娜（10.png）
    image yedina = build_talking_layer(
        "yedina",
        "characters_baked/yedina/idle.png",
        [
            "characters_baked/yedina/yedina-1.png",
            "characters_baked/yedina/yedina-2.png",
            "characters_baked/yedina/yedina-3.png",
            "characters_baked/yedina/yedina-4.png",
            "characters_baked/yedina/yedina-5.png"
        ],
        _character_sprite_scale,
        "mouth"
    )
    image yedina active = build_talking_layer(
        "yedina",
        "characters_baked/yedina/active/idle.png",
        [
            "characters_baked/yedina/active/yedina-1.png",
            "characters_baked/yedina/active/yedina-2.png",
            "characters_baked/yedina/active/yedina-3.png",
            "characters_baked/yedina/active/yedina-4.png",
            "characters_baked/yedina/active/yedina-5.png"
        ],
        _character_sprite_scale,
        "mouth"
    )
    image yedina dim = build_talking_layer(
        "yedina",
        "characters_baked/yedina/dim/idle.png",
        [
            "characters_baked/yedina/dim/yedina-1.png",
            "characters_baked/yedina/dim/yedina-2.png",
            "characters_baked/yedina/dim/yedina-3.png",
            "characters_baked/yedina/dim/yedina-4.png",
            "characters_baked/yedina/dim/yedina-5.png"
        ],
        _character_sprite_scale,
        "mouth"
    )
    image yedina neutral = "yedina"
    image yedina sad = "yedina"

init -2 python:
    ## 自动显示立绘的角色标签（与 Character.image 对应）
    _auto_sprite_tags = {
        "andrea",
        "tsibela",
        "telina",
        "molorava",
        "badebiete",
        "hafu",
        "bolai",
        "ileina",
        "rolinda",
        "yedina",
    }

    def set_auto_sprite_enabled(enabled=True, hide=True):
        """
        开关自动立绘显示。
        enabled=True/False；hide=True 时会隐藏已显示的角色立绘。
        """
        store.auto_sprite_enabled = enabled
        if hide:
            for tag in _auto_sprite_tags:
                if renpy.showing(tag):
                    renpy.hide(tag)
            store.auto_sprite_pair = []
            store.auto_sprite_active = None

    def suppress_auto_sprite_once():
        """
        仅抑制下一句对白的自动立绘显示。
        """
        store.auto_sprite_suppress_next = True

    def suppress_auto_sprite_for(tag):
        """
        仅抑制下一句某角色对白的自动立绘显示。
        """
        store.auto_sprite_suppress_next_tag = tag

    def set_auto_sprite_for(tag, enabled=True, hide=True):
        """
        设置单个角色的自动立绘显示开关。
        """
        store.auto_sprite_tag_enabled[tag] = enabled
        if hide and not enabled and renpy.showing(tag):
            renpy.hide(tag)
        if not enabled and tag in store.auto_sprite_pair:
            store.auto_sprite_pair = [t for t in store.auto_sprite_pair if t != tag]
            if store.auto_sprite_active == tag:
                store.auto_sprite_active = store.auto_sprite_pair[0] if store.auto_sprite_pair else None
        if not enabled and tag in store.auto_sprite_force_side:
            store.auto_sprite_force_side.pop(tag, None)

    def force_auto_sprite_side(tag, side):
        """
        强制指定角色显示在左/右侧（用于手动 show 的预定位）。
        side: "left" 或 "right"
        """
        if side not in ("left", "right"):
            return
        store.auto_sprite_force_side[tag] = side

    def clear_auto_sprite_force_side(tag=None):
        """
        清除强制侧边设置。
        tag=None 时清空所有。
        """
        if tag is None:
            store.auto_sprite_force_side = {}
            return
        store.auto_sprite_force_side.pop(tag, None)

    def _get_sprite_image(tag, state=None):
        """
        获取角色立绘名称。

        优先级：
        1) 指定 state（active/dim）且存在对应图像；
        2) neutral；
        3) tag 本身。
        """
        if state:
            name = f"{tag} {state}"
            if renpy.has_image(name):
                return name
        if renpy.has_image(f"{tag} neutral"):
            return f"{tag} neutral"
        return tag

    def _refresh_auto_sprite_pair():
        """
        刷新双人立绘显示：非说话角色变暗缩小。
        """
        pair = list(getattr(store, "auto_sprite_pair", []))
        active = getattr(store, "auto_sprite_active", None)

        if pair and active not in pair:
            active = pair[-1]
            store.auto_sprite_active = active

        for other_tag in _auto_sprite_tags:
            if other_tag not in pair and renpy.showing(other_tag):
                renpy.hide(other_tag)

        if len(pair) >= 1:
            left_tag = pair[0]
            if len(pair) == 1:
                forced = store.auto_sprite_force_side.get(left_tag, "left")
                state = "active" if left_tag == active else "dim"
                if forced == "right":
                    right_transform = character_right_active if left_tag == active else character_right_dim
                    renpy.show(_get_sprite_image(left_tag, state), at_list=[right_transform])
                else:
                    left_transform = character_left_active if left_tag == active else character_left_dim
                    renpy.show(_get_sprite_image(left_tag, state), at_list=[left_transform])
            else:
                left_transform = character_left_active if left_tag == active else character_left_dim
                state = "active" if left_tag == active else "dim"
                renpy.show(_get_sprite_image(left_tag, state), at_list=[left_transform])

        if len(pair) >= 2:
            right_tag = pair[1]
            right_transform = character_right_active if right_tag == active else character_right_dim
            state = "active" if right_tag == active else "dim"
            renpy.show(_get_sprite_image(right_tag, state), at_list=[right_transform])

    def _set_auto_sprite_active(tag):
        """
        设置当前说话者并更新左右位置。
        """
        if tag not in _auto_sprite_tags:
            return

        pair = [t for t in list(getattr(store, "auto_sprite_pair", [])) if renpy.showing(t)]
        last_side = getattr(store, "auto_sprite_last_side", None)

        # 角色已在屏幕上：保持原侧并更新说话者
        if tag in pair:
            store.auto_sprite_active = tag
            if len(pair) >= 2:
                store.auto_sprite_last_side = "left" if pair[0] == tag else "right"
            else:
                store.auto_sprite_last_side = store.auto_sprite_force_side.get(tag, "left")
            _refresh_auto_sprite_pair()
            return

        # 新说话者：根据上一句说话方决定落位
        if len(pair) >= 2:
            pair = [pair[0], tag] if last_side == "left" else [tag, pair[1]]
        elif len(pair) == 1:
            if last_side == "left":
                pair = [pair[0], tag]
            else:
                pair = [tag, pair[0]]
        else:
            forced = store.auto_sprite_force_side.get(tag, "left")
            pair = [tag]
            store.auto_sprite_last_side = forced

        store.auto_sprite_pair = pair
        store.auto_sprite_active = tag
        if len(pair) >= 2:
            store.auto_sprite_last_side = "left" if pair[0] == tag else "right"
        _refresh_auto_sprite_pair()

    def make_character_callback(tag):
        """
        生成绑定到指定角色的回调函数。
        """
        def _cb(event, interact=True, **kwargs):
            if event in ("slow_done", "end", "hide"):
                stop_sprite_talk(tag)
            if event in ("begin", "show"):
                if hasattr(renpy.store, "meet_character"):
                    _resolved_name = tag
                    if hasattr(renpy.store, "resolve_character_name"):
                        _resolved_name = renpy.store.resolve_character_name(tag)
                    if 'character_database' in globals() and _resolved_name in character_database:
                        renpy.store.meet_character(_resolved_name)
            if not getattr(store, "auto_sprite_enabled", True):
                return
            if getattr(store, "auto_sprite_suppress_next", False):
                store.auto_sprite_suppress_next = False
                return
            if getattr(store, "auto_sprite_suppress_next_tag", None) == tag:
                store.auto_sprite_suppress_next_tag = None
                return
            if not store.auto_sprite_tag_enabled.get(tag, True):
                return
            if event in ("begin", "show"):
                start_sprite_talk(tag, kwargs.get("what", None))
                _set_auto_sprite_active(tag)
        return _cb
