from PyQt6.QtCore import QLineF, QRectF, Qt
from PyQt6.QtGui import QPainter, QTransform
from PyQt6.QtWidgets import QGraphicsLineItem

from qt.graphics.common import QCGItemGroup, CustomGraphicsItem
from qt.graphics.element import QCGLineElement
from qt.graphics.point import QCGPoint


class QCGFixedLine(CustomGraphicsItem, QGraphicsLineItem):
    # def __init__(self, line: QLineF):
    #     super().__init__(line.translated(0.5, 0.5))

    def shape(self):
        # virtually extends the line width for click detection
        temp_line = QGraphicsLineItem(self.line())
        pen = self.pen()
        pen.setWidthF(pen.widthF() * 5)
        temp_line.setPen(pen)
        return temp_line.shape()





class QCGEditableLine(QCGItemGroup):
    def __init__(self, q_dvd_item, line: QLineF):
        super().__init__(q_dvd_item)

        self.p1_item = QCGPoint(self.odv_object, line.p1(), movable=True, deletable=False)
        self.p2_item = QCGPoint(self.odv_object, line.p2(), movable=True, deletable=False)
        self.line_item = QCGLineElement(self.odv_object, self.p1_item, self.p2_item, secable=False, deletable=True)
        self.setZValue(1)

        self.add_child(self.p1_item)
        self.add_child(self.p2_item)
        self.add_child(self.line_item)

        self.update()

    def point_moved(self, point_item: QCGPoint):
        self.line_item.update()

    def point_deleted(self, point_item: QCGPoint):
        pass

    def line_deleted(self, line_item: QCGLineElement):
        # self.p1_item.delete()
        # self.p2_item.delete()
        self.delete()
