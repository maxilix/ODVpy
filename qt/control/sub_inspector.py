from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QCheckBox, QSlider, QPushButton, QFileDialog


class QSubInspectorWidget(QWidget):

    def __init__(self, inspector, prop):
        super().__init__()
        self.inspector = inspector
        self.prop = prop
        # self.get = getter
        # self.set = setter

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def get(self):
        rop = [getattr(item, self.prop) for item in self.inspector.item_list]
        if rop == []:
            return None
        elif all(rop[0] == e for e in rop):
            return rop[0]
        else:
            return rop







class InfoQSIW(QSubInspectorWidget):
    info: QLabel
    def __init__(self, inspector, prop):
        super().__init__(inspector, prop)

        self.info = QLabel()
        self.main_layout.addWidget(self.info)
        self.setLayout(self.main_layout)

    def update(self):
        self.info.setText(str(self.get()))



class MapPropertyWidget(QWidget):

    image_changed: pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        sub_layout = QHBoxLayout()
        self.visibility_label = QLabel("Visibility")
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
        self.localise_button.setStatusTip(f"Localise {self.inspector.odv_object.name}")
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

        self.map_graphic_item = None

    def visibility_checkbox_clicked(self):
        self.map_graphic_item.setVisible(self.visibility_checkbox.isChecked())
        if self.visibility_checkbox.isChecked() is False:
            self.opacity_slider_last_state = self.opacity_slider.value()
            self.opacity_slider.setValue(0)
        else:
            self.opacity_slider.setValue(self.opacity_slider_last_state)

    def opacity_slider_changed(self):
        self.map_graphic_item.setOpacity(self.opacity_slider.value() / 100)
        if self.opacity_slider.value() == 0:
            self.visibility_checkbox.setChecked(False)
            self.map_graphic_item.setVisible(False)
        else:
            # self.opacity_slider_last_state = self.opacity_slider.value()
            self.visibility_checkbox.setChecked(True)
            self.map_graphic_item.setVisible(True)


    def localise_button_clicked(self):
        self.map_graphic_item.localise()
        # self.inspector.tab.control.sendStatus.emit("Localise", 1500)

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
                self.image_changed.emit(filenames[0])
                # self.set(filenames[0])
                # self.graphic.image = self.get()
                self.opacity_slider.setValue(100)  # set visibility_checkbox to True in the change callback
                self.map_graphic_item.reset()
                # self.inspector.update()

    # def update(self):
    #     self.graphic.update()