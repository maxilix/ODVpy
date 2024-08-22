from PyQt6.QtCore import Qt, QLineF
from PyQt6.QtGui import QColor, QBrush, QPolygonF, QAction, QImage
from PyQt6.QtWidgets import QPushButton, QCheckBox, QWidget, QSlider, QHBoxLayout, QStackedLayout, QLabel, QVBoxLayout, \
    QFileDialog

from common import Gateway
from qt.control.inspector_abstract import SubInspector
from qt.graphics import OdvThinPen, OdvLightBrush, OdvHighBrush, GraphicPolygon, GraphicLine, GraphicGateway, \
    GraphicMap, GraphicMask


class GraphicSubInspector(SubInspector):

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

    def init_actions(self):
        self.a_localise = QAction("Localise")
        self.a_localise.triggered.connect(self.localise_button_clicked)

        self.a_show = QAction("Show")
        self.a_show.triggered.connect(self.show)

        self.a_hide = QAction("Hide")
        self.a_hide.triggered.connect(self.hide)

        if isinstance(self, GeometrySubInspector):
            self.a_edit = QAction("Edit")
            self.a_edit.triggered.connect(self.edit_button_clicked)

            self.a_save = QAction("Save")
            self.a_save.triggered.connect(self.save_button_clicked)

            self.a_cancel = QAction("Cancel")
            self.a_cancel.triggered.connect(self.cancel_button_clicked)

    def init_graphic(self, *args, **kwargs):
        # must be overwritten
        self.graphic = None

    def show(self):
        self.visibility_checkbox.setChecked(True)
        self.global_update()

    def hide(self):
        self.visibility_checkbox.setChecked(False)
        self.global_update()

    def update(self):
        self.graphic.update()
        super().update()

    @property
    def scene(self):
        return self._inspector.scene

    def visibility_checkbox_clicked(self):
        # self.graphic.update()
        self.global_update()

    def opacity_slider_changed(self):
        self.graphic.setOpacity(self.opacity_slider.value() / 100)
        # self.update()

    def localise_button_clicked(self):
        self.graphic.localise()
        self.visibility_checkbox.setChecked(True)
        self.global_update()


    def scene_menu_name(self):
        return self._inspector.scene_menu_name()

    def scene_menu_exclusive(self):
        if isinstance(self, GeometrySubInspector):
            return self.edit
        else:
            return self._inspector.scene_menu_exclusive()

    def scene_menu_enabled(self):
        return self._inspector.scene_menu_enabled()

    def scene_menu_priority(self):
        return self._inspector.scene_menu_priority()

    def scene_menu_common_actions(self, scene_position):
        rop = []
        if self.graphic.visible:
            rop.append(self.a_hide)
        else:
            rop.append(self.a_show)
        if isinstance(self, GeometrySubInspector):
            if self.edit is True:
                rop.append(self.a_save)
                rop.append(self.a_cancel)
            else:
                rop.append(self.a_edit)
        return rop + self._inspector.scene_menu_common_actions(scene_position)

    def tree_menu_common_actions(self):
        rop = []
        rop.append(self.a_localise)
        if isinstance(self, GeometrySubInspector):
            if self.edit is True:
                rop.append(self.a_save)
                rop.append(self.a_cancel)
            else:
                rop.append(self.a_edit)
        return rop + self._inspector.tree_menu_common_actions()


class GeometrySubInspector(GraphicSubInspector):
    graphic_type = {QPolygonF: GraphicPolygon,
                    QLineF: GraphicLine,
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


class PixmapSubInspector(GraphicSubInspector):
    def sub_init(self):
        super().sub_init()

        self.visibility_label = QLabel("Visibility ")

        l1 = QHBoxLayout()
        l1.setContentsMargins(0, 0, 0, 0)
        l1.addWidget(self.visibility_label)
        l1.addWidget(self.visibility_checkbox)
        l1.addWidget(self.opacity_slider)

        # self.filename_label = QLabel()
        self.change_image_button = QPushButton("Change Image")
        self.change_image_button.clicked.connect(self.change_image_button_clicked)

        l2 = QHBoxLayout()
        l2.setContentsMargins(0, 0, 0, 0)
        l2.addStretch(1)
        l2.addWidget(self.change_image_button)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(l1)
        main_layout.addLayout(l2)

        self.init_graphic()
        self.init_actions()

        self.setLayout(main_layout)
        # self.update()

    def init_graphic(self):
        color = QColor(64, 64, 64)
        self.pen = OdvThinPen(color)
        self.light_brush = OdvLightBrush(color)
        self.high_brush = QBrush(Qt.GlobalColor.transparent)

        self.graphic = GraphicMap(self)
        self.scene.addItem(self.graphic)

    def change_image_button_clicked(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        filters = ["PNG Image (*.png)", "BMP Image (*.bmp)"]
        dialog.setNameFilters(filters)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if len(filenames) == 1:
                self.current = QImage(filenames[0]).convertedTo(QImage.Format.Format_RGB16)
                self.graphic.rest_map()
                self.visibility_checkbox.setChecked(True)
                self.opacity_slider.setValue(100)
                self.global_update()

class MaskImageSubInspector(GraphicSubInspector):
    def sub_init(self):
        super().sub_init()

        self.visibility_label = QLabel("Visibility ")

        l1 = QHBoxLayout()
        l1.setContentsMargins(0, 0, 0, 0)
        l1.addWidget(self.visibility_label)
        l1.addWidget(self.visibility_checkbox)
        l1.addWidget(self.opacity_slider)

        # self.filename_label = QLabel()
        # self.change_image_button = QPushButton("Change Image")
        # self.change_image_button.clicked.connect(self.change_image_button_clicked)
        #
        # l2 = QHBoxLayout()
        # l2.setContentsMargins(0, 0, 0, 0)
        # l2.addStretch(1)
        # l2.addWidget(self.change_image_button)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(l1)
        # main_layout.addLayout(l2)

        self.init_graphic()
        self.init_actions()

        self.setLayout(main_layout)
        # self.update()

    def init_graphic(self):
        self.graphic = GraphicMask(self)
        self.scene.addItem(self.graphic)

    # def change_image_button_clicked(self):
    #     dialog = QFileDialog(self)
    #     dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
    #     filters = ["PNG Image (*.png)", "BMP Image (*.bmp)"]
    #     dialog.setNameFilters(filters)
    #     if dialog.exec():
    #         filenames = dialog.selectedFiles()
    #         if len(filenames) == 1:
    #             self.current = QImage(filenames[0]).convertedTo(QImage.Format.Format_RGB16)
    #             self.graphic.rest_map()
    #             self.visibility_checkbox.setChecked(True)
    #             self.opacity_slider.setValue(100)
    #             self.global_update()