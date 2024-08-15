from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsRectItem

from qt.graphics.common import CustomGraphicsItem, QCGItemGroup


class QCGPixmap(CustomGraphicsItem, QGraphicsPixmapItem):
    pass


class QCGMap(QCGItemGroup):
    def __init__(self, sub_inspector):
        super().__init__(sub_inspector)

        self.map_item = QCGPixmap(self.sub_inspector, QPixmap(self.map))
        # self.map.setVisible(True)
        self.map_item.setZValue(0.1)
        # self.map_rect = QGraphicsRectItem(map_pixmap.rect().toRectF())
        # self.map_rect.setZValue(0)
        # TODO force visibility for map_rect

        self.add_child(self.map_item)
        # self.add_child(self.map_rect)

        self.update()

    @property
    def map(self):
        return self.sub_inspector.current

    @map.setter
    def map(self, map):
        self.sub_inspector.current = map



    def setOpacity(self, opacity):
        # opacity only affect map_item
        self.map_item.setOpacity(opacity)
