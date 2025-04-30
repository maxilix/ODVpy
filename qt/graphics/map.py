from PyQt6.QtWidgets import QGraphicsItem


class GraphicMap(QGraphicsItem):
    grid_alignment = None

    def __init__(self, sub_inspector, *args, **kwargs):
        # assert isinstance(sub_inspector, GraphicSubInspector)
        self.sub_inspector = sub_inspector
        super().__init__(*args, **kwargs)
        self.setFlag(self.flags() | QGraphicsItem.GraphicsItemFlag.ItemHasNoContents)

        self.map_item = None
        self.map_rect = None
        self.reset_map()

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


    @property
    def map(self) -> QImage :
        return self.sub_inspector.current

    def reset_map(self):
        self.remove(self.map_item)
        self.remove(self.map_rect)

        self.map_item = OdvFixPixmapElement(self, QPixmap(self.map))
        self.map_item.setZValue(0.1)
        self.map_rect = OdvFixPolygonElement(self, QPolygonF(self.map.rect().toRectF()))
        self.map_rect.force_visible = True
        self.map_rect.setZValue(0)

        self.update()

    def setOpacity(self, opacity):
        # opacity only affect map_item
        self.map_item.setOpacity(opacity)