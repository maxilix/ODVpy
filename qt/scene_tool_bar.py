from math import floor

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSpinBox, QPushButton, QGroupBox


class QSceneToolBar(QWidget):

    def __init__(self, scene):
        super().__init__()
        self.scene = scene

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        localise_group = QGroupBox()
        localise_layout = QVBoxLayout(localise_group)
        # localise_layout.setContentsMargins(0, 0, 0, 0)


        xy_localise_layout = QHBoxLayout()
        self.position_x = QSpinBox()
        # self.position_x.setPrefix("x")
        self.position_x.setMaximum(9999)
        self.position_x.setValue(800)
        xy_localise_layout.addWidget(self.position_x)
        self.position_y = QSpinBox()
        # self.position_y.setPrefix("y")
        self.position_y.setMaximum(9999)
        self.position_y.setValue(800)
        xy_localise_layout.addWidget(self.position_y)
        localise_layout.addLayout(xy_localise_layout)

        self.localize_button = QPushButton('Localize')
        self.localize_button.clicked.connect(self.localise)
        localise_layout.addWidget(self.localize_button)

        main_layout.addWidget(localise_group)

        main_layout.addStretch()

    def localise(self):
        self.scene.move_to(self.position_x.value(), self.position_y.value())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if self.position_x.hasFocus():
                self.position_y.setFocus()
                self.position_y.selectAll()
            elif self.position_y.hasFocus():
                self.position_y.clearFocus()
                self.localise()

    def set_xy_localise(self, x, y):
        self.position_x.setValue(floor(x))
        self.position_y.setValue(floor(y))
