
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from .info_bar import QInfoBar
from .scene import QScene


class QViewer(QWidget):
    def __init__(self, level):
        super().__init__()

        self.info_bar = QInfoBar()
        self.scene = QScene(self, self.info_bar, level)
        #self.viewport = QViewport(self.scene)

        layout = QVBoxLayout()
        layout.addWidget(self.scene.viewport)
        layout.addWidget(self.info_bar)

        self.setLayout(layout)
