from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QAction, QBrush, QPen, QPainter
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsEllipseItem

from qt.graphics.common import CustomGraphicsItem


class QCGPoint(CustomGraphicsItem, QGraphicsEllipseItem):
    size: float = 2.2

    def __init__(self, sub_inspector, position: QPointF, movable: bool = False, deletable: bool = False):
        super().__init__(sub_inspector, -self.size / 2, -self.size / 2, self.size, self.size)
        self.setPen(self.sub_inspector.pen)
        self.setBrush(self.sub_inspector.light_brush)
        self.setPos(position)
        self._is_moving = False
        self.movable = movable
        self.deletable = deletable
        self.update()

    def setPos(self, position: QPointF):
        super().setPos(position.truncated() + QPointF(0.5, 0.5))

    def paint(self, painter: QPainter, option, widget=None):
        if self.visible:
            painter.setRenderHints(QPainter.RenderHint.Antialiasing)
            super().paint(painter, option, widget)
            if self.movable is False:
                lock_pen = QPen(self.pen())
                lock_pen.setWidthF(lock_pen.widthF() / 2)
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
        if self.visible and self.movable and event.button() == Qt.MouseButton.LeftButton:
            self._is_moving = True
            self.setBrush(self.sub_inspector.high_brush)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        if self.visible and self.movable:
            self._is_moving = False
            self.setBrush(self.sub_inspector.light_brush)
        else:
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):

        if self.visible and self.movable and self._is_moving:
            self.setPos(self.mapToScene(event.pos()))
            if self.parentItem() is not None:
                self.parentItem().point_moved(self)
        else:
            super().mouseMoveEvent(event)

    def scene_menu_local_actions(self, scene_position):
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