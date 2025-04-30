from PyQt6.QtGui import QImage, QPixmap, QPolygonF, QColor

from qt.graphics import OdvPen
from qt.graphics.base import OdvGraphic
from qt.graphics.pixmap_elem import OdvFixPixmapElement
from qt.graphics.polygon_elem import OdvFixPolygonElement
from qt.graphics_old import OdvBrush


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
    def __init__(self, initial_image: QImage):
        super().__init__()
        self._image = initial_image
        self.map_item = None
        self.map_rect = None
        self.reset()

    @property
    def image(self) -> QImage:
        return self._image

    @image.setter
    def image(self, image: QImage):
        self._image = image

    def reset(self):
        self.remove(self.map_item)
        self.remove(self.map_rect)

        self.map_item = OdvFixPixmapElement(self, QPixmap(self.image))
        self.map_item.setZValue(0.1)
        self.map_rect = OdvFixPolygonElement(self, QPolygonF(self.image.rect().toRectF()))
        self.map_rect.setPen(OdvPen(color=QColor(0,0,0), width=1))
        self.map_rect.setBrush(OdvBrush(color=QColor(0,0,0), alpha=30))
        self.map_rect.force_visible = True
        self.map_rect.setZValue(0)

        # self.update()

    def setVisible(self, visible: bool):
        self.map_item.setVisible(visible)

    def setOpacity(self, opacity):
        # opacity only affect map_item
        self.map_item.setOpacity(opacity)
