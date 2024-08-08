from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QPushButton, QStyle, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox, QFrame, \
    QGroupBox, QStackedLayout, QLineEdit

TITLE_SIZE = 22


class IntegerLineEditInspectorWidget(QLineEdit):
    def __init__(self, odv_object, property_name):
        self.odv_object = odv_object
        self.property_name = property_name
        super().__init__(str(getattr(self.odv_object, self.property_name)))

        int_validator = QIntValidator()
        # int_validator.setBottom(0)
        # int_validator.setTop(100)
        self.setValidator(int_validator)
        # self.textChanged.connect(self.text_changed)
        self.editingFinished.connect(self.editing_finished)
        self.textEdited.connect(lambda: self.setStyleSheet("color: black;"))

    def editing_finished(self):
        try:
            setattr(self.odv_object, self.property_name, int(self.text()))
            self.setText(str(getattr(self.odv_object, self.property_name)))
        except (ValueError, IndexError):
            self.setStyleSheet("color: red;")




class GraphicInspectorWidget(QWidget):
    def __init__(self, graphic):
        super().__init__()
        self.graphic = graphic
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

    def edit_button_clicked(self):
        self.visibility_checkbox.setChecked(True)
        self.edit_layout.setCurrentWidget(self.edit_out)
        print("edit_button_clicked")

    def save_button_clicked(self):
        self.edit_layout.setCurrentWidget(self.edit_in)
        print("save_button_clicked")

    def cancel_button_clicked(self):
        self.edit_layout.setCurrentWidget(self.edit_in)
        print("cancel_button_clicked")

    def visibility_checkbox_clicked(self):
        self.graphic.setVisible(self.visibility_checkbox.isChecked())

    def localise_button_clicked(self):
        self.visibility_checkbox.setChecked(True)
        self.graphic.localise()


# class AbstractInspectorSection(QGroupBox):
#     def __init__(self, title="Inspector Section"):
#         super().__init__()
#         self.setTitle(title)
#         self.setAlignment(Qt.AlignmentFlag.AlignCenter)
#
#
#
# class GraphicInspectorSection(AbstractInspectorSection):
#     def __init__(self):
#         super().__init__("Line")
#         self.edit_button = QPushButton("Edit")
#         self.edit_button.clicked.connect(self.edit_button_clicked)
#         self.save_button = QPushButton("Save")
#         self.save_button.clicked.connect(self.save_button_clicked)
#         self.cancel_button = QPushButton("Cancel")
#         self.cancel_button.clicked.connect(self.cancel_button_clicked)
#
#         self.visibility_checkbox = QCheckBox()
#         self.localise_button = QPushButton("Localise")
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
#         main_layout.setContentsMargins(8, 2, 8, 8)
#         main_layout.addLayout(self.edit_layout)
#         main_layout.addStretch(1)
#         main_layout.addWidget(self.visibility_checkbox)
#         main_layout.addWidget(self.localise_button)
#
#         self.setLayout(main_layout)
#
#     def edit_button_clicked(self):
#         self.edit_layout.setCurrentWidget(self.edit_out)
#
#     def save_button_clicked(self):
#         self.edit_layout.setCurrentWidget(self.edit_in)
#
#     def cancel_button_clicked(self):
#         self.edit_layout.setCurrentWidget(self.edit_in)


class Inspector(QWidget):
    def __init__(self, tab_control, odv_object):
        super().__init__()
        self._tab_control = tab_control
        self.odv_object = odv_object
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

        self.init_sections()

    @property
    def scene(self):
        return self._tab_control.scene

    def tree_item(self):
        return self._tab_control.tree_items[self.odv_object]


    def init_sections(self):
        # init inspector sections from self.odv_object properties
        # add sections to self.main_layout
        pass



