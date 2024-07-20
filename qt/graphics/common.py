from PyQt6.QtCore import Qt, QPointF, QRectF, QLineF, QEvent
from PyQt6.QtGui import QPixmap, QPainter, QPolygonF, QMouseEvent, QAction, QPen, QColor, QBrush, QPainterPath
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsPolygonItem, QGraphicsItem, QGraphicsEllipseItem, \
    QGraphicsLineItem, QGraphicsSceneMouseEvent, QGraphicsPathItem, QGraphicsItemGroup

from qt.control.common import QSharedMenuSection


# CG : CustomGraphicsItem
# QCG : QCustomGraphicsItem
#
# H : highlightable
# M : movable


class CustomGraphicsItem(object):

    def __init__(self, control, *args, **kwargs):
        self.control = control
        super().__init__(*args, **kwargs)

    def paint(self, painter: QPainter, option, widget=None):
        if self.control.item_visibility():
            painter.setRenderHints(QPainter.RenderHint.Antialiasing)
            super().paint(painter, option, widget)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            section = QSharedMenuSection(self, event)
            event.shared_menu.add_section(section)
        super().mousePressEvent(event)

    def local_action_list(self, scene_position):
        return []


class QCGPixmap(CustomGraphicsItem, QGraphicsPixmapItem):
    pass


class QCGFixedPolygon(CustomGraphicsItem, QGraphicsPolygonItem):
    def __init__(self, control, polygon: QPolygonF):
        super().__init__(control, polygon.translated(0.5, 0.5))
        self.setBrush(control.brush)
        self.setPen(control.pen)


class QCGHighlightablePolygon(QCGFixedPolygon):
    def __init__(self, control, polygon: QPolygonF):
        super().__init__(control, polygon)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.setBrush(self.control.high_brush)
        # self.update()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(self.control.brush)
        # self.update()
        super().hoverLeaveEvent(event)


class QCGPoint(CustomGraphicsItem, QGraphicsEllipseItem):
    size: float = 2.2

    def __init__(self, control, position: QPointF, movable: bool = False, deletable: bool = False):
        super().__init__(control, -self.size / 2, -self.size / 2, self.size, self.size)
        self.setPen(control.pen)
        self.setBrush(control.brush)
        self.setPos(position)
        self._is_moving = False
        self.movable = movable
        self.deletable = deletable
        self.update()

    def setPos(self, position: QPointF):
        super().setPos(position.truncated() + QPointF(0.5, 0.5))

    def paint(self, painter: QPainter, option, widget=None):
        if self.control.item_visibility():
            painter.setRenderHints(QPainter.RenderHint.Antialiasing)
            super().paint(painter, option, widget)
            if self.movable is False:
                lock_pen = QPen(self.control.pen)
                lock_pen.setWidthF(self.control.pen.widthF() / 2)
                lock_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                painter.setPen(lock_pen)
                painter.setBrush(QBrush(Qt.GlobalColor.transparent))
                painter.drawEllipse(QRectF(-0.1 * self.size, -0.25 * self.size, 0.2 * self.size, 0.5 * self.size))
                painter.setBrush(QBrush(lock_pen.color()))
                painter.drawRect(QRectF(-0.15 * self.size, 0, 0.3 * self.size, 0.27 * self.size))

    def move(self, vector: QPointF):
        self.setPos(self.pos() + vector)

    def delete(self):
        if self.parentItem() is not None:
            self.parentItem().point_deleted(self)
        self.scene().removeItem(self)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if self.movable is True and event.button() == Qt.MouseButton.LeftButton:

            self._is_moving = True
            self.setBrush(self.control.high_brush)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        if self.movable is True:
            self._is_moving = False
            self.setBrush(self.control.low_brush)
        else:
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):

        if self.movable is True and self._is_moving is True:
            self.setPos(self.mapToScene(event.pos()))
            if self.parentItem() is not None:
                self.parentItem().point_moved(self)
        else:
            super().mouseMoveEvent(event)

    def local_action_list(self, scene_position):
        rop = []

        if self.deletable:
            a_delete = QAction("Delete Point")
            a_delete.triggered.connect(self.delete)
            rop.append(a_delete)

        if self.movable:
            a_lock = QAction("Lock Point")
            a_lock.triggered.connect(self.lock)
            rop.append(a_lock)
        else:
            a_unlock = QAction("Unlock Point")
            a_unlock.triggered.connect(self.unlock)
            rop.append(a_unlock)

        return rop

    def lock(self):
        self.movable = False
        self.update()

    def unlock(self):
        self.movable = True
        self.update()


class QCGLine(CustomGraphicsItem, QGraphicsLineItem):
    def __init__(self, control, p1: QCGPoint, p2: QCGPoint, secable: bool = False, deletable: bool = False):
        super().__init__(control)
        self.setPen(control.pen)
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
        new_point = QCGPoint(self.control, pos, movable=True, deletable=deletable)
        self.scene().addItem(new_point)
        old_p2 = self.p2
        self.p2 = new_point
        new_line = QCGLine(self.control, new_point, old_p2, secable=True)
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

    def local_action_list(self, scene_position):
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


class QCGPolygonShape(CustomGraphicsItem, QGraphicsPathItem):
    def __init__(self, control, p_list: list[QCGPoint], movable: bool = False):
        super().__init__(control)
        self.setBrush(control.brush)
        self.setPen(QPen(Qt.GlobalColor.transparent))
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
        if self.movable and event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = self.mapToScene(event.pos()).truncated()
            self.setBrush(self.control.high_brush)
        else:
            super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        if self.movable:
            self._drag_position = None
            self.setBrush(self.control.brush)
        else:
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if self.movable and self._drag_position is not None:
            delta = self.mapToScene(event.pos()).truncated() - self._drag_position
            for p in self.p_list:
                p.move(delta)
                if self.parentItem() is not None:
                    self.parentItem().point_moved(p)
            self._drag_position = self.mapToScene(event.pos()).truncated()
        else:
            super().mouseMoveEvent(event)


# TODO create proper group
# TODO fusion section of same name
class QCGEditablePolygon(QGraphicsItem):
    def __init__(self, control, polygon: QPolygonF):
        super().__init__()
        self.control = control
        self.setFlag(self.flags() | QGraphicsItem.GraphicsItemFlag.ItemHasNoContents)

        deletable = len(polygon) > 3
        self.point_item = [QCGPoint(self.control, p, movable=True, deletable=deletable) for p in polygon]
        self.line_item = [QCGLine(self.control, p1, p2, secable=True, deletable=False) for p1, p2 in
                          zip(self.point_item, self.point_item[1:] + [self.point_item[0]])]
        self.polygone_shape = QCGPolygonShape(self.control, self.point_item, movable=True)

        for point in self.point_item:
            point.setParentItem(self)
        for line in self.line_item:
            line.setParentItem(self)
        self.polygone_shape.setParentItem(self)

        self.update()

    def boundingRect(self):
        return QRectF()

    def __iter__(self):
        return iter(self.point_item)

    def update(self, rect: QRectF = QRectF()):
        [p.update() for p in self.point_item]
        [l.update() for l in self.line_item]
        self.polygone_shape.update()
        # super().update(rect)

    def point_moved(self, point_item: QCGPoint):
        n = len(self.point_item)
        index = self.point_item.index(point_item)
        self.line_item[(index - 1) % n].update()
        self.line_item[index].update()
        self.polygone_shape.update()

    def point_added(self,
                    previous_point_item: QCGPoint,
                    new_point_item: QCGPoint,
                    new_line_item: QCGLine):
        index = self.point_item.index(previous_point_item)
        self.point_item.insert(index + 1, new_point_item)
        new_point_item.setParentItem(self)
        self.line_item.insert(index + 1, new_line_item)
        new_line_item.setParentItem(self)

        for p in self.point_item:
            p.deletable = True
        self.polygone_shape.p_list = self.point_item

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
        self.polygone_shape.p_list = self.point_item

    def line_deleted(self, line_item: QCGLine):
        pass

    def polygon_shape_deleted(self, polygon_shape: QCGPolygonShape):
        pass

    def delete(self):
        self.scene().removeItem(self)

