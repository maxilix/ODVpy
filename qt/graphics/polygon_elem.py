from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPolygonF, QPen, QPainterPath
from PyQt6.QtWidgets import QGraphicsPolygonItem, QGraphicsPathItem, QGraphicsSceneMouseEvent

from qt.graphics.base_elem import OdvGraphicElement
from qt.graphics.point_elem import OdvEditPointElement


class OdvFixPolygonElement(OdvGraphicElement, QGraphicsPolygonItem):
    def __init__(self, parent_item, polygon: QPolygonF):
        super().__init__(parent_item)
        if (ga := self.parentItem().grid_alignment) is not None:
            polygon = polygon.truncated().translated(ga)
        self.setPolygon(polygon)
        self.setPen(self.sub_inspector.pen)
        self.setBrush(self.sub_inspector.light_brush)
        self.update()


class OdvEditPolygonShapeElement(OdvGraphicElement, QGraphicsPathItem):
    def __init__(self, parent_item, p_list: list[OdvEditPointElement], movable: bool = False):
        super().__init__(parent_item)
        self.setPen(QPen(Qt.GlobalColor.transparent))
        self.setBrush(self.sub_inspector.light_brush)
        self.movable = movable
        self._drag_position = None
        self.p_list = p_list  # performs an update

    @property
    def p_list(self):
        return self._p_list

    @p_list.setter
    def p_list(self, value):
        self._p_list = value
        self.update()

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
