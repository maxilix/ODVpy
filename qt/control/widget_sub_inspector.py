from collections.abc import Callable

from PyQt6.QtCore import Qt, QPointF, QLineF
from PyQt6.QtGui import QPolygonF
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QSlider, QPushButton, QHBoxLayout, \
    QFileDialog, QStackedLayout

from common import Gateway
from qt.graphics import GraphicMap, GraphicPoint, GraphicGateway, GraphicPolygon, GraphicLine


class QSubInspectorWidget(QWidget):

    def __init__(self, inspector, getter, setter=None):
        super().__init__()
        self.inspector = inspector
        self.get = getter
        self.set = setter

        # self.inspector = inspector
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    @property
    def scene(self):
        return self.inspector.scene




class InfoQSIW(QSubInspectorWidget):
    info: QLabel
    def __init__(self, inspector, getter: Callable[[], str]):
        super().__init__(inspector, getter)

        self.info = QLabel()
        self.main_layout.addWidget(self.info)
        self.setLayout(self.main_layout)

    def update(self):
        self.info.setText(self.get())



# class GraphicSubInspector(QSubInspectorWidget):
#
#     def sub_init(self):
#         self.visibility_checkbox = QCheckBox()
#         self.visibility_checkbox.clicked.connect(self.visibility_checkbox_clicked)
#         self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
#         self.opacity_slider.setMinimum(0)
#         self.opacity_slider.setMaximum(100)
#         self.opacity_slider.setValue(100)
#         self.opacity_slider.valueChanged.connect(self.opacity_slider_changed)
#         self.localise_button = QPushButton("Localise")
#         self.localise_button.clicked.connect(self.localise_button_clicked)
#
#         black = QColor(0, 0, 0)
#         self.pen = OdvThinPen(black)
#         self.light_brush = OdvLightBrush(black)
#         self.high_brush = OdvHighBrush(black)
#
#     def show(self):
#         self.visibility_checkbox.setChecked(True)
#         self.global_update()
#
#     def hide(self):
#         self.visibility_checkbox.setChecked(False)
#         self.global_update()






class PixmapQSIW(QSubInspectorWidget):

    def __init__(self, inspector, getter, setter):
        super().__init__(inspector, getter, setter)

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

        self.graphic = GraphicMap(self.get())
        self.scene.addItem(self.graphic)

    def visibility_checkbox_clicked(self):
        self.graphic.setVisible(self.visibility_checkbox.isChecked())
        if self.visibility_checkbox.isChecked() is False:
            self.opacity_slider_last_state = self.opacity_slider.value()
            self.opacity_slider.setValue(0)
        else:
            self.opacity_slider.setValue(self.opacity_slider_last_state)

    def opacity_slider_changed(self):
        self.graphic.setOpacity(self.opacity_slider.value() / 100)
        if self.opacity_slider.value() == 0:
            self.visibility_checkbox.setChecked(False)
            self.graphic.setVisible(False)
        else:
            # self.opacity_slider_last_state = self.opacity_slider.value()
            self.visibility_checkbox.setChecked(True)
            self.graphic.setVisible(True)


    def localise_button_clicked(self):
        self.graphic.localise()
        self.inspector.tab.control.sendStatus.emit("Localise", 1500)

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
                self.set(filenames[0])
                self.graphic.image = self.get()
                self.opacity_slider.setValue(100)  # set visibility_checkbox to True in the change callback
                self.graphic.reset()
                self.inspector.update()

    def update(self):
        self.graphic.update()







class GeometryQSIW(QSubInspectorWidget):
    graphic_type = {
        QPointF: GraphicPoint,
        QLineF: GraphicLine,
        QPolygonF: GraphicPolygon,
        Gateway: GraphicGateway}


    def __init__(self, inspector, getter, setter):
        super().__init__(inspector, getter, setter)

        sub_layout = QHBoxLayout()
        self.visibility_label = QLabel("Visibility")
        self.visibility_checkbox = QCheckBox()
        self.visibility_checkbox.setChecked(True)
        self.visibility_checkbox.clicked.connect(self.visibility_checkbox_clicked)
        self.localise_button = QPushButton("Localise")
        self.localise_button.setStatusTip(f"Localise {self.inspector.odv_object.name}")
        self.localise_button.clicked.connect(self.localise_button_clicked)

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_button_clicked)
        self.edit_in = QWidget()
        edit_layout_in = QHBoxLayout(self.edit_in)
        edit_layout_in.setContentsMargins(0, 0, 0, 0)
        edit_layout_in.addWidget(self.edit_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_button_clicked)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_button_clicked)
        self.edit_out = QWidget()
        edit_layout_out = QHBoxLayout(self.edit_out)
        edit_layout_out.setContentsMargins(0, 0, 0, 0)
        edit_layout_out.addWidget(self.save_button)
        edit_layout_out.addWidget(self.cancel_button)

        self.edit_layout = QStackedLayout()
        self.edit_layout.addWidget(self.edit_in)
        self.edit_layout.addWidget(self.edit_out)


        sub_layout.addWidget(self.visibility_label)
        sub_layout.addWidget(self.visibility_checkbox)
        sub_layout.addWidget(self.localise_button)
        sub_layout.addLayout(self.edit_layout)

        self.main_layout.addLayout(sub_layout)
        self.setLayout(self.main_layout)

        # self.graphic = self.graphic_type[type(self.get())]
        # self.scene.addItem(self.graphic)

    @property
    def edit(self):
        return self.edit_layout.currentWidget() == self.edit_out

    def edit_button_clicked(self):
        self.visibility_checkbox.setChecked(True)
        self.edit_layout.setCurrentWidget(self.edit_out)
        # self.graphic.enter_edit_mode()
        # self.global_update()

    def save_button_clicked(self):
        self.edit_layout.setCurrentWidget(self.edit_in)
        # self.graphic.exit_edit_mode(save=True)
        # self.global_update()

    def cancel_button_clicked(self):
        self.edit_layout.setCurrentWidget(self.edit_in)
        # self.graphic.exit_edit_mode(save=False)
        # self.global_update()

    def visibility_checkbox_clicked(self):
        # self.graphic.setVisible(self.visibility_checkbox.isChecked())
        pass

    def localise_button_clicked(self):
        # self.graphic.localise()
        self.inspector.tab.control.sendStatus.emit("Localise", 1500)