from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtWidgets import QGraphicsItem

from qt.graphics_old.line_elem import OdvEditLineElement
from qt.graphics_old.point_elem import OdvEditPointElement


class OdvGraphic(QGraphicsItem):
    grid_alignment = None

    def __init__(self, sub_inspector, *args, **kwargs):
        # assert isinstance(sub_inspector, GraphicSubInspector)
        self.sub_inspector = sub_inspector
        super().__init__(*args, **kwargs)
        self.setFlag(self.flags() | QGraphicsItem.GraphicsItemFlag.ItemHasNoContents)

    def boundingRect(self):
        return self.childrenBoundingRect()

    @property
    def visible(self):
        return self.sub_inspector.visibility_checkbox.isChecked()

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