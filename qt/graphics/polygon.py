from PyQt6.QtGui import QPolygonF
from PyQt6.QtWidgets import QGraphicsPolygonItem

from qt.graphics.common import CustomGraphicsItem, QCGItemGroup
from qt.graphics.element import QCGPoint, QCGLineElement, QCGPolygonShapeElement


class QCGPolygon(CustomGraphicsItem, QGraphicsPolygonItem):
    def __init__(self, q_dvd_item, polygon: QPolygonF):
        super().__init__(q_dvd_item, polygon.translated(0.5, 0.5))
        self.setBrush(q_dvd_item.brush)
        self.setPen(q_dvd_item.pen)


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


class QCGEditablePolygon(QCGItemGroup):
    def __init__(self, q_dvd_item, polygon: QPolygonF):
        super().__init__(q_dvd_item)

        deletable = len(polygon) > 3
        self.point_item = [QCGPoint(self.q_dvd_item, p, movable=True, deletable=deletable) for p in polygon]
        self.line_item = [QCGLineElement(self.q_dvd_item, p1, p2, secable=True, deletable=False) for p1, p2 in
                          zip(self.point_item, self.point_item[1:] + [self.point_item[0]])]
        self.polygon_shape = QCGPolygonShapeElement(self.q_dvd_item, self.point_item, movable=True)

        self.add_child(self.polygon_shape)
        self.add_children(self.line_item)
        self.add_children(self.point_item)

        self.update()

    def __iter__(self):
        return iter(self.point_item)

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
