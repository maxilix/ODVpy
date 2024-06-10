from math import ceil

from PyQt6.QtCore import QRectF, Qt, QPointF
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter, QPainterPath, QFont
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsPathItem, QGraphicsPolygonItem, QGraphicsLineItem, \
    QGraphicsSimpleTextItem

from .abstract_view import View, HierarchicalView


class QViewArea(View, QGraphicsPolygonItem):
    def __init__(self, scene, control):
        super().__init__(control, control.area.QPolygonF())

        if self.control.area.main:
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
        if self.control.area.main:
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
