from PyQt6.QtCore import Qt, QPointF, QLineF
from PyQt6.QtGui import QAction, QPainter
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem

from qt.graphics.base_elem import OdvGraphicElement

POINT_SIZE = 2.2


class OdvFixPointElement(OdvGraphicElement, QGraphicsItem):
    size: float = POINT_SIZE

    def __init__(self, parent_item, position: QPointF):
        super().__init__(parent_item)
        self.branch1 = QLineF(-self.size / 2, -self.size / 2, self.size / 2, self.size / 2)
        self.branch2 = QLineF(-self.size / 2, self.size / 2, self.size / 2, -self.size / 2)
        if (ga := self.parentItem().grid_alignment) is not None:
            position = position.truncated() + ga
        self.setPos(position)

        self.update()

    def paint(self, painter: QPainter, option, widget=None):
        if self.visible:
            painter.setRenderHints(QPainter.RenderHint.Antialiasing)
            painter.setPen(self.sub_inspector.pen)
            painter.drawLine(self.branch1)
            painter.drawLine(self.branch2)

    def shape(self):
        temp_branch_1 = QGraphicsLineItem(self.branch1)
        temp_branch_1.setPen(self.sub_inspector.pen)
        temp_branch_2 = QGraphicsLineItem(self.branch2)
        temp_branch_2.setPen(self.sub_inspector.pen)
        return temp_branch_1.shape() + temp_branch_2.shape()

    def boundingRect(self):
        return self.shape().boundingRect()


class OdvEditPointElement(OdvGraphicElement, QGraphicsEllipseItem):
    size: float = POINT_SIZE

    def __init__(self, parent_item, position: QPointF, deletable: bool = False):
        super().__init__(parent_item)
        self.setRect(-self.size / 2, -self.size / 2, self.size, self.size)
        self.setPen(self.sub_inspector.pen)
        self.setBrush(self.sub_inspector.light_brush)

        self.setPos(position, notify=False)
        self._is_moving = False
        self.deletable = deletable

    def setPos(self, position: QPointF, notify=True):
        if (ga:=self.parentItem().grid_alignment) is not None:
            position =  position.truncated() + ga
        if position != self.pos():
            super().setPos(position)
        if notify:
            self.parentItem().point_moved(self)

    # def paint(self, painter: QPainter, option, widget=None):
    #     super().paint(painter, option, widget)
    #     if self.visible and self.movable is False:
    #         painter.setRenderHints(QPainter.RenderHint.Antialiasing)
    #         lock_pen = QPen(self.pen())
    #         lock_pen.setWidthF(lock_pen.widthF() / 2)
    #         lock_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    #         painter.setPen(lock_pen)
    #         painter.setBrush(QBrush(Qt.GlobalColor.transparent))
    #         painter.drawEllipse(QRectF(-0.1 * self.size, -0.25 * self.size, 0.2 * self.size, 0.5 * self.size))
    #         painter.setBrush(QBrush(lock_pen.color()))
    #         painter.drawRect(QRectF(-0.15 * self.size, 0, 0.3 * self.size, 0.27 * self.size))

    def move(self, vector: QPointF):
        self.setPos(self.pos() + vector)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if self.visible and event.button() == Qt.MouseButton.LeftButton:
            self._is_moving = True
            self.setBrush(self.sub_inspector.high_brush)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        if self.visible:
            self._is_moving = False
            self.setBrush(self.sub_inspector.light_brush)
        else:
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):

        if self.visible and self._is_moving:
            self.setPos(self.mapToScene(event.pos()))
        else:
            super().mouseMoveEvent(event)

    def scene_menu_local_actions(self, scene_position):
        rop = []
        if self.deletable:
            a_delete = QAction("Delete Point")
            a_delete.triggered.connect(lambda: self.parentItem().delete_point(self))
            rop.append(a_delete)
        return rop
