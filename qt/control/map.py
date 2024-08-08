from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QSlider, QGraphicsScene, QGraphicsPixmapItem, \
    QGraphicsView, QGraphicsRectItem, QHBoxLayout, QLabel, QPushButton, QFileDialog

from qt.control.q_tab_control import QTabControl
from qt.graphics.pixmap import QCGMap
from qt.scene import QScene


class QMapTabControl(QTabControl):
    def __init__(self, parent, dvm, bgnd):
        super().__init__(parent)
        self.dvm = dvm
        self.bgnd = bgnd
        self.wf = self.dvm.level_map.size().width() / self.bgnd.minimap.size().width()
        self.hf = self.dvm.level_map.size().height() / self.bgnd.minimap.size().height()
        self.scene.viewport().view_changed.connect(self.refresh_minimap)

        self.init_ui()
        self.init_actions()

        self.graphic = QCGMap(self, QPixmap(self.dvm.level_map))
        self.scene.addItem(self.graphic)

        self.update()

    @property
    def visible(self):
        return self.check_box.isChecked()

    @visible.setter
    def visible(self, visible):
        self.check_box.setChecked(visible)
        self.graphic.update()

    def init_ui(self):
        content = QWidget()
        layout = QVBoxLayout(content)

        h1_layout = QHBoxLayout()
        label = QLabel("Map visibility")
        h1_layout.addWidget(label)
        self.check_box = QCheckBox()
        self.check_box.setCheckState(Qt.CheckState.Checked)
        self.check_box.stateChanged.connect(self.update)
        h1_layout.addWidget(self.check_box)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(255)
        self.slider.setValue(255)
        self.slider.valueChanged.connect(self.update)
        h1_layout.addWidget(self.slider)
        layout.addLayout(h1_layout)

        h2_layout = QHBoxLayout()
        self.size_label = QLabel()
        h2_layout.addWidget(self.size_label)
        h2_layout.addStretch(255)
        change_dvm_button = QPushButton("Change DVM")
        change_dvm_button.clicked.connect(self.change_dvm)
        h2_layout.addWidget(change_dvm_button)
        layout.addLayout(h2_layout)



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


    def init_actions(self):
        self.a_show = QAction("Show")
        self.a_show.triggered.connect(lambda: self.check_box.setCheckState(Qt.CheckState.Checked))
        self.a_hide = QAction("Hide")
        self.a_hide.triggered.connect(lambda: self.check_box.setCheckState(Qt.CheckState.Unchecked))

    def scene_menu_name(self):
        return "Map"

    def scene_menu_exclusive(self):
        return super().scene_menu_exclusive()

    def scene_menu_priority(self):
        return (super().scene_menu_priority()
                + 0.5 * self.has_focus())

    def scene_menu_enabled(self):
        return super().scene_menu_enabled()

    def scene_menu_common_actions(self, scene_position: QPointF = QPointF()):
        if self.visible:
            return [self.a_hide]
        else:
            return [self.a_show]

    def update(self):
        # r = self.scene.viewport().current_visible_scene_rect()
        # self.minimap_rect_item.setRect(r.x()/self.wf, r.y()/self.hf, r.width()/self.wf, r.height()/self.wf)
        self.size_label.setText(f"Size {self.dvm.width}x{self.dvm.height}")
        self.graphic.setOpacity(self.slider.value() / 255)
        self.graphic.update()
        super().update()

    def refresh_minimap(self, rect_view: QRectF):
        r = rect_view
        self.minimap_rect_item.setRect(r.x() / self.wf, r.y() / self.hf, r.width() / self.wf, r.height() / self.wf)
        self.minimap_viewport.centerOn(self.minimap_item.boundingRect().center())

    def change_dvm(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        filters = ["BMP Image (*.bmp)",
                   "PNG Image (*.png)",]
        dialog.setNameFilters(filters)
        # dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if len(filenames) == 1:
                self.dvm.change_level_map_image(filenames[0])
                self.scene.removeItem(self.graphic)
                self.graphic = QCGMap(self, QPixmap(self.dvm.level_map_image))
                self.scene.addItem(self.graphic)
                self.update()

