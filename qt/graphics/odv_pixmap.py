from PyQt6.QtGui import QPixmap, QImage, QPolygonF
from PyQt6.QtWidgets import QGraphicsPixmapItem

from qt.graphics.common import OdvGraphicElement, OdvGraphic
from qt.graphics.odv_polygon import OdvFixPolygonElement


class OdvFixPixmapElement(OdvGraphicElement, QGraphicsPixmapItem):
    pass


class OdvMask(OdvGraphic):
    def __init__(self, sub_inspector):
        super().__init__(sub_inspector)

        self.mask_item = None
        self.reset_mask()

    @property
    def mask(self) -> QImage :
        return self.sub_inspector.current

    def reset_mask(self):
        self.remove_child(self.mask_item)

        self.mask_item = OdvFixPixmapElement(self.sub_inspector, QPixmap(self.mask))
        self.add_child(self.mask_item)
        super().update()

    def setOpacity(self, opacity):
        # opacity only affect map_item
        self.mask_item.setOpacity(opacity)


class OdvMap(OdvGraphic):
    def __init__(self, sub_inspector):
        super().__init__(sub_inspector)

        self.map_item = None
        self.map_rect = None
        self.rest_map()

    @property
    def map(self) -> QImage :
        return self.sub_inspector.current

    def rest_map(self):
        self.remove_child(self.map_item)
        self.remove_child(self.map_rect)

        self.map_item = OdvFixPixmapElement(self.sub_inspector, QPixmap(self.map))
        self.map_item.setZValue(0.1)
        self.map_rect = OdvFixPolygonElement(self.sub_inspector, QPolygonF(self.map.rect().toRectF()), half_pixel=False)
        self.map_rect.force_visible = True
        self.map_rect.setZValue(0)
        self.add_child(self.map_item)
        self.add_child(self.map_rect)
        super().update()

    def setOpacity(self, opacity):
        # opacity only affect map_item
        self.map_item.setOpacity(opacity)
