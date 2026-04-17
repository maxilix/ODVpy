from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPolygonF

from qt.graphics.base import OdvEditGraphic, GraphicState
from qt.graphics.line_elem import OdvEditLineElement
from qt.graphics.point_elem import OdvEditPointElement
from qt.graphics.polygon_elem import OdvEditPolygonShapeElement, OdvFixPolygonElement


class GraphicPolygon(OdvEditGraphic):
    grid_alignment = QPointF(0.5, 0.5)

    def __init__(self, item, polygon:QPolygonF = QPolygonF()):
        super().__init__(item)
        self.setZValue(10)

        self.polygon_fix_item = OdvFixPolygonElement(self, polygon)
        self.point_edit_items = []
        self.line_edit_items = []
        self.shape_edit_item = None
        self.shadow.setPolygon(polygon.translated(self.grid_alignment))

    @property
    def polygon(self) -> QPolygonF:
        if self.polygon_fix_item.scene() is not None:
            return self.polygon_fix_item.polygon().truncated()
        if self.shape_edit_item is not None:
            return QPolygonF(p.pos() for p in self.point_edit_items).truncated()
        print(f"WARNING: {self} cannot obtain polygon")
        return QPolygonF()

    @property
    def state(self):
        if self.pointer is not None:
            return GraphicState.Create
        if self.polygon_fix_item is not None and self.polygon_fix_item.scene() is not None:
            return GraphicState.Lock
        if  self.shape_edit_item is not None and self.shape_edit_item.scene() is not None:
            return GraphicState.Unlock
        return GraphicState.NoGraph

    def enter_creation_mode(self, followers):
        assert self.state == GraphicState.NoGraph
        assert all(f.state == GraphicState.NoGraph for f in followers)
        if self.claim_pointer():
            self.setVisible(True)
            self.point_edit_items = []
            self.shape_edit_item = None
            self.line_edit_items = []
            self.item.update_both()
            self._followers = followers
        else:
            print(f"WARNING: {self} cannot obtain pointer")


    def exit_creation_mode(self):
        assert self.state == GraphicState.Create
        self.release_pointer()
        if len(self.point_edit_items) >= 3:
            self.line_edit_items[-1].p2 = self.point_edit_items[0]
            self.shape_edit_item.p_list = self.point_edit_items
            deletable = len(self.point_edit_items) > 3
            for p in self.point_edit_items:
                p.deletable = deletable
            self.shadow.setPolygon(QPolygonF(p.pos() for p in self.point_edit_items))

            for follower in self._followers:
                follower.point_edit_items = [OdvEditPointElement(follower, p.pos(), deletable=deletable) for p in self.point_edit_items]
                follower.shape_edit_item = OdvEditPolygonShapeElement(follower, follower.point_edit_items, movable=True)
                follower.line_edit_items = [OdvEditLineElement(follower, p1, p2, secable=True) for p1, p2 in
                                            zip(follower.point_edit_items, follower.point_edit_items[1:] + [follower.point_edit_items[0]])]
                follower.shadow.setPolygon(QPolygonF(p.pos() for p in follower.point_edit_items))
                follower.item.update_both()
                follower.edit_zone.update()

        else:
            self.remove(self.shape_edit_item)
            self.remove(self.line_edit_items)
            self.remove(self.point_edit_items)

        self.edit_zone.update()
        self.item.update_both()
        self._followers = []


    def unlock(self):
        assert self.state == GraphicState.Lock
        self.setVisible(True)

        deletable = len(self.polygon) > 3
        self.point_edit_items = [OdvEditPointElement(self, p, deletable=deletable) for p in self.polygon]
        self.shape_edit_item = OdvEditPolygonShapeElement(self, self.point_edit_items, movable=True)
        self.line_edit_items = [OdvEditLineElement(self, p1, p2, secable=True) for p1, p2 in
                                zip(self.point_edit_items, self.point_edit_items[1:] + [self.point_edit_items[0]])]

        self.remove(self.polygon_fix_item)

        self.edit_zone.update()
        self.item.update_both()

    def lock(self):
        assert self.state == GraphicState.Unlock

        self.polygon_fix_item = OdvFixPolygonElement(self, self.polygon)

        self.remove(self.point_edit_items)
        self.remove(self.shape_edit_item)
        self.remove(self.line_edit_items)

        self.edit_zone.update()
        self.item.update_both()

    def copy_from(self, graphic_item):
        assert isinstance(graphic_item, type(self))
        self.delete()
        self.polygon_fix_item = OdvFixPolygonElement(self, graphic_item.polygon)
        self.point_edit_items = []
        self.line_edit_items = []
        self.shadow.setPolygon(self.polygon.translated(self.grid_alignment))
        self.edit_zone.update()


    def delete(self):
        match self.state:
            case GraphicState.NoGraph:
                pass
            case GraphicState.Lock:
                self.remove(self.polygon_fix_item)
            case GraphicState.Unlock:
                self.remove(self.shape_edit_item)
                self.remove(self.line_edit_items)
                self.remove(self.point_edit_items)
            case GraphicState.Create:
                self.release_pointer()
                self.remove(self.shape_edit_item)
                self.remove(self.line_edit_items)
                self.remove(self.point_edit_items)

        self.shadow.setPolygon(QPolygonF())
        self.edit_zone.update()
        self.item.update_both()

    def point_moved(self, moved_point: OdvEditPointElement):
        if self.state == GraphicState.Unlock:
            i = self.point_edit_items.index(moved_point)

            self.line_edit_items[i - 1].update()
            self.line_edit_items[i].update()
            self.shape_edit_item.update()

            # update shadow
            self.shadow.setPolygon(QPolygonF([p.pos() for p in self.point_edit_items]))

            # update edit zone
            self.edit_zone.update()

        elif self.state == GraphicState.Create:
            if len(self.point_edit_items) > 0:
                self.line_edit_items[-1].update()
            if len(self.point_edit_items) > 1:
                self.shape_edit_item.update()

    def add_point(self, position: QPointF, cut_line: OdvEditLineElement = None):
        match self.state:
            case GraphicState.Create:
                assert cut_line is None
                if self.point_edit_items==[] or position.truncated() != self.point_edit_items[-1].pos().truncated():
                    new_point = OdvEditPointElement(self, position.truncated(), deletable=False)
                    self.point_edit_items.append(new_point)
                    new_line = OdvEditLineElement(self, self.point_edit_items[-1], self.pointer, secable=True)
                    self.line_edit_items.append(new_line)
                    if len(self.point_edit_items) > 1:
                        self.line_edit_items[-2].p2 = new_point
                    if len(self.point_edit_items) == 2:
                        self.shape_edit_item = OdvEditPolygonShapeElement(self, self.point_edit_items + [self.pointer], movable=True)
                    elif len(self.point_edit_items) > 2:
                        self.shape_edit_item.p_list = self.point_edit_items + [self.pointer]
                else:
                    print("WARNING, the last point is already at this position.")

            case GraphicState.Unlock:
                i = self.line_edit_items.index(cut_line)
                # create new point
                new_point = OdvEditPointElement(self, position.truncated(), deletable=True)
                self.point_edit_items.insert(i + 1, new_point)
                # update previous line
                cut_line.p2 = new_point
                # create next line
                n = len(self.point_edit_items)
                new_line = OdvEditLineElement(self, self.point_edit_items[i + 1], self.point_edit_items[(i + 2) % n], secable=True)
                self.line_edit_items.insert(i + 1, new_line)
                # update polygon shape
                self.shape_edit_item.p_list = self.point_edit_items
                # update shadow
                self.shadow.setPolygon(QPolygonF([p.pos() for p in self.point_edit_items]))
                # update edit zone
                self.edit_zone.update()
                for p in self.point_edit_items:
                    p.deletable = True

    def delete_point(self, old_point: OdvEditPointElement):
        assert self.state == GraphicState.Unlock
        n = len(self.point_edit_items)
        i = self.point_edit_items.index(old_point)
        # remove next line
        old_line = self.line_edit_items.pop(i)
        self.remove(old_line)
        # update previous line
        self.line_edit_items[i - 1].p2 = self.point_edit_items[(i + 1) % n]
        # remove old point
        old_point = self.point_edit_items.pop(i)
        self.remove(old_point)
        # update polygon shape
        self.shape_edit_item.p_list = self.point_edit_items
        # update shadow
        self.shadow.setPolygon(QPolygonF([p.pos() for p in self.point_edit_items]))
        # update edit zone
        self.edit_zone.update()
        if n == 4:  # then there are 3 points left
            for p in self.point_edit_items:
                p.deletable = False
