from enum import Enum

from PyQt6.QtCore import QRectF, QPointF, Qt
from PyQt6.QtGui import QColor, QBrush, QPolygonF
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsPolygonItem

from qt.graphics import OdvThinPen, OdvLightBrush, OdvHighBrush
from qt.graphics.line_elem import OdvEditLineElement
from qt.graphics.point_elem import OdvEditPointElement, OdvPointerElement


class OdvGraphic(QGraphicsItem):
    grid_alignment = QPointF(0, 0)
    initial_opacity = 1

    shadow = None

    thin_pen = OdvThinPen(QColor("black"))
    light_brush = OdvLightBrush(QColor("black"))
    high_brush = OdvHighBrush(QColor("black"))

    def __init__(self, item, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item = item
        self.setFlag(self.flags() | QGraphicsItem.GraphicsItemFlag.ItemHasNoContents)
        self.setOpacity(self.initial_opacity)
        self.setVisible(False)

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



class GraphicState(Enum):
    NoGraph = 0
    Fix = 1
    Edit = 2
    Create = 3



class OdvEditGraphic(OdvGraphic):
    _state = GraphicState.NoGraph

    @property
    def state(self):
        return self._state

    def enter_creation_mode(self):
        raise NotImplementedError

    def exit_creation_mode(self, save):
        raise NotImplementedError

    def enter_edit_mode(self):
        raise NotImplementedError

    def exit_edit_mode(self, save):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def point_moved(self, moved_point: OdvEditPointElement|OdvPointerElement):
        raise NotImplementedError

    def add_point(self, position: QPointF, cut_line: OdvEditLineElement=None):
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
