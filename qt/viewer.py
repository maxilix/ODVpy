from math import floor, ceil

from PyQt6.QtCore import Qt, QSize, QPoint, QLineF, QRectF, QPointF
from PyQt6.QtGui import QImage, QPixmap, QPolygonF
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, \
    QGraphicsLineItem, QVBoxLayout, QLabel
from PyQt6.QtGui import QPen, QBrush, QColor, QPainterPath

from debug import *

from common import *
from dvd import DvdParser
from dvm import DvmParser

from .scene import QScene
from .info_bar import QInfoBar



class QViewer(QWidget):
    def __init__(self, level):
        super().__init__()

        self.info_bar = QInfoBar()
        self.scene = QScene(self, self.info_bar, level.dvm)
        #self.viewport = QViewport(self.scene)

        layout = QVBoxLayout()
        layout.addWidget(self.scene.viewport)
        layout.addWidget(self.info_bar)

        self.setLayout(layout)