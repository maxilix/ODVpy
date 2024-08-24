from PyQt6.QtCore import QPointF

from qt.graphics.base import OdvGraphic
from qt.graphics.point_elem import OdvEditPointElement, OdvFixPointElement


class GraphicPoint(OdvGraphic):
    grid_alignment = QPointF(0.5, 0.5)

    def __init__(self, sub_inspector):
        super().__init__(sub_inspector)

        self.point_fix = None
        self.point_edit = None

        self.exit_edit_mode(save=False)

    @property
    def position(self):
        return self.sub_inspector.current

    @position.setter
    def position(self, position: QPointF):
        self.sub_inspector.current = position.truncated()

    def enter_edit_mode(self):
        self.remove(self.point_fix)

        self.point_edit = OdvEditPointElement(self, self.position, deletable=False)

        self.update()

    def exit_edit_mode(self, save=True):
        if save is True:
            self.position = self.point_edit.pos()

        self.remove(self.point_edit)

        self.point_fix = OdvFixPointElement(self, self.position)

        self.update()

    def point_moved(self, point_item: OdvEditPointElement):
        pass

