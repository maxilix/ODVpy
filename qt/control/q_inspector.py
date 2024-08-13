from typing import Any

from PyQt6.QtCore import QSize, Qt, pyqtSignal, QLineF
from PyQt6.QtGui import QIntValidator, QColor, QPen, QBrush, QPolygonF
from PyQt6.QtWidgets import QWidget, QPushButton, QStyle, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox, QFrame, \
    QGroupBox, QStackedLayout, QLineEdit, QComboBox, QFormLayout, QSpinBox, QGraphicsScene

from common import UShort
from qt.graphics.line import QCEGLine
from qt.graphics.polygon import QCEGPolygon

TITLE_SIZE = 22


class SubInspector(QWidget):

    def __init__(self, parent, prop_name):
        assert isinstance(parent, Inspector)
        super().__init__(parent)
        self._prop_name = prop_name

    @property
    def current(self):
        return self.parent().__getattribute__(self._prop_name)

    @current.setter
    def current(self, value):
        self.parent().__setattr__(self._prop_name, value)





class OdvObjectListSubInspector(QComboBox, SubInspector):

    def __init__(self, parent, prop_name):
        super().__init__(parent, prop_name)
        self.iterable = self.current.parent
        self.update()
        self.currentIndexChanged.connect(self.current_index_changed)

    def update(self):
        super().update()
        self.clear()
        self.addItems([str(e) for e in self.iterable])
        self.setCurrentIndex(self.iterable.index(self.current))

    def current_index_changed(self, index):
        self.current = self.iterable[index]



class UShortBoxInspector(QSpinBox, SubInspector):

    def __init__(self, parent, prop_name):
        super().__init__(parent, prop_name)
        self.setMinimum(UShort.min())
        self.setMaximum(UShort.max())
        self.update()
        self.valueChanged.connect(self.value_changed)

    def update(self):
        self.setValue(self.current)
        super().update()

    def value_changed(self):
        self.current = self.value()


class UShortTwinBoxInspector(SubInspector):
    def __init__(self, parent, prop_name):
        super().__init__(parent, prop_name)
        self.spinbox0 = QSpinBox()
        self.spinbox0.setMinimum(UShort.min())
        self.spinbox0.setMaximum(UShort.max())
        self.spinbox0.valueChanged.connect(self.value_changed)

        self.spinbox1 = QSpinBox()
        self.spinbox1.setMinimum(UShort.min())
        self.spinbox1.setMaximum(UShort.max())
        self.spinbox1.valueChanged.connect(self.value_changed)

        self.swap_button = QPushButton("Swap")
        self.swap_button.clicked.connect(self.swap_button_clicked)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.spinbox0)
        main_layout.addWidget(self.spinbox1)
        main_layout.addStretch(1)
        main_layout.addWidget(self.swap_button)
        self.setLayout(main_layout)
        self.update()

    def update(self):
        self.spinbox0.setValue(self.current[0])
        self.spinbox1.setValue(self.current[1])
        super().update()

    def value_changed(self):
        self.current = (self.spinbox0.value(), self.spinbox1.value())

    def swap_button_clicked(self):
        temp = self.spinbox1.value()
        self.spinbox1.setValue(self.spinbox0.value())
        self.spinbox0.setValue(temp)






        # Q LINE EDIT
    #     self.odv_object = odv_object
    #     self.property_name = property_name
    #     super().__init__(str(getattr(self.odv_object, self.property_name)))
    #
    #     int_validator = QIntValidator()
    #     # int_validator.setBottom(0)
    #     # int_validator.setTop(100)
    #     self.setValidator(int_validator)
    #     # self.textChanged.connect(self.text_changed)
    #     self.editingFinished.connect(self.editing_finished)
    #     self.textEdited.connect(lambda: self.setStyleSheet("color: black;"))
    #
    # def editing_finished(self):
    #     try:
    #         setattr(self.odv_object, self.property_name, int(self.text()))
    #         self.setText(str(getattr(self.odv_object, self.property_name)))
    #     except (ValueError, IndexError):
    #         self.setStyleSheet("color: red;")


# class GraphicSubInspector(SubInspector):
#
#     def __init__(self, parent, prop_name):
#         super().__init__()
#         self.graphic = graphic
#
#         self.edit_button = QPushButton("Edit")
#         self.edit_button.clicked.connect(self.edit_button_clicked)
#         self.save_button = QPushButton("Save")
#         self.save_button.clicked.connect(self.save_button_clicked)
#         self.cancel_button = QPushButton("Cancel")
#         self.cancel_button.clicked.connect(self.cancel_button_clicked)
#
#         self.visibility_checkbox = QCheckBox()
#         self.visibility_checkbox.stateChanged.connect(self.visibility_checkbox_clicked)
#         self.localise_button = QPushButton("Localise")
#         self.localise_button.clicked.connect(self.localise_button_clicked)
#
#         self.edit_in = QWidget()
#         l1 = QHBoxLayout(self.edit_in)
#         l1.setContentsMargins(0, 0, 0, 0)
#         l1.addWidget(self.edit_button)
#
#         self.edit_out = QWidget()
#         l1 = QHBoxLayout(self.edit_out)
#         l1.setContentsMargins(0, 0, 0, 0)
#         l1.addWidget(self.save_button)
#         l1.addWidget(self.cancel_button)
#
#         self.edit_layout = QStackedLayout()
#         self.edit_layout.addWidget(self.edit_in)
#         self.edit_layout.addWidget(self.edit_out)
#
#         main_layout = QHBoxLayout()
#         main_layout.setContentsMargins(0, 0, 0, 0)
#         main_layout.addLayout(self.edit_layout)
#         main_layout.addStretch(1)
#         main_layout.addWidget(self.visibility_checkbox)
#         main_layout.addWidget(self.localise_button)
#
#         self.setLayout(main_layout)
#         #
#         # if color is None:
#         #     self.pen = QPen(Qt.GlobalColor.transparent)
#         #     self.light_brush = QBrush(Qt.GlobalColor.transparent)
#         #     self.high_brush = QBrush(Qt.GlobalColor.transparent)
#         # else:
#         #     color.setAlpha(255)
#         #     self.pen = QPen(color)
#         #     self.pen.setWidthF(0.3)
#         #     self.pen.setCapStyle(Qt.PenCapStyle.FlatCap)
#         #     self.pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
#         #
#         #     color.setAlpha(32)
#         #     self.light_brush = QBrush(color)
#         #
#         #     color.setAlpha(96)
#         #     self.high_brush = QBrush(color)
#         #
#         # self.graphic = graphic_type(self)
#         # self.scene.addItem(self.graphic)
#
#     @property
#     def scene(self):
#         return self.parent().scene
#
#     def edit_button_clicked(self):
#         self.visibility_checkbox.setChecked(True)
#         self.edit_layout.setCurrentWidget(self.edit_out)
#         self.graphic.enter_edit_mode()
#
#     def save_button_clicked(self):
#         self.edit_layout.setCurrentWidget(self.edit_in)
#         self.graphic.exit_edit_mode(save=True)
#         # self.changed.emit(self.object_to_emit)
#
#     def cancel_button_clicked(self):
#         self.edit_layout.setCurrentWidget(self.edit_in)
#         self.graphic.exit_edit_mode(save=False)
#
#
#     def visibility_checkbox_clicked(self):
#         self.graphic.update()
#
#     def localise_button_clicked(self):
#         self.visibility_checkbox.setChecked(True)
#         self.graphic.localise()


class GeometrySubInspector(SubInspector):
    graphic_type = {QPolygonF : QCEGPolygon,
                    QLineF : QCEGLine}

    def __init__(self, parent, prop_name, color: QColor = None):
        super().__init__(parent, prop_name)

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_button_clicked)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_button_clicked)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_button_clicked)

        self.visibility_checkbox = QCheckBox()
        self.visibility_checkbox.stateChanged.connect(self.visibility_checkbox_clicked)
        self.localise_button = QPushButton("Localise")
        self.localise_button.clicked.connect(self.localise_button_clicked)

        self.edit_in = QWidget()
        l1 = QHBoxLayout(self.edit_in)
        l1.setContentsMargins(0, 0, 0, 0)
        l1.addWidget(self.edit_button)

        self.edit_out = QWidget()
        l1 = QHBoxLayout(self.edit_out)
        l1.setContentsMargins(0, 0, 0, 0)
        l1.addWidget(self.save_button)
        l1.addWidget(self.cancel_button)

        self.edit_layout = QStackedLayout()
        self.edit_layout.addWidget(self.edit_in)
        self.edit_layout.addWidget(self.edit_out)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(self.edit_layout)
        main_layout.addStretch(1)
        main_layout.addWidget(self.visibility_checkbox)
        main_layout.addWidget(self.localise_button)

        self.setLayout(main_layout)

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
    def scene(self):
        return self.parent().scene

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


    def visibility_checkbox_clicked(self):
        self.graphic.update()

    def localise_button_clicked(self):
        self.visibility_checkbox.setChecked(True)
        self.graphic.localise()




class Inspector(QWidget):

    def __init__(self, tab_control, odv_object):
        super().__init__()
        self._tab_control = tab_control
        self.odv_object = odv_object
        self.prop = dict()
        self.main_layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()
        self.settings_button = QPushButton(self)
        self.settings_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarUnshadeButton))
        self.settings_button.setIconSize(QSize(TITLE_SIZE, TITLE_SIZE))
        self.settings_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                padding: 0;
            }
            QPushButton:hover {
                background: #f0f0f0;
            }
        """)
        header_layout.addWidget(self.settings_button)

        self.title = QLabel(self)
        self.title.setText(self.odv_object.name)
        f = self.title.font()
        f.setPointSizeF(TITLE_SIZE)
        self.title.setFont(f)
        header_layout.addWidget(self.title)

        header_layout.addStretch(1)

        self.main_layout.addLayout(header_layout)

        sub_layout = QFormLayout()
        sub_layout.setHorizontalSpacing(15)

        # self.graphics = [graphic_type(self) for graphic_type in self.graphic_types]
        # for graphic, i in enumerate(self.graphic_types):
        #     self.scene.addItem(graphic)
        #     self.prop[f"g{i}"] = GraphicSubInspector(graphic)

        self.init_prop_section()
        for prop_label in self.prop:
            sub_layout.addRow(prop_label, self.prop[prop_label])
        self.main_layout.addLayout(sub_layout)
        self.main_layout.addStretch(1)


    @property
    def scene(self):
        return self._tab_control.scene

    @property
    def level(self):
        return self._tab_control.level

    def tree_item(self):
        return self._tab_control.tree_items[self.odv_object]


    def init_prop_section(self):
        # must define self.prop = {property_label : property_widget, ...}
        # must connect property_widget.changed signal to the right edition of self.odv_object
        #
        # note: for graphical properties, don't forget to add graphic item to self.scene
        pass



class SectionInspector(Inspector):
    def init_prop_section(self):
        self.prop["Version"] = QLabel(str(self.odv_object.version))

