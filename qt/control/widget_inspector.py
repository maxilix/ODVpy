from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QPushButton, QStyle, QLabel, QVBoxLayout, QHBoxLayout


class QInspectorWidget(QWidget):
    title_size = 22

    def __init__(self, tab, odv_object):
        super().__init__()
        self.tab = tab
        self.odv_object = odv_object
        self.sub_inspector_list = []

        self.main_layout = QVBoxLayout(self)

        # self.main_layout.insertWidget(0)

        header_layout = QHBoxLayout()
        self.settings_button = QPushButton(self)
        self.settings_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarUnshadeButton))
        self.settings_button.setIconSize(QSize(self.title_size, self.title_size))
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
        self.title.setText(f"{self.odv_object.name}")
        f = self.title.font()
        f.setPointSizeF(self.title_size)
        self.title.setFont(f)
        header_layout.addWidget(self.title)
        header_layout.addStretch()

        self.main_layout.addLayout(header_layout)
        self.main_layout.addStretch()
        # self.main_layout.addWidget(QLabel("Stretch"))

    def add_sub_inspector(self, sub_inspector):
        self.sub_inspector_list.append(sub_inspector)
        n = self.main_layout.count()
        self.main_layout.insertWidget(n - 1, sub_inspector)

    def update(self):
        # print("inspector updated")
        for sub_inspector in self.sub_inspector_list:
            sub_inspector.update()
        super().update()