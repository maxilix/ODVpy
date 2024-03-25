#!/usr/bin/enc python3

import sys
from math import floor, ceil

from PyQt6.QtCore import Qt, QSize, QPoint, QLineF, QRectF, QPointF
from PyQt6.QtGui import QImage, QPixmap, QPolygonF, QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsLineItem, QVBoxLayout, QLabel, QToolBar
from PyQt6.QtGui import QPen, QBrush, QColor

from q_scene import QViewer

from settings import LEVEL, LOG_FILENAME
from debug import *

from common import *
from dvd import DvdParser
from dvm import DvmParser


class QWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Main Window')
        self.setMinimumSize(QSize(800, 600))
        self.showMaximized()
        self.level_index = -1

        #toolbar = QToolBar("My main toolbar")
        #toolbar.setIconSize(QSize(16, 16))
        #self.addToolBar(toolbar)



        #toolbar.addSeparator()

        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        #file_menu.addAction(button_action)
        #file_menu.addSeparator()

        file_submenu = file_menu.addMenu("Open Original Level")
        #file_submenu.addAction(button_action2)


        for i in range (26):
            if i == 0:
                load_level_action = QAction(f"Demo level", self)
                #load_level_action.setData(i)
                #load_level_action.setStatusTip(f"Load demo level")
            else:
                load_level_action = QAction(f"Level {i}", self)
                #load_level_action.setData(i)
                #load_level_action.setStatusTip(f"Load level {i}")
            #load_level_action.
            load_level_action.triggered.connect(lambda state, index=i: self.load_level(index))
            file_submenu.addAction(load_level_action)
        self.update()
            #load_level_action.setCheckable(True)

        #toolbar.addAction(button_action)

        #toolbar.addWidget(QLabel("Hello"))
        #toolbar.addWidget(QCheckBox())

        #self.setStatusBar(QStatusBar(self))


    def load_level(self, level_index):
        self.level_index = level_index
        self.update()

        #print(level_index)

    def update(self):
        if self.level_index >= 0:
            w = QViewer(self.level_index)
        else:
            w = QLabel("Select level")
            w.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(w)

def main():
    #level_index = int(sys.argv[1])
    #level = LEVEL[level_index]
    #dvm = DvmParser(level.dvm)
    #dvd = DvdParser(level.dvd)
    app = QApplication([])
    viewer = QWindow()
    viewer.show()
    app.exec()


if __name__ == '__main__':
    main()