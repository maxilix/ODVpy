from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent, QGraphicsItem, QMenu

from qt.graphics.base import OdvGraphic, OdvShadow
from qt.graphics.point_elem import OdvPointerElement


class QScene(QGraphicsScene):
    pointer = None

    def center_view(self, zoom=1.5):
        r = self.sceneRect().center()
        x = r.x()
        y = r.y()
        self.viewport().x = x
        self.viewport().y = y
        self.viewport().zoom = zoom

    def viewport(self):
        return self.views()[0]

    def move_to_item(self, item: QGraphicsItem):
        self.viewport().move_to_rect(item.sceneBoundingRect())

    def move_to_rect(self, rect: QRectF):
        self.viewport().move_to_rect(rect)

    def addItem(self, item):
        assert isinstance(item, OdvGraphic)
        super().addItem(item)
        if item.shadow is not None:
            super().addItem(item.shadow)

    def removeItem(self, item):
        if isinstance(item, OdvGraphic) and item.shadow is not None:
            super().removeItem(item.shadow)
        super().removeItem(item)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        super().mousePressEvent(event)

        if event.button() == Qt.MouseButton.RightButton and not event.isAccepted():
            menu = QMenu()
            actions = []
            for tree_item in [g.tree_item for g in self.items(event.scenePos()) if isinstance(g, OdvShadow)]:
                actions.append(QAction(tree_item.name))
                # actions[-1].triggered.connect(lambda state, inner_item=tree_item: inner_item.focus())
                actions[-1].triggered.connect(lambda state, inner_item=tree_item: self.focus_on(inner_item))
            menu.addActions(actions)
            menu.exec(QCursor.pos())

    def add_pointer(self, parent_graphic):
        if self.pointer is None:
            self.pointer = OdvPointerElement(parent_graphic)
        else:
            print(f"WARNING: pointer already exists for {self.pointer.parentItem()}")

    @staticmethod
    def focus_on(tree_item):
        tree_item.focus()
        tree_item.show_graphics()
        tree_item.localise_graphics()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        shadow_list = [g.tree_item for g in self.items(event.scenePos()) if isinstance(g, OdvShadow)]
        self.viewport().info_bar.set_tree_items(shadow_list)
        if self.pointer is not None:
            self.pointer.setPos(event.scenePos())
        super().mouseMoveEvent(event)

    # def new_centered_line(self, scale:float):
    #     r: QRectF = self.viewport().current_visible_scene_rect()
    #     length = r.width() * scale
    #     c = r.center()
    #     p1 = QPointF(c.x() - length/2, c.y()).truncated()
    #     p2 = QPointF(c.x() + length/2, c.y()).truncated()
    #     return QLineF(p1, p2)
    #
    #
    # def new_centered_polygon(self, scale:float):
    #     r: QRectF = self.viewport().current_visible_scene_rect()
    #     width = r.width() * scale
    #     height = r.height() * scale
    #     c = r.center()
    #     p1 = QPointF(c.x() - width/2, c.y() - height/2).truncated()
    #     p2 = QPointF(c.x() + width/2, c.y() - height/2).truncated()
    #     p3 = QPointF(c.x() + width/2, c.y() + height/2).truncated()
    #     p4 = QPointF(c.x() - width/2, c.y() + height/2).truncated()
    #     return QPolygonF([p1, p2, p3, p4])
    #
    # def new_centered_gateway(self, scale:float):
    #     r: QRectF = self.viewport().current_visible_scene_rect()
    #     width = r.width() * scale
    #     height = r.height() * scale
    #     c = r.center()
    #     p1 = QPointF(c.x() - width/2, c.y() - height/8).truncated()
    #     p3 = QPointF(c.x() + width/2, c.y() - height/8).truncated()
    #     return Gateway(p1, c, p3)
