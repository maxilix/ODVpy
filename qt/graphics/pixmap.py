from PyQt6.QtGui import QImage, QPixmap, QPolygonF, QColor

from qt.graphics import OdvPen, OdvLightBrush
from qt.graphics.base import OdvGraphic, OdvShadow
from qt.graphics.pixmap_elem import OdvFixPixmapElement


class GraphicMask(OdvGraphic):
    def __init__(self, sub_inspector):
        super().__init__(sub_inspector)

        self.mask_item = None
        self.reset_mask()

    @property
    def mask(self) -> QImage :
        return self.sub_inspector.current

    def reset_mask(self):
        self.remove(self.mask_item)

        self.mask_item = OdvFixPixmapElement(self, QPixmap(self.mask))

        self.update()

    def setOpacity(self, opacity):
        # opacity only affect mask_item
        self.mask_item.setOpacity(opacity)


class GraphicMap(OdvGraphic):
    thin_pen = OdvPen(color=QColor("black"), width=1)

    def __init__(self, item, image: QImage):
        super().__init__(item)
        self.setZValue(1)
        self.map_item = OdvFixPixmapElement(self, QPixmap(image))
        self.shadow = OdvShadow(item, QPolygonF(image.rect().toRectF()))
        self.shadow.setPen(OdvPen(color=QColor("black"), width=1))
        self.shadow.setBrush(OdvLightBrush(color=QColor("black")))
