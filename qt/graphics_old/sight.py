from PyQt6.QtCore import QLineF, QPointF
from PyQt6.QtGui import QPolygonF

from qt.graphics_old.base import OdvGraphic
from qt.graphics_old.line_elem import OdvFixLineElement
from qt.graphics_old.point_elem import OdvEditPointElement
from qt.graphics_old.polygon_elem import OdvFixPolygonElement


class GraphicSightObstacle(OdvGraphic):

    def __init__(self, sub_inspector):
        super().__init__(sub_inspector)

        self.poly_below_fix = None
        self.poly_above_fix = None
        self.vline_fix = []

        self.exit_edit_mode(save=False)

    @property
    def sight_line_list(self):
        return self.sub_inspector.current


    def enter_edit_mode(self):
        pass

        # self.update()

    def exit_edit_mode(self, save):
        if save is True:
            pass

        vline_list = [QLineF(QPointF(vline.x, vline.y - vline.z_bottom), QPointF(vline.x, vline.y - vline.z_top))
                          for vline in self.sight_line_list]

        self.vline_fix = [OdvFixLineElement(self, line) for line in vline_list]
        self.poly_below_fix = OdvFixPolygonElement(self, QPolygonF([line.p1() for line in vline_list]))
        self.poly_above_fix = OdvFixPolygonElement(self, QPolygonF([line.p2() for line in vline_list]))

        self.update()

    def point_moved(self, point_item: OdvEditPointElement):
        pass
