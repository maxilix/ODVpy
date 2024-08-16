from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPen, QBrush, QPainter
from PyQt6.QtWidgets import QGraphicsItem

from qt.control.q_scene_menu import QSceneMenuSection


# TODO ZValue

class OdvPen(QPen):
    def __init__(self, color, width):
        super().__init__(color)
        self.setWidthF(width)
        self.setCapStyle(Qt.PenCapStyle.FlatCap)
        self.setJoinStyle(Qt.PenJoinStyle.RoundJoin)


class OdvThinPen(OdvPen):
    def __init__(self, color):
        super().__init__(color, 0.3)


class OdvBrush(QBrush):
    def __init__(self, color, alpha):
        color.setAlpha(alpha)
        super().__init__(color)


class OdvLightBrush(OdvBrush):
    def __init__(self, color):
        super().__init__(color, 32)


class OdvHighBrush(OdvBrush):
    def __init__(self, color):
        super().__init__(color, 96)


class OdvGraphicElement(object):

    def __init__(self, sub_inspector, *args, **kwargs):
        self.sub_inspector = sub_inspector
        self.force_visible = False
        super().__init__(*args, **kwargs)


    def paint(self, painter: QPainter, option, widget=None):
        if self.visible:
            painter.setRenderHints(QPainter.RenderHint.Antialiasing)
            super().paint(painter, option, widget)

    @property
    def visible(self):
        return self.parentItem().visible or self.force_visible

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


class OdvGraphic(QGraphicsItem):
    def __init__(self, sub_inspector, *args, **kwargs):
        # assert isinstance(sub_inspector, GraphicSubInspector)
        self.sub_inspector = sub_inspector
        self._visible = False
        super().__init__(*args, **kwargs)
        self.setFlag(self.flags() | QGraphicsItem.GraphicsItemFlag.ItemHasNoContents)

    def boundingRect(self):
        return self.childrenBoundingRect()

    def add_child(self, item):
        item.setParentItem(self)
        # new child is automatically added to the scene

    @property
    def visible(self):
        return self.sub_inspector.visibility_checkbox.isChecked()

    def add_children(self, items):
        for item in items:
            self.add_child(item)

    def remove_child(self, item):
        if item is not None:
            assert item in self.childItems()
            item.setParentItem(None)
            # old child is automatically removed from the scene


    def remove_children(self, items):
        for item in items:
            self.remove_child(item)

    def update(self, rect: QRectF = QRectF()):
        for child in self.childItems():
            child.update(rect)
        super().update(rect)

    def delete(self):
        self.scene().removeItem(self)

    def localise(self):
        self.scene().move_to_item(self)
