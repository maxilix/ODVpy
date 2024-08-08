from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsRectItem

from qt.graphics.common import CustomGraphicsItem, QCGItemGroup


class QCGPixmap(CustomGraphicsItem, QGraphicsPixmapItem):
    pass


class QCGMap(QCGItemGroup):
    def __init__(self, q_dvd_item, map_pixmap: QPixmap):
        super().__init__(q_dvd_item)

        self.map = QCGPixmap(self.q_dvd_item, map_pixmap)
        self.map.setVisible(True)
        self.map.setZValue(0.1)
        # self.map_rect = QGraphicsRectItem(map_pixmap.rect().toRectF())
        # self.map_rect.setZValue(0)
        # TODO force visibility for map_rect

        self.add_child(self.map)
        # self.add_child(self.map_rect)

        self.update()

    def setOpacity(self, opacity):
        # opacity only affect map
        self.map.setOpacity(opacity)
