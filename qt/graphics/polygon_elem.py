from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPolygonF, QPen, QPainterPath
from PyQt6.QtWidgets import QGraphicsPolygonItem, QGraphicsPathItem, QGraphicsSceneMouseEvent

from qt.graphics.base import OdvGraphic
from qt.graphics.point_elem import OdvEditPointElement


class OdvFixPolygonElement(QGraphicsPolygonItem):
    def __init__(self, parent_item: OdvGraphic, polygon: QPolygonF):
        super().__init__(parent_item)
        self.setPolygon(polygon.translated(self.parentItem().grid_alignment))
        self.setPen(self.parentItem().thin_pen)
        self.setBrush(self.parentItem().light_brush)


class OdvEditPolygonShapeElement(QGraphicsPathItem):
    def __init__(self, parent_item, p_list: list[OdvEditPointElement], movable: bool = False):
        super().__init__(parent_item)
        self.setPen(QPen(Qt.GlobalColor.transparent))
        self.setBrush(self.parentItem().light_brush)
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
        if self.movable and event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = self.mapToScene(event.pos()).truncated()
            self.setBrush(self.parentItem().high_brush)
            event.accept()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        if self.movable:
            self._drag_position = None
            self.setBrush(self.parentItem().light_brush)
            event.accept()
        else:
            event.ignore()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if self.movable and self._drag_position is not None:
            delta = self.mapToScene(event.pos()).truncated() - self._drag_position
            for p in self.p_list:
                p.move(delta, notify=False)  # the parent is not notified to avoid multiple updates
            for l in self.parentItem().line_edit_items:
                l.update()  # the lines must therefore be updated individually
            self.update()
            # the shadow and the edit zone must also be updated separately
            self.parentItem().shadow.setPolygon(QPolygonF([p.pos() for p in self.p_list]))
            self.parentItem().edit_zone.update()

            self._drag_position = self.mapToScene(event.pos()).truncated()
            event.accept()
        else:
            event.ignore()
