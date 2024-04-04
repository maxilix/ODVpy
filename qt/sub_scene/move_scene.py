from math import ceil

from PyQt6.QtCore import QRectF, Qt, QPointF
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsPathItem, QGraphicsPolygonItem, QGraphicsLineItem


class QGraphicPathLinkItem(QGraphicsLineItem):
    def __init__(self, path_link_line):
        super().__init__(path_link_line)
        self.main_color = QColor(0, 255, 255)

        pen_color = self.main_color
        pen_color.setAlpha(128)
        pen = QPen(pen_color)
        pen.setWidth(1)
        pen.setStyle(Qt.PenStyle.DotLine)

        self.setVisible(False)
        self.setPen(pen)


class QGraphicPointItem(QGraphicsItem):
    def __init__(self, position, size=3):
        super().__init__()
        self.size = size
        self.main_color = QColor(0, 180, 255)
        pen_color = self.main_color
        pen_color.setAlpha(255)
        self.pen = QPen(pen_color)
        self.pen.setWidth(1)
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        self.setVisible(False)
        self.setPos(position - QPointF(size/2, size/2))

    def boundingRect(self) -> QRectF:
        return QRectF(-1, -1, self.size + 2, self.size + 2)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(self.pen)
        # draw cross
        painter.drawLine(QPointF(0, 0), QPointF(self.size, self.size))
        painter.drawLine(QPointF(0, self.size), QPointF(self.size, 0))

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path


class QGraphicAreaItem(QGraphicsPolygonItem):
    def __init__(self, area_polygon, is_main=False):
        super().__init__(area_polygon)
        if is_main:
            self.main_color = QColor(160, 200, 40)
        else:
            self.main_color = QColor(255, 90, 40)

        pen_color = self.main_color
        pen_color.setAlpha(128)
        pen = QPen(pen_color)
        pen.setWidth(1)

        brush_color = self.main_color
        brush_color.setAlpha(32)
        brush = QBrush(brush_color)

        self.setVisible(False)
        self.setPen(pen)
        self.setBrush(brush)

    def refresh(self, mousse_position):
        if self.isVisible():
            brush_color = self.main_color
            if self.polygon().containsPoint(mousse_position, Qt.FillRule.OddEvenFill):
                brush_color.setAlpha(64)
            else:
                brush_color.setAlpha(32)
            self.setBrush(QBrush(brush_color))


class QGraphicSublayerItem(QGraphicsPathItem):
    def __init__(self, sublayer_path):
        super().__init__(sublayer_path)
        # self.main_color = QColor(64, 128, 64)
        self.main_color = QColor(180, 110, 30)

        pen_color = self.main_color
        pen_color.setAlpha(128)
        pen = QPen(pen_color)
        pen.setWidth(1)

        # brush_color = self.main_color
        # brush_color.setAlpha(16)
        # brush = QBrush(brush_color)

        self.setVisible(False)
        self.setPen(pen)
        # self.setBrush(brush)

    def refresh(self, mousse_position):
        pass
        # if self.isVisible():
        #     brush_color = self.main_color
        #     if self.path().contains(mousse_position):
        #         brush_color.setAlpha(32)
        #     else:
        #         brush_color.setAlpha(16)
        #     self.setBrush(QBrush(brush_color))


class MoveScene(object):
    def __init__(self, scene, motion):
        self.scene = scene
        self.motion = motion

        self.sublayer_item = []  # [QGraphicSublayerItem(sublayer.QPainterPath()) for sublayer in layer] for layer in self.motion]
        for layer in self.motion:
            self.sublayer_item.append([])
            for sublayer in layer:
                sublayer_item = QGraphicSublayerItem(sublayer.QPainterPath())
                self.sublayer_item[-1].append(sublayer_item)
                self.scene.addItem(sublayer_item)

        self.area_item = []
        for layer in self.motion:
            self.area_item.append([])
            for sublayer in layer:
                self.area_item[-1].append([])
                for k, area in enumerate(sublayer):
                    area_item = QGraphicAreaItem(area.QPolygonF(), k == 0)
                    self.area_item[-1][-1].append(area_item)
                    self.scene.addItem(area_item)

        self.crossing_point_item = []
        for layer in self.motion:
            self.crossing_point_item.append([])
            for sublayer in layer:
                self.crossing_point_item[-1].append([])
                for area in sublayer:
                    self.crossing_point_item[-1][-1].append([])
                    for crossing_point in area:
                        crossing_point_item = QGraphicPointItem(crossing_point.QPointF())
                        self.crossing_point_item[-1][-1][-1].append(crossing_point_item)
                        self.scene.addItem(crossing_point_item)

        self.path_link_item = []
        for path_link in motion.path_link_list:
            path_link_item = QGraphicPathLinkItem(path_link.QLineF(motion))
            self.path_link_item.append(path_link_item)
            self.scene.addItem(path_link_item)

    def refresh(self, mousse_position):
        for item_list in self.sublayer_item:
            for item in item_list:
                item.refresh(mousse_position)

        for item_list_list in self.area_item:
            for item_list in item_list_list:
                for item in item_list:
                    item.refresh(mousse_position)

    def show_sublayer(self, i, j):
        self.sublayer_item[i][j].setVisible(True)

    def hide_sublayer(self, i, j):
        self.sublayer_item[i][j].setVisible(False)

    def show_area(self, i, j, k):
        self.area_item[i][j][k].setVisible(True)

    def hide_area(self, i, j, k):
        self.area_item[i][j][k].setVisible(False)

    def show_crossing_point(self, i, j, k, l):
        self.crossing_point_item[i][j][k][l].setVisible(True)

    def hide_crossing_point(self, i, j, k, l):
        self.crossing_point_item[i][j][k][l].setVisible(False)

    def show_path_link(self, m):
        self.path_link_item[m].setVisible(True)

    def hide_path_link(self, m):
        self.path_link_item[m].setVisible(False)