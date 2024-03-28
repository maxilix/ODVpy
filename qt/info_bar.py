#!/usr/bin/enc python3


from math import floor, ceil

from PyQt6.QtCore import Qt, QSize, QPoint, QLineF, QRectF, QPointF
from PyQt6.QtGui import QImage, QPixmap, QPolygonF
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsLineItem, QVBoxLayout, QLabel
from PyQt6.QtGui import QPen, QBrush, QColor, QPainterPath

from debug import *

from common import *
from dvd import DvdParser
from dvm import DvmParser


class QInfoBar(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._x = 0
        self._y = 0
        self._zoom = 100
        self.refresh()

    def update(self, **kwargs):
        if "x" in kwargs:
            self._x = kwargs["x"]
        if "y" in kwargs:
            self._y = kwargs["y"]
        if "zoom" in kwargs:
            self._zoom = kwargs["zoom"]
        self.refresh()

    def refresh(self):
        self.setText(f"x:{floor(self._x)}\ty:{floor(self._y)}\tzoom:{round(self._zoom*100)}%")

