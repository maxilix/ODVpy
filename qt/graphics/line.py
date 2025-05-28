from PyQt6.QtCore import QLineF, QPointF
from PyQt6.QtGui import QPolygonF

from common import Gateway
from qt.graphics.base import OdvGraphic, OdvEditGraphic, GraphicState
from qt.graphics.line_elem import OdvEditLineElement, OdvFixLineElement, OdvArrowElement
from qt.graphics.point_elem import OdvEditPointElement


class GraphicLine(OdvGraphic):
    grid_alignment = QPointF(0.5, 0.5)

    def __init__(self, sub_inspector):
        super().__init__(sub_inspector)

        self.line_fix = None
        self.p1_item = None
        self.p2_item = None
        self.line_edit = None

        self.exit_edit_mode(save=False)

    @property
    def line(self):
        return self.sub_inspector.current

    @line.setter
    def line(self, line):
        self.sub_inspector.current = line.truncated()

    def enter_edit_mode(self):
        self.remove(self.line_fix)

        self.p1_item = OdvEditPointElement(self, self.line.p1(), deletable=False)
        self.p2_item = OdvEditPointElement(self, self.line.p2(), deletable=False)
        self.line_edit = OdvEditLineElement(self, self.p1_item, self.p2_item, secable=False)

        self.update()

    def exit_edit_mode(self, save):
        if save is True:
            self.line = QLineF(self.p1_item.pos(), self.p2_item.pos())

        self.remove(self.p1_item)
        self.remove(self.p2_item)
        self.remove(self.line_edit)

        self.line_fix = OdvFixLineElement(self, self.line)

        self.update()

    def point_moved(self, point_edit: OdvEditPointElement):
        self.line_edit.update()


class GraphicMultiLine(OdvEditGraphic):
    grid_alignment = QPointF(0.5, 0.5)

    def __init__(self, item, point_list:list[QPointF] | None = None):
        super().__init__(item)
        self.point_list = point_list
        self.setZValue(10)

        self.line_fix = None
        self.point_edit = []
        self.line_edit = []

        if self.point_list is None:
            self._state = GraphicState.NoGraph
        else:
            self.line_fix = [OdvFixLineElement(self, QLineF(p1, p2)) for p1, p2 in zip(self.point_list[:-1], self.point_list[1:])]
            self.shadow.setPolygon(QPolygonF())  # TODO
            self._state = GraphicState.Fix

    def enter_creation_mode(self):
        if self.state == GraphicState.NoGraph:
            self._state = GraphicState.Create
            self.claim_pointer()
            self.point_edit = []
            self.line_edit = []
            self.item.update_both()

    def exit_creation_mode(self, save):
        if self.state == GraphicState.Create:
            if save is True and len(self.point_edit) >= 2:
                # deletable = len(self.point_edit) > 2
                for p in self.point_edit:
                    p.deletable = True
                self.point_edit[0].deletable = False
                self.point_edit[-1].deletable = False
                self.shadow.setPolygon(QPolygonF())  # TODO
                self._state = GraphicState.Edit
                self.release_pointer()
            else:
                self.shadow.setPolygon(QPolygonF())  # TODO
                pass
            self.item.update_both()

    def enter_edit_mode(self):
        if self.state == GraphicState.Fix:
            self._state = GraphicState.Edit
            self.remove(self.line_fix)

            self.point_edit = [OdvEditPointElement(self, self.point_list[0], deletable=False)] + \
                              [OdvEditPointElement(self, p, deletable=True) for p in self.point_list[1:-1]] + \
                              [OdvEditPointElement(self, self.point_list[-1], deletable=False)]

            self.line_edit = [OdvEditLineElement(self, p1, p2, secable=True) for p1, p2 in
                              zip(self.point_edit[:-1], self.point_edit[1:])]
            self.item.update_both()

    def exit_edit_mode(self, save):
        if self.state == GraphicState.Edit:
            self._state = GraphicState.Fix
            if save is True:
                self.point_list.clear()
                self.point_list.extend([p.pos() for p in self.point_edit])
            else:
                # update shadow
                self.shadow.setPolygon(QPolygonF())  # TODO

            self.remove(self.point_edit)
            self.remove(self.line_edit)

            self.line_fix = [OdvFixLineElement(self, QLineF(p1,p2)) for p1, p2 in zip(self.point_list[:-1], self.point_list[1:])]
            self.item.update_both()

    def delete(self):
        match self.state:
            case GraphicState.NoGraph:
                pass
            case GraphicState.Fix:
                self.remove(self.line_fix)
            case GraphicState.Edit:
                self.remove(self.line_edit)
                self.remove(self.point_edit)
            case GraphicState.Create:
                pass

        self.shadow.setPolygon(QPolygonF())
        self.point_list = None
        self._state = GraphicState.NoGraph
        self.item.update_both()

    def point_moved(self, moved_point: OdvEditPointElement):
        if self.state == GraphicState.Edit:
            n = len(self.point_edit)
            i = self.point_edit.index(moved_point)
            if i>0:
                self.line_edit[i-1].update()
            if i<n-1:
                self.line_edit[i].update()

            self.shadow.setPolygon(QPolygonF([p.pos() for p in self.point_edit]))
        elif self.state == GraphicState.Create:
            if len(self.point_edit) > 0:
                self.line_edit[-1].update()


    def add_point(self, position: QPointF, cut_line: OdvEditLineElement = None):
        match self.state:
            case GraphicState.Create:
                assert cut_line is None
                if self.point_edit==[] or position.truncated() != self.point_edit[-1].pos().truncated():
                    new_point = OdvEditPointElement(self, position.truncated(), deletable=False)
                    self.point_edit.append(new_point)
                    new_line = OdvEditLineElement(self, self.point_edit[-1], self.pointer, secable=True)
                    self.line_edit.append(new_line)
                    if len(self.point_edit) > 1:
                        self.line_edit[-2].p2 = new_point
                else:
                    print("WARNING, the last point is already at this position.")

            case GraphicState.Edit:
                i = self.line_edit.index(cut_line)
                # create new point
                new_point = OdvEditPointElement(self, position, deletable=True)
                self.point_edit.insert(i+1, new_point)
                # update previous line
                cut_line.p2 = new_point
                # create next line
                n = len(self.point_edit)
                new_line = OdvEditLineElement(self, self.point_edit[i+1], self.point_edit[(i+2)%n], secable=True)
                self.line_edit.insert(i+1, new_line)

    def delete_point(self, old_point: OdvEditPointElement):
        assert self.state == GraphicState.Edit
        n = len(self.point_edit)
        i = self.point_edit.index(old_point)
        # remove next line
        old_line = self.line_edit.pop(i)
        self.remove(old_line)
        # update previous line
        self.line_edit[i-1].p2 = self.point_edit[(i+1) % n]
        # remove old point
        old_point = self.point_edit.pop(i)
        self.remove(old_point)



class GraphicGateway(OdvGraphic):
    grid_alignment = QPointF(0.5, 0.5)

    def __init__(self, sub_inspector):
        super().__init__(sub_inspector)

        self.arrow1 = OdvArrowElement(self)
        self.arrow2 = OdvArrowElement(self)

        self.line1_fix = None
        self.line2_fix = None
        self.p1_edit = None
        self.p2_edit = None
        self.p3_edit = None
        self.line1_edit = None
        self.line2_edit = None

        self.exit_edit_mode(save=False)

    @property
    def gateway(self):
        return self.sub_inspector.current

    @gateway.setter
    def gateway(self, gateway):
        self.sub_inspector.current = gateway.truncated()

    def enter_edit_mode(self):
        self.remove(self.line1_fix)
        self.remove(self.line2_fix)

        p1,p2,p3 = self.gateway
        self.p1_edit = OdvEditPointElement(self, p1, deletable=False)
        self.p2_edit = OdvEditPointElement(self, p2, deletable=False)
        self.p3_edit = OdvEditPointElement(self, p3, deletable=False)


        self.line1_edit = OdvEditLineElement(self, self.p1_edit, self.p2_edit, secable=False)
        self.line2_edit = OdvEditLineElement(self, self.p2_edit, self.p3_edit, secable=False)

        self.update()

    def exit_edit_mode(self, save):
        if save is True:
            self.gateway = Gateway(self.p1_edit.pos(), self.p2_edit.pos(), self.p3_edit.pos())

        self.remove(self.p1_edit)
        self.remove(self.p2_edit)
        self.remove(self.p3_edit)
        self.remove(self.line1_edit)
        self.remove(self.line2_edit)

        p1, p2, p3 = self.gateway
        self.line1_fix = OdvFixLineElement(self, QLineF(p1, p2))
        self.line2_fix = OdvFixLineElement(self, QLineF(p2, p3))

        self.arrow1.base_line = self.line1_fix.line()
        self.arrow2.base_line = self.line2_fix.line()

        self.update()

    def point_moved(self, point_edit: OdvEditPointElement):
        if point_edit == self.p1_edit or point_edit == self.p2_edit:
            self.line1_edit.update()
            self.arrow1.base_line = self.line1_edit.line()
        if point_edit == self.p2_edit or point_edit == self.p3_edit:
            self.line2_edit.update()
            self.arrow2.base_line = QLineF(self.p2_edit.pos(), self.p3_edit.pos())
