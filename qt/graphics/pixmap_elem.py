from math import floor

from PyQt6.QtCore import Qt, QPointF, QRectF, QLineF, QRect
from PyQt6.QtGui import QPixmap, QPainterPath, QColor, QImage, QPolygonF, QTransform, QPainter
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsPolygonItem, \
    QGraphicsLineItem

from qt.graphics import OdvThinPen, OdvPen

class OdvFixPixmapElement(QGraphicsPixmapItem):
    def __init__(self, parent_item, pixmap: QPixmap):
        super().__init__(parent_item)
        self.setPixmap(pixmap)



class OdvEditCardinalElement(QGraphicsItem):
    width = 1.2

    def __init__(self, parent_item: QGraphicsItem, direction:int):
        super().__init__(parent_item)
        self.l1 = QLineF()
        self.l2 = QLineF()
        self._base_rect = QRect()
        self.d = direction
        self._drag_position = None
        # wait to have base_rect before update

    def setPos(self, position: QPointF, notify=True):
        # if (ga:=self.parentItem().grid_alignment) is not None:
        #     position =  position.truncated() + ga
        if position != self.pos():
            super().setPos(position)
            if notify:
                self.parentItem().point_moved(self)

    @property
    def base_rect(self):
        return self._base_rect

    @base_rect.setter
    def base_rect(self, base_rect: QRectF):
        self._base_rect = base_rect
        self.update()

    def update(self, rect: QRectF = QRectF()):
        w = self._base_rect.width()
        h = self._base_rect.height()

        length = min(w, h)/10

        self.l1 = QLineF(-self.width / 2, -self.width / 2, -self.width / 2 + length, -self.width / 2)
        self.l2 = QLineF(-self.width / 2, -self.width / 2, -self.width / 2, -self.width / 2 + length)
        rot_90 = QTransform(0, 1, -1, 0, 0, 0)

        for _ in range(self.d // 2):
            self.l1 = rot_90.map(self.l1)
        for _ in range((self.d + 1) // 2):
            self.l2 = rot_90.map(self.l2)

        match self.d:
            case 0:
                self.setPos(QPointF(0, 0), notify=False)
            case 1:
                self.setPos(QPointF(w / 2, 0), notify=False)
            case 2:
                self.setPos(QPointF(w, 0), notify=False)
            case 3:
                self.setPos(QPointF(w, h / 2), notify=False)
            case 4:
                self.setPos(QPointF(w, h), notify=False)
            case 5:
                self.setPos(QPointF(w/2, h), notify=False)
            case 6:
                self.setPos(QPointF(0, h), notify=False)
            case 7:
                self.setPos(QPointF(0, h/2), notify=False)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(OdvPen(QColor("yellow"), self.width))
        painter.drawLine(self.l1)
        painter.drawLine(self.l2)

    def shape(self):
        temp_l1 = QGraphicsLineItem(self.l1)
        temp_l1.setPen(OdvPen(QColor("yellow"), self.width))
        temp_l2 = QGraphicsLineItem(self.l2)
        temp_l2.setPen(OdvPen(QColor("yellow"), self.width))
        return temp_l1.shape() + temp_l2.shape()

    def boundingRect(self):
        return self.shape().boundingRect()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = self.mapToScene(event.pos()).truncated()
            event.accept()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self._drag_position = None
        event.accept()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if self._drag_position is not None:
            scene_position = self.mapToScene(event.pos()).truncated()
            delta = scene_position - self._drag_position
            self.setPos(self.pos() + delta)
            self._drag_position = scene_position
            event.accept()
        else:
            event.ignore()



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
        self._drag_position = None
        self._pixel_setter = None
        self._pixel_clicked_state = None
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

    # TODO refactor mousse events
    # use event.accept() and event.ignore()
    # change strategy to handle double click

    def set_pixel_from_mousse_event(self, event: QGraphicsSceneMouseEvent):
        if self._pixel_setter is not None:
            scene_position = self.mapToScene(event.pos())
            mousse_relative_position = scene_position - self.parentItem().pos()
            x = floor(mousse_relative_position.x())
            y = floor(mousse_relative_position.y())
            self.mask_image.set_pixel(x, y, self._pixel_setter)
            self.update()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        mousse_relative_position = self.mapToScene(event.pos()) - self.parentItem().pos()
        x = floor(mousse_relative_position.x())
        y = floor(mousse_relative_position.y())
        self._pixel_clicked_state = self.mask_image.get_pixel(x, y)

        if event.button() == Qt.MouseButton.LeftButton:
            self._pixel_setter = True
            # self.mouseMoveEvent(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self._pixel_setter = False
            # self.mouseMoveEvent(event)
        # else:
        # super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        mousse_relative_position = self.mapToScene(event.pos()) - self.parentItem().pos()
        x = floor(mousse_relative_position.x())
        y = floor(mousse_relative_position.y())
        self.mask_image.set_pixel(x, y, self._pixel_clicked_state)
        self.update()

        if event.button() == Qt.MouseButton.LeftButton:
            self._pixel_setter = None
            self._drag_position = self.mapToScene(event.pos()).truncated()
        # else:
        # super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        self._drag_position = None
        self._pixel_setter = None
        # super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        scene_position = self.mapToScene(event.pos())
        if self._pixel_setter is not None:
            mousse_relative_position = scene_position - self.parentItem().pos()
            x = floor(mousse_relative_position.x())
            y = floor(mousse_relative_position.y())
            self.mask_image.set_pixel(x, y, self._pixel_setter)
            self.update()
        if self._drag_position is not None:
            new_pos = self.parentItem().pos() + scene_position.truncated() - self._drag_position
            self.parentItem().setPos(new_pos)
            self._drag_position = scene_position.truncated()
        # super().mouseMoveEvent(event)

    def shape(self):
        path = QPainterPath()
        path.addRect(QRectF(0,0, self.mask_image.width, self.mask_image.height))
        return path
