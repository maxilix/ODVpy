from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainterPath, QBrush
from PyQt6.QtWidgets import QGraphicsPathItem

from qt.graphics.common import CustomGraphicsItem


class QCGPath(CustomGraphicsItem, QGraphicsPathItem):
    def __init__(self, q_dvd_item, path: QPainterPath):
        super().__init__(q_dvd_item, path.translated(0.5, 0.5))
        self.setBrush(q_dvd_item.brush)
        self.setPen(q_dvd_item.pen)


class QCGHighlightablePath(QCGPath):
    def __init__(self, q_dvd_item, path: QPainterPath):
        super().__init__(q_dvd_item, path)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self._force_visibility = True
        self.setBrush(QBrush(Qt.GlobalColor.transparent))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._force_visibility = False
        self.setBrush(self.q_dvd_item.brush)
        super().hoverLeaveEvent(event)
