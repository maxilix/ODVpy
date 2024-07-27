from PyQt6.QtCore import QLineF

from qt.graphics.common import QCGItemGroup
from qt.graphics.element import QCGLineElement
from qt.graphics.point import QCGPoint


class QCGLine(QCGItemGroup):
    def __init__(self, control, line: QLineF):
        super().__init__(control)

        self.p1_item = QCGPoint(self.control, line.p1(), movable=True, deletable=False)
        self.p2_item = QCGPoint(self.control, line.p2(), movable=True, deletable=False)
        self.line_item = QCGLineElement(self.control, self.p1_item, self.p2_item, secable=False, deletable=True)

        self.add_child(self.p1_item)
        self.add_child(self.p2_item)
        self.add_child(self.line_item)

        self.update()

    def __iter__(self):
        return iter(self.point_item)

    def point_moved(self, point_item: QCGPoint):
        self.line_item.update()

    def point_deleted(self, point_item: QCGPoint):
        pass

    def line_deleted(self, line_item: QCGLineElement):
        self.p1_item.delete()
        self.p2_item.delete()
        self.delete()
