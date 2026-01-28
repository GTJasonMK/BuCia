## 角色立绘绑定（来自 asset/charcater2）
## 说明：当前仅有单张立绘，所有表情/状态复用同一图片

## 自动立绘显示开关与一次性抑制
default auto_sprite_enabled = True
default auto_sprite_suppress_next = False
default auto_sprite_suppress_next_tag = None
default auto_sprite_pair = []
default auto_sprite_active = None
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

init -2:
    ## 立绘尺寸较大（约 2813x5000），直接显示会超出常见纹理上限
    ## 统一缩放到 20%，接近 1080p 下常规立绘高度（约 1000px）
    $ _character_sprite_scale = 0.2

    ## 统一角色显示位置（对话框左侧）
    transform character_center:
        xalign 0.2
        yalign 1.0
        xanchor 0.5
        yanchor 1.0

    ## 双人对话立绘位置（以屏幕中线为对称轴）
    $ _character_pair_offset = 0.18
    $ _character_dim_alpha = 0.6
    $ _character_dim_scale = 0.9
    $ _character_active_scale = 1.05

    ## 左侧-高亮
    transform character_left_active:
        xalign (0.5 - _character_pair_offset)
        yalign 1.0
        xanchor 0.5
        yanchor 1.0
        zoom _character_active_scale
        alpha 1.0

    ## 左侧-变暗缩小
    transform character_left_dim:
        xalign (0.5 - _character_pair_offset)
        yalign 1.0
        xanchor 0.5
        yanchor 1.0
        zoom _character_dim_scale
        alpha _character_dim_alpha

    ## 右侧-高亮
    transform character_right_active:
        xalign (0.5 + _character_pair_offset)
        yalign 1.0
        xanchor 0.5
        yanchor 1.0
        zoom _character_active_scale
        alpha 1.0

    ## 右侧-变暗缩小
    transform character_right_dim:
        xalign (0.5 + _character_pair_offset)
        yalign 1.0
        xanchor 0.5
        yanchor 1.0
        zoom _character_dim_scale
        alpha _character_dim_alpha

    ## 安德莉娅（文件名来源：1.png）
    image andrea = im.FactorScale("characters/andrea.png", _character_sprite_scale)
    image andrea neutral = im.FactorScale("characters/andrea.png", _character_sprite_scale)

    ## 茨贝拉（2.png）
    image tsibela = im.FactorScale("characters/tsibela.png", _character_sprite_scale)
    image tsibela neutral = im.FactorScale("characters/tsibela.png", _character_sprite_scale)

    ## 特莉娜（3.png）
    image telina = im.FactorScale("characters/telina.png", _character_sprite_scale)
    image telina neutral = im.FactorScale("characters/telina.png", _character_sprite_scale)

    ## 莫洛拉瓦（4.png）
    image molorava = im.FactorScale("characters/molorava.png", _character_sprite_scale)
    image molorava neutral = im.FactorScale("characters/molorava.png", _character_sprite_scale)

    ## 巴德别特（5.png）
    image badebiete = im.FactorScale("characters/badebiete.png", _character_sprite_scale)
    image badebiete neutral = im.FactorScale("characters/badebiete.png", _character_sprite_scale)
    image badebiete serious = im.FactorScale("characters/badebiete.png", _character_sprite_scale)

    ## 哈夫（6.png）
    image hafu = im.FactorScale("characters/hafu.png", _character_sprite_scale)
    image hafu neutral = im.FactorScale("characters/hafu.png", _character_sprite_scale)

    ## 博莱斯（7.png）
    image bolai = im.FactorScale("characters/bolai.png", _character_sprite_scale)
    image bolai neutral = im.FactorScale("characters/bolai.png", _character_sprite_scale)

    ## 伊蕾娜（8.png）
    image ileina = im.FactorScale("characters/ileina.png", _character_sprite_scale)
    image ileina neutral = im.FactorScale("characters/ileina.png", _character_sprite_scale)

    ## 罗琳达（9.png）
    image rolinda = im.FactorScale("characters/rolinda.png", _character_sprite_scale)
    image rolinda neutral = im.FactorScale("characters/rolinda.png", _character_sprite_scale)
    image rolinda serious = im.FactorScale("characters/rolinda.png", _character_sprite_scale)

    ## 叶蒂娜（10.png）
    image yedina = im.FactorScale("characters/yedina.png", _character_sprite_scale)
    image yedina neutral = im.FactorScale("characters/yedina.png", _character_sprite_scale)
    image yedina sad = im.FactorScale("characters/yedina.png", _character_sprite_scale)

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

    def _get_sprite_image(tag):
        """
        获取角色立绘名称，优先 neutral。
        """
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
            left_transform = character_left_active if left_tag == active else character_left_dim
            renpy.show(_get_sprite_image(left_tag), at_list=[left_transform])

        if len(pair) >= 2:
            right_tag = pair[1]
            right_transform = character_right_active if right_tag == active else character_right_dim
            renpy.show(_get_sprite_image(right_tag), at_list=[right_transform])

    def _set_auto_sprite_active(tag):
        """
        设置当前说话者并更新左右位置。
        """
        if tag not in _auto_sprite_tags:
            return

        pair = [t for t in list(getattr(store, "auto_sprite_pair", [])) if renpy.showing(t)]

        if tag not in pair:
            if len(pair) >= 2:
                pair = [tag]
            else:
                pair.append(tag)

        store.auto_sprite_pair = pair
        store.auto_sprite_active = tag
        _refresh_auto_sprite_pair()

    def make_character_callback(tag):
        """
        生成绑定到指定角色的回调函数。
        """
        def _cb(event, interact=True, **kwargs):
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
                _set_auto_sprite_active(tag)
        return _cb
