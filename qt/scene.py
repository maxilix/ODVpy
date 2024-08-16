from PyQt6.QtCore import QRectF, QLineF, QPointF
from PyQt6.QtGui import QPolygonF
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

    def new_centered_line(self):
        r: QRectF = self.viewport().current_visible_scene_rect()
        p1 = QPointF(0.7 * r.left() + 0.3 * r.right(), 0.5*r.top() + 0.5*r.bottom()).truncated()
        p2 = QPointF(0.7 * r.right() + 0.3 * r.left(), 0.5*r.top() + 0.5*r.bottom()).truncated()
        return QLineF(p1, p2)


    def new_centered_polygon(self):
        r: QRectF = self.viewport().current_visible_scene_rect()
        p1 = (0.7 * r.topLeft() + 0.3 * r.bottomRight()).truncated()
        p2 = (0.7 * r.topRight() + 0.3 * r.bottomLeft()).truncated()
        p3 = (0.7 * r.bottomRight() + 0.3 * r.topLeft()).truncated()
        p4 = (0.7 * r.bottomLeft() + 0.3 * r.topRight()).truncated()
        return QPolygonF([0.5*p1 + 0.5*p2, p3, p4])