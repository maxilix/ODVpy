from math import floor, ceil

from PyQt6.QtCore import Qt, QSize, QPoint, QLineF, QRectF, QPointF
from PyQt6.QtGui import QImage, QPixmap, QPolygonF
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, \
    QGraphicsLineItem, QVBoxLayout, QLabel
from PyQt6.QtGui import QPen, QBrush, QColor, QPainterPath

from settings import LEVEL, LOG_FILENAME
from debug import *

from common import *
from dvd import DvdParser
from dvm import DvmParser

from .map_scene import QMapScene
from .label_view import QLabelView


class QViewer(QWidget):
    def __init__(self, level_index):
        super().__init__()

        self.scene = QMapScene(self, level_index)
        self.label = QLabelView()

        layout = QVBoxLayout()
        layout.addWidget(self.scene.view)
        layout.addWidget(self.label)

        self.setLayout(layout)