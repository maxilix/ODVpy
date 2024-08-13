from PyQt6.QtCore import QPointF, Qt, QRectF, QLineF
from PyQt6.QtGui import QPen, QAction, QPainterPath, QPolygonF
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsPathItem, QGraphicsLineItem, QGraphicsPolygonItem

from qt.graphics.common import CustomGraphicsItem
from qt.graphics.point import QCGPoint


class QCGLineElement(CustomGraphicsItem, QGraphicsLineItem):
    def __init__(self, sub_inspector, p1: QCGPoint, p2: QCGPoint, secable: bool = False, deletable: bool = False):
        super().__init__(sub_inspector)
        self.setPen(self.sub_inspector.pen)
        self._p1 = p1
        self._p2 = p2
        self.secable = secable
        self.deletable = deletable
        self.update()

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, value):
        self._p1 = value
        self.update()

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, value):
        self._p2 = value
        self.update()

    def update(self, rect: QRectF = QRectF()):
        temp_line = QLineF(self.p1.pos(), self.p2.pos())
        length = temp_line.length()
        if length > QCGPoint.size:
            p1 = self.p1.pos()
            p2 = self.p2.pos()
            f = (QCGPoint.size / 2) / length
            p1, p2 = (1 - f) * p1 + f * p2, (1 - f) * p2 + f * p1
            self.setLine(QLineF(p1, p2))
        else:
            self.setLine(QLineF())
        super().update(rect)

    def delete(self):
        if self.parentItem() is not None:
            self.parentItem().line_deleted(self)
        self.scene().removeItem(self)

    def add_point(self, pos: QPointF):
        deletable = self.p1.deletable or self.p2.deletable
        new_point = QCGPoint(self.inspector, pos, movable=True, deletable=deletable)
        self.scene().addItem(new_point)
        old_p2 = self.p2
        self.p2 = new_point
        new_line = QCGLineElement(self.inspector, new_point, old_p2, secable=True)
        self.scene().addItem(new_line)
        if self.parentItem() is not None:
            self.parentItem().point_added(self.p1, new_point, new_line)

    def shape(self):
        # virtually extends the line width for click detection
        temp_line = QGraphicsLineItem(self.line())
        pen = self.pen()
        pen.setWidthF(pen.widthF() * 5)
        temp_line.setPen(pen)
        return temp_line.shape()

    def scene_menu_local_actions(self, scene_position):
        rop = []
        if self.secable is True:
            a_add_point = QAction("Add Point")
            a_add_point.triggered.connect(lambda: self.add_point(scene_position))
            rop.append(a_add_point)

        if self.deletable and self.p1.deletable and self.p2.deletable:
            a_delete = QAction("Delete Line")
            a_delete.triggered.connect(self.delete)
            rop.append(a_delete)

        if self.p1.movable or self.p2.movable:
            a_lock = QAction("Lock Points")
            a_lock.triggered.connect(self.lock)
            rop.append(a_lock)

        if self.p1.movable is False or self.p2.movable is False:
            a_unlock = QAction("Unlock Points")
            a_unlock.triggered.connect(self.unlock)
            rop.append(a_unlock)

        return rop

    def lock(self):
        self.p1.lock()
        self.p2.lock()

    def unlock(self):
        self.p1.unlock()
        self.p2.unlock()


class QCGPolygonFixElement(CustomGraphicsItem, QGraphicsPolygonItem):
    def __init__(self, sub_inspector, polygon: QPolygonF):
        super().__init__(sub_inspector, polygon.truncated().translated(0.5, 0.5))
        self.setPen(self.sub_inspector.pen)
        self.setBrush(self.sub_inspector.light_brush)

class QCGPolygonShapeElement(CustomGraphicsItem, QGraphicsPathItem):
    def __init__(self, inspector, p_list: list[QCGPoint], movable: bool = False):
        super().__init__(inspector)
        self.setPen(QPen(Qt.GlobalColor.transparent))
        self.setBrush(self.sub_inspector.light_brush)
        self.movable = movable
        self._p_list = p_list
        self._drag_position = None
        self.update()

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
            self.setBrush(self.inspector.high_brush)
        else:
            super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        if self.visible and self.movable:
            self._drag_position = None
            self.setBrush(self.inspector.light_brush)
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
            
