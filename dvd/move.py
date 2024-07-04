from typing import Iterator, Self

from common import *
from debug import timeit
from odv.pathfinder import PathFinder
from .section import Section




class MovePolygon():
    _main: bool
    _poly: QPolygonF
    i: int
    j: int
    k: int

    def __init__(self, poly: QPolygonF):
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

    def __iter__(self) -> Iterator[QPointF]:
        return iter(self._poly)

    def __len__(self) -> int:
        return len(self._poly)

    def __getitem__(self, index: int) -> QPointF:
        return self._poly[index % len(self._poly)]

    @classmethod
    def from_stream(cls,  stream: ReadStream):
        poly = stream.read(QPolygonF)
        return cls(poly)

    def to_stream(self, stream: WriteStream):
        stream.write(self._poly)


class MainArea(MovePolygon):
    _main = True


class Obstacle(MovePolygon):
    _main = False


class Sublayer(RWStreamable):
    i: int
    j: int

    def __init__(self, main: MainArea, obstacles: [Obstacle]) -> None:
        self.main = main
        self.obstacles = obstacles
        # Segments seem to be an optimization for the pathfinder, probably no longer necessary today
        # The pathfinder works well without segments
        # self.segment_list = segment_list

    def __iter__(self) -> Iterator[MovePolygon]:
        return iter([self.main] + self.obstacles)

    def __getitem__(self, index: int) -> MovePolygon:
        if index == 0:
            return self.main
        else:
            return self.obstacles[index - 1]

    def __len__(self) -> int:
        return 1 + len(self.obstacles)

    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        main = stream.read(MainArea)
        nb_segment = stream.read(UShort)
        segment_list = [stream.read(QLineF) for _ in range(nb_segment)]
        nb_obstacle = stream.read(UShort)
        obstacles = [stream.read(Obstacle) for _ in range(nb_obstacle)]

        return cls(main, obstacles)

    def to_stream(self, substream: WriteStream) -> None:
        substream.write(self.main)

        substream.write(UShort(0))  # always write zero segments
        # nb_segment = len(self.segment_list)
        # substream.write(UShort(nb_segment))
        # for segment in self.segment_list:
        #     substream.write(segment)

        nb_obstacle = UShort(len(self.obstacles))
        substream.write(nb_obstacle)
        for obstacle in self.obstacles:
            substream.write(obstacle)

    # @property
    # def allow_path(self):
    #     if self._allow_path is None:
    #         self._allow_path = QPainterPath()
    #         self._allow_path.addPolygon(self.main.QPolygonF())
    #         self._allow_path.closeSubpath()
    #         for obstacle in self.obstacles:
    #             negative = QPainterPath()
    #             negative.addPolygon(obstacle.QPolygonF())
    #             negative.closeSubpath()
    #             self._allow_path -= negative
    #     return self._allow_path

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
    i: int

    def __init__(self, sublayer_list):
        self.sublayer_list = sublayer_list

    def __iter__(self):
        return iter(self.sublayer_list)

    def __getitem__(self, item: int) -> Sublayer:
        return self.sublayer_list[item]

    def __len__(self):
        return len(self.sublayer_list)

    def total_area(self) -> int:
        return sum([len(sublayer) for sublayer in self])

    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        # total_area is not used by the constructor and it's rebuilt on demand
        total_area = stream.read(UShort)
        nb_sublayer = stream.read(UShort)
        sublayer_list = [stream.read(Sublayer) for _ in range(nb_sublayer)]
        return cls(sublayer_list)

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

    def _load(self, substream: ReadStream) -> None:
        assert substream.read(Version) == self._version

        nb_layer = substream.read(UShort)
        self.layer_list = [substream.read(Layer) for _ in range(nb_layer)]
        for i, layer in enumerate(self):
            layer.i = i
            for j, sublayer in enumerate(layer):
                sublayer.i = i
                sublayer.j = j
                for k, area in enumerate(sublayer):
                    area.i = i
                    area.j = j
                    area.k = k

        self.pathfinder = substream.read(PathFinder, move=self)

    def _save(self, substream: WriteStream) -> None:
        substream.write(Version(self._version))
        nb_layer = len(self)
        substream.write(UShort(nb_layer))
        for layer in self:
            substream.write(layer)

        substream.write(self.pathfinder)
