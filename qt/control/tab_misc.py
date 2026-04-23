from PyQt6.QtWidgets import QLabel, QHBoxLayout, QSpinBox, QPushButton, QDoubleSpinBox

from common import Short, UShort
from odv.data_section import Misc
from qt.control.generic_inspector import Inspector
from qt.control.generic_tree import QGenericTreeItem


class MiscInspector(Inspector):
    def __init__(self):
        super().__init__()

        # MiscInspector can only be connected to a single item
        self.item = None

        ### View Widget #########################################################
        view_layout = QHBoxLayout()
        view_layout.setContentsMargins(0, 0, 0, 0)

        view_layout.addWidget(QLabel("Standard view length"))
        self.radius_box = QSpinBox()
        self.radius_box.setRange(UShort.min(), UShort.max())
        self.radius_box.valueChanged.connect(self.radius_value_changed)
        view_layout.addWidget(self.radius_box)

        view_layout.addSpacing(100)

        self.night_button = QPushButton()
        self.night_button.setCheckable(True)
        self.night_button.clicked.connect(self.night_button_clicked)
        view_layout.addWidget(self.night_button)
        view_layout.addStretch()

        view_layout.addStretch()

        self.main_layout.addLayout(view_layout)
        #########################################################################

        ### Wind Widget #########################################################
        wind_layout = QHBoxLayout()
        wind_layout.setContentsMargins(0, 0, 0, 0)

        wind_layout.addWidget(QLabel("Wind vector"))
        self.wind_x = QSpinBox()
        self.wind_x.setRange(Short.min(), Short.max())
        self.wind_x.valueChanged.connect(self.wind_x_value_changed)
        wind_layout.addWidget(self.wind_x)
        self.wind_y = QSpinBox()
        self.wind_y.setRange(Short.min(), Short.max())
        self.wind_y.valueChanged.connect(self.wind_y_value_changed)
        wind_layout.addWidget(self.wind_y)
        wind_layout.addStretch()

        self.main_layout.addLayout(wind_layout)
        #########################################################################

        ### Hearing Widget ######################################################
        hearing_layout = QHBoxLayout()
        hearing_layout.setContentsMargins(0, 0, 0, 0)

        hearing_layout.addWidget(QLabel("Hearing factor"))
        self.hearing_box = QDoubleSpinBox()
        self.hearing_box.setDecimals(2)
        self.hearing_box.setMinimum(0)
        self.hearing_box.setSingleStep(0.05)
        self.hearing_box.valueChanged.connect(self.hearing_value_changed)
        hearing_layout.addWidget(self.hearing_box)
        hearing_layout.addStretch()

        self.main_layout.addLayout(hearing_layout)
        #########################################################################

        self.main_layout.addStretch()

        ### Debug Widget ########################################################
        self.debug_label = QLabel()
        self.main_layout.addWidget(self.debug_label)
        #########################################################################

    def wind_x_value_changed(self):
        self.item.misc.wind_vector[0] = self.wind_x.value()

    def wind_y_value_changed(self):
        self.item.misc.wind_vector[1] = self.wind_y.value()

    def night_button_clicked(self):
        if self.night_button.isChecked():
            self.night_button.setText("Night")
            self.item.misc.night = 1
            # self.toggle_button.setStyleSheet("background-color: green; color: white;")
        else:
            self.night_button.setText("Day")
            self.item.misc.night = 0

    def hearing_value_changed(self):
        self.item.misc.hearing_factor = self.hearing_box.value()

    def radius_value_changed(self):
        self.item.misc.view_length = self.radius_box.value()

    def connect_to(self, new_items):
        # MiscInspector can only be connected to a single item
        assert len(new_items) == 1
        super().connect_to(new_items)
        self.item = self.items[0]

        self.debug_label.setText(self.item.debug_label)
        self.wind_x.setValue(self.item.misc.wind_vector[0])
        self.wind_y.setValue(self.item.misc.wind_vector[1])
        self.night_button.setChecked(self.item.misc.night)
        self.night_button_clicked()  # simulates a click to refresh the button
        self.hearing_box.setValue(self.item.misc.hearing_factor)
        self.radius_box.setValue(self.item.misc.view_length)


class MiscItem(QGenericTreeItem):

    def __init__(self,section_control, misc:Misc):
        super().__init__(section_control, misc)
        self.misc = misc

    @property
    def debug_label(self):
        return (f"Debug:\n"
                f"  unk0:\t{int.from_bytes(self.misc.unk0)}\n"
                f"  unk1:\t{int.from_bytes(self.misc.unk1)}\n"
                f"  unk2:\t{int.from_bytes(self.misc.unk2)}\n"
                f"  thunder:\t{self.misc.tail}")
