from enum import Enum
from typing import List

from PyQt6.QtCore import QRectF, QPointF, Qt
from PyQt6.QtGui import QColor, QBrush, QPolygonF, QPainterPathStroker, QPainterPath
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsPolygonItem, QGraphicsPathItem

from qt.graphics import OdvThinPen, OdvLightBrush, OdvHighBrush
from qt.graphics.line_elem import OdvEditLineElement
from qt.graphics.point_elem import OdvEditPointElement


class OdvGraphic(QGraphicsItem):
    grid_alignment = QPointF(0, 0)
    initial_opacity = 1

    thin_pen = OdvThinPen(QColor("black"))
    light_brush = OdvLightBrush(QColor("black"))
    high_brush = OdvHighBrush(QColor("black"))

    def __init__(self, item, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item = item
        self.shadow = OdvShadow(item)
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

    # Todo remove localize, cause item is always localized by group (eventually group of 1)
    def localize(self):
        raise DeprecationWarning
        self.scene().move_to_item(self)

    # def setVisible(self, visible: bool):
    #     if visible != self.isVisible():
    #         super().setVisible(visible)
    #         self.item.update()
    #
    # def setOpacity(self, opacity: float):
    #     if opacity != self.opacity():
    #         super().setOpacity(opacity)
    #         self.item.update()



class GraphicState(Enum):
    NoGraph = 0
    Lock = 1
    Unlock = 2
    Create = 3



class OdvEditGraphic(OdvGraphic):

    def __init__(self, item):
        super().__init__(item)
        self._state = GraphicState.NoGraph
        self.edit_zone = OdvEditZone(self)
        self._followers = []

    @property
    def state(self):
        return self._state

    @property
    def pointer(self):
        if self == self.scene().pointer_item:
            return self.scene().pointer
        return None

    def setVisible(self, visibility: bool):
        if self.scene() is not None and visibility is False:
            if self.state == GraphicState.Unlock:
                self.lock()
            elif self.state == GraphicState.Create:
                self.delete()
        super().setVisible(visibility)

    def claim_pointer(self):
        return self.scene().claim_pointer(self)

    def release_pointer(self):
        return self.scene().release_pointer(self)

    def enter_creation_mode(self, followers:List[OdvEditGraphic]):
        raise NotImplementedError

    def exit_creation_mode(self):
        raise NotImplementedError

    def copy_from(self, graphic_item):
        raise NotImplementedError

    def unlock(self):
        raise NotImplementedError

    def lock(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def point_moved(self, moved_point: OdvEditPointElement):
        raise NotImplementedError

    def add_point(self, position: QPointF, cut_line: OdvEditLineElement=None):
        raise NotImplementedError

    def delete_point(self, old_point: OdvEditPointElement):
        raise NotImplementedError



class OdvShadow(QGraphicsPolygonItem):
    def __init__(self, tree_item, polygon: QPolygonF = QPolygonF()):
        super().__init__()
        self.tree_item = tree_item
        self.setPolygon(polygon)
        # self.setPen(OdvThinPen(Qt.GlobalColor.transparent))
        self.setPen(OdvThinPen(Qt.GlobalColor.black))
        self.setBrush(QBrush(Qt.GlobalColor.transparent))
        self.setZValue(0)

    def __bool__(self):
        return self.polygon() != QPolygonF()


class OdvEditZone(QGraphicsPathItem):
    def __init__(self, graphic_item: OdvEditGraphic):
        assert isinstance(graphic_item, OdvEditGraphic)
        super().__init__(graphic_item)
        self.stroker = QPainterPathStroker()
        self.stroker.setWidth(20)
        self.stroker.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

    def update(self, rect: QRectF = QRectF()):
        super().update(rect)
        path = QPainterPath()
        if (parent:=self.parentItem()).state == GraphicState.Unlock:
            poly = parent.shadow.polygon()
            if not poly.isEmpty():
                if not poly.isClosed():
                    poly.append(poly.first())
                path.addPolygon(poly)
                path = self.stroker.createStroke(path) + path
            else:
                print(f"WARNING: Shadow of {parent} is empty.")
        self.setPath(path)
