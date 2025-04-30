from collections.abc import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QSlider, QPushButton, QHBoxLayout, \
    QGraphicsPixmapItem, QMainWindow, QFileDialog

from qt.graphics import GraphicMap


class AbstractQInspectorWidget(QWidget):

    def __init__(self, inspector):
        super().__init__()
        self.inspector = inspector
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    @property
    def scene(self):
        return self.inspector.scene




class InfoQInspectorWidget(AbstractQInspectorWidget):
    info: QLabel
    def __init__(self, inspector,  get_info: Callable[[], str]):
        super().__init__(inspector)
        self.get_info = get_info

        self.info = QLabel()
        self.main_layout.addWidget(self.info)
        self.setLayout(self.main_layout)

    def update(self):
        self.info.setText(self.get_info())



class PixmapQInspectorWidget(AbstractQInspectorWidget):
    def __init__(self, inspector, get_map: Callable[[], QImage], set_map: Callable[[str],[]]):
        super().__init__(inspector)
        self.get_map = get_map
        self.set_map = set_map

        sub_layout = QHBoxLayout()
        self.visibility_label = QLabel("Visibility ")
        self.visibility_checkbox = QCheckBox()
        self.visibility_checkbox.setChecked(True)
        self.visibility_checkbox.clicked.connect(self.visibility_checkbox_clicked)
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(100)
        self.opacity_slider_last_state = self.opacity_slider.value()
        self.opacity_slider.valueChanged.connect(self.opacity_slider_changed)
        self.localise_button = QPushButton("Localise")
        self.localise_button.clicked.connect(self.localise_button_clicked)
        self.change_image_button = QPushButton("Change Image")
        self.change_image_button.clicked.connect(self.change_image_button_clicked)

        sub_layout.addWidget(self.visibility_label)
        sub_layout.addWidget(self.visibility_checkbox)
        sub_layout.addWidget(self.opacity_slider)
        sub_layout.addWidget(self.localise_button)
        sub_layout.addWidget(self.change_image_button)

        self.main_layout.addLayout(sub_layout)
        self.setLayout(self.main_layout)

        self.graphic_map = GraphicMap(self.get_map())
        self.scene.addItem(self.graphic_map)

    def visibility_checkbox_clicked(self):
        self.graphic_map.setVisible(self.visibility_checkbox.isChecked())
        if self.visibility_checkbox.isChecked() is False:
            self.opacity_slider_last_state = self.opacity_slider.value()
            self.opacity_slider.setValue(0)
        else:
            self.opacity_slider.setValue(self.opacity_slider_last_state)

    def opacity_slider_changed(self):
        self.graphic_map.setOpacity(self.opacity_slider.value() / 100)
        if self.opacity_slider.value() == 0:
            self.visibility_checkbox.setChecked(False)
            self.graphic_map.setVisible(False)
        else:
            # self.opacity_slider_last_state = self.opacity_slider.value()
            self.visibility_checkbox.setChecked(True)
            self.graphic_map.setVisible(True)


    def localise_button_clicked(self):
        self.graphic_map.localise()

    def change_image_button_clicked(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        filters = ["Image or DVM (*.png *.bmp *.dvm)",
                   "BMP Image (*.bmp)",
                   "PNG Image (*.png)",
                   "DVM File (*.dvm)",]
        dialog.setNameFilters(filters)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if len(filenames) == 1:
                self.set_map(filenames[0])
                self.graphic_map.image = self.get_map()
                self.opacity_slider.setValue(100)  # set visibility_checkbox to True in the change callback
                self.graphic_map.reset()
                self.inspector.update()

    def update(self):
        self.graphic_map.update()
