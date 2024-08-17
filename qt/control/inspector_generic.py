from PyQt6.QtWidgets import QComboBox, QSpinBox, QPushButton, QHBoxLayout, QLabel

from common import UShort
from qt.control.inspector_abstract import SubInspector


class OdvObjectListSubInspector(SubInspector):

    def __init__(self, inspector, prop_name: str, iterable = None):
        super().__init__(inspector, prop_name)
        # print(self.current, iterable_prop_name)
        if iterable is None:
            self.iterable = self.current.parent
        else:
            self.iterable = iterable

        self.combo_box = QComboBox()
        self.main_layout.addWidget(self.combo_box)

        self.setLayout(self.main_layout)
        self.combo_box.currentIndexChanged.connect(self.current_index_changed)

    def update(self):
        self.combo_box.currentIndexChanged.disconnect()
        super().update()
        self.combo_box.clear()
        self.combo_box.addItems([str(e) for e in self.iterable])
        try:
            self.combo_box.setCurrentIndex(self.iterable.index(self.current))
        except ValueError:
            self.combo_box.setCurrentIndex(-1)
            self.valid_state = False
        self.combo_box.currentIndexChanged.connect(self.current_index_changed)

    def current_index_changed(self, index):
        self.current = self.iterable[index]
        self.valid_state = True
        self.global_update()


class UShortBoxInspector(SubInspector):

    def __init__(self, inspector, prop_name):
        super().__init__(inspector, prop_name)
        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(UShort.min())
        self.spin_box.setMaximum(UShort.max())
        self.main_layout.addWidget(self.spin_box)

        self.setLayout(self.main_layout)
        self.spin_box.valueChanged.connect(self.value_changed)

    def update(self):
        self.spin_box.setValue(self.current)
        super().update()

    def value_changed(self):
        self.current = self.spin_box.value()


class UShortTwinBoxInspector(SubInspector):
    def __init__(self, parent, prop_name):
        super().__init__(parent, prop_name)
        self.spinbox0 = QSpinBox()
        self.spinbox0.setMinimum(UShort.min())
        self.spinbox0.setMaximum(UShort.max())

        self.spinbox1 = QSpinBox()
        self.spinbox1.setMinimum(UShort.min())
        self.spinbox1.setMaximum(UShort.max())

        self.swap_button = QPushButton("Swap")

        l1 = QHBoxLayout()
        l1.setContentsMargins(0, 0, 0, 0)
        l1.addWidget(self.spinbox0)
        l1.addWidget(self.spinbox1)
        l1.addStretch(1)
        l1.addWidget(self.swap_button)
        self.main_layout.addLayout(l1)

        self.setLayout(self.main_layout)
        self.spinbox0.valueChanged.connect(self.value_changed)
        self.spinbox1.valueChanged.connect(self.value_changed)
        self.swap_button.clicked.connect(self.swap_button_clicked)

    def update(self):
        self.spinbox0.valueChanged.disconnect()
        self.spinbox1.valueChanged.disconnect()
        super().update()
        self.spinbox0.setValue(self.current[0])
        self.spinbox1.setValue(self.current[1])
        self.spinbox0.valueChanged.connect(self.value_changed)
        self.spinbox1.valueChanged.connect(self.value_changed)

    def value_changed(self):
        self.current = (self.spinbox0.value(), self.spinbox1.value())

    def swap_button_clicked(self):
        temp = self.spinbox1.value()
        self.spinbox1.setValue(self.spinbox0.value())
        self.spinbox0.setValue(temp)


class InfoSubInspector(SubInspector):

    def __init__(self, parent, prop_name):
        super().__init__(parent, prop_name)
        self.info = QLabel()

        self.main_layout.addWidget(self.info)

        self.setLayout(self.main_layout)


    def update(self):
        self.info.setText(self.current)

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
