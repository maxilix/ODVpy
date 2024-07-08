from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent, QMenu

from qt.common.q_shared_menu import QSharedMenu


class QScene(QGraphicsScene):
    # def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
    #     print("lkjhf")


    # def __init__(self, parent):
    #     super().__init__(parent)
    #     self.

    def viewport(self):
        return self.views()[0]

    def move_to_item(self, item):
        self.viewport().move_to_item(item)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        # TODO double click doesn't work
        event.shared_menu = QSharedMenu()
        super().mousePressEvent(event)

        event.shared_menu.exec()

        # if event.button() == Qt.MouseButton.RightButton:
        #     event.menu.exec(QCursor.pos())

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
        event.menu = QMenu()
        super().mouseDoubleClickEvent(event)

