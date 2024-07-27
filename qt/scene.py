from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent, QMenu, QGraphicsItemGroup, QGraphicsItem

from qt.control.common import QSharedMenu



class QScene(QGraphicsScene):



    def viewport(self):
        return self.views()[0]

    def move_to_item(self, item):
        self.viewport().move_to_item(item)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        event.shared_menu = QSharedMenu()
        super().mousePressEvent(event)

        event.shared_menu.exec()


    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
        event.shared_menu = QSharedMenu()
        super().mouseDoubleClickEvent(event)
        event.shared_menu.exec()
