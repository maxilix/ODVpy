from math import floor

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSpinBox, QPushButton, QGroupBox

from app_context import AppContext as AC


class QSceneToolBar(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        localize_group = QGroupBox()
        localize_layout = QVBoxLayout(localize_group)
        # localize_layout.setContentsMargins(0, 0, 0, 0)


        xy_localize_layout = QHBoxLayout()
        self.position_x = QSpinBox()
        # self.position_x.setPrefix("x")
        self.position_x.setMaximum(9999)
        self.position_x.setValue(800)
        xy_localize_layout.addWidget(self.position_x)
        self.position_y = QSpinBox()
        # self.position_y.setPrefix("y")
        self.position_y.setMaximum(9999)
        self.position_y.setValue(800)
        xy_localize_layout.addWidget(self.position_y)
        localize_layout.addLayout(xy_localize_layout)

        self.localize_button = QPushButton('Localize')
        self.localize_button.clicked.connect(self.localize)
        localize_layout.addWidget(self.localize_button)

        main_layout.addWidget(localize_group)

        main_layout.addStretch()

    def localize(self):
        AC.scene.move_to(self.position_x.value(), self.position_y.value())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if self.position_x.hasFocus():
                self.position_y.setFocus()
                self.position_y.selectAll()
            elif self.position_y.hasFocus():
                self.position_y.clearFocus()
                self.localize()

    def set_xy_localize(self, x, y):
        self.position_x.setValue(floor(x))
        self.position_y.setValue(floor(y))
