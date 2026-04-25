from collections.abc import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QSlider, QPushButton, QHBoxLayout, \
    QGraphicsPixmapItem, QMainWindow, QFileDialog

from qt.graphics import GraphicMap


class QSubInspectorWidget(QWidget):

    def __init__(self, getter, setter=None):
        super().__init__()
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
    def __init__(self, inspector,  get_info: Callable[[], str]):
        super().__init__(inspector)
        self.get_info = get_info

        self.info = QLabel()
        self.main_layout.addWidget(self.info)
        self.setLayout(self.main_layout)

    def update(self):
        self.info.setText(self.get_info())



class GraphicSubInspector(QSubInspectorWidget):

    def sub_init(self):
        self.visibility_checkbox = QCheckBox()
        self.visibility_checkbox.clicked.connect(self.visibility_checkbox_clicked)
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self.opacity_slider_changed)
        self.localise_button = QPushButton("Localise")
        self.localise_button.clicked.connect(self.localise_button_clicked)

        black = QColor(0, 0, 0)
        self.pen = OdvThinPen(black)
        self.light_brush = OdvLightBrush(black)
        self.high_brush = OdvHighBrush(black)

    def show(self):
        self.visibility_checkbox.setChecked(True)
        self.global_update()

    def hide(self):
        self.visibility_checkbox.setChecked(False)
        self.global_update()





class PixmapQSIW(QSubInspectorWidget):

    def __init__(self, get, set=None):
        super().__init__(get, set)
        # self.get_map = get_map
        # self.set_map = set_map

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
        # self.localise_button.setStatusTip(f"Localise {self.inspector.odv_object.name}")
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

        # self.graphic_map = GraphicMap(self.get())
        # self.scene.addItem(self.graphic_map)

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
        self.inspector._control.control.sendStatus.emit("Localise", 1500)

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







class GeometrySubInspector(GraphicSubInspector):
    graphic_type = {
        QPointF: GraphicPoint,
        QLineF: GraphicLine,
        QPolygonF: GraphicPolygon,
        Gateway: GraphicGateway}

    def sub_init(self, *, color, graphic_type=None):
        super().sub_init()

        self.edit_button = QPushButton("Edit")
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.edit_in = QWidget()
        l_edit_in = QHBoxLayout(self.edit_in)
        l_edit_in.setContentsMargins(0, 0, 0, 0)
        l_edit_in.addWidget(self.edit_button)

        self.edit_out = QWidget()
        l_edit_out = QHBoxLayout(self.edit_out)
        l_edit_out.setContentsMargins(0, 0, 0, 0)
        l_edit_out.addWidget(self.save_button)
        l_edit_out.addWidget(self.cancel_button)

        self.edit_layout = QStackedLayout()
        self.edit_layout.addWidget(self.edit_in)
        self.edit_layout.addWidget(self.edit_out)

        l1 = QHBoxLayout()
        l1.setContentsMargins(0, 0, 0, 0)
        l1.addLayout(self.edit_layout)
        l1.addStretch(1)
        l1.addWidget(self.visibility_checkbox)
        l1.addWidget(self.localise_button)
        self.main_layout.addLayout(l1)

        self.init_graphic(color, graphic_type)
        self.init_actions()

        self.setLayout(self.main_layout)
        # self.update()

        self.edit_button.clicked.connect(self.edit_button_clicked)
        self.save_button.clicked.connect(self.save_button_clicked)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)

    def init_graphic(self, color: QColor, graphic_type):
        self.pen = OdvThinPen(color)
        self.light_brush = OdvLightBrush(color)
        self.high_brush = OdvHighBrush(color)
        if graphic_type is None:
            self.graphic = self.graphic_type[type(self.current)](self)
        else:
            self.graphic = graphic_type(self)
        self.scene.addItem(self.graphic)

    @property
    def edit(self):
        return self.edit_layout.currentWidget() == self.edit_out

    def edit_button_clicked(self):
        self.visibility_checkbox.setChecked(True)
        self.edit_layout.setCurrentWidget(self.edit_out)
        self.graphic.enter_edit_mode()
        self.global_update()

    def save_button_clicked(self):
        self.edit_layout.setCurrentWidget(self.edit_in)
        self.graphic.exit_edit_mode(save=True)
        self.global_update()

    def cancel_button_clicked(self):
        self.edit_layout.setCurrentWidget(self.edit_in)
        self.graphic.exit_edit_mode(save=False)
        self.global_update()

