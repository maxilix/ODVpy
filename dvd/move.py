from typing import Iterator, Self

from PyQt6.QtGui import QPainterPath

from common import *
from debug import timeit
from odv.pathfinder import PathFinder
from .section import Section


class MovePolygon(RWStreamable):
    _main: bool
    _poly: QPolygonF

    def __init__(self, parent, poly: QPolygonF = None):
        assert isinstance(parent, Sublayer)
        self.parent = parent
        if poly is None:
            self._poly = QPolygonF()
        else:
            self.poly = poly

    @property
    def main(self) -> bool:
        return self._main

    @property
    def poly(self) -> QPolygonF:
        return self._poly

    @poly.setter
    def poly(self, poly: QPolygonF):
        # check if poly is clockwise
        if poly.signed_area() <= 0:
            # clockwise
            self._poly = poly
        else:
            # counter-clockwise
            self._poly = QPolygonF(poly[::-1])

    def __str__(self):
        if self.main:
            return f"Main Area {self.global_id}"
        else:
            return f"Obstacle {self.global_id}"


    @property
    def i(self):
        return self.parent.i

    @property
    def j(self):
        return self.parent.j

    @property
    def k(self):
        return self.parent.area_list.index(self)

    @property
    def global_id(self) -> int:
        return (self.k +
                sum([len(self.parent.parent[j]) for j in range(self.j)]) +
                sum([self.parent.parent.parent[i].total_area() for i in range(self.i)]))

    def __iter__(self) -> Iterator[QPointF]:
        return iter(self._poly)

    def __len__(self) -> int:
        return len(self._poly)

    def __getitem__(self, index: int) -> QPointF:
        return self._poly[index % len(self._poly)]

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent):
        poly = stream.read(QPolygonF)
        return cls(parent, poly)

    def to_stream(self, stream: WriteStream):
        stream.write(self._poly)


class MainArea(MovePolygon):
    _main = True


class Obstacle(MovePolygon):
    _main = False


class Sublayer(RWStreamable):

    def __init__(self, parent, main: MainArea | None = None, obstacles: list[Obstacle] | None = None) -> None:
        assert isinstance(parent, Layer)
        self.parent = parent
        self._path = None
        if main is None:
            self.area_list = []
        else:
            if obstacles is None:
                self.area_list = [main]
            else:
                self.area_list = [main] + obstacles
        # Segments seem to be an optimization for the pathfinder, probably no longer necessary today
        # The pathfinder works well without segments
        # self.segment_list = segment_list

    @property
    def i(self):
        return self.parent.i

    @property
    def j(self):
        return self.parent.sublayer_list.index(self)

    def __str__(self):
        return f"Sublayer {self.j}"

    def __iter__(self) -> Iterator[MovePolygon]:
        return iter(self.area_list)

    def __getitem__(self, index: int) -> MovePolygon:
        return self.area_list[index]

    def __len__(self) -> int:
        return len(self.area_list)

    @property
    def main(self) -> MainArea:
        return self.area_list[0]

    @property
    def obstacles(self) -> list[Obstacle]:
        return self.area_list[1:]

    def add_obstacle(self, poly: QPolygonF, index: int = 0) -> Obstacle:
        self._path = None
        obstacle = Obstacle(self, poly)
        if index <= 0:
            self.area_list.append(obstacle)
        else:
            self.area_list.insert(index, obstacle)
        return obstacle

    def delete_obstacle(self, index: int):
        self._path = None
        assert 0 < index < len(self.area_list)
        self.area_list.pop(index)

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent) -> Self:
        rop = cls(parent)

        main = stream.read(MainArea, parent=rop)
        nb_segment = stream.read(UShort)
        segment_list = [stream.read(QLineF) for _ in range(nb_segment)]
        nb_obstacle = stream.read(UShort)
        obstacles = [stream.read(Obstacle, parent=rop) for _ in range(nb_obstacle)]
        rop.area_list = [main] + obstacles
        return rop

    def to_stream(self, substream: WriteStream) -> None:
        substream.write(self.main)

        substream.write(UShort(0))  # always write zero segments
        # nb_segment = len(self.segment_list)
        # substream.write(UShort(nb_segment))
        # for segment in self.segment_list:
        #     substream.write(segment)

        nb_obstacle = len(self.obstacles)
        substream.write(UShort(nb_obstacle))
        for obstacle in self.obstacles:
            substream.write(obstacle)

    @property
    def path(self):
        if self._path is None:
            self._path = QPainterPath()
            self._path.addPolygon(self.main.poly)
            self._path.closeSubpath()
            for obstacle in self.obstacles:
                negative = QPainterPath()
                negative.addPolygon(obstacle.poly)
                negative.closeSubpath()
                self._path -= negative
        return self._path

    # def build_allow_path(self):
    #     self.allow_path = QPainterPath()
    #     self.allow_path.addPolygon(self.main.qpf)
    #     self.allow_path.closeSubpath()
    #     for obstacle in self.obstacles:
    #         negative = QPainterPath()
    #         negative.addPolygon(obstacle.qpf)
    #         negative.closeSubpath()
    #         self.allow_path -= negative

    @timeit
    def contains(self, poly: QPolygonF) -> bool:
        poly_area = poly.area()
        inter = self.main.poly.intersected(poly)
        inter_area = inter.area()
        if (poly_area - inter_area) <= 0.1:
            # poly is in main
            for obstacle in self.obstacles:
                inter = obstacle.poly.intersected(poly)
                if inter.isEmpty():
                    continue
                inter_area = inter.area()
                if inter_area > 0.1:
                    # obstacle intersects poly
                    return False
            return True
        else:
            return False


class Layer(RWStreamable):

    def __init__(self, parent, sublayer_list=None):
        assert isinstance(parent, Move)
        self.parent = parent
        if sublayer_list is None:
            self.sublayer_list = []
        else:
            self.sublayer_list = sublayer_list

    @property
    def i(self):
        return self.parent.layer_list.index(self)

    def __str__(self):
        return f"Layer {self.i}"

    def __iter__(self):
        return iter(self.sublayer_list)

    def __getitem__(self, item: int) -> Sublayer:
        return self.sublayer_list[item]

    def __len__(self):
        return len(self.sublayer_list)

    def total_area(self) -> int:
        return sum([len(sublayer) for sublayer in self])

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent) -> Self:
        rop = cls(parent)
        # total_area is not used by the constructor and it's rebuilt on demand
        total_area = stream.read(UShort)
        nb_sublayer = stream.read(UShort)
        rop.sublayer_list = [stream.read(Sublayer, parent=rop) for _ in range(nb_sublayer)]
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(UShort(self.total_area()))
        nb_sublayer = len(self.sublayer_list)
        stream.write(UShort(nb_sublayer))
        for sublayer in self.sublayer_list:
            stream.write(sublayer)


class Move(Section):
    _name = "MOVE"
    _version = 1

    # def __init__(self, *args, **kwargs) -> None:
    #     super().__init__(*args, **kwargs)
    #     self.layer_list = []
    #     self.pathfinder = None

    def __iter__(self) -> Iterator[Layer]:
        return iter(self.layer_list)

    def __getitem__(self, index: int) -> Layer:
        return self.layer_list[index]

    def __len__(self) -> int:
        return len(self.layer_list)

    def get_by_global(self, k: int) -> MainArea:
        i = 0
        while (ta_i := self[i].total_area()) <= k:
            i += 1
            k -= ta_i
        j = 0
        while (ta_j := len(self[i][j])) <= k:
            j += 1
            k -= ta_j
        rop = self[i][j][k]
        # assert isinstance(rop, MainArea)
        return rop

    def _load(self, substream: ReadStream) -> None:
        nb_layer = substream.read(UShort)
        self.layer_list = [substream.read(Layer, parent=self) for _ in range(nb_layer)]

        self.pathfinder = substream.read(PathFinder, move=self)

    def _save(self, substream: WriteStream) -> None:
        nb_layer = len(self)
        substream.write(UShort(nb_layer))
        for layer in self:
            substream.write(layer)

        self.pathfinder.rebuild()
        substream.write(self.pathfinder)
