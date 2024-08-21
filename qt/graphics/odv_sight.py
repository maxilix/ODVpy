from PyQt6.QtCore import QLineF, QPointF
from PyQt6.QtGui import QPolygonF

from qt.graphics.common import OdvGraphic
from qt.graphics.odv_line import OdvFixLineElement, OdvEditLineElement
from qt.graphics.odv_point import OdvEditPointElement
from qt.graphics.odv_polygon import OdvFixPolygonElement


class OdvGraphicSightObstacle(OdvGraphic):

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
        # self.remove_child(self.polygon_fix)
        # self.polygon_fix = None
        #
        # deletable = len(self.polygon) > 3
        # self.point_item = [OdvEditPointElement(self.sub_inspector, p, movable=True, deletable=deletable) for p in self.polygon]
        # self.line_item = [OdvEditLineElement(self.sub_inspector, p1, p2, secable=True, deletable=False) for p1, p2 in
        #                   zip(self.point_item, self.point_item[1:] + [self.point_item[0]])]
        # self.polygon_shape = OdvEditPolygonShapeElement(self.sub_inspector, self.point_item, movable=True)
        # self.add_child(self.polygon_shape)
        # self.add_children(self.line_item)
        # self.add_children(self.point_item)
        #
        # self.update()

    def exit_edit_mode(self, save):
        if save is True:
            pass

        # self.remove_child(self.polygon_shape)
        # self.remove_children(self.line_fix)
        # self.remove_children(self.point_item)
        # self.polygon_shape = None
        # self.line_item = []
        # self.point_item = []

        vline_list = [QLineF(QPointF(vline.x, vline.y - vline.z_bottom), QPointF(vline.x, vline.y - vline.z_top))
                          for vline in self.sight_line_list]

        self.vline_fix = [OdvFixLineElement(self.sub_inspector, line) for line in vline_list]
        self.poly_below_fix = OdvFixPolygonElement(self.sub_inspector, QPolygonF([line.p1() for line in vline_list]))
        self.poly_above_fix = OdvFixPolygonElement(self.sub_inspector, QPolygonF([line.p2() for line in vline_list]))

        self.add_children(self.vline_fix)
        self.add_child(self.poly_below_fix)
        self.add_child(self.poly_above_fix)

        self.update()

    def point_moved(self, point_item: OdvEditPointElement):
        pass

    def point_added(self,
                    previous_point_item: OdvEditPointElement,
                    new_point_item: OdvEditPointElement,
                    new_line_item: OdvEditLineElement):
        raise

    def point_deleted(self, point_item: OdvEditPointElement):
        raise

    def line_deleted(self, line_item: OdvEditLineElement):
        raise
