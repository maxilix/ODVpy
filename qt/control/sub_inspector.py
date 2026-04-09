from PyQt6.QtCore import Qt, pyqtSignal, QLineF
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QCheckBox, QSlider, QPushButton, QFileDialog, \
    QLineEdit


# class QSubInspectorWidget(QWidget):
#
#     def __init__(self, inspector, prop):
#         super().__init__()
#         self.inspector = inspector
#         self.prop = prop
#         # self.get = getter
#         # self.set = setter
#
#         self.main_layout = QVBoxLayout()
#         self.main_layout.setContentsMargins(0, 0, 0, 0)
#
#     def get(self):
#         rop = [getattr(item, self.prop) for item in self.inspector.item_list]
#         if rop == []:
#             return None
#         elif all(rop[0] == e for e in rop):
#             return rop[0]
#         else:
#             return rop

# class InfoQSIW(QSubInspectorWidget):
#     info: QLabel
#     def __init__(self, inspector, prop):
#         super().__init__(inspector, prop)
#
#         self.info = QLabel()
#         self.main_layout.addWidget(self.info)
#         self.setLayout(self.main_layout)
#
#     def update(self):
#         self.info.setText(str(self.get()))

class LabelPropertyWidget(QLabel):

    def connect_to(self, item, prop):
        self.item = item
        self.prop = prop
        self.setText(str(getattr(self.item, prop)))



class TextPropertyWidget(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel("Test")
        main_layout.addWidget(self.label)

        self.line_edit = QLineEdit()
        self.line_edit.textChanged.connect(self.text_changed)
        main_layout.addWidget(self.line_edit)

    def connect_to(self, item, prop):
        self.item = item
        self.prop = prop
        self.line_edit.setText(str(getattr(self.item, prop)))

    def text_changed(self):
        setattr(self.item, self.prop, self.line_edit.text())



class QGraphicVisibilityWidget(QWidget):

    new_image_file_requested = pyqtSignal(str)

    def __init__(self, title=""):
        super().__init__()

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.visibility_label = QLabel("Visibility")
        main_layout.addWidget(self.visibility_label)

        self.visibility_checkbox = QCheckBox()
        self.visibility_checkbox.setChecked(True)
        self.visibility_checkbox.clicked.connect(self.visibility_checkbox_clicked)
        main_layout.addWidget(self.visibility_checkbox)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self.opacity_slider_changed)
        main_layout.addWidget(self.opacity_slider)

        self.localize_button = QPushButton("Localize")
        self.localize_button.clicked.connect(self.localize_button_clicked)
        main_layout.addWidget(self.localize_button)

        # self.change_image_button = QPushButton("Change Image")
        # self.change_image_button.clicked.connect(self.change_image_button_clicked)
        # main_layout.addWidget(self.change_image_button)

        self.map_graphic_item = None

    def connect_to(self, graphic_item):
        self.map_graphic_item = graphic_item
        self.visibility_checkbox.setChecked(self.map_graphic_item.isVisible())
        self.opacity_slider.setValue(int(100*self.map_graphic_item.opacity()))

    def visibility_checkbox_clicked(self):
        self.map_graphic_item.setVisible(self.visibility_checkbox.isChecked())
        # self.opacity_slider.setEnabled(self.visibility_checkbox.isChecked())

    def opacity_slider_changed(self):
        self.map_graphic_item.setOpacity(self.opacity_slider.value() / 100)

    def localize_button_clicked(self):
        if not self.visibility_checkbox.isChecked():
            self.visibility_checkbox.click()

        self.map_graphic_item.localize()

    # def change_image_button_clicked(self):
    #     dialog = QFileDialog(self)
    #     dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
    #     filters = ["Image or DVM (*.png *.bmp *.dvm)",
    #                "BMP Image (*.bmp)",
    #                "PNG Image (*.png)",
    #                "DVM File (*.dvm)",]
    #     dialog.setNameFilters(filters)
    #     if dialog.exec():
    #         filenames = dialog.selectedFiles()
    #         if len(filenames) == 1:
    #             self.new_image_file_requested.emit(filenames[0])
    #             # self.set(filenames[0])
    #             # self.graphic.image = self.get()
    #             # self.opacity_slider.setValue(100)  # set visibility_checkbox to True in the change callback
    #             # self.map_graphic_item.reset()
    #             # self.inspector.update()

    # def update(self):
    #     self.graphic.update()
