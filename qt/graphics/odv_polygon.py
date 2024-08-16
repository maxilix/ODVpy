from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPolygonF, QPen, QPainterPath
from PyQt6.QtWidgets import QGraphicsPolygonItem, QGraphicsPathItem, QGraphicsSceneMouseEvent

from qt.graphics.common import OdvGraphicElement, OdvGraphic
from qt.graphics.odv_line import OdvEditLineElement
from qt.graphics.odv_point import OdvEditPointElement


class OdvFixPolygonElement(OdvGraphicElement, QGraphicsPolygonItem):
    def __init__(self, sub_inspector, polygon: QPolygonF, half_pixel=True):
        if half_pixel:
            super().__init__(sub_inspector, polygon.truncated().translated(0.5, 0.5))
        else:
            super().__init__(sub_inspector, polygon)

        self.setPen(self.sub_inspector.pen)
        self.setBrush(self.sub_inspector.light_brush)


class OdvEditPolygonShapeElement(OdvGraphicElement, QGraphicsPathItem):
    def __init__(self, inspector, p_list: list[OdvEditPointElement], movable: bool = False):
        super().__init__(inspector)
        self.setPen(QPen(Qt.GlobalColor.transparent))
        self.setBrush(self.sub_inspector.light_brush)
        self.movable = movable
        self._p_list = p_list
        self._drag_position = None

    @property
    def p_list(self):
        return self._p_list

    @p_list.setter
    def p_list(self, value):
        self._p_list = value
        self.update()

    def delete(self):
        if self.parentItem() is not None:
            self.parentItem().polygon_shape_deleted(self)
        self.scene().removeItem(self)

    def update(self, rect: QRectF = QRectF()):
        path = QPainterPath()
        path.addPolygon(QPolygonF([p.pos() for p in self.p_list]))
        negative = QPainterPath()
        for p in self.p_list:
            negative.addEllipse(p.boundingRect().translated(p.pos()))
        self.setPath(path - negative)
        super().update(rect)

    def mouseDoubleClickEvent(self, event):
        if self.visible and self.movable and event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = self.mapToScene(event.pos()).truncated()
            self.setBrush(self.sub_inspector.high_brush)
        else:
            super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        if self.visible and self.movable:
            self._drag_position = None
            self.setBrush(self.sub_inspector.light_brush)
        else:
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if self.visible and self.movable and self._drag_position is not None:
            delta = self.mapToScene(event.pos()).truncated() - self._drag_position
            for p in self.p_list:
                p.move(delta)
                if self.parentItem() is not None:
                    self.parentItem().point_moved(p)
            self._drag_position = self.mapToScene(event.pos()).truncated()
        else:
            super().mouseMoveEvent(event)


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


class QCEGPolygon(OdvGraphic):

    def __init__(self, sub_inspector):
        super().__init__(sub_inspector)

        self.polygon_fix = None
        self.point_item = []
        self.line_item = []
        self.polygon_shape = None

        self.exit_edit_mode(save=False)

    @property
    def polygon(self):
        return self.sub_inspector.current

    @polygon.setter
    def polygon(self, polygon):
        self.sub_inspector.current = polygon.truncated()

    def enter_edit_mode(self):
        self.remove_child(self.polygon_fix)
        self.polygon_fix = None

        deletable = len(self.polygon) > 3
        self.point_item = [OdvEditPointElement(self.sub_inspector, p, movable=True, deletable=deletable) for p in self.polygon]
        self.line_item = [OdvEditLineElement(self.sub_inspector, p1, p2, secable=True, deletable=False) for p1, p2 in
                          zip(self.point_item, self.point_item[1:] + [self.point_item[0]])]
        self.polygon_shape = OdvEditPolygonShapeElement(self.sub_inspector, self.point_item, movable=True)
        self.add_child(self.polygon_shape)
        self.add_children(self.line_item)
        self.add_children(self.point_item)

        self.update()

    def exit_edit_mode(self, save):
        if save is True:
            self.polygon = QPolygonF(p.pos() for p in self.point_item)

        self.remove_child(self.polygon_shape)
        self.remove_children(self.line_item)
        self.remove_children(self.point_item)
        self.polygon_shape = None
        self.line_item = []
        self.point_item = []

        self.polygon_fix = OdvFixPolygonElement(self.sub_inspector, self.polygon)
        self.add_child(self.polygon_fix)

        self.update()

    def point_moved(self, point_item: OdvEditPointElement):
        n = len(self.point_item)
        index = self.point_item.index(point_item)
        self.line_item[(index - 1) % n].update()
        self.line_item[index].update()
        self.polygon_shape.update()

    def point_added(self,
                    previous_point_item: OdvEditPointElement,
                    new_point_item: OdvEditPointElement,
                    new_line_item: OdvEditLineElement):
        index = self.point_item.index(previous_point_item)
        self.point_item.insert(index + 1, new_point_item)
        self.add_child(new_point_item)
        self.line_item.insert(index + 1, new_line_item)
        self.add_child(new_line_item)

        for p in self.point_item:
            p.deletable = True
        self.polygon_shape.p_list = self.point_item
        self.update()

    def point_deleted(self, point_item: OdvEditPointElement):
        n = len(self.point_item)
        index = self.point_item.index(point_item)
        self.line_item[(index - 1) % n].p2 = self.point_item[(index + 1) % n]
        self.line_item[index].delete()
        self.line_item.remove(self.line_item[index])
        self.point_item.remove(point_item)
        self.remove_child(point_item)
        if len(self.point_item) <= 3:
            for p in self.point_item:
                p.deletable = False
        self.polygon_shape.p_list = self.point_item

    def line_deleted(self, line_item: OdvEditLineElement):
        self.remove_child(line_item)

    def polygon_shape_deleted(self, polygon_shape: OdvEditPolygonShapeElement):
        self.delete()
