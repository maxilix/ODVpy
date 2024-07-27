from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainterPath, QBrush
from PyQt6.QtWidgets import QGraphicsPathItem

from qt.graphics.common import CustomGraphicsItem


class QCGPath(CustomGraphicsItem, QGraphicsPathItem):
    def __init__(self, control, path: QPainterPath):
        super().__init__(control, path.translated(0.5, 0.5))
        self.setBrush(control.brush)
        self.setPen(control.pen)


class QCGHighlightablePath(QCGPath):
    def __init__(self, control, path: QPainterPath):
        super().__init__(control, path)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self._force_visibility = True
        self.setBrush(QBrush(Qt.GlobalColor.transparent))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._force_visibility = False
        self.setBrush(self.control.brush)
        super().hoverLeaveEvent(event)
