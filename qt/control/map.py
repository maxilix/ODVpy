from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QScrollArea, QCheckBox, QVBoxLayout, QSlider, QGraphicsScene, QGraphicsPixmapItem, \
    QLabel


class QMapControl(QScrollArea):
    def __init__(self, parent, scene: QGraphicsScene, dvm, bgnd):
        super().__init__(parent)
        self.scene = scene
        self.dvm = dvm
        self.bgnd = bgnd
        self.init_ui()

        self.graphic_map_item = QGraphicsPixmapItem(QPixmap(self.dvm.level_map))
        self.scene.addItem(self.graphic_map_item)
        self.graphic_map_item.setVisible(self.check_box.isChecked())


    def init_ui(self):
        content = QWidget()
        layout = QVBoxLayout(content)

        self.check_box = QCheckBox("Show Map")
        self.check_box.setCheckState(Qt.CheckState.Checked)
        self.check_box.clicked.connect(self.update)
        layout.addWidget(self.check_box)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(255)
        self.slider.setValue(255)
        self.slider.valueChanged.connect(self.update)
        layout.addWidget(self.slider)

        # layout.addStretch(255)

        self.minimap = QLabel(self)
        self.minimap.setPixmap(QPixmap.fromImage(self.bgnd.minimap))
        layout.addWidget(self.minimap)

        self.setWidgetResizable(True)
        self.setWidget(content)

    def update(self):
        if self.check_box.isChecked() is True:
            self.graphic_map_item.setVisible(True)
            self.graphic_map_item.setOpacity(self.slider.value() / 255)

        else:
            self.graphic_map_item.setVisible(False)
