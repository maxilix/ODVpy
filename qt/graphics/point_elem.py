from PyQt6.QtCore import Qt, QPointF, QLineF
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem

from qt.graphics import darker_pen

POINT_SIZE = 2.2


class OdvFixPointElement(QGraphicsItem):
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



class OdvEditPointElement(QGraphicsEllipseItem):
    size: float = POINT_SIZE

    def __init__(self, parent_item, position: QPointF, deletable: bool = False):
        super().__init__(parent_item)
        self.setRect(-self.size / 2, -self.size / 2, self.size, self.size)
        self.setPen(self.parentItem().thin_pen)
        self.setBrush(self.parentItem().light_brush)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)

        self.b1 = QGraphicsLineItem(QLineF(-self.size / 2, -self.size / 2, self.size / 2, self.size / 2), self)
        self.b2 = QGraphicsLineItem(QLineF(-self.size / 2, self.size / 2, self.size / 2, -self.size / 2), self)
        self.b1.setPen(darker_pen(self.pen()))
        self.b2.setPen(darker_pen(self.pen()))
        self.b1.setVisible(False)
        self.b2.setVisible(False)

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

    def move(self, delta: QPointF, notify=True):
        self.setPos(self.pos() + delta, notify=notify)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        ctrl = bool(event.modifiers() & Qt.KeyboardModifier.ControlModifier)
        if event.button() == Qt.MouseButton.LeftButton:
            if ctrl:
                if self.deletable:
                    self.parentItem().delete_point(self)
            else:
                self._is_moving = True
                self.setBrush(self.parentItem().high_brush)
                event.accept()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        self._is_moving = False
        self.setBrush(self.parentItem().light_brush)
        event.accept()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if self._is_moving:
            self.setPos(self.mapToScene(event.pos()) - self.parentItem().pos())
        event.accept()

    def hoverEnterEvent(self, event):
        self.setFocus()
        ctrl = bool(event.modifiers() & Qt.KeyboardModifier.ControlModifier)
        self.b1.setVisible(ctrl and self.deletable)
        self.b2.setVisible(ctrl and self.deletable)

    def hoverLeaveEvent(self, event):
        self.b1.setVisible(False)
        self.b2.setVisible(False)

    def keyPressEvent(self, event):
        if self.isUnderMouse():
            ctrl = bool(event.modifiers() & Qt.KeyboardModifier.ControlModifier)
            self.b1.setVisible(ctrl and self.deletable)
            self.b2.setVisible(ctrl and self.deletable)
        else:
            self.clearFocus()

    def keyReleaseEvent(self, event):
        if self.isUnderMouse():
            self.b1.setVisible(False)
            self.b2.setVisible(False)
        else:
            self.clearFocus()
