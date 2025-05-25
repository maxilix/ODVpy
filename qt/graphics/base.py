from enum import Enum

from PyQt6.QtCore import QRectF, QPointF, Qt
from PyQt6.QtGui import QColor, QBrush, QPolygonF, QAction, QCursor
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsPolygonItem, QGraphicsEllipseItem, QMenu

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
        self.shadow = OdvShadow(item, QPolygonF())
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

    # Todo remove localise, cause item is always localised by group (eventually group of 1)
    def localise(self):
        self.scene().move_to_item(self)

    def setVisible(self, visible: bool):
        if visible != self.isVisible():
            super().setVisible(visible)
            self.item.update_both()

    def setOpacity(self, opacity: float):
        if opacity != self.opacity():
            super().setOpacity(opacity)
            self.item.update_both()


class Pointer(QGraphicsEllipseItem):
    size: float = 2.2
    attached_item = None

    def __init__(self):
        super().__init__()
        self.setRect(-self.size / 2, -self.size / 2, self.size, self.size)
        self.setZValue(100)

    def is_attached(self):
        return self.attached_item is not None

    def attache_to(self, item):
        self.attached_item = item
        self.attached_item.setVisible(True)
        self.setVisible(True)
        self.setPen(self.attached_item.thin_pen)
        self.setBrush(self.attached_item.high_brush)

    def release(self):
        self.attached_item = None
        self.setVisible(False)

    def setPos(self, position: QPointF, notify=True):
        if (ga:=self.attached_item.grid_alignment) is not None:
            position =  position.truncated() + ga
        if position != self.pos():
            super().setPos(position)
            if notify:
                self.attached_item.point_moved(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            menu = QMenu()
            a_finalize = QAction("Finalize")
            a_finalize.triggered.connect(lambda: self.attached_item.exit_creation_mode(save=True))
            a_cancel = QAction("Cancel")
            a_cancel.triggered.connect(lambda: self.attached_item.exit_creation_mode(save=False))
            menu.addAction(a_finalize)
            menu.addAction(a_cancel)
            menu.exec(QCursor.pos())
        # accepts all events, no matter how it reacts to them.
        # ZValue=max (100) allows the pointer to be the first to react to mouse events.scene TODO not working
        # Accepting them blocks them for all other items.
        event.accept()

    def mouseDoubleClickEvent(self, event):
        self.attached_item.exit_creation_mode(save=True)
        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.attached_item.add_point(self.pos())
        event.accept()




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

    @property
    def pointer(self):
        pointer = self.scene().pointer
        assert self == pointer.attached_item
        return pointer

    def claim_pointer(self):
        self.scene().claim_pointer(self)

    def release_pointer(self):
        self.scene().release_pointer(self)

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

    def point_moved(self, moved_point: OdvEditPointElement | Pointer):
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

    def __bool__(self):
        return self.polygon() != QPolygonF()

