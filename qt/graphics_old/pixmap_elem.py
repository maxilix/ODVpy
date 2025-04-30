from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsPixmapItem

from qt.graphics_old.base_elem import OdvGraphicElement


class OdvFixPixmapElement(OdvGraphicElement, QGraphicsPixmapItem):
    def __init__(self, parent_item, pixmap: QPixmap):
        super().__init__(parent_item)
        self.setPixmap(pixmap)
