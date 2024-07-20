from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QSlider, QGraphicsScene, QGraphicsPixmapItem, \
    QGraphicsView, QGraphicsRectItem

from qt.graphics.common import QCGPixmap
from qt.control.common import QTabControl
from qt.scene import QScene


class QMapControl(QTabControl):
    def __init__(self, parent, scene: QScene, dvm, bgnd):
        super().__init__(parent, scene)
        self.dvm = dvm
        self.bgnd = bgnd
        self.wf = self.dvm.level_map.size().width() / self.bgnd.minimap.size().width()
        self.hf = self.dvm.level_map.size().height() / self.bgnd.minimap.size().height()
        self.scene.viewport().view_changed.connect(self.refresh_minimap)

        self.init_ui()
        self.init_actions()

        self.graphic_map_item = QCGPixmap(self, QPixmap(self.dvm.level_map))

        self.scene.addRect(QRectF(QPointF(0, 0), self.dvm.level_map.size().toSizeF()))
        self.scene.addItem(self.graphic_map_item)
        self.graphic_map_item.setVisible(self.check_box.isChecked())

    def context_menu_exclusive(self):
        return False

    def context_menu_name(self):
        return "Map"

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

    def item_visibility(self):
        return self.check_box.isChecked()

    def init_actions(self):
        self.a_show = QAction("Show")
        self.a_show.triggered.connect(lambda: self.check_box.setCheckState(Qt.CheckState.Checked))
        self.a_hide = QAction("Hide")
        self.a_hide.triggered.connect(lambda: self.check_box.setCheckState(Qt.CheckState.Unchecked))

    def common_action_list(self, scene_position):
        if self.item_visibility():
            return [self.a_hide]
        else:
            return [self.a_show]

    def update(self):
        # r = self.scene.viewport().current_visible_scene_rect()
        # self.minimap_rect_item.setRect(r.x()/self.wf, r.y()/self.hf, r.width()/self.wf, r.height()/self.wf)
        self.graphic_map_item.setOpacity(self.slider.value() / 255)
        self.graphic_map_item.update()
        super().update()

    def refresh_minimap(self, rect_view: QRectF):
        # r = self.scene.viewport().current_visible_scene_rect()
        r = rect_view
        self.minimap_rect_item.setRect(r.x() / self.wf, r.y() / self.hf, r.width() / self.wf, r.height() / self.wf)
        self.minimap_viewport.centerOn(self.minimap_item.boundingRect().center())
