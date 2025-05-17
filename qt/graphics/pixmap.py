import copy

from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtGui import QImage, QPixmap, QPolygonF, QColor
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem

from common import MaskImage
from qt.graphics import OdvPen, OdvLightBrush
from qt.graphics.base import OdvGraphic, OdvShadow, OdvEditGraphic
from qt.graphics.pixmap_elem import OdvFixPixmapElement, OdvFixMaskElement, OdvEditMaskElement


class GraphicMask(OdvEditGraphic):
    initial_opacity = 0.4

    def __init__(self, item, mask_image: MaskImage, position: QPointF):
        super().__init__(item)
        self.mask_image = mask_image
        self.setZValue(2)
        self.setPos(position)

        self.mask_fix = OdvFixMaskElement(self, self.mask_image)
        self.mask_edit = None
        self.rect_edit = None

        self.shadow = OdvShadow(item, QPolygonF([QPointF(x,y) for x,y in self.mask_image.hull()]).translated(position+QPointF(0.5,0.5)))

    def enter_edit_mode(self):
        if self.edit is False:
            self._edit = True

            self.remove(self.mask_fix)

            self.mask_edit = OdvEditMaskElement(self, copy.deepcopy(self.mask_image))
            rect_pen = OdvPen(QColor("yellow"), 0.5)
            self.rect_edit = QGraphicsRectItem(QRectF(-rect_pen.widthF()/2, -rect_pen.widthF()/2, self.mask_image.width+rect_pen.widthF(), self.mask_image.height+rect_pen.widthF()), self)
            self.rect_edit.setPen(rect_pen)
            self.rect_edit.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIgnoresParentOpacity)

    def exit_edit_mode(self, save):
        if self.edit is True:
            self._edit = False
            if save is True:
                print("SAVE")
                # self.polygon = QPolygonF(p.pos() for p in self.point_edit).truncated()
            else:
                print("NO SAVE")
                # update shadow
                # self.shadow.setPolygon(self.polygon.translated(self.grid_alignment))

            self.remove(self.mask_edit)
            self.remove(self.rect_edit)

            self.mask_fix = OdvFixMaskElement(self, self.mask_image)



class GraphicMap(OdvGraphic):

    def __init__(self, item, image: QImage):
        super().__init__(item)
        self.setZValue(1)
        self.map_item = OdvFixPixmapElement(self, QPixmap(image))
        self.shadow = OdvShadow(item, QPolygonF(image.rect().toRectF()))
        self.shadow.setPen(OdvPen(color=QColor("black"), width=1))
        self.shadow.setBrush(OdvLightBrush(color=QColor("black")))
