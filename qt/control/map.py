from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtWidgets import QWidget, QScrollArea, QCheckBox, QVBoxLayout, QSlider, QGraphicsScene, QGraphicsPixmapItem, \
    QLabel, QGraphicsView, QGraphicsRectItem

from qt.common.q_shared_menu import QSharedMenuSection
from qt.control.common import QControl


class QGraphicsMapItem(QGraphicsPixmapItem):

    def __init__(self, pixmap: QPixmap, control):
        super().__init__(pixmap)
        self.control = control
        self.a_show = QAction("Show")
        self.a_show.triggered.connect(lambda: self.control.check_box.toggle())
        self.a_hide = QAction("Hide")
        self.a_hide.triggered.connect(lambda: self.control.check_box.toggle())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton and self.control.context_menu_enabled():
            section = QSharedMenuSection("Map", [], self.control.context_menu_priority, False)
            if self.control.check_box.isChecked():
                section.append(self.a_hide)
            else:
                section.append(self.a_show)
            event.shared_menu.add_section(section)

        super().mousePressEvent(event)


class QMapControl(QControl):
    def __init__(self, parent, scene: QGraphicsScene, dvm, bgnd):
        super().__init__(parent, scene)
        self.dvm = dvm
        self.bgnd = bgnd
        self.wf = self.dvm.level_map.size().width() / self.bgnd.minimap.size().width()
        self.hf = self.dvm.level_map.size().height() / self.bgnd.minimap.size().height()
        self.scene.viewport().view_changed.connect(self.refresh_minimap)
        self.init_ui()

        self.graphic_map_item = QGraphicsMapItem(QPixmap(self.dvm.level_map), self)
        self.scene.addItem(self.graphic_map_item)
        self.graphic_map_item.setVisible(self.check_box.isChecked())

    def init_ui(self):
        content = QWidget()
        layout = QVBoxLayout(content)

        self.check_box = QCheckBox("Show Map")
        self.check_box.setCheckState(Qt.CheckState.Checked)
        self.check_box.stateChanged.connect(self.update)
        layout.addWidget(self.check_box)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(255)
        self.slider.setValue(255)
        self.slider.valueChanged.connect(self.update)
        layout.addWidget(self.slider)

        layout.addStretch(1)

        self.minimap_scene = QGraphicsScene()
        mf = 0.3  # marge factor
        self.minimap_scene.setSceneRect(- mf * self.bgnd.minimap.size().width(),
                                        - mf * self.bgnd.minimap.size().height(),
                                        (2 * mf + 1) * self.bgnd.minimap.size().width(),
                                        (2 * mf + 1) * self.bgnd.minimap.size().height())
        self.minimap_viewport = QGraphicsView(self.minimap_scene)
        self.minimap_viewport.scale(2, 2)
        self.minimap_viewport.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.minimap_viewport.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.minimap_item = QGraphicsPixmapItem(QPixmap.fromImage(self.bgnd.minimap))
        self.minimap_scene.addItem(self.minimap_item)
        self.minimap_rect_item = QGraphicsRectItem()
        self.minimap_scene.addItem(self.minimap_rect_item)
        layout.addWidget(self.minimap_viewport)

        self.setWidget(content)

    def update(self):
        # r = self.scene.viewport().current_visible_scene_rect()
        # self.minimap_rect_item.setRect(r.x()/self.wf, r.y()/self.hf, r.width()/self.wf, r.height()/self.wf)
        if self.check_box.isChecked() is True:
            self.graphic_map_item.setVisible(True)
            self.graphic_map_item.setOpacity(self.slider.value() / 255)

        else:
            self.graphic_map_item.setVisible(False)
        super().update()

    def refresh_minimap(self, rect_view: QRectF):
        # r = self.scene.viewport().current_visible_scene_rect()
        r = rect_view
        self.minimap_rect_item.setRect(r.x() / self.wf, r.y() / self.hf, r.width() / self.wf, r.height() / self.wf)
        self.minimap_viewport.centerOn(self.minimap_item.boundingRect().center())
