
from math import floor, ceil

from PyQt6.QtCore import Qt, QSize, QPoint, QLineF, QRectF, QPointF
from PyQt6.QtGui import QImage, QPixmap, QPolygonF
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, \
    QGraphicsLineItem, QVBoxLayout, QLabel
from PyQt6.QtGui import QPen, QBrush, QColor, QPainterPath


class MoveScene(object):
    def __init__(self, scene, motion):
        self.scene = scene
        self.motion = motion
        # self.sublayer_color = QColor(0, 255, 0)
        # pen_color = self.sublayer_color
        # pen_color.setAlpha(32)
        self.sublayer_pen = QPen(QColor(0, 255, 0, 128))
        self.sublayer_brush = QBrush(QColor(0, 255, 0, 16))
        self.sublayer_highlight = True
        self.sublayer_draw = []
        for layer in self.motion:
            self.sublayer_draw.append([])
            for sublayer in layer:
                sublayer_draw = self.scene.addPath(sublayer.QPainterPath(),
                                                   self.sublayer_pen,
                                                   self.sublayer_brush)
                sublayer_draw.setVisible(False)
                self.sublayer_draw[-1].append(sublayer_draw)

        self.area_pen = QColor(255, 0, 0, 128)
        self.area_blush = QColor(255, 0, 0, 16)

    def refresh(self, mousse_position):
        # pos = event.scenePos()
        if self.sublayer_highlight:
            for draw_list in self.sublayer_draw:
                for draw in draw_list:
                    if draw.isVisible():
                        color = self.sublayer_brush.color()
                        if draw.path().contains(mousse_position):
                            color.setAlpha(32)
                        else:
                            color.setAlpha(16)
                        draw.setBrush(QBrush(color))

    def show_sublayer(self, i, j):
        self.sublayer_draw[i][j].setVisible(True)

    def hide_sublayer(self, i, j):
        self.sublayer_draw[i][j].setVisible(False)

    # def add_move_area(self, indexes, move_area):
    #     if indexes in self.drawn_move_area:
    #         self.drawn_move_area[indexes].setVisible(True)
    #     else:
    #         color = QColor(255, 0, 0, 128)
    #         pen = QPen(color)  # outline color
    #         color.setAlpha(16)
    #         brush = QBrush(color)  # fill color
    #         self.drawn_move_area[indexes] = self.addPolygon(move_area.QPolygonF(), pen, brush)
    #
    # def remove_move_area(self, indexes):
    #     if indexes in self.drawn_move_area:
    #         self.drawn_move_area[indexes].setVisible(False)
    #
    # def add_sublayer(self, indexes, sublayer):
    #     if indexes in self.drawn_sublayer:
    #         self.drawn_sublayer[indexes].setVisible(True)
    #     else:
    #         color = QColor(0, 255, 0, 128)
    #         pen = QPen(color)  # outline color
    #         color.setAlpha(16)
    #         brush = QBrush(color)  # fill color
    #         self.drawn_sublayer[indexes] = self.addPath(sublayer.QPainterPath(), pen, brush)
    #
    # def remove_sublayer(self, indexes):
    #     if indexes in self.drawn_sublayer:
    #         self.drawn_sublayer[indexes].setVisible(False)
