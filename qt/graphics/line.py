from PyQt6.QtCore import QLineF, QRectF, Qt
from PyQt6.QtGui import QPainter, QTransform
from PyQt6.QtWidgets import QGraphicsLineItem

from qt.graphics.common import QCGItemGroup, CustomGraphicsItem
from qt.graphics.element import QCGLineElement
from qt.graphics.point import QCGPoint


class QCFGLine(CustomGraphicsItem, QGraphicsLineItem):
    def __init__(self, sub_inspector, line: QLineF):
        super().__init__(sub_inspector, line.truncated().translated(0.5, 0.5))
        self.setPen(self.sub_inspector.pen)

    def shape(self):
        # virtually extends the line width for click detection
        temp_line = QGraphicsLineItem(self.line())
        pen = self.pen()
        pen.setWidthF(pen.widthF() * 5)
        temp_line.setPen(pen)
        return temp_line.shape()


class QCEGLine(QCGItemGroup):
    def __init__(self, sub_inspector):
        super().__init__(sub_inspector)

        self.line_fix = None
        self.p1_item = None
        self.p2_item = None
        self.line_item = None

        # self.setZValue(1)

        self.exit_edit_mode(save=False)
        self.update()

    @property
    def line(self):
        return self.sub_inspector.current

    @line.setter
    def line(self, line):
        self.sub_inspector.current = line


    def enter_edit_mode(self):
        self.remove_child(self.line_fix)
        self.line_fix = None

        self.p1_item = QCGPoint(self.sub_inspector, self.line.p1(), movable=True, deletable=False)
        self.p2_item = QCGPoint(self.sub_inspector, self.line.p2(), movable=True, deletable=False)
        self.line_item = QCGLineElement(self.sub_inspector, self.p1_item, self.p2_item, secable=False, deletable=True)
        self.add_child(self.p1_item)
        self.add_child(self.p2_item)
        self.add_child(self.line_item)

        self.update()

    def exit_edit_mode(self, save):
        if save is True:
            self.line = QLineF(self.p1_item.pos(), self.p2_item.pos())

        self.remove_child(self.p1_item)
        self.p1_item = None
        self.remove_child(self.p2_item)
        self.p2_item = None
        self.remove_child(self.line_item)
        self.line_item = None

        self.line_fix = QCFGLine(self.sub_inspector, self.line)
        self.add_child(self.line_fix)

        self.update()




    def point_moved(self, point_item: QCGPoint):
        self.line_item.update()

    def point_deleted(self, point_item: QCGPoint):
        pass

    def line_deleted(self, line_item: QCGLineElement):
        # self.p1_item.delete()
        # self.p2_item.delete()
        self.delete()
