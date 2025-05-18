import copy

from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtGui import QImage, QPixmap, QPolygonF, QColor
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem

from common import MaskImage
from qt.graphics import OdvPen, OdvLightBrush
from qt.graphics.base import OdvGraphic, OdvShadow, OdvEditGraphic
from qt.graphics.pixmap_elem import OdvFixPixmapElement, OdvFixMaskElement, OdvEditMaskElement, OdvEditCardinalElement


class GraphicMask(OdvEditGraphic):
    initial_opacity = 0.4

    # thin_pen = OdvThinPen(QColor("yellow"))
    # light_brush = OdvLightBrush(QColor("yellow"))
    # high_brush = OdvHighBrush(QColor("yellow"))

    def __init__(self, item, mask_image: MaskImage, position: QPointF):
        super().__init__(item)
        self.mask_image = mask_image
        self.position = position
        self.copy_mask_image = None
        self.setZValue(2)
        self.setPos(position)

        self.mask_fix = OdvFixMaskElement(self, self.mask_image)
        self.mask_edit = None
        self.base_rect = QRectF()
        self.rect_edit = None
        self.cardinals_edit = None

        self.shadow = OdvShadow(item, QPolygonF([QPointF(x,y) for x,y in self.mask_image.hull()])
                                .translated(self.pos() + QPointF(0.5,0.5)))

    def enter_edit_mode(self):
        if self.edit is False:
            self._edit = True

            self.remove(self.mask_fix)

            self.copy_mask_image = copy.deepcopy(self.mask_image)
            self.mask_edit = OdvEditMaskElement(self, self.copy_mask_image)
            self.base_rect = QRectF(0, 0, self.copy_mask_image.width, self.copy_mask_image.height)
            # 8 directions : [ NW, N , NE, E, SE, S, SW, W ]
            self.cardinals_edit = [OdvEditCardinalElement(self, d) for d in range(8)]
            for cp in self.cardinals_edit:
                cp.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIgnoresParentOpacity)
                cp.base_rect = self.base_rect

            rect_pen = OdvPen(QColor("yellow"), 0.1)
            w_f = rect_pen.widthF()
            self.rect_edit = QGraphicsRectItem(self.base_rect.adjusted(-w_f / 2, -w_f / 2, w_f / 2, w_f / 2), self)
            self.rect_edit.setPen(rect_pen)
            self.rect_edit.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIgnoresParentOpacity)

    def exit_edit_mode(self, save):
        if self.edit is True:
            self._edit = False
            if save is True:
                self.copy_mask_image.crop_to_view()
                # save mask_image in model
                self.mask_image = copy.deepcopy(self.copy_mask_image)
                # save current position in model
                self.position = self.pos()
            else:
                # return to original position
                self.setPos(self.position)
                # update shadow
                self.shadow.setPolygon(QPolygonF([QPointF(x, y) for x, y in self.mask_image.hull()])
                                        .translated(self.pos() + QPointF(0.5, 0.5)))

            self.copy_mask_image = None
            self.remove(self.mask_edit)
            self.base_rect = QRectF()
            self.remove(self.rect_edit)
            self.remove(self.cardinals_edit)

            self.mask_fix = OdvFixMaskElement(self, self.mask_image)

    def point_moved(self, moved_point: OdvEditCardinalElement):
        x1, y1, x2, y2 = self.base_rect.getCoords()
        xp = moved_point.pos().x()
        yp = moved_point.pos().y()
        match moved_point.d:
            case 0:
                new_rect = QRectF(QPointF(xp, yp), QPointF(x2, y2))
            case 1:
                new_rect = QRectF(QPointF(x1, yp), QPointF(x2, y2))
            case 2:
                new_rect = QRectF(QPointF(x1, yp), QPointF(xp, y2))
            case 3:
                new_rect = QRectF(QPointF(x1, y1), QPointF(xp, y2))
            case 4:
                new_rect = QRectF(QPointF(x1, y1), QPointF(xp, yp))
            case 5:
                new_rect = QRectF(QPointF(x1, y1), QPointF(x2, yp))
            case 6:
                new_rect = QRectF(QPointF(xp, y1), QPointF(x2, yp))
            case 7:
                new_rect = QRectF(QPointF(xp, y1), QPointF(x2, y2))
            case _:
                raise Exception("Direction of OdvEditCardinalElement must be in [0 ... 7]")

        self.setPos(self.pos() + new_rect.topLeft())
        self.base_rect = QRectF(0, 0, new_rect.width(), new_rect.height())

        self.copy_mask_image.resize_view_to(int(new_rect.x()), int(new_rect.y()), int(new_rect.width()), int(new_rect.height()))
        self.mask_edit.mask_image = self.copy_mask_image
        self.mask_edit.update()

        self.rect_edit.setRect(self.base_rect)
        for cp in self.cardinals_edit:
            cp.base_rect = self.base_rect



class GraphicMap(OdvGraphic):

    def __init__(self, item, image: QImage):
        super().__init__(item)
        self.setZValue(1)
        self.map_item = OdvFixPixmapElement(self, QPixmap(image))
        self.shadow = OdvShadow(item, QPolygonF(image.rect().toRectF()))
        self.shadow.setPen(OdvPen(color=QColor("black"), width=1))
        self.shadow.setBrush(OdvLightBrush(color=QColor("black")))
