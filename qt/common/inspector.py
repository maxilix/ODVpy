from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QPushButton, QStyle, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox

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


class QInspector(QWidget):
    def __init__(self, parent, dvd_item):
        super().__init__(parent)
        self._dvd_item = dvd_item

        self.main_layout = QVBoxLayout(self)

        l1_layout = QHBoxLayout()

        self.settings_button = QSettingsButtons(self)
        l1_layout.addWidget(self.settings_button)

        self.title = QTitleLabel(self)
        l1_layout.addWidget(self.title)

        l1_layout.addStretch(255)

        if dvd_item.has_graphic:
            self.visible_checkbox = QCheckBox()
            self.visible_checkbox.setChecked(False)
            l1_layout.addWidget(self.visible_checkbox)

            self.localise = QPushButton("Localise")
            l1_layout.addWidget(self.localise)
        else:
            self.visible_checkbox = None
            self.localise = None

        self.main_layout.addLayout(l1_layout)

        self.edit_widget = QEditWidget(self)
        self.main_layout.addWidget(self.edit_widget)



    # def update(self):
    #     if self.item is not None:
    #         self.localise.clicked.connect(self.item.localise)
    #         self.title.setText(self.item.context_menu_name)

