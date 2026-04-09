from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPolygonF
from PyQt6.QtWidgets import QGraphicsItem

from qt.graphics.base import OdvEditGraphic, GraphicState
from qt.graphics.line_elem import OdvEditLineElement
from qt.graphics.point_elem import OdvEditPointElement
from qt.graphics.polygon_elem import OdvEditPolygonShapeElement, OdvFixPolygonElement


class GraphicPolygon(OdvEditGraphic):
    grid_alignment = QPointF(0.5, 0.5)

    def __init__(self, item, polygon:QPolygonF = QPolygonF()):
        super().__init__(item)
        self.polygon = polygon
        self.setZValue(10)

        self.polygon_fix = None
        self.point_edit = []
        self.line_edit = []
        self.polygon_edit = None

        if self.polygon.isEmpty():
            self._state = GraphicState.NoGraph
        else:
            self.polygon_fix = OdvFixPolygonElement(self, self.polygon)
            self.shadow.setPolygon(self.polygon.translated(self.grid_alignment))
            self._state = GraphicState.Fix

    def enter_creation_mode(self, followers):
        assert self.state == GraphicState.NoGraph
        assert all(f.state == GraphicState.NoGraph for f in followers)
        if self.claim_pointer():
            self.setVisible(True)
            self._state = GraphicState.Create
            self.point_edit = []
            self.line_edit = []
            self.polygon_edit = None
            self.item.update_both()
            self._followers = followers
        else:
            print(f"WARNING: {self} cannot obtain pointer")


    def exit_creation_mode(self, save):
        if self.state == GraphicState.Create:
            if save is True and len(self.point_edit) >= 3:
                self.line_edit[-1].p2 = self.point_edit[0]
                self.polygon_edit.p_list = self.point_edit
                deletable = len(self.point_edit) > 3
                for p in self.point_edit:
                    p.deletable = deletable
                self.shadow.setPolygon(QPolygonF(p.pos() for p in self.point_edit))
                # self.polygon = QPolygonF(p.pos() for p in self.point_edit).truncated()
                self._state = GraphicState.Edit
                self.release_pointer()
                for follower in self._followers:
                    follower.point_edit = [OdvEditPointElement(follower, p.pos(), deletable=deletable) for p in self.point_edit]
                    follower.polygon_edit = OdvEditPolygonShapeElement(follower, follower.point_edit, movable=True)
                    follower.line_edit = [OdvEditLineElement(follower, p1, p2, secable=True) for p1, p2 in
                                          zip(follower.point_edit, follower.point_edit[1:] + [follower.point_edit[0]])]
                    follower.shadow.setPolygon(QPolygonF(p.pos() for p in follower.point_edit))
                    follower._state = GraphicState.Edit
                    follower.item.update()

            else:
                # TODO Cancel creation is not handle
                # update shadow
                # self.shadow.setPolygon(self.polygon.translated(self.grid_alignment))
                pass
            self._followers = []
            self.item.update_both()

    def enter_edit_mode(self):
        assert self.state == GraphicState.Fix
        self.setVisible(True)
        self._state = GraphicState.Edit

        self.remove(self.polygon_fix)
        deletable = len(self.polygon) > 3
        self.point_edit = [OdvEditPointElement(self, p, deletable=deletable) for p in self.polygon]
        self.polygon_edit = OdvEditPolygonShapeElement(self, self.point_edit, movable=True)
        self.line_edit = [OdvEditLineElement(self, p1, p2, secable=True) for p1, p2 in
                          zip(self.point_edit, self.point_edit[1:] + [self.point_edit[0]])]
        self.item.update_both()

    def exit_edit_mode(self, save):
        assert self.state == GraphicState.Edit
        self._state = GraphicState.Fix
        if save is True:
            self.polygon.swap(QPolygonF(p.pos() for p in self.point_edit).truncated())
        else:
            # reset shadow
            self.shadow.setPolygon(self.polygon.translated(self.grid_alignment))
            if self.polygon.isEmpty():
                self._state = GraphicState.NoGraph

        self.remove(self.polygon_edit)
        self.remove(self.line_edit)
        self.remove(self.point_edit)

        self.polygon_fix = OdvFixPolygonElement(self, self.polygon)
        self.item.update_both()

    def copy_from(self, graphic_item):
        # print(type(graphic_item))
        # print(type(self))
        # exit()
        assert isinstance(graphic_item, type(self))
        self.delete()
        self.polygon = QPolygonF(graphic_item.polygon)
        self.polygon_fix = OdvFixPolygonElement(self, self.polygon)
        self.point_edit = []
        self.line_edit = []
        self.polygon_edit = None
        self.shadow.setPolygon(self.polygon.translated(self.grid_alignment))
        self._state = GraphicState.Fix


    def delete(self):
        match self.state:
            case GraphicState.NoGraph:
                pass
            case GraphicState.Fix:
                self.remove(self.polygon_fix)
            case GraphicState.Edit:
                self.remove(self.polygon_edit)
                self.remove(self.line_edit)
                self.remove(self.point_edit)
            case GraphicState.Create:
                # TODO remove and release the pointer
                pass

        self.shadow.setPolygon(QPolygonF())
        self.polygon = QPolygonF()
        self._state = GraphicState.NoGraph
        self.item.update_both()

    def point_moved(self, moved_point: OdvEditPointElement):
        if self.state == GraphicState.Edit:
            # n = len(self.point_edit)
            i = self.point_edit.index(moved_point)

            self.line_edit[i - 1].update()
            self.line_edit[i].update()
            self.polygon_edit.update()

            # update shadow
            self.shadow.setPolygon(QPolygonF([p.pos() for p in self.point_edit]))
        elif self.state == GraphicState.Create:
            if len(self.point_edit) > 0:
                self.line_edit[-1].update()
            if len(self.point_edit) > 1:
                self.polygon_edit.update()

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
                    if len(self.point_edit) == 2:
                        self.polygon_edit = OdvEditPolygonShapeElement(self, self.point_edit + [self.pointer], movable=True)
                    elif len(self.point_edit) > 2:
                        self.polygon_edit.p_list = self.point_edit + [self.pointer]
                else:
                    print("WARNING, the last point is already at this position.")

            case GraphicState.Edit:
                i = self.line_edit.index(cut_line)
                # create new point
                new_point = OdvEditPointElement(self, position.truncated(), deletable=True)
                self.point_edit.insert(i+1, new_point)
                # update previous line
                cut_line.p2 = new_point
                # create next line
                n = len(self.point_edit)
                new_line = OdvEditLineElement(self, self.point_edit[i+1], self.point_edit[(i+2)%n], secable=True)
                self.line_edit.insert(i + 1, new_line)
                # update polygon shape
                self.polygon_edit.p_list = self.point_edit
                # update shadow
                self.shadow.setPolygon(QPolygonF([p.pos() for p in self.point_edit]))
                for p in self.point_edit:
                    p.deletable = True

    def delete_point(self, old_point: OdvEditPointElement):
        assert self.state == GraphicState.Edit
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
        # update shadow
        self.shadow.setPolygon(QPolygonF([p.pos() for p in self.point_edit]))
        if n == 4:  # then there are 3 points left
            for p in self.point_edit:
                p.deletable = False
