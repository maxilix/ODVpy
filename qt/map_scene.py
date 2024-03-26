#!/usr/bin/enc python3


from math import floor, ceil

from PyQt6.QtCore import Qt, QSize, QPoint, QLineF, QRectF, QPointF
from PyQt6.QtGui import QImage, QPixmap, QPolygonF
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsLineItem, QVBoxLayout, QLabel
from PyQt6.QtGui import QPen, QBrush, QColor, QPainterPath

from settings import LEVEL, LOG_FILENAME
from debug import *

from common import *
from dvd import DvdParser
from dvm import DvmParser


class QMapScene(QGraphicsScene):
    def __init__(self, parent, level_index):
        super().__init__(parent)

        self.view = QGraphicsView(self)
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setMouseTracking(True)

        self.max_zoom = 35
        self.min_zoom = 0.7
        self.zoom = 1
        self.zoom_factor = 1.2

        level = LEVEL[level_index]
        dvm = DvmParser(level.dvm)
        dvd = DvdParser(level.dvd)
        dvd.move.build()

        pixmap = QPixmap.fromImage(dvm.level_map)
        self.map = self.addPixmap(pixmap)

        pen = QPen(QColor(0, 255, 0), 2, )
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setBrush(QColor(0, 255, 0, 50))
        #line = QLineF(10, 10, 200, 200)
        #self.rect = QRectF(0,0,500,500)
        #self.line = self.addLine(line, pen)

        self.color = QColor(0, 255, 0, 128)
        pen = QPen(self.color)  # Couleur du contour du polygone
        self.color.setAlpha(48)
        brush = QBrush(self.color)
        poly_t = QPolygonF([QPointF(100-0.5, 100-0.5), QPointF(300-0.5, 120-0.5), QPointF(350-0.5, 500-0.5), QPointF(200-0.5, 550-0.5), QPointF(50-0.5, 250-0.5)])
        poly_t_sub = QPolygonF([QPointF(130-0.5, 130-0.5), QPointF(150-0.5, 130-0.5), QPointF(150-0.5, 150-0.5), QPointF(130-0.5, 150-0.5)])
        #poly_t = poly_t.subtracted(poly_t_sub)
        #self.addPolygon(poly_t, pen, brush)

        #painter = QPainter(self)
        #painter.setRenderHint(QPainter.Antialiasing)  # Pour un rendu plus lisse

        path = QPainterPath()
        path.addPolygon(poly_t)

        hole = QPainterPath()
        hole.addPolygon(poly_t_sub)

        path = path.subtracted(hole)

        #painter.fillPath(path, QColor(100, 100, 255))  # Remplit la forme résultante avec une couleur

        self.addPath(path, pen, brush)


        self.color = QColor(255, 0, 0, 128)
        pen = QPen(self.color)  # Couleur du contour du polygone
        self.color.setAlpha(16)
        brush = QBrush(self.color)
        self.disallow_poly = dvd.move.disallow_QPolygonF(0, 0)
        #print(self.disallow_poly[0])
        self.disallow_poly_item = [self.addPolygon(poly, pen, brush) for poly in self.disallow_poly]
        #print(self.disallow_poly_item[0].polygon())

    def mouseMoveEvent(self, event):
        pos = event.scenePos()
        for poly_item in self.disallow_poly_item:
            if poly_item.polygon().containsPoint(pos, Qt.FillRule.OddEvenFill):
                self.color.setAlpha(32)
                brush = QBrush(self.color)
            else:
                self.color.setAlpha(16)
                brush = QBrush(self.color)
            poly_item.setBrush(brush)
        self.parent().label.setText(f"x:{floor(pos.x())}\ty:{floor(pos.y())}\tzoom:{round(self.zoom*100)}%")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            pos = event.scenePos()
            print(pos)
            #self.line.setPen(QPen(QColor(255, 0, 0), 1))
            #print(self.line.scale())

            #self.line.setVisible(False)
            #self.line.setVisible(True)

    def wheelEvent(self, event):
        event.accept()
        # print(event.delta())

        if event.delta() > 0 and self.zoom < self.max_zoom:
            self.view.scale(self.zoom_factor, self.zoom_factor)
            self.zoom *= self.zoom_factor
        elif event.delta() < 0 and self.zoom > self.min_zoom:
            self.view.scale(1.0 / self.zoom_factor, 1.0 / self.zoom_factor)
            self.zoom /= self.zoom_factor
        else:
            pass

        scene_position = event.scenePos()
        global_position = event.screenPos()
        relative_position = self.view.mapFromGlobal(global_position)
        size = self.view.size()
        new_position = QPointF(scene_position.x() + (size.width() /2-relative_position.x())/(1.1 * self.zoom),
                               scene_position.y() + (size.height()/2-relative_position.y())/(1.1 * self.zoom))
        self.view.centerOn(new_position)

