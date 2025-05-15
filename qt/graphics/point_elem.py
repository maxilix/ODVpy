from PyQt6.QtCore import Qt, QPointF, QLineF
from PyQt6.QtGui import QAction, QPainter, QCursor
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QMenu

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

    def move(self, vector: QPointF):
        self.setPos(self.pos() + vector)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_moving = True
            self.setBrush(self.parentItem().high_brush)
        elif event.button() == Qt.MouseButton.RightButton:
            # scene_position = self.mapToScene(event.pos())
            menu = QMenu()
            a_delete = QAction("Delete Point")
            a_delete.triggered.connect(lambda: self.parentItem().delete_point(self))
            menu.addAction(a_delete)
            menu.exec(QCursor.pos())
            event.accept()
        else:
            super().mousePressEvent(event)


    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        self._is_moving = False
        self.setBrush(self.parentItem().light_brush)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if self._is_moving:
            self.setPos(self.mapToScene(event.pos()))
        super().mouseMoveEvent(event)
