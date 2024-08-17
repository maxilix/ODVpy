from PyQt6.QtWidgets import QComboBox, QSpinBox, QPushButton, QHBoxLayout, QLabel, QCheckBox, QGridLayout


from qt.control.inspector_abstract import SubInspector


class OdvObjectListSubInspector(SubInspector):

    def sub_init(self, *, iterable=None):
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
        # print(len(self.iterable))
        self.combo_box.addItems([str(e) for e in self.iterable])
        try:
            self.combo_box.setCurrentIndex(list(self.iterable).index(self.current))
        except ValueError:
            self.combo_box.setCurrentIndex(-1)
            self.valid_state = False
        self.combo_box.currentIndexChanged.connect(self.current_index_changed)

    def current_index_changed(self, index):
        self.current = self.iterable[index]
        self.valid_state = True
        self.global_update()


class IntegerBoxInspector(SubInspector):

    def sub_init(self, *, int_type):
        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(int_type.min())
        self.spin_box.setMaximum(int_type.max())
        self.main_layout.addWidget(self.spin_box)

        self.setLayout(self.main_layout)
        self.spin_box.valueChanged.connect(self.value_changed)

    def update(self):
        self.spin_box.setValue(self.current)
        super().update()

    def value_changed(self):
        self.current = self.spin_box.value()


class ConstantEnumListInspector(SubInspector):
    def sub_init(self, *, enum: dict):
        self.enum = enum
        self.combo_box = QComboBox()
        self.combo_box.addItems([str(e) for e in self.enum.values()])
        self.main_layout.addWidget(self.combo_box)

        self.setLayout(self.main_layout)
        self.combo_box.currentIndexChanged.connect(self.current_index_changed)

    def update(self):
        self.combo_box.setCurrentText(str(self.enum[self.current]))
        super().update()

    def current_index_changed(self, index):
        for k,v in self.enum.items():
            if self.combo_box.currentText() == str(v):
                self.current = k
                break


class IntegerTwinBoxInspector(SubInspector):

    def sub_init(self, *, int_type):
        self.spinbox0 = QSpinBox()
        self.spinbox0.setMinimum(int_type.min())
        self.spinbox0.setMaximum(int_type.max())

        self.spinbox1 = QSpinBox()
        self.spinbox1.setMinimum(int_type.min())
        self.spinbox1.setMaximum(int_type.max())

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


class CheckBoxInspector(SubInspector):
    def sub_init(self, *, label=""):
        self.checkbox = QCheckBox(label)
        self.main_layout.addWidget(self.checkbox)

        self.setLayout(self.main_layout)
        self.checkbox.stateChanged.connect(self.value_changed)

    def update(self):
        self.checkbox.setChecked(bool(self.current))
        super().update()

    def value_changed(self):
        self.current = 1 if self.checkbox.isChecked() else 0

class MultiCheckBoxInspector(SubInspector):
    def sub_init(self, *, label_list=None, column=2, conditional=None):
        if label_list is None:
            label_list = [""]*len(self.current)
        if conditional is None:
            conditional = [None]*len(self.current)
        self.conditional = conditional

        assert len(label_list) == len(self.current) == len(self.conditional)
        self.checkbox_list = [QCheckBox(label) for label in label_list]
        sub_layout = QGridLayout()
        sub_layout.setContentsMargins(0, 0, 0, 0)
        for i, checkbox in enumerate(self.checkbox_list):
            sub_layout.addWidget (checkbox, i//column, i%column)

        self.main_layout.addLayout(sub_layout)

        self.setLayout(self.main_layout)
        for i, checkbox in enumerate(self.checkbox_list):
            checkbox.stateChanged.connect(lambda state, index=i: self.value_changed(index))

    def update(self):
        for i, checkbox in enumerate(self.checkbox_list):
            checkbox.setChecked(bool(self.current[i]))
        super().update()

    def value_changed(self, index):
        if self.checkbox_list[index].isChecked():  # just checked
            if (c:=self.conditional[index]) is not None:
                self.checkbox_list[c].setChecked(True)
                self.checkbox_list[c].update()
        else:  # just unchecked
            for i, c in enumerate(self.conditional):
                if c == index:
                    self.checkbox_list[i].setChecked(False)
                    self.checkbox_list[i].update()

        self.current = [1 if checkbox.isChecked() else 0 for checkbox in self.checkbox_list]



class InfoSubInspector(SubInspector):

    def sub_init(self):
        self.info = QLabel()
        self.main_layout.addWidget(self.info)
        self.setLayout(self.main_layout)


    def update(self):
        self.info.setText(str(self.current))

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
