
import sys
from math import floor, ceil

from PyQt6.QtCore import Qt, QSize, QPoint, QLineF, QRectF, QPointF
from PyQt6.QtGui import QImage, QPixmap, QPolygonF, QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsLineItem, QVBoxLayout, QHBoxLayout, QLabel, QToolBar
from PyQt6.QtGui import QPen, QBrush, QColor

from qt.viewer import QViewer
from qt.control import QControl

from settings import original_level_filename
from debug import *

from common import *
from dvd import DvdParser
from dvm import DvmParser


class ODVLevel(object):
    def __init__(self, filename):
        self.dvd = DvdParser(filename + ".dvd")
        self.dvm = DvmParser(filename + ".dvm")


class QWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Open Death Valley py')
        # self.setMinimumSize(QSize(800, 600))
        self.showMaximized()
        # self.setGeometry(0, 0, 500, 500)
        self.current_level = None
        # self.current_level = ODVLevel(original_level_filename(0))

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

        unload_level_action = QAction("Close level", self)
        unload_level_action.triggered.connect(self.unload_level)
        file_menu.addAction(unload_level_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(exit)
        file_menu.addAction(quit_action)

        self.update()

    def load_level(self, index=None):
        self.current_level = ODVLevel(original_level_filename(index))
        self.update()

    def unload_level(self):
        self.current_level = None
        self.update()

    def update(self):
        layout = QHBoxLayout()
        if self.current_level is None:
            q_label = QLabel("Select level")
            q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(q_label)
        else:
            viewer = QViewer(self.current_level)
            control = QControl(viewer.scene, self.current_level)
            viewer.scene.set_control_pointer(control)

            layout.addWidget(viewer)
            layout.addWidget(control)

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)


if __name__ == '__main__':
    app = QApplication([])
    window = QWindow()
    window.show()
    app.exec()
