from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPolygonF

from qt.graphics.base import OdvGraphic
from qt.graphics.line_elem import OdvEditLineElement
from qt.graphics.point_elem import OdvEditPointElement
from qt.graphics.polygon_elem import OdvEditPolygonShapeElement, OdvFixPolygonElement


class GraphicPolygon(OdvGraphic):
    grid_alignment = QPointF(0.5, 0.5)
    def __init__(self, sub_inspector):
        super().__init__(sub_inspector)

        self.polygon_fix = None
        self.point_edit = []
        self.line_edit = []
        self.polygon_edit = None

        self.exit_edit_mode(save=False)

    @property
    def polygon(self):
        return self.sub_inspector.current

    @polygon.setter
    def polygon(self, polygon):
        self.sub_inspector.current = polygon.truncated()

    def enter_edit_mode(self):
        self.remove(self.polygon_fix)

        deletable = len(self.polygon) > 3
        self.point_edit = [OdvEditPointElement(self, p, deletable=deletable) for p in self.polygon]
        self.polygon_edit = OdvEditPolygonShapeElement(self, self.point_edit, movable=True)
        self.line_edit = [OdvEditLineElement(self, p1, p2, secable=True) for p1, p2 in
                          zip(self.point_edit, self.point_edit[1:] + [self.point_edit[0]])]

        self.update()


    def exit_edit_mode(self, save):
        if save is True:
            self.polygon = QPolygonF(p.pos() for p in self.point_edit)

        self.remove(self.polygon_edit)
        self.remove(self.line_edit)
        self.remove(self.point_edit)

        self.polygon_fix = OdvFixPolygonElement(self, self.polygon)

        self.update()

    def point_moved(self, moved_point: OdvEditPointElement):
        n = len(self.point_edit)
        i = self.point_edit.index(moved_point)

        self.line_edit[i - 1].update()
        self.line_edit[i].update()
        self.polygon_edit.update()

    def add_point(self, position: QPointF, cut_line: OdvEditLineElement):
        i = self.line_edit.index(cut_line)

        # create new point
        new_point = OdvEditPointElement(self, position, deletable=True)
        self.point_edit.insert(i+1, new_point)

        # update previous line
        cut_line.p2 = new_point

        # create next line
        n = len(self.point_edit)
        new_line = OdvEditLineElement(self, self.point_edit[i+1], self.point_edit[(i+2)%n], secable=True)
        self.line_edit.insert(i + 1, new_line)

        # update polygon shape
        self.polygon_edit.p_list = self.point_edit

        for p in self.point_edit:
            p.deletable = True

    def delete_point(self, old_point: OdvEditPointElement):
        n = len(self.point_edit)
        i = self.point_edit.index(old_point)

        # remove next line
        old_line = self.line_edit.pop(i)
        self.remove(old_line)

        # update previous line
        self.line_edit[i - 1].p2 = self.point_edit[(i + 1) % n]

        # remove old point
        old_point = self.point_edit.pop(i)
        self.remove(old_point)

        # update polygon shape
        self.polygon_edit.p_list = self.point_edit

        if n == 4:  # then there are 3 points left
            for p in self.point_edit:
                p.deletable = False
