
import sys
from math import floor, ceil

from PyQt6.QtCore import Qt, QSize, QPoint, QLineF, QRectF, QPointF
from PyQt6.QtGui import QImage, QPixmap, QPolygonF, QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsLineItem, QVBoxLayout, QHBoxLayout, QLabel, QToolBar
from PyQt6.QtGui import QPen, QBrush, QColor

from qt.viewer import QViewer
from qt.control import QControl

from settings import LEVEL, LOG_FILENAME
from debug import *

from common import *
from dvd import DvdParser
from dvm import DvmParser


class QWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Open Death Valley py')
        self.setMinimumSize(QSize(800, 600))
        self.showMaximized()
        self.level_index = 0

        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_submenu = file_menu.addMenu("Open Original Level")

        for i in range (26):
            if i == 0:
                load_level_action = QAction(f"Demo level", self)
            else:
                load_level_action = QAction(f"Level {i}", self)
            load_level_action.triggered.connect(lambda state, index=i: self.load_level(index))
            file_submenu.addAction(load_level_action)

        self.update()

    def load_level(self, level_index):
        self.level_index = level_index
        self.update()

    def update(self):
        layout = QHBoxLayout()
        layout.addWidget(QViewer(self.level_index))
        layout.addWidget(QControl())

        # if self.level_index >= 0:
        #     w = QViewer(self.level_index)
        # else:
        #     w = QLabel("Select level")
        #     w.setAlignment(Qt.AlignmentFlag.AlignCenter)

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)


if __name__ == '__main__':
    app = QApplication([])
    viewer = QWindow()
    viewer.show()
    app.exec()