from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QPushButton, QStyle, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox, QFrame

TITLE_SIZE = 22


class QSettingsButtons(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarUnshadeButton))
        self.setIconSize(QSize(TITLE_SIZE, TITLE_SIZE))
        self.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                padding: 0;
            }
            QPushButton:hover {
                background: #f0f0f0;
            }
        """)


class QTitleLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        f = self.font()
        f.setPointSizeF(TITLE_SIZE)
        self.setFont(f)


class QEditWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
        self._edit = False
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.edit_button = QPushButton("Edit")
        self.edit_button.setEnabled(not self._edit)
        layout.addWidget(self.edit_button)

        layout.addStretch(255)

        self.save_button = QPushButton("Save")
        self.save_button.setEnabled(self._edit)
        layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setEnabled(self._edit)
        layout.addWidget(self.cancel_button)

    @property
    def edit(self):
        return self._edit

    @edit.setter
    def edit(self, value):
        self._edit = value
        self.edit_button.setEnabled(not self._edit)
        self.save_button.setEnabled(self._edit)
        self.cancel_button.setEnabled(self._edit)


class QDVDInspectorItem(QWidget):
    properties_layout = None

    def __init__(self, q_odv_item):
        super().__init__()
        self.q_odv_item = q_odv_item

        self.main_layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()
        self.settings_button = QSettingsButtons(self)
        header_layout.addWidget(self.settings_button)
        self.title = QTitleLabel(self)
        self.title.setText(self.q_odv_item.name)
        header_layout.addWidget(self.title)
        header_layout.addStretch(255)
        if self.q_odv_item.q_graphic_item is not None:
            self.visible_checkbox = QCheckBox()
            self.visible_checkbox.setStyleSheet(f"QCheckBox::indicator {{width: {TITLE_SIZE}px; height: {TITLE_SIZE}px;}}")
            self.visible_checkbox.setChecked(self.q_odv_item.visible)
            self.visible_checkbox.stateChanged.connect(self.visible_checkbox_clicked)
            header_layout.addWidget(self.visible_checkbox)
            self.localise_button = QPushButton("Localise")
            self.localise_button.clicked.connect(self.q_odv_item.localise)
            header_layout.addWidget(self.localise_button)
        else:
            self.visible_checkbox = None
            self.localise_button = None
        self.main_layout.addLayout(header_layout)

        self.edit_widget = QEditWidget(self)
        self.main_layout.addWidget(self.edit_widget)
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        self.main_layout.addWidget(separator)
        if self.properties_layout is not None:
            self.main_layout.addLayout(self.properties_layout)
        self.main_layout.addStretch(255)

    @property
    def visible(self):
        if self.q_odv_item.q_graphic_item is not None:
            return self.visible_checkbox.isChecked()
        else:
            return False

    @visible.setter
    def visible(self, state):
        if self.q_odv_item.q_graphic_item is not None:
            self.visible_checkbox.setChecked(state)

    def visible_checkbox_clicked(self):#, state: Qt.CheckState):
        self.q_odv_item.visible = self.visible


