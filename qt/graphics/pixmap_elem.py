from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsPixmapItem

from qt.graphics.base import OdvGraphic


class OdvFixPixmapElement(QGraphicsPixmapItem):
    def __init__(self, parent_item: OdvGraphic, pixmap: QPixmap):
        super().__init__(parent_item)
        self.setPixmap(pixmap)
