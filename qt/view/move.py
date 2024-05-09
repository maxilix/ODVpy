from math import ceil

from PyQt6.QtCore import QRectF, Qt, QPointF
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsPathItem, QGraphicsPolygonItem, QGraphicsLineItem

from .abstract_view import View, HierarchicalView


class QViewPathLink(View, QGraphicsLineItem):
    def __init__(self, scene, control):
        super().__init__(control, control.path_link.QLineF())
        self.main_color = QColor(0, 255, 255)

        pen_color = self.main_color
        pen_color.setAlpha(128)
        pen = QPen(pen_color)
        pen.setWidth(1)
        pen.setStyle(Qt.PenStyle.DotLine)

        self.setVisible(False)
        self.setPen(pen)
        scene.addItem(self)



class QViewCrossingPoint(HierarchicalView, QGraphicsItem):
    def __init__(self, scene, control):
        super().__init__(control)
        for m, _ in enumerate(self.control):
            self.view_list.append(QViewPathLink(scene, self.control[m]))

        self.size = 3
        self.main_color = QColor(0, 180, 255)
        pen_color = self.main_color
        pen_color.setAlpha(255)
        self.pen = QPen(pen_color)
        self.pen.setWidth(1)
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        self.setVisible(False)
        self.setPos(self.control.crossing_point.QPointF() - QPointF(self.size/2, self.size/2))
        scene.addItem(self)


    def boundingRect(self) -> QRectF:
        return QRectF(-1, -1, self.size + 2, self.size + 2)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(self.pen)

        # draw cross
        painter.drawLine(QPointF(0, 0), QPointF(self.size, self.size))
        painter.drawLine(QPointF(0, self.size), QPointF(self.size, 0))

        # draw cardinal point
        pad = 3
        # North
        font = painter.font()
        font.setPixelSize(int(2*self.size))
        painter.setFont(font)

        v = self.control.crossing_point.unk_short[1]
        if v >= 32768:
            painter.setPen(QPen(QColor(255, 0, 0)))
            painter.setBrush(QBrush(QColor(255, 0, 0)))
            t = str(65535-v)
        else:
            painter.setPen(QPen(QColor(0, 255, 0)))
            painter.setBrush(QBrush(QColor(0, 255, 0)))
            t = str(v)
        painter.drawText(QRectF(-self.size, -3*self.size-pad, 3*self.size, 3*self.size), Qt.AlignmentFlag.AlignCenter, t)

        # East
        v = self.control.crossing_point.unk_short[2]
        if v >= 32768:
            painter.setPen(QPen(QColor(255, 0, 0)))
            painter.setBrush(QBrush(QColor(255, 0, 0)))
            t = str(65535-v)
        else:
            painter.setPen(QPen(QColor(0, 255, 0)))
            painter.setBrush(QBrush(QColor(0, 255, 0)))
            t = str(v)
        painter.drawText(QRectF(self.size+pad, -self.size, 3*self.size, 3*self.size), Qt.AlignmentFlag.AlignCenter, t)

        # South
        v = self.control.crossing_point.unk_short[3]
        if v >= 32768:
            painter.setPen(QPen(QColor(255, 0, 0)))
            painter.setBrush(QBrush(QColor(255, 0, 0)))
            t = str(65535-v)
        else:
            painter.setPen(QPen(QColor(0, 255, 0)))
            painter.setBrush(QBrush(QColor(0, 255, 0)))
            t = str(v)
        painter.drawText(QRectF(-self.size, self.size+pad, 3*self.size, 3*self.size), Qt.AlignmentFlag.AlignCenter, t)


        # West
        v = self.control.crossing_point.unk_short[0]
        if v >= 32768:
            painter.setPen(QPen(QColor(255, 0, 0)))
            painter.setBrush(QBrush(QColor(255, 0, 0)))
            t = str(65535-v)
        else:
            painter.setPen(QPen(QColor(0, 255, 0)))
            painter.setBrush(QBrush(QColor(0, 255, 0)))
            t = str(v)
        painter.drawText(QRectF(-3*self.size-pad, -self.size, 3*self.size, 3*self.size), Qt.AlignmentFlag.AlignCenter, t)


    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path


class QViewArea(HierarchicalView, QGraphicsPolygonItem):
    def __init__(self, scene, control):
        super().__init__(control, control.area.QPolygonF())
        for l, _ in enumerate(self.control):
            self.view_list.append(QViewCrossingPoint(scene, self.control[l]))

        if self.control.area.is_main():
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

        scene.addItem(self)

    def refresh(self, mousse_position):
        if self.control.area.is_main():
            pass
        else:
            brush_color = self.main_color
            if self.polygon().containsPoint(mousse_position, Qt.FillRule.OddEvenFill):
                self.control.setSelected(True)
                brush_color.setAlpha(64)
                self.setBrush(QBrush(brush_color))
                self.setVisible(True)
            else:
                self.control.setSelected(False)
                brush_color.setAlpha(32)
                self.setBrush(QBrush(brush_color))
                if self.control.checkState(0) == Qt.CheckState.Checked:
                    self.setVisible(True)
                else:
                    self.setVisible(False)

        for view in self.view_list:
            view.refresh(mousse_position)


class QViewSublayer(HierarchicalView, QGraphicsPathItem):
    def __init__(self, scene, control):
        super().__init__(control, control.sublayer.QPainterPath())
        # super(QGraphicsPathItem, self).__init__(control)
        for k, _ in enumerate(self.control):
            self.view_list.append(QViewArea(scene, self.control[k]))


        # self.graphic_area_list = []
        # for k, _ in enumerate(self.control_sublayer.sublayer):
        #     graphic_area = QViewArea(self.control_sublayer.control_area_list[k])
        #     self.graphic_area_list.append(graphic_area)


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
        scene.addItem(self)

    def refresh(self, mousse_position):
        # if self.isVisible():
        #     brush_color = self.main_color
        #     if self.path().contains(mousse_position):
        #         brush_color.setAlpha(32)
        #     else:
        #         brush_color.setAlpha(16)
        #     self.setBrush(QBrush(brush_color))
        for view in self.view_list:
            view.refresh(mousse_position)

class QViewLayer(HierarchicalView):
    def __init__(self, scene, control):
        super().__init__(control)

        for j, _ in enumerate(self.control):
            self.view_list.append(QViewSublayer(scene, self.control[j]))

    def refresh(self, mousse_position):
        for view in self.view_list:
            view.refresh(mousse_position)







class QViewMotion(HierarchicalView):
    def __init__(self, scene, control):
        super().__init__(control)

        for i, _ in enumerate(self.control):
            self.view_list.append(QViewLayer(scene, self.control[i]))

    def refresh(self, mousse_position):
        for view in self.view_list:
            view.refresh(mousse_position)
