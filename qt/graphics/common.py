from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QGraphicsItem

from qt.control.q_scene_menu import QSceneMenuSection


# CG : CustomGraphicsItem
# QCG : QCustomGraphicsItem
#
# H : highlightable
# M : movable

# TODO ZValue

class QThinPen(QPen):
    def __init__(self, color):
        super().__init__(color)
        self.setWidthF(0.3)
        self.setCapStyle(Qt.PenCapStyle.FlatCap)
        self.setJoinStyle(Qt.PenJoinStyle.RoundJoin)


class CustomGraphicsItem(object):

    def __init__(self, odv_object, *args, **kwargs):
        self.odv_object = odv_object
        self._visible = False
        self._force_visibility = False
        super().__init__(*args, **kwargs)
        super().setVisible(True)
        self.update()

    def paint(self, painter: QPainter, option, widget=None):
        if self.visible:
            painter.setRenderHints(QPainter.RenderHint.Antialiasing)
            super().paint(painter, option, widget)

    @property
    def visible(self):
        return self._visible or self._force_visibility

    @visible.setter
    def visible(self, value):
        self._visible = value
        if value:
            self.update()

    def setVisible(self, value):
        self.visible = value

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            section = QSceneMenuSection(self, event)
            event.shared_menu.add_section(section)
            event.accept()
        super().mousePressEvent(event)

    def scene_menu_local_actions(self, scene_position):
        return []

    def localise(self):
        self.scene().move_to_item(self)


class QCGItemGroup(QGraphicsItem):
    def __init__(self, q_dvd_item, *args, **kwargs):
        self.q_dvd_item = q_dvd_item
        super().__init__(*args, **kwargs)
        self.setFlag(self.flags() | QGraphicsItem.GraphicsItemFlag.ItemHasNoContents)

    def boundingRect(self):
        return self.childrenBoundingRect()

    def add_child(self, item):
        item.setParentItem(self)

    def add_children(self, items):
        for item in items:
            self.add_child(item)

    def remove_child(self, item):
        assert item in self.childItems()
        self.setParentItem(None)

    def remove_children(self, items):
        for item in items:
            self.remove_child(item)

    def update(self, rect: QRectF = QRectF()):
        for child in self.childItems():
            child.update(rect)
        super().update(rect)

    def delete(self):
        self.scene().removeItem(self)
