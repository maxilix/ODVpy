from math import floor

from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QPixmap, QPainterPath, QColor, QImage, QPolygonF
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsPolygonItem

from qt.graphics import OdvThinPen


class OdvFixPixmapElement(QGraphicsPixmapItem):
    def __init__(self, parent_item, pixmap: QPixmap):
        super().__init__(parent_item)
        self.setPixmap(pixmap)



class OdvFixMaskElement(QGraphicsPixmapItem):
    def __init__(self, parent_item, mask_image):
        super().__init__(parent_item)
        color = QColor(0, 180, 255)
        h = mask_image.height
        w = mask_image.width
        i = QImage(mask_image.rgba(color.getRgb()).data, w, h, 4 * w, QImage.Format.Format_RGBA8888)
        self.setPixmap(QPixmap(i))



class OdvEditMaskElement(QGraphicsPixmapItem):
    def __init__(self, parent_item, mask_image):
        super().__init__(parent_item)
        self.mask_image = mask_image
        self.pixel_setter = None
        self.color = QColor(0, 180, 255)
        self.hull = None
        self.update()

    def update(self, rect: QRectF = QRectF()):
        h = self.mask_image.height
        w = self.mask_image.width
        i = QImage(self.mask_image.rgba(self.color.getRgb()).data, w, h, 4 * w, QImage.Format.Format_RGBA8888)
        self.setPixmap(QPixmap(i))
        if self.hull is not None:
            self.scene().removeItem(self.hull)
        hull = QPolygonF([QPointF(x,y) for x,y in self.mask_image.hull()]).translated(0.5,0.5)
        self.hull = QGraphicsPolygonItem(hull, self)
        self.hull.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIgnoresParentOpacity)
        self.hull.setPen(OdvThinPen(QColor("black")))
        super().update(rect)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pixel_setter = True
            self.mouseMoveEvent(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.pixel_setter = False
            self.mouseMoveEvent(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        self.pixel_setter = None

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if self.pixel_setter is not None:
            mousse_relative_position = self.mapToScene(event.pos()) - self.parentItem().pos()
            x = floor(mousse_relative_position.x())
            y = floor(mousse_relative_position.y())
            self.mask_image.set_pixel(x, y, self.pixel_setter)
            self.update(QRectF(x, y, 1, 1))

    def shape(self):
        path = QPainterPath()
        path.addRect(QRectF(0,0, self.mask_image.width, self.mask_image.height))
        return path
