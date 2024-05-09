
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from .info_bar import QInfoBar
from qt.view import QMainView


class QViewer(QWidget):
    def __init__(self, parent, control):
        super().__init__(parent)
        self.setMinimumWidth(550)

        self.info_bar = QInfoBar()
        self.main_view = QMainView(control, self.info_bar)
        #self.viewport = QViewport(self.scene)

        layout = QVBoxLayout()
        layout.addWidget(self.main_view.viewport)
        layout.addWidget(self.info_bar)

        self.setLayout(layout)
