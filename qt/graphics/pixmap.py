from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QImage, QPixmap, QPolygonF, QColor

from qt.graphics import OdvPen, OdvLightBrush
from qt.graphics.base import OdvGraphic, OdvShadow
from qt.graphics.pixmap_elem import OdvFixPixmapElement


class GraphicMask(OdvGraphic):
    def __init__(self, item, mask_image: QImage, position: QPointF):
        super().__init__(item)
        self.setZValue(2)
        self.setPos(position)
        self.mask_item = OdvFixPixmapElement(self, QPixmap(mask_image))
        self.shadow = OdvShadow(item, QPolygonF(mask_image.rect().toRectF().translated(position)))




class GraphicMap(OdvGraphic):
    thin_pen = OdvPen(color=QColor("black"), width=1)

    def __init__(self, item, image: QImage):
        super().__init__(item)
        self.setZValue(1)
        self.map_item = OdvFixPixmapElement(self, QPixmap(image))
        self.shadow = OdvShadow(item, QPolygonF(image.rect().toRectF()))
        self.shadow.setPen(OdvPen(color=QColor("black"), width=1))
        self.shadow.setBrush(OdvLightBrush(color=QColor("black")))
