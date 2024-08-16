from PyQt6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent

from qt.control._scene_menu import QSceneMenu


class QScene(QGraphicsScene):



    def viewport(self):
        return self.views()[0]

    def move_to_item(self, item):
        self.viewport().move_to_item(item)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        event.shared_menu = QSceneMenu()
        super().mousePressEvent(event)

        event.shared_menu.exec()


    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
        event.shared_menu = QSceneMenu()
        super().mouseDoubleClickEvent(event)
        event.shared_menu.exec()
