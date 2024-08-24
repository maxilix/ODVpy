from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent

from common import *
from qt.control.scene_menu import QSceneMenu


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

    def new_centered_line(self, scale:float):
        r: QRectF = self.viewport().current_visible_scene_rect()
        length = r.width() * scale
        c = r.center()
        p1 = QPointF(c.x() - length/2, c.y()).truncated()
        p2 = QPointF(c.x() + length/2, c.y()).truncated()
        return QLineF(p1, p2)


    def new_centered_polygon(self, scale:float):
        r: QRectF = self.viewport().current_visible_scene_rect()
        width = r.width() * scale
        height = r.height() * scale
        c = r.center()
        p1 = QPointF(c.x() - width/2, c.y() - height/2).truncated()
        p2 = QPointF(c.x() + width/2, c.y() - height/2).truncated()
        p3 = QPointF(c.x() + width/2, c.y() + height/2).truncated()
        p4 = QPointF(c.x() - width/2, c.y() + height/2).truncated()
        return QPolygonF([p1, p2, p3, p4])

    def new_centered_gateway(self, scale:float):
        r: QRectF = self.viewport().current_visible_scene_rect()
        width = r.width() * scale
        height = r.height() * scale
        c = r.center()
        p1 = QPointF(c.x() - width/2, c.y() - height/8).truncated()
        p3 = QPointF(c.x() + width/2, c.y() - height/8).truncated()
        return Gateway(p1, c, p3)
