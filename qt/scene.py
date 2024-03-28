#!/usr/bin/enc python3


from math import floor, ceil

from PyQt6.QtCore import Qt, QSize, QPoint, QLineF, QRectF, QPointF
from PyQt6.QtGui import QImage, QPixmap, QPolygonF
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, \
    QGraphicsLineItem, QVBoxLayout, QLabel
from PyQt6.QtGui import QPen, QBrush, QColor, QPainterPath


class QViewport(QGraphicsView):

    def __init__(self, scene):
        super().__init__(scene)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMouseTracking(True)

        self.max_zoom = 35
        self.min_zoom = 0.5
        self.zoom = 1
        self.zoom_factor = 1.2


class QScene(QGraphicsScene):
    def __init__(self, parent, info_bar, dvm):
        super().__init__(parent)
        self.info_bar = info_bar
        self.viewport = QViewport(self)

        pixmap = QPixmap(dvm.level_map)
        self.map = self.addPixmap(pixmap)

        self.drawn_move_area = dict()
        self.drawn_sublayer = dict()

    def mouseMoveEvent(self, event):
        pos = event.scenePos()
        self.info_bar.update(x=pos.x(), y=pos.y())

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

    def wheelEvent(self, event):
        event.accept()

        if event.delta() > 0 and self.viewport.zoom < self.viewport.max_zoom:
            self.viewport.scale(self.viewport.zoom_factor, self.viewport.zoom_factor)
            self.viewport.zoom *= self.viewport.zoom_factor
        elif event.delta() < 0 and self.viewport.zoom > self.viewport.min_zoom:
            self.viewport.scale(1.0 / self.viewport.zoom_factor, 1.0 / self.viewport.zoom_factor)
            self.viewport.zoom /= self.viewport.zoom_factor
        else:
            pass

        scene_position = event.scenePos()
        global_position = event.screenPos()
        relative_position = self.viewport.mapFromGlobal(global_position)
        size = self.viewport.size()
        new_position = QPointF(scene_position.x() + (size.width() /2-relative_position.x()) / (1.1 * self.viewport.zoom),
                               scene_position.y() + (size.height()/2-relative_position.y()) / (1.1 * self.viewport.zoom))
        self.viewport.centerOn(new_position)
        self.info_bar.update(zoom=self.viewport.zoom)

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