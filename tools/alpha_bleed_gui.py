#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实验性 GUI：调参预览 alpha bleed + 软边羽化效果。
左侧参数，右侧显示处理前后动画对比。

依赖：PyQt5 或 PySide6 + Pillow
"""

from __future__ import annotations

import json
import sys
import hashlib
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image, ImageFilter
except Exception as exc:  # pragma: no cover
    print("缺少 Pillow，请先安装：pip install Pillow", file=sys.stderr)
    raise


def _load_qt():
    """按优先级加载 Qt 绑定。"""
    try:
        from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore
        return QtCore, QtGui, QtWidgets
    except Exception:
        try:
            from PySide6 import QtCore, QtGui, QtWidgets  # type: ignore
            return QtCore, QtGui, QtWidgets
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("缺少 PyQt5 或 PySide6") from exc


QtCore, QtGui, QtWidgets = _load_qt()
_Signal = QtCore.pyqtSignal if hasattr(QtCore, "pyqtSignal") else QtCore.Signal
_Slot = QtCore.pyqtSlot if hasattr(QtCore, "pyqtSlot") else QtCore.Slot

BASE_MAP_PATH = Path(__file__).resolve().parent / "alpha_bleed_map.json"
STATE_PATH = Path.home() / ".alpha_bleed_gui_state.json"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_ROOT = Path.home() / ".alpha_bleed_gui_cache"
CACHE_VERSION = 1


def _log(message: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {message}", flush=True)

def _resolve_user_path(text: str) -> Path | None:
    """
    将输入框里的路径解析为实际路径。

    约定：相对路径按仓库根目录（tools/ 的上一层）解析，避免从不同工作目录启动 GUI 时找不到文件。
    """
    raw = text.strip()
    if not raw:
        return None
    p = Path(raw)
    if p.is_absolute():
        return p
    return PROJECT_ROOT / p

def _cache_key(data: dict) -> str:
    """生成用于本地缓存目录的短 key（非安全用途，仅用于稳定命名）。"""
    payload = json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha1(payload).hexdigest()[:16]


def _pixmap_from_pil(image: Image.Image) -> "QtGui.QPixmap":
    """将 PIL.Image 转为 QPixmap，兼容 PyQt5/PySide6。"""
    # 不能依赖 PIL.ImageQt：它可能选择与本脚本不同的 Qt 绑定，导致 QPixmap 创建失败。
    app = QtWidgets.QApplication.instance()
    if app is None:
        raise RuntimeError("未检测到 QApplication，无法渲染预览")

    img = image.convert("RGBA")
    w, h = img.size
    data = img.tobytes("raw", "RGBA")

    qimage = QtGui.QImage(data, w, h, QtGui.QImage.Format_RGBA8888)
    # 绑定数据生命周期，避免 QImage 引用悬空内存
    qimage._pil_bytes = data  # type: ignore[attr-defined]
    return QtGui.QPixmap.fromImage(qimage)

class ZoomableGraphicsView(QtWidgets.QGraphicsView):
    zoom_changed = _Signal(float)

    def __init__(self) -> None:
        super().__init__()
        self._scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self._scene)
        self._item = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._item)
        self._zoom = 1.0

        self.setRenderHints(
            QtGui.QPainter.Antialiasing
            | QtGui.QPainter.SmoothPixmapTransform
            | QtGui.QPainter.TextAntialiasing
        )
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))

    def set_pixmap(self, pixmap: QtGui.QPixmap) -> None:
        self._item.setPixmap(pixmap)
        if pixmap.isNull():
            self._scene.setSceneRect(QtCore.QRectF(0, 0, 0, 0))
            return
        # QGraphicsScene 需要 QRectF，某些 Qt 绑定不会自动把 QRect 转换过去
        self._scene.setSceneRect(QtCore.QRectF(pixmap.rect()))

    def fit(self) -> float:
        if self._item.pixmap().isNull():
            return self._zoom
        self.fitInView(self._item, QtCore.Qt.KeepAspectRatio)
        self._zoom = float(self.transform().m11())
        return self._zoom

    def set_zoom(self, zoom: float) -> None:
        if zoom <= 0:
            return
        if self._item.pixmap().isNull():
            self._zoom = zoom
            return
        current = float(self.transform().m11())
        if current <= 0:
            current = 1.0
        factor = zoom / current
        self.scale(factor, factor)
        self._zoom = float(self.transform().m11())

    def zoom_in(self, step: float = 1.1) -> float:
        self.set_zoom(self._zoom * step)
        return self._zoom

    def zoom_out(self, step: float = 1.1) -> float:
        self.set_zoom(self._zoom / step)
        return self._zoom

    def wheelEvent(self, event) -> None:  # type: ignore[override]
        # Ctrl+滚轮缩放；普通滚轮保持滚动条行为
        if event.modifiers() & QtCore.Qt.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom_in()
            elif delta < 0:
                self.zoom_out()
            try:
                self.zoom_changed.emit(float(self._zoom))
            except Exception:
                pass
            event.accept()
            return
        return super().wheelEvent(event)


def alpha_bleed(image: Image.Image, iterations: int) -> Image.Image:
    """对透明区域做颜色外扩。"""
    if iterations <= 0:
        return image

    img = image.copy()
    w, h = img.size
    pixels = img.load()

    alpha = img.split()[3]
    bbox = alpha.getbbox()
    if not bbox:
        return img
    x0, y0, x1, y1 = bbox
    pad = iterations + 2
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(w, x1 + pad)
    y1 = min(h, y1 + pad)

    for _ in range(iterations):
        new_img = img.copy()
        new_pixels = new_img.load()

        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b, a = pixels[x, y]
                if a != 0:
                    continue

                total_r = total_g = total_b = count = 0
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if nx < 0 or ny < 0 or nx >= w or ny >= h:
                            continue
                        nr, ng, nb, na = pixels[nx, ny]
                        if na > 0:
                            total_r += nr
                            total_g += ng
                            total_b += nb
                            count += 1
                if count > 0:
                    new_pixels[x, y] = (
                        total_r // count,
                        total_g // count,
                        total_b // count,
                        0,
                    )

        img = new_img
        pixels = img.load()

    return img


def feather_alpha(image: Image.Image, radius: float) -> Image.Image:
    """对 alpha 通道做轻度模糊。"""
    if radius <= 0:
        return image
    r, g, b, a = image.split()
    a = a.filter(ImageFilter.GaussianBlur(radius=radius))
    return Image.merge("RGBA", (r, g, b, a))


def apply_base_color(
    overlay: Image.Image,
    base: Image.Image,
    threshold: int,
    resize_if_needed: bool,
    pad: int = 0,
) -> Image.Image:
    """用原立绘颜色覆盖透明/半透明边缘。"""
    if threshold <= 0:
        return overlay

    if overlay.size != base.size:
        if not resize_if_needed:
            raise ValueError(f"尺寸不一致：overlay={overlay.size} base={base.size}")
        base = base.resize(overlay.size, resample=Image.LANCZOS)

    img = overlay.copy()
    w, h = img.size
    pixels = img.load()
    base_pixels = base.load()

    alpha = img.split()[3]
    bbox = alpha.getbbox()
    if not bbox:
        return img

    x0, y0, x1, y1 = bbox
    if pad > 0:
        x0 = max(0, x0 - pad)
        y0 = max(0, y0 - pad)
        x1 = min(w, x1 + pad)
        y1 = min(h, y1 + pad)
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = pixels[x, y]
            if a <= threshold:
                br, bg, bb, _ = base_pixels[x, y]
                pixels[x, y] = (br, bg, bb, a)

    return img


def unmatte_with_base(
    overlay: Image.Image,
    base: Image.Image,
    max_alpha: int,
    min_alpha: int,
    strength: float,
    resize_if_needed: bool,
) -> Image.Image:
    """基于原立绘去底色/去光晕（unmatte），用于消除半透明边缘的亮度不一致。"""
    if max_alpha <= 0 or strength <= 0:
        return overlay

    max_alpha = max(0, min(255, int(max_alpha)))
    min_alpha = max(1, min(255, int(min_alpha)))
    strength = max(0.0, min(1.0, float(strength)))

    if overlay.size != base.size:
        if not resize_if_needed:
            raise ValueError(f"尺寸不一致：overlay={overlay.size} base={base.size}")
        base = base.resize(overlay.size, resample=Image.LANCZOS)

    img = overlay.copy()
    pixels = img.load()
    base_pixels = base.load()

    alpha = img.split()[3]
    bbox = alpha.getbbox()
    if not bbox:
        return img

    x0, y0, x1, y1 = bbox
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = pixels[x, y]
            if a <= 0 or a > max_alpha:
                continue

            br, bg, bb, _ = base_pixels[x, y]
            if a < min_alpha:
                pixels[x, y] = (br, bg, bb, a)
                continue

            af = a / 255.0
            inv = 1.0 - af

            cr = (r - br * inv) / af
            cg = (g - bg * inv) / af
            cb = (b - bb * inv) / af

            cr = 0.0 if cr < 0.0 else 255.0 if cr > 255.0 else cr
            cg = 0.0 if cg < 0.0 else 255.0 if cg > 255.0 else cg
            cb = 0.0 if cb < 0.0 else 255.0 if cb > 255.0 else cb

            nr = r * (1.0 - strength) + cr * strength
            ng = g * (1.0 - strength) + cg * strength
            nb = b * (1.0 - strength) + cb * strength

            pixels[x, y] = (int(round(nr)), int(round(ng)), int(round(nb)), a)

    return img

def compose(base: Image.Image, overlay: Image.Image) -> Image.Image:
    """合成预览。"""
    if base.size != overlay.size:
        base = base.resize(overlay.size, resample=Image.LANCZOS)
    return Image.alpha_composite(base, overlay)


class PreviewWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        _log("GUI 启动")
        self.setWindowTitle("Alpha Bleed 预览工具")
        # 默认窗口尽量大一些（原图较大，预览区域太小会很难看清边缘）
        self.resize(1600, 900)
        self.setMinimumSize(1400, 800)

        self.frames: list[Path] = []
        self.before_frames: list[Image.Image] = []
        self.after_frames: list[Image.Image] = []
        self.frame_index = 0
        self._busy = False
        self._thread = None
        self._worker = None
        self._pending_auto_export = False
        self._pending_auto_export_dir: Path | None = None

        self._base_map = {}
        if BASE_MAP_PATH.exists():
            self._base_map = json.loads(BASE_MAP_PATH.read_text(encoding="utf-8"))
            _log(f"已加载映射文件: {BASE_MAP_PATH}")

        self._build_ui()
        self._bind_events()
        self._load_state()
        self._auto_fill_base()

        self._save_timer = QtCore.QTimer(self)
        self._save_timer.setInterval(400)
        self._save_timer.setSingleShot(True)
        self._save_timer.timeout.connect(self._save_state)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(120)
        self.timer.timeout.connect(self._next_frame)
        self.timer.start()

        self._debounce_timer = QtCore.QTimer(self)
        self._debounce_timer.setInterval(200)
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.timeout.connect(self._rebuild_frames)

    def _build_ui(self) -> None:
        root = QtWidgets.QHBoxLayout(self)

        # 使用 splitter，避免左侧参数挤占右侧预览区域
        self._splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        root.addWidget(self._splitter, 1)

        # 左侧参数区：用滚动区域包裹，避免参数过多时挤出窗口
        panel_content = QtWidgets.QWidget()
        panel = QtWidgets.QVBoxLayout(panel_content)
        panel_scroll = QtWidgets.QScrollArea()
        panel_scroll.setWidgetResizable(True)
        panel_scroll.setWidget(panel_content)
        panel_scroll.setMinimumWidth(320)
        panel_scroll.setMaximumWidth(520)
        self._splitter.addWidget(panel_scroll)

        self.frames_dir_edit = QtWidgets.QLineEdit()
        self.base_image_edit = QtWidgets.QLineEdit()
        self.output_dir_edit = QtWidgets.QLineEdit()

        # 默认路径（尽量用仓库相对路径，避免换机器/换盘符就失效）
        self.frames_dir_edit.setText("game/images/anime/茨贝拉序列帧")
        self.base_image_edit.setText("")
        self.output_dir_edit.setText("")

        panel.addWidget(QtWidgets.QLabel("序列帧目录"))
        panel.addLayout(self._with_button(self.frames_dir_edit, "选择", self._pick_frames_dir))

        panel.addWidget(QtWidgets.QLabel("原立绘路径"))
        panel.addLayout(self._with_button(self.base_image_edit, "选择", self._pick_base_image))

        panel.addWidget(QtWidgets.QLabel("输出目录"))
        panel.addLayout(self._with_button(self.output_dir_edit, "选择", self._pick_output_dir))

        self.bleed_spin = QtWidgets.QSpinBox()
        self.bleed_spin.setRange(0, 6)
        self.bleed_spin.setValue(1)

        self.feather_spin = QtWidgets.QDoubleSpinBox()
        self.feather_spin.setRange(0.0, 2.0)
        self.feather_spin.setSingleStep(0.1)
        self.feather_spin.setValue(0.6)

        self.threshold_spin = QtWidgets.QSpinBox()
        self.threshold_spin.setRange(0, 255)
        self.threshold_spin.setValue(16)

        self.unmatte_check = QtWidgets.QCheckBox("启用 unmatte（去光晕）")
        self.unmatte_check.setChecked(True)

        self.unmatte_max_alpha_spin = QtWidgets.QSpinBox()
        self.unmatte_max_alpha_spin.setRange(0, 255)
        self.unmatte_max_alpha_spin.setValue(220)

        self.unmatte_min_alpha_spin = QtWidgets.QSpinBox()
        self.unmatte_min_alpha_spin.setRange(1, 255)
        self.unmatte_min_alpha_spin.setValue(8)

        self.unmatte_strength_spin = QtWidgets.QDoubleSpinBox()
        self.unmatte_strength_spin.setRange(0.0, 1.0)
        self.unmatte_strength_spin.setSingleStep(0.1)
        self.unmatte_strength_spin.setValue(1.0)

        self.resize_check = QtWidgets.QCheckBox("尺寸不一致时缩放原立绘")
        self.resize_check.setChecked(True)

        self.interval_spin = QtWidgets.QSpinBox()
        self.interval_spin.setRange(30, 500)
        self.interval_spin.setValue(120)

        self.preview_limit_spin = QtWidgets.QSpinBox()
        self.preview_limit_spin.setRange(0, 999)
        self.preview_limit_spin.setValue(12)

        self.preview_scale_spin = QtWidgets.QDoubleSpinBox()
        self.preview_scale_spin.setRange(0.1, 1.0)
        self.preview_scale_spin.setSingleStep(0.05)
        # 默认 1.0：避免“预览看起来很好，但游戏内不同”的误解（0.5 会先把素材缩小一半再处理）
        self.preview_scale_spin.setValue(1.0)

        self.auto_preview_check = QtWidgets.QCheckBox("参数变更自动刷新预览")
        self.auto_preview_check.setChecked(False)

        panel.addWidget(QtWidgets.QLabel("Bleed（颜色外扩）"))
        panel.addWidget(self.bleed_spin)
        panel.addWidget(QtWidgets.QLabel("Feather（羽化半径）"))
        panel.addWidget(self.feather_spin)
        panel.addWidget(QtWidgets.QLabel("Base 阈值（覆盖透明边缘）"))
        panel.addWidget(self.threshold_spin)
        panel.addWidget(self.unmatte_check)
        panel.addWidget(QtWidgets.QLabel("unmatte 最大 alpha"))
        panel.addWidget(self.unmatte_max_alpha_spin)
        panel.addWidget(QtWidgets.QLabel("unmatte 最小 alpha"))
        panel.addWidget(self.unmatte_min_alpha_spin)
        panel.addWidget(QtWidgets.QLabel("unmatte 强度"))
        panel.addWidget(self.unmatte_strength_spin)
        panel.addWidget(self.resize_check)

        panel.addWidget(QtWidgets.QLabel("播放间隔(ms)"))
        panel.addWidget(self.interval_spin)

        panel.addWidget(QtWidgets.QLabel("预览帧数（0=全部，越小越快）"))
        panel.addWidget(self.preview_limit_spin)
        panel.addWidget(QtWidgets.QLabel("预览缩放（仅预览；要和游戏一致请用 1.0）"))
        panel.addWidget(self.preview_scale_spin)
        panel.addWidget(self.auto_preview_check)

        self.refresh_btn = QtWidgets.QPushButton("刷新预览")
        self.export_btn = QtWidgets.QPushButton("导出处理结果")
        self.auto_export_check = QtWidgets.QCheckBox("预览完成后自动导出（耗时）")
        self.auto_export_check.setChecked(False)
        self.skip_existing_check = QtWidgets.QCheckBox("导出时跳过已存在文件（可断点续跑）")
        self.skip_existing_check.setChecked(False)
        self.cancel_btn = QtWidgets.QPushButton("取消")
        self.cancel_btn.setEnabled(False)
        panel.addWidget(self.refresh_btn)
        panel.addWidget(self.export_btn)
        panel.addWidget(self.auto_export_check)
        panel.addWidget(self.skip_existing_check)
        panel.addWidget(self.cancel_btn)

        panel.addStretch(1)

        # 右侧预览
        preview_widget = QtWidgets.QWidget()
        preview = QtWidgets.QVBoxLayout(preview_widget)
        self._splitter.addWidget(preview_widget)
        self._splitter.setStretchFactor(0, 0)
        self._splitter.setStretchFactor(1, 1)
        self._splitter.setSizes([420, 1180])

        preview_controls = QtWidgets.QHBoxLayout()
        preview_controls.addWidget(QtWidgets.QLabel("预览缩放（Ctrl+滚轮也可）"))
        self.view_zoom_spin = QtWidgets.QDoubleSpinBox()
        self.view_zoom_spin.setRange(0.1, 3.0)
        self.view_zoom_spin.setSingleStep(0.1)
        self.view_zoom_spin.setValue(1.0)
        preview_controls.addWidget(self.view_zoom_spin)
        self.view_fit_btn = QtWidgets.QPushButton("适应窗口")
        self.view_100_btn = QtWidgets.QPushButton("100%")
        preview_controls.addWidget(self.view_fit_btn)
        preview_controls.addWidget(self.view_100_btn)
        self.view_sync_scroll_check = QtWidgets.QCheckBox("同步滚动")
        self.view_sync_scroll_check.setChecked(True)
        preview_controls.addWidget(self.view_sync_scroll_check)
        preview_controls.addStretch(1)
        preview.addLayout(preview_controls)

        header = QtWidgets.QHBoxLayout()
        self.before_label = QtWidgets.QLabel("处理前")
        self.after_label = QtWidgets.QLabel("处理后")
        self.before_label.setAlignment(QtCore.Qt.AlignCenter)
        self.after_label.setAlignment(QtCore.Qt.AlignCenter)
        header.addWidget(self.before_label, 1)
        header.addWidget(self.after_label, 1)
        preview.addLayout(header)

        body = QtWidgets.QHBoxLayout()
        self.before_view = ZoomableGraphicsView()
        self.after_view = ZoomableGraphicsView()
        self.before_view.setMinimumSize(600, 650)
        self.after_view.setMinimumSize(600, 650)
        body.addWidget(self.before_view, 1)
        body.addWidget(self.after_view, 1)
        preview.addLayout(body)

        self.status_label = QtWidgets.QLabel("等待加载…")
        preview.addWidget(self.status_label)

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        preview.addWidget(self.progress_bar)

    def _with_button(self, line: QtWidgets.QLineEdit, text: str, cb) -> QtWidgets.QHBoxLayout:
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(line, 1)
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(cb)
        layout.addWidget(button)
        return layout

    def _bind_events(self) -> None:
        self.refresh_btn.clicked.connect(self._rebuild_frames)
        self.export_btn.clicked.connect(self._export_frames)
        self.cancel_btn.clicked.connect(self._cancel_current_task)
        self.interval_spin.valueChanged.connect(self._update_interval)
        self.view_zoom_spin.valueChanged.connect(self._apply_view_zoom)
        self.view_fit_btn.clicked.connect(self._fit_views)
        self.view_100_btn.clicked.connect(lambda: self._set_view_zoom(1.0))
        self.view_sync_scroll_check.stateChanged.connect(self._schedule_save)
        self.before_view.zoom_changed.connect(self._on_zoom_from_before)
        self.after_view.zoom_changed.connect(self._on_zoom_from_after)
        self.before_view.horizontalScrollBar().valueChanged.connect(self._sync_scroll_from_before)
        self.before_view.verticalScrollBar().valueChanged.connect(self._sync_scroll_from_before)
        self.after_view.horizontalScrollBar().valueChanged.connect(self._sync_scroll_from_after)
        self.after_view.verticalScrollBar().valueChanged.connect(self._sync_scroll_from_after)
        if hasattr(self, "_splitter") and self._splitter is not None:
            self._splitter.splitterMoved.connect(lambda *_: self._schedule_save())

        self.bleed_spin.valueChanged.connect(self._schedule_rebuild)
        self.feather_spin.valueChanged.connect(self._schedule_rebuild)
        self.threshold_spin.valueChanged.connect(self._schedule_rebuild)
        self.unmatte_check.stateChanged.connect(self._schedule_rebuild)
        self.unmatte_max_alpha_spin.valueChanged.connect(self._schedule_rebuild)
        self.unmatte_min_alpha_spin.valueChanged.connect(self._schedule_rebuild)
        self.unmatte_strength_spin.valueChanged.connect(self._schedule_rebuild)
        self.resize_check.stateChanged.connect(self._schedule_rebuild)
        self.preview_limit_spin.valueChanged.connect(self._schedule_rebuild)
        self.preview_scale_spin.valueChanged.connect(self._schedule_rebuild)
        self.frames_dir_edit.textChanged.connect(self._auto_fill_base)
        self.frames_dir_edit.textChanged.connect(self._schedule_save)
        self.base_image_edit.textChanged.connect(self._schedule_save)
        self.output_dir_edit.textChanged.connect(self._schedule_save)
        self.auto_preview_check.stateChanged.connect(self._schedule_save)
        self.auto_export_check.stateChanged.connect(self._schedule_save)
        self.skip_existing_check.stateChanged.connect(self._schedule_save)

    def _pick_frames_dir(self) -> None:
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择序列帧目录")
        if path:
            self.frames_dir_edit.setText(path)
            _log(f"选择序列帧目录: {path}")
            self._auto_fill_output(Path(path))
            self._schedule_rebuild()

    def _pick_base_image(self) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择原立绘", filter="PNG (*.png)")
        if path:
            self.base_image_edit.setText(path)
            _log(f"选择原立绘: {path}")
            self._schedule_rebuild()

    def _pick_output_dir(self) -> None:
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择输出目录")
        if path:
            self.output_dir_edit.setText(path)
            _log(f"选择输出目录: {path}")

    def _schedule_save(self) -> None:
        """参数变化时延迟保存，避免频繁写盘。"""
        if hasattr(self, "_save_timer") and self._save_timer is not None:
            self._save_timer.start()

    def _auto_fill_base(self) -> None:
        frames_dir = _resolve_user_path(self.frames_dir_edit.text())
        if not frames_dir or not frames_dir.exists():
            return
        root_name = frames_dir.name
        if root_name in self._base_map and not self.base_image_edit.text().strip():
            self.base_image_edit.setText(self._base_map[root_name])
            _log(f"自动填充原立绘: {self._base_map[root_name]}")
        self._auto_fill_output(frames_dir)

    def _auto_fill_output(self, frames_dir: Path) -> None:
        if self.output_dir_edit.text().strip():
            return
        parent = frames_dir.parent
        if parent.name.lower() == "anime":
            output_dir = parent.parent / "anime_processed" / frames_dir.name
        else:
            output_dir = parent / f"{frames_dir.name}_processed"
        self.output_dir_edit.setText(str(output_dir))
        _log(f"自动填充输出目录: {output_dir}")

    def _schedule_rebuild(self) -> None:
        if not self.auto_preview_check.isChecked():
            self.status_label.setText("参数已修改，点击“刷新预览”应用")
            self._schedule_save()
            return
        self._debounce_timer.start()
        self._schedule_save()

    def _update_interval(self, value: int) -> None:
        self.timer.setInterval(value)
        _log(f"播放间隔调整为 {value}ms")

    def _set_progress(self, done: int, total: int, prefix: str) -> None:
        if total <= 0:
            self.progress_bar.setValue(0)
            self.progress_bar.setFormat("")
            return
        pct = int(round(done * 100 / total))
        self.progress_bar.setValue(pct)
        self.progress_bar.setFormat(f"{prefix} {done}/{total}（{pct}%）")

    def _cancel_current_task(self) -> None:
        if not self._worker:
            return
        _log("请求取消当前任务")
        self.status_label.setText("正在取消...")
        try:
            QtCore.QMetaObject.invokeMethod(self._worker, "cancel", QtCore.Qt.QueuedConnection)
        except Exception:
            # 兜底：取消仅仅是一个布尔标记，即使 invoke 失败也不应导致崩溃
            pass

    def _rebuild_frames(self) -> None:
        frames_dir = _resolve_user_path(self.frames_dir_edit.text())
        base_path = _resolve_user_path(self.base_image_edit.text()) if self.base_image_edit.text().strip() else None

        if not frames_dir or not frames_dir.exists():
            self.status_label.setText("序列帧目录无效")
            _log("序列帧目录无效")
            return
        if base_path and not base_path.exists():
            self.status_label.setText("原立绘路径无效")
            _log("原立绘路径无效")
            return

        self.frames = sorted(frames_dir.glob("*.png"))
        if not self.frames:
            self.status_label.setText("未找到任何序列帧")
            _log("未找到任何序列帧")
            return

        if self._busy:
            _log("正在处理，忽略新的刷新请求")
            return

        self._busy = True
        self.refresh_btn.setEnabled(False)
        self.export_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.status_label.setText("处理中...")
        _log("开始构建预览帧（后台线程）")

        bleed = int(self.bleed_spin.value())
        feather = float(self.feather_spin.value())
        threshold = int(self.threshold_spin.value())
        unmatte = bool(self.unmatte_check.isChecked())
        unmatte_max_alpha = int(self.unmatte_max_alpha_spin.value())
        unmatte_min_alpha = int(self.unmatte_min_alpha_spin.value())
        unmatte_strength = float(self.unmatte_strength_spin.value())
        resize_if_needed = bool(self.resize_check.isChecked())
        preview_limit = int(self.preview_limit_spin.value())
        preview_scale = float(self.preview_scale_spin.value())

        self._thread = QtCore.QThread(self)
        self._worker = FrameBuildWorker(
            frames_dir=frames_dir,
            base_path=base_path,
            bleed=bleed,
            feather=feather,
            threshold=threshold,
            unmatte=unmatte,
            unmatte_max_alpha=unmatte_max_alpha,
            unmatte_min_alpha=unmatte_min_alpha,
            unmatte_strength=unmatte_strength,
            resize_if_needed=resize_if_needed,
            preview_limit=preview_limit,
            preview_scale=preview_scale,
        )
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_build_finished, QtCore.Qt.QueuedConnection)
        self._worker.error.connect(self._on_build_error, QtCore.Qt.QueuedConnection)
        self._worker.progress.connect(self._on_worker_progress, QtCore.Qt.QueuedConnection)
        self._worker.finished.connect(self._thread.quit, QtCore.Qt.QueuedConnection)
        self._worker.error.connect(self._thread.quit, QtCore.Qt.QueuedConnection)
        self._thread.finished.connect(self._cleanup_worker)
        self._thread.start()

    def _next_frame(self) -> None:
        if not self.before_frames:
            return
        self.frame_index = (self.frame_index + 1) % len(self.before_frames)
        self._request_render()

    @_Slot()
    def _render_frame(self) -> None:
        if QtCore.QThread.currentThread() != self.thread():
            QtCore.QMetaObject.invokeMethod(self, "_render_frame", QtCore.Qt.QueuedConnection)
            return
        if not self.before_frames or not self.after_frames:
            return
        try:
            before = self.before_frames[self.frame_index]
            after = self.after_frames[self.frame_index]

            before_px = _pixmap_from_pil(before)
            after_px = _pixmap_from_pil(after)

            self.before_view.set_pixmap(before_px)
            self.after_view.set_pixmap(after_px)

            if getattr(self, "_view_fit_mode", True):
                self._fit_views(update_spin=True)
            else:
                self._apply_view_zoom()
        except Exception as exc:
            self.status_label.setText(f"预览渲染失败：{exc}")
            _log(f"预览渲染失败：{exc}")
            # 渲染失败时停止刷新，避免刷屏/崩溃
            try:
                self.timer.stop()
            except Exception:
                pass
            try:
                self.before_view.set_pixmap(QtGui.QPixmap())
                self.after_view.set_pixmap(QtGui.QPixmap())
            except Exception:
                pass

    def _request_render(self) -> None:
        QtCore.QMetaObject.invokeMethod(self, "_render_frame", QtCore.Qt.QueuedConnection)

    def _update_view_zoom_spin(self, zoom: float) -> None:
        blockers = [QtCore.QSignalBlocker(self.view_zoom_spin)]
        try:
            self.view_zoom_spin.setValue(float(zoom))
        finally:
            del blockers

    def _set_view_zoom(self, zoom: float) -> None:
        self._view_fit_mode = False
        self._update_view_zoom_spin(zoom)
        self._apply_view_zoom()

    def _apply_view_zoom(self) -> None:
        self._view_fit_mode = False
        zoom = float(self.view_zoom_spin.value())
        self.before_view.set_zoom(zoom)
        self.after_view.set_zoom(zoom)
        self._schedule_save()

    def _fit_views(self, update_spin: bool = True) -> None:
        self._view_fit_mode = True
        z1 = self.before_view.fit()
        z2 = self.after_view.fit()
        zoom = min(z1, z2) if z1 and z2 else z1 or z2 or 1.0
        if update_spin:
            self._update_view_zoom_spin(zoom)

    def _on_zoom_from_before(self, zoom: float) -> None:
        """Ctrl+滚轮缩放后：退出“适应窗口”模式，并同步到另一侧预览。"""
        try:
            self._view_fit_mode = False
            self._update_view_zoom_spin(float(zoom))
            self.after_view.set_zoom(float(zoom))
            self._schedule_save()
        except Exception:
            pass

    def _on_zoom_from_after(self, zoom: float) -> None:
        """Ctrl+滚轮缩放后：退出“适应窗口”模式，并同步到另一侧预览。"""
        try:
            self._view_fit_mode = False
            self._update_view_zoom_spin(float(zoom))
            self.before_view.set_zoom(float(zoom))
            self._schedule_save()
        except Exception:
            pass

    def _sync_scroll_from_before(self) -> None:
        if not self.view_sync_scroll_check.isChecked():
            return
        hb = self.before_view.horizontalScrollBar()
        vb = self.before_view.verticalScrollBar()
        ha = self.after_view.horizontalScrollBar()
        va = self.after_view.verticalScrollBar()
        blockers = [QtCore.QSignalBlocker(ha), QtCore.QSignalBlocker(va)]
        try:
            ha.setValue(hb.value())
            va.setValue(vb.value())
        finally:
            del blockers

    def _sync_scroll_from_after(self) -> None:
        if not self.view_sync_scroll_check.isChecked():
            return
        hb = self.before_view.horizontalScrollBar()
        vb = self.before_view.verticalScrollBar()
        ha = self.after_view.horizontalScrollBar()
        va = self.after_view.verticalScrollBar()
        blockers = [QtCore.QSignalBlocker(hb), QtCore.QSignalBlocker(vb)]
        try:
            hb.setValue(ha.value())
            vb.setValue(va.value())
        finally:
            del blockers


    def _export_frames(self) -> None:
        output_dir = _resolve_user_path(self.output_dir_edit.text())
        if not output_dir:
            self.status_label.setText("请先选择输出目录")
            _log("导出失败：未选择输出目录")
            return
        if not self.frames:
            self.status_label.setText("请先加载序列帧")
            _log("导出失败：未加载序列帧")
            return

        if self._busy:
            _log("正在处理，忽略导出请求")
            return

        self._start_export(output_dir, auto=False)

    def _start_export(self, output_dir: Path, auto: bool) -> None:
        if self._busy:
            return

        base_path_text = self.base_image_edit.text().strip()
        if not base_path_text:
            self.status_label.setText("导出需要原立绘路径")
            _log("导出失败：缺少原立绘路径")
            return
        base_path = _resolve_user_path(base_path_text)
        if not base_path or not base_path.exists():
            self.status_label.setText("原立绘路径无效")
            _log("导出失败：原立绘路径无效")
            return

        output_dir.mkdir(parents=True, exist_ok=True)

        bleed = int(self.bleed_spin.value())
        feather = float(self.feather_spin.value())
        threshold = int(self.threshold_spin.value())
        unmatte = bool(self.unmatte_check.isChecked())
        unmatte_max_alpha = int(self.unmatte_max_alpha_spin.value())
        unmatte_min_alpha = int(self.unmatte_min_alpha_spin.value())
        unmatte_strength = float(self.unmatte_strength_spin.value())
        resize_if_needed = bool(self.resize_check.isChecked())
        skip_existing = bool(self.skip_existing_check.isChecked())

        base = Image.open(base_path).convert("RGBA")

        self._busy = True
        self.refresh_btn.setEnabled(False)
        self.export_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.status_label.setText("导出中..." if not auto else "自动导出中...")

        self._thread = QtCore.QThread(self)
        self._worker = ExportWorker(
            frames=list(self.frames),
            output_dir=output_dir,
            base=base,
            bleed=bleed,
            feather=feather,
            threshold=threshold,
            unmatte=unmatte,
            unmatte_max_alpha=unmatte_max_alpha,
            unmatte_min_alpha=unmatte_min_alpha,
            unmatte_strength=unmatte_strength,
            resize_if_needed=resize_if_needed,
            skip_existing=skip_existing,
        )
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_export_finished, QtCore.Qt.QueuedConnection)
        self._worker.error.connect(self._on_export_error, QtCore.Qt.QueuedConnection)
        self._worker.progress.connect(self._on_worker_progress, QtCore.Qt.QueuedConnection)
        self._worker.finished.connect(self._thread.quit, QtCore.Qt.QueuedConnection)
        self._worker.error.connect(self._thread.quit, QtCore.Qt.QueuedConnection)
        self._thread.finished.connect(self._cleanup_worker)
        self._thread.start()

    def _on_build_finished(self, before_frames, after_frames) -> None:
        self.before_frames = before_frames
        self.after_frames = after_frames
        self.frame_index = 0
        self.status_label.setText(f"已加载 {len(self.before_frames)} 帧")
        _log(f"已加载 {len(self.before_frames)} 帧，开始预览")
        self._set_progress(len(self.before_frames), len(self.before_frames), "预览")
        self._request_render()
        if self.auto_export_check.isChecked() and self.output_dir_edit.text().strip():
            output_dir = _resolve_user_path(self.output_dir_edit.text())
            if output_dir:
                _log("自动导出已开启：等待预览线程结束后导出")
                self._pending_auto_export = True
                self._pending_auto_export_dir = output_dir

    def _on_build_error(self, message: str) -> None:
        self.status_label.setText(f"处理失败：{message}")
        _log(f"处理失败：{message}")

    def _on_export_finished(self) -> None:
        self.status_label.setText("导出完成")
        _log("导出完成")
        self._set_progress(len(self.frames), len(self.frames), "导出")

    def _on_export_error(self, message: str) -> None:
        self.status_label.setText(f"导出失败：{message}")
        _log(f"导出失败：{message}")

    def _on_worker_progress(self, done: int, total: int, prefix: str) -> None:
        self._set_progress(done, total, prefix)
        if total > 0:
            self.status_label.setText(f"{prefix}处理中 {done}/{total}…")

    def _cleanup_worker(self) -> None:
        self._worker = None
        self._thread = None
        self._busy = False
        self.refresh_btn.setEnabled(True)
        self.export_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        if self._pending_auto_export and self._pending_auto_export_dir:
            output_dir = self._pending_auto_export_dir
            self._pending_auto_export = False
            self._pending_auto_export_dir = None
            _log("触发自动导出")
            self._start_export(output_dir, auto=True)

    def closeEvent(self, event) -> None:  # type: ignore[override]
        # 关闭窗口时保存状态，避免异常退出导致参数丢失
        self._save_state()
        return super().closeEvent(event)

    def _collect_state(self) -> dict:
        state = {
            "frames_dir": self.frames_dir_edit.text(),
            "base_image": self.base_image_edit.text(),
            "output_dir": self.output_dir_edit.text(),
            "bleed": int(self.bleed_spin.value()),
            "feather": float(self.feather_spin.value()),
            "threshold": int(self.threshold_spin.value()),
            "unmatte": bool(self.unmatte_check.isChecked()),
            "unmatte_max_alpha": int(self.unmatte_max_alpha_spin.value()),
            "unmatte_min_alpha": int(self.unmatte_min_alpha_spin.value()),
            "unmatte_strength": float(self.unmatte_strength_spin.value()),
            "resize_if_needed": bool(self.resize_check.isChecked()),
            "interval_ms": int(self.interval_spin.value()),
            "preview_limit": int(self.preview_limit_spin.value()),
            "preview_scale": float(self.preview_scale_spin.value()),
            "auto_preview": bool(self.auto_preview_check.isChecked()),
            "auto_export": bool(self.auto_export_check.isChecked()),
            "skip_existing": bool(self.skip_existing_check.isChecked()),
        }
        if hasattr(self, "_splitter") and self._splitter is not None:
            try:
                state["splitter_sizes"] = list(self._splitter.sizes())
            except Exception:
                pass
        state["view_zoom"] = float(self.view_zoom_spin.value())
        state["view_fit"] = bool(getattr(self, "_view_fit_mode", True))
        state["view_sync_scroll"] = bool(self.view_sync_scroll_check.isChecked())
        return state

    def _apply_state(self, state: dict) -> None:
        blockers = [
            QtCore.QSignalBlocker(self.frames_dir_edit),
            QtCore.QSignalBlocker(self.base_image_edit),
            QtCore.QSignalBlocker(self.output_dir_edit),
            QtCore.QSignalBlocker(self.bleed_spin),
            QtCore.QSignalBlocker(self.feather_spin),
            QtCore.QSignalBlocker(self.threshold_spin),
            QtCore.QSignalBlocker(self.unmatte_check),
            QtCore.QSignalBlocker(self.unmatte_max_alpha_spin),
            QtCore.QSignalBlocker(self.unmatte_min_alpha_spin),
            QtCore.QSignalBlocker(self.unmatte_strength_spin),
            QtCore.QSignalBlocker(self.resize_check),
            QtCore.QSignalBlocker(self.interval_spin),
            QtCore.QSignalBlocker(self.preview_limit_spin),
            QtCore.QSignalBlocker(self.preview_scale_spin),
            QtCore.QSignalBlocker(self.auto_preview_check),
            QtCore.QSignalBlocker(self.auto_export_check),
            QtCore.QSignalBlocker(self.skip_existing_check),
            QtCore.QSignalBlocker(self.view_zoom_spin),
            QtCore.QSignalBlocker(self.view_sync_scroll_check),
        ]
        try:
            if "frames_dir" in state:
                self.frames_dir_edit.setText(str(state["frames_dir"]))
            if "base_image" in state:
                self.base_image_edit.setText(str(state["base_image"]))
            if "output_dir" in state:
                self.output_dir_edit.setText(str(state["output_dir"]))

            if "bleed" in state:
                self.bleed_spin.setValue(int(state["bleed"]))
            if "feather" in state:
                self.feather_spin.setValue(float(state["feather"]))
            if "threshold" in state:
                self.threshold_spin.setValue(int(state["threshold"]))

            if "unmatte" in state:
                self.unmatte_check.setChecked(bool(state["unmatte"]))
            if "unmatte_max_alpha" in state:
                self.unmatte_max_alpha_spin.setValue(int(state["unmatte_max_alpha"]))
            if "unmatte_min_alpha" in state:
                self.unmatte_min_alpha_spin.setValue(int(state["unmatte_min_alpha"]))
            if "unmatte_strength" in state:
                self.unmatte_strength_spin.setValue(float(state["unmatte_strength"]))

            if "resize_if_needed" in state:
                self.resize_check.setChecked(bool(state["resize_if_needed"]))
            if "interval_ms" in state:
                self.interval_spin.setValue(int(state["interval_ms"]))

            if "preview_limit" in state:
                self.preview_limit_spin.setValue(int(state["preview_limit"]))
            if "preview_scale" in state:
                self.preview_scale_spin.setValue(float(state["preview_scale"]))
            if "auto_preview" in state:
                self.auto_preview_check.setChecked(bool(state["auto_preview"]))

            if "auto_export" in state:
                self.auto_export_check.setChecked(bool(state["auto_export"]))
            if "skip_existing" in state:
                self.skip_existing_check.setChecked(bool(state["skip_existing"]))
            if "splitter_sizes" in state and hasattr(self, "_splitter") and self._splitter is not None:
                try:
                    sizes = state["splitter_sizes"]
                    if isinstance(sizes, list) and len(sizes) == 2:
                        self._splitter.setSizes([int(sizes[0]), int(sizes[1])])
                except Exception:
                    pass
            if "view_zoom" in state:
                self.view_zoom_spin.setValue(float(state["view_zoom"]))
            if "view_fit" in state:
                self._view_fit_mode = bool(state["view_fit"])
            if "view_sync_scroll" in state:
                self.view_sync_scroll_check.setChecked(bool(state["view_sync_scroll"]))
        finally:
            # 显式释放 blocker，避免被误用
            del blockers

    def _load_state(self) -> None:
        try:
            if not STATE_PATH.exists():
                return
            state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
            if isinstance(state, dict):
                self._apply_state(state)
                _log(f"已加载上次状态: {STATE_PATH}")
        except Exception as exc:
            _log(f"加载状态失败（忽略）：{exc}")

    def _save_state(self) -> None:
        try:
            STATE_PATH.write_text(
                json.dumps(self._collect_state(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            _log(f"已保存状态: {STATE_PATH}")
        except Exception as exc:
            _log(f"保存状态失败（忽略）：{exc}")


class FrameBuildWorker(QtCore.QObject):
    finished = _Signal(object, object)
    error = _Signal(str)
    progress = _Signal(int, int, str)

    def __init__(
        self,
        frames_dir: Path,
        base_path: Path | None,
        bleed: int,
        feather: float,
        threshold: int,
        unmatte: bool,
        unmatte_max_alpha: int,
        unmatte_min_alpha: int,
        unmatte_strength: float,
        resize_if_needed: bool,
        preview_limit: int,
        preview_scale: float,
    ) -> None:
        super().__init__()
        self.frames_dir = frames_dir
        self.base_path = base_path
        self.bleed = bleed
        self.feather = feather
        self.threshold = threshold
        self.unmatte = unmatte
        self.unmatte_max_alpha = unmatte_max_alpha
        self.unmatte_min_alpha = unmatte_min_alpha
        self.unmatte_strength = unmatte_strength
        self.resize_if_needed = resize_if_needed
        self.preview_limit = preview_limit
        self.preview_scale = preview_scale
        self._cancelled = False

    @_Slot()
    def cancel(self) -> None:
        self._cancelled = True

    def run(self) -> None:
        try:
            frames = sorted(self.frames_dir.glob("*.png"))
            if not frames:
                self.error.emit("未找到任何序列帧")
                return

            base = Image.open(self.base_path).convert("RGBA") if self.base_path else None
            if base and self.preview_scale < 1.0:
                w, h = base.size
                base = base.resize((int(w * self.preview_scale), int(h * self.preview_scale)), resample=Image.LANCZOS)

            cache_before_dir: Path | None = None
            cache_after_dir: Path | None = None
            try:
                key_data = {
                    "v": CACHE_VERSION,
                    "frames_dir": str(self.frames_dir.resolve()),
                    "base_path": str(self.base_path.resolve()) if self.base_path else "",
                    "bleed": int(self.bleed),
                    "feather": float(self.feather),
                    "threshold": int(self.threshold),
                    "unmatte": bool(self.unmatte),
                    "unmatte_max_alpha": int(self.unmatte_max_alpha),
                    "unmatte_min_alpha": int(self.unmatte_min_alpha),
                    "unmatte_strength": float(self.unmatte_strength),
                    "resize_if_needed": bool(self.resize_if_needed),
                    "preview_scale": float(self.preview_scale),
                }
                key = _cache_key(key_data)
                cache_dir = CACHE_ROOT / key
                cache_before_dir = cache_dir / "before"
                cache_after_dir = cache_dir / "after"
                cache_before_dir.mkdir(parents=True, exist_ok=True)
                cache_after_dir.mkdir(parents=True, exist_ok=True)
                _log(f"预览缓存目录: {cache_dir}")
            except Exception as exc:
                cache_before_dir = None
                cache_after_dir = None
                _log(f"创建预览缓存目录失败（将不缓存）：{exc}")

            # 预览只抽样部分帧，避免每次调参都跑完整序列
            if self.preview_limit and self.preview_limit > 0 and len(frames) > self.preview_limit:
                keep = self.preview_limit
                if keep == 1:
                    frames = [frames[0]]
                else:
                    last = len(frames) - 1
                    indices = [int(round(i * last / (keep - 1))) for i in range(keep)]
                    frames = [frames[i] for i in indices]

            before_frames = []
            after_frames = []

            total = len(frames)
            self.progress.emit(0, total, "预览")
            for idx, frame in enumerate(frames, start=1):
                if self._cancelled:
                    self.error.emit("已取消")
                    return

                before_path = (cache_before_dir / frame.name) if cache_before_dir else None
                after_path = (cache_after_dir / frame.name) if cache_after_dir else None

                before_cached = bool(before_path and before_path.exists())
                after_cached = bool(after_path and after_path.exists())

                overlay: Image.Image | None = None
                base_for_compose: Image.Image | None = None
                if not before_cached or not after_cached:
                    overlay = Image.open(frame).convert("RGBA")
                    if self.preview_scale < 1.0:
                        w, h = overlay.size
                        overlay = overlay.resize(
                            (int(w * self.preview_scale), int(h * self.preview_scale)),
                            resample=Image.LANCZOS,
                        )
                    base_for_compose = base if base else overlay

                # 处理前
                if before_cached:
                    before_img = Image.open(before_path).convert("RGBA")  # type: ignore[arg-type]
                else:
                    assert overlay is not None and base_for_compose is not None
                    before_img = compose(base_for_compose, overlay)
                    if before_path:
                        try:
                            before_img.save(before_path)
                        except Exception as exc:
                            _log(f"保存预览缓存失败（before）：{before_path} {exc}")

                # 处理后
                if after_cached:
                    after_img = Image.open(after_path).convert("RGBA")  # type: ignore[arg-type]
                else:
                    assert overlay is not None and base_for_compose is not None
                    overlay_after = overlay.copy()
                    if base and self.unmatte:
                        overlay_after = unmatte_with_base(
                            overlay_after,
                            base,
                            max_alpha=self.unmatte_max_alpha,
                            min_alpha=self.unmatte_min_alpha,
                            strength=self.unmatte_strength,
                            resize_if_needed=self.resize_if_needed,
                        )
                    overlay_after = alpha_bleed(overlay_after, self.bleed)
                    overlay_after = feather_alpha(overlay_after, self.feather)
                    if base:
                        pad = max(self.bleed + 2, int(self.feather * 3) + 2)
                        overlay_after = apply_base_color(
                            overlay_after,
                            base,
                            self.threshold,
                            self.resize_if_needed,
                            pad=pad,
                        )
                    after_img = compose(base_for_compose, overlay_after)
                    if after_path:
                        try:
                            after_img.save(after_path)
                        except Exception as exc:
                            _log(f"保存预览缓存失败（after）：{after_path} {exc}")

                before_frames.append(before_img)
                after_frames.append(after_img)
                self.progress.emit(idx, total, "预览")

            self.finished.emit(before_frames, after_frames)
        except Exception as exc:  # pragma: no cover
            self.error.emit(str(exc))


class ExportWorker(QtCore.QObject):
    finished = _Signal()
    error = _Signal(str)
    progress = _Signal(int, int, str)

    def __init__(
        self,
        frames: list[Path],
        output_dir: Path,
        base: Image.Image,
        bleed: int,
        feather: float,
        threshold: int,
        unmatte: bool,
        unmatte_max_alpha: int,
        unmatte_min_alpha: int,
        unmatte_strength: float,
        resize_if_needed: bool,
        skip_existing: bool,
    ) -> None:
        super().__init__()
        self.frames = frames
        self.output_dir = output_dir
        self.base = base
        self.bleed = bleed
        self.feather = feather
        self.threshold = threshold
        self.unmatte = unmatte
        self.unmatte_max_alpha = unmatte_max_alpha
        self.unmatte_min_alpha = unmatte_min_alpha
        self.unmatte_strength = unmatte_strength
        self.resize_if_needed = resize_if_needed
        self.skip_existing = skip_existing
        self._cancelled = False

    @_Slot()
    def cancel(self) -> None:
        self._cancelled = True

    def run(self) -> None:
        try:
            _log(f"开始导出，共 {len(self.frames)} 帧")
            self.output_dir.mkdir(parents=True, exist_ok=True)
            total = len(self.frames)
            self.progress.emit(0, total, "导出")
            for idx, frame in enumerate(self.frames, start=1):
                if self._cancelled:
                    self.error.emit("已取消")
                    return

                out_path = self.output_dir / frame.name
                if self.skip_existing and out_path.exists():
                    self.progress.emit(idx, total, "导出")
                    continue

                overlay = Image.open(frame).convert("RGBA")
                if self.unmatte:
                    overlay = unmatte_with_base(
                        overlay,
                        self.base,
                        max_alpha=self.unmatte_max_alpha,
                        min_alpha=self.unmatte_min_alpha,
                        strength=self.unmatte_strength,
                        resize_if_needed=self.resize_if_needed,
                    )
                overlay = alpha_bleed(overlay, self.bleed)
                overlay = feather_alpha(overlay, self.feather)
                pad = max(self.bleed + 2, int(self.feather * 3) + 2)
                overlay = apply_base_color(overlay, self.base, self.threshold, self.resize_if_needed, pad=pad)

                out_path.parent.mkdir(parents=True, exist_ok=True)
                overlay.save(out_path)
                self.progress.emit(idx, total, "导出")
            self.finished.emit()
        except Exception as exc:  # pragma: no cover
            self.error.emit(str(exc))


def main() -> int:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    window = PreviewWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
