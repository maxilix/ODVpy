from PyQt6.QtGui import QPolygonF

from qt.graphics.common import QCGItemGroup
from qt.graphics.element import QCGPoint, QCGLineElement, QCGPolygonShapeElement, QCGPolygonFixElement


# class QCGHighlightablePolygon(QCGPolygon):
#     def __init__(self, q_dvd_item, polygon: QPolygonF):
#         super().__init__(q_dvd_item, polygon)
#         self.setAcceptHoverEvents(True)
#
#     def hoverEnterEvent(self, event):
#         # self._force_visibility = True
#         # self.setBrush(QBrush(Qt.GlobalColor.transparent))
#         self.setBrush(self.q_dvd_item.high_brush)
#         # self.update()
#         super().hoverEnterEvent(event)
#
#     def hoverLeaveEvent(self, event):
#         # self._force_visibility = False
#         self.setBrush(self.q_dvd_item.brush)
#         # self.update()
#         super().hoverLeaveEvent(event)


class QCGPolygonGroup(QCGItemGroup):

    def __init__(self, inspector):
        super().__init__(inspector)
        self.polygon_fix = None
        self.point_item = []
        self.line_item = []
        self.polygon_shape = None

        self.exit_edit_mode(save=False)
        self.update()

    @property
    def polygon(self):
        return self.inspector.polygon

    @polygon.setter
    def polygon(self, polygon):
        self.inspector.polygon = polygon

    def enter_edit_mode(self):
        self.remove_child(self.polygon_fix)
        self.polygon_fix = None

        deletable = len(self.inspector.polygon) > 3
        self.point_item = [QCGPoint(self.inspector, p, movable=True, deletable=deletable) for p in self.polygon]
        self.line_item = [QCGLineElement(self.inspector, p1, p2, secable=True, deletable=False) for p1, p2 in
                          zip(self.point_item, self.point_item[1:] + [self.point_item[0]])]
        self.polygon_shape = QCGPolygonShapeElement(self.inspector, self.point_item, movable=True)
        self.add_child(self.polygon_shape)
        self.add_children(self.line_item)
        self.add_children(self.point_item)

        self.update()

    def exit_edit_mode(self, save):
        if save is True:
            self.polygon = QPolygonF(p.pos() for p in self.point_item)

        self.remove_child(self.polygon_shape)
        self.polygon_shape = None
        self.remove_children(self.line_item)
        self.line_item = []
        self.remove_children(self.point_item)
        self.point_item = []

        self.polygon_fix = QCGPolygonFixElement(self.inspector, self.polygon)
        self.add_child(self.polygon_fix)

        self.update()

    def point_moved(self, point_item: QCGPoint):
        n = len(self.point_item)
        index = self.point_item.index(point_item)
        self.line_item[(index - 1) % n].update()
        self.line_item[index].update()
        self.polygon_shape.update()

    def point_added(self,
                    previous_point_item: QCGPoint,
                    new_point_item: QCGPoint,
                    new_line_item: QCGLineElement):
        index = self.point_item.index(previous_point_item)
        self.point_item.insert(index + 1, new_point_item)
        new_point_item.setParentItem(self)
        self.line_item.insert(index + 1, new_line_item)
        new_line_item.setParentItem(self)

        for p in self.point_item:
            p.deletable = True
        self.polygon_shape.p_list = self.point_item

    def point_deleted(self, point_item: QCGPoint):
        n = len(self.point_item)
        index = self.point_item.index(point_item)
        self.line_item[(index - 1) % n].p2 = self.point_item[(index + 1) % n]
        self.line_item[index].delete()
        self.line_item.remove(self.line_item[index])
        self.point_item.remove(point_item)
        if len(self.point_item) <= 3:
            for p in self.point_item:
                p.deletable = False
        self.polygon_shape.p_list = self.point_item

    def line_deleted(self, line_item: QCGLineElement):
        pass

    def polygon_shape_deleted(self, polygon_shape: QCGPolygonShapeElement):
        pass
