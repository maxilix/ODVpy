from PyQt6.QtCore import QRectF, QPointF, QObject, Qt
from PyQt6.QtGui import QColor, QBrush, QPen, QPolygonF
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsPolygonItem

from qt.graphics import OdvThinPen, OdvLightBrush, OdvHighBrush, OdvBrush
from qt.graphics.line_elem import OdvEditLineElement
from qt.graphics.point_elem import OdvEditPointElement


class OdvGraphic(QGraphicsItem):
    grid_alignment = QPointF(0, 0)

    thin_pen = OdvThinPen(QColor("black"))
    light_brush = OdvLightBrush(QColor("black"))
    high_brush = OdvHighBrush(QColor("black"))

    def __init__(self, item, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item = item
        self.shadow = None
        self.setFlag(self.flags() | QGraphicsItem.GraphicsItemFlag.ItemHasNoContents)

    def boundingRect(self):
        return self.childrenBoundingRect()

    def remove(self, items):
        if items is not None:
            if isinstance(items, QGraphicsItem):
                items = [items]
            for item in items:
                self.scene().removeItem(item)

    def update(self, rect: QRectF = QRectF()):
        for child in self.childItems():
            child.update(rect)
        super().update(rect)

    def localise(self):
        self.scene().move_to_item(self)

    def point_moved(self, moved_point: OdvEditPointElement):
        raise NotImplementedError

    def add_point(self, position: QPointF, cut_line: OdvEditLineElement):
        raise NotImplementedError

    def delete_point(self, old_point: OdvEditPointElement):
        raise NotImplementedError




class OdvShadow(QGraphicsPolygonItem):
    def __init__(self, tree_item, polygon: QPolygonF):
        super().__init__()
        self.tree_item = tree_item
        self.setPolygon(polygon)
        self.setPen(OdvThinPen(Qt.GlobalColor.transparent))
        # self.setPen(OdvThinPen(Qt.GlobalColor.black))
        self.setBrush(QBrush(Qt.GlobalColor.transparent))
        self.setZValue(0)
