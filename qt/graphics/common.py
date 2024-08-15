from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtWidgets import QGraphicsItem

from qt.control.q_scene_menu import QSceneMenuSection


# CG : CustomGraphicsItem
# QCG : QCustomGraphicsItem
#
# H : highlightable
# M : movable

# TODO ZValue

class QCGPen(QPen):
    def __init__(self, color, width):
        super().__init__(color)
        self.setWidthF(width)
        self.setCapStyle(Qt.PenCapStyle.FlatCap)
        self.setJoinStyle(Qt.PenJoinStyle.RoundJoin)


class QCGThinPen(QCGPen):
    def __init__(self, color):
        super().__init__(color, 0.3)


class QCGBrush(QBrush):
    def __init__(self, color, alpha):
        color.setAlpha(alpha)
        super().__init__(color)


class QCGLightBrush(QCGBrush):
    def __init__(self, color):
        super().__init__(color, 32)


class QCGHighBrush(QCGBrush):
    def __init__(self, color):
        super().__init__(color, 96)


class CustomGraphicsItem(object):

    def __init__(self, sub_inspector, *args, **kwargs):
        self.sub_inspector = sub_inspector
        super().__init__(*args, **kwargs)
        # super().setVisible(True)
        # self.update()

    def paint(self, painter: QPainter, option, widget=None):
        if self.visible:
            painter.setRenderHints(QPainter.RenderHint.Antialiasing)
            super().paint(painter, option, widget)

    @property
    def visible(self):
        return self.sub_inspector.visibility_checkbox.isChecked()

    # @visible.setter
    # def visible(self, value):
    #     self._visible = value
    #     self.update()
    #
    # def setVisible(self, value):
    #     self.visible = value

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
    def __init__(self, sub_inspector, *args, **kwargs):
        self.sub_inspector = sub_inspector
        super().__init__(*args, **kwargs)
        self.setFlag(self.flags() | QGraphicsItem.GraphicsItemFlag.ItemHasNoContents)

    def boundingRect(self):
        return self.childrenBoundingRect()

    def add_child(self, item):
        item.setParentItem(self)
        # new child is automatically added to the scene

    @property
    def visible(self):
        cv = [child.visible for child in self.childItems()]

        if cv[0] is True:
            assert all(cv)
        else:
            assert not any(cv)
        return cv[0]


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
