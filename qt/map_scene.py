#!/usr/bin/enc python3


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


class QMapScene(QGraphicsScene):
    def __init__(self, parent, level):
        super().__init__(parent)

        self.view = QGraphicsView(self)
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setMouseTracking(True)

        self.max_zoom = 35
        self.min_zoom = 0.5
        self.zoom = 1
        self.zoom_factor = 1.2


        dvm = level.dvm
        dvd = level.dvd
        dvd.move.build()

        pixmap = QPixmap.fromImage(dvm.level_map)
        self.map = self.addPixmap(pixmap)

        # pen = QPen(QColor(0, 255, 0), 2, )
        # pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        # pen.setBrush(QColor(0, 255, 0, 50))
        # #line = QLineF(10, 10, 200, 200)
        # #self.rect = QRectF(0,0,500,500)
        # #self.line = self.addLine(line, pen)
        #
        # self.color = QColor(0, 255, 0, 128)
        # pen = QPen(self.color)  # Couleur du contour du polygone
        # self.color.setAlpha(48)
        # brush = QBrush(self.color)
        # poly_t = QPolygonF([QPointF(100-0.5, 100-0.5), QPointF(300-0.5, 120-0.5), QPointF(350-0.5, 500-0.5), QPointF(200-0.5, 550-0.5), QPointF(50-0.5, 250-0.5)])
        # poly_t_sub = QPolygonF([QPointF(130-0.5, 130-0.5), QPointF(150-0.5, 130-0.5), QPointF(150-0.5, 150-0.5), QPointF(130-0.5, 150-0.5)])
        # #poly_t = poly_t.subtracted(poly_t_sub)
        # #self.addPolygon(poly_t, pen, brush)
        #
        # #painter = QPainter(self)
        # #painter.setRenderHint(QPainter.Antialiasing)  # Pour un rendu plus lisse
        #
        # path = QPainterPath()
        # path.addPolygon(poly_t)
        #
        # hole = QPainterPath()
        # hole.addPolygon(poly_t_sub)
        #
        # path = path.subtracted(hole)
        #
        # #painter.fillPath(path, QColor(100, 100, 255))  # Remplit la forme résultante avec une couleur
        #
        # path_draw = self.addPath(path, pen, brush)

        self.drawn_move_area = dict()
        self.drawn_sublayer = dict()

    def mouseMoveEvent(self, event):
        pos = event.scenePos()

        self.parent().label.setText(f"x:{floor(pos.x())}\ty:{floor(pos.y())}\tzoom:{round(self.zoom*100)}%")

        for move_area_key in self.drawn_move_area:
            if (draw := self.drawn_move_area[move_area_key]).isVisible():
                color = draw.brush().color()
                if draw.polygon().containsPoint(pos, Qt.FillRule.OddEvenFill):
                    color.setAlpha(32)
                else:
                    color.setAlpha(16)
                draw.setBrush(QBrush(color))

        for sublayer_key in self.drawn_sublayer:
            if (draw := self.drawn_sublayer[sublayer_key]).isVisible():
                color = draw.brush().color()
                if draw.path().contains(pos):
                    color.setAlpha(32)
                else:
                    color.setAlpha(16)
                draw.setBrush(QBrush(color))

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

    def add_move_area(self, indexes, move_area):
        if indexes in self.drawn_move_area:
            self.drawn_move_area[indexes].setVisible(True)
        else:
            color = QColor(255, 0, 0, 128)
            pen = QPen(color)  # outline color
            color.setAlpha(16)
            brush = QBrush(color)  # fill color
            self.drawn_move_area[indexes] = self.addPolygon(move_area.QPolygonF(), pen, brush)

    def remove_move_area(self, indexes):
        if indexes in self.drawn_move_area:
            self.drawn_move_area[indexes].setVisible(False)

    def add_sublayer(self, indexes, sublayer):
        if indexes in self.drawn_sublayer:
            self.drawn_sublayer[indexes].setVisible(True)
        else:
            color = QColor(0, 255, 0, 128)
            pen = QPen(color)  # outline color
            color.setAlpha(16)
            brush = QBrush(color)  # fill color
            self.drawn_sublayer[indexes] = self.addPath(sublayer.QPainterPath(), pen, brush)

    def remove_sublayer(self, indexes):
        if indexes in self.drawn_sublayer:
            self.drawn_sublayer[indexes].setVisible(False)