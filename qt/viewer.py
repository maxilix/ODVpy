
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from .info_bar import QInfoBar
from qt.view import QScene


class QViewer(QWidget):
    def __init__(self, parent, control):
        super().__init__(parent)
        self.setMinimumWidth(550)

        self.info_bar = QInfoBar()
        self.scene = QScene(control, self.info_bar)
        #self.viewport = QViewport(self.scene)

        layout = QVBoxLayout()
        layout.addWidget(self.scene.viewport)
        layout.addWidget(self.info_bar)

        self.setLayout(layout)
