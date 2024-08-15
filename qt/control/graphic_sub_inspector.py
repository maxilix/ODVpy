from PyQt6.QtCore import Qt, QLineF
from PyQt6.QtGui import QColor, QBrush, QPen, QPolygonF, QAction
from PyQt6.QtWidgets import QPushButton, QCheckBox, QWidget, QSlider, QHBoxLayout, QStackedLayout, QLabel, QVBoxLayout, \
    QFileDialog

from qt.control.sub_inspector import SubInspector
from qt.graphics.line import QCEGLine
from qt.graphics.pixmap import QCGMap
from qt.graphics.polygon import QCEGPolygon


class GraphicSubInspector(SubInspector):

    def __init__(self, parent, prop_name):
        super().__init__(parent, prop_name)
        self.visibility_checkbox = QCheckBox()
        self.visibility_checkbox.stateChanged.connect(self.visibility_checkbox_changed)
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.valueChanged.connect(self.opacity_slider_changed)
        self.localise_button = QPushButton("Localise")
        self.localise_button.clicked.connect(self.localise_button_clicked)


    def init_actions(self):
        self.a_localise = QAction("Localise")
        self.a_localise.triggered.connect(self.localise_button_clicked)

        self.a_show = QAction("Show")
        self.a_show.triggered.connect(lambda: self.visibility_checkbox.setChecked(True))

        self.a_hide = QAction("Hide")
        self.a_hide.triggered.connect(lambda: self.visibility_checkbox.setChecked(False))

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

    def update(self):
        self.graphic.update()
        super().update()

    @property
    def scene(self):
        return self._inspector.scene

    def visibility_checkbox_changed(self):
        self.graphic.update()

    def opacity_slider_changed(self):
        self.graphic.setOpacity(self.opacity_slider.value() / 100)
        self.graphic.update()

    def localise_button_clicked(self):
        self.visibility_checkbox.setChecked(True)
        self.graphic.localise()

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
    graphic_type = {QPolygonF : QCEGPolygon,
                    QLineF : QCEGLine}

    def __init__(self, parent, prop_name, color: QColor = None):
        super().__init__(parent, prop_name)

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

        self.init_graphic(color)
        self.init_actions()

        self.setLayout(self.main_layout)
        self.update()

        self.edit_button.clicked.connect(self.edit_button_clicked)
        self.save_button.clicked.connect(self.save_button_clicked)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)


    def init_graphic(self, color: QColor):
        if color is None:
            self.pen = QPen(Qt.GlobalColor.transparent)
            self.light_brush = QBrush(Qt.GlobalColor.transparent)
            self.high_brush = QBrush(Qt.GlobalColor.transparent)
        else:
            color.setAlpha(255)
            self.pen = QPen(color)
            self.pen.setWidthF(0.3)
            self.pen.setCapStyle(Qt.PenCapStyle.FlatCap)
            self.pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

            color.setAlpha(32)
            self.light_brush = QBrush(color)

            color.setAlpha(96)
            self.high_brush = QBrush(color)

        self.graphic = self.graphic_type[type(self.current)](self)
        self.scene.addItem(self.graphic)

    @property
    def edit(self):
        return self.edit_layout.currentWidget() == self.edit_out

    def edit_button_clicked(self):
        self.visibility_checkbox.setChecked(True)
        self.edit_layout.setCurrentWidget(self.edit_out)
        self.graphic.enter_edit_mode()

    def save_button_clicked(self):
        self.edit_layout.setCurrentWidget(self.edit_in)
        self.graphic.exit_edit_mode(save=True)

    def cancel_button_clicked(self):
        self.edit_layout.setCurrentWidget(self.edit_in)
        self.graphic.exit_edit_mode(save=False)


class PixmapSubInspector(GraphicSubInspector):
    def __init__(self, parent, prop_name):
        super().__init__(parent, prop_name)

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
        self.update()

    def init_graphic(self):
        self.graphic = QCGMap(self)
        self.scene.addItem(self.graphic)

    def change_image_button_clicked(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        filters = ["BMP Image (*.bmp)",
                   "PNG Image (*.png)",]
        dialog.setNameFilters(filters)
        # dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if len(filenames) == 1:
                # self.dvm.change_level_map_image(filenames[0])
                # self.scene.removeItem(self.graphic)
                # self.graphic = QCGMap(self, QPixmap(self.dvm.level_map_image))
                # self.scene.addItem(self.graphic)
                self.update()

