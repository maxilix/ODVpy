from typing import Iterator, Self, Type
from math import acos, pi

from PyQt6.QtCore import QPointF, QLineF, QRectF, QPoint
from PyQt6.QtGui import QPainterPath

# from shapely.geometry import Polygon as SPolygon
# from shapely.geometry import MultiPolygon as SMultiPolygon

from common import *
from odv.pathfinder import PathFinder, timeit
from .section import Section


# def QPolygonF_signed_area(self: QPolygonF) -> float:
#     """
#     Return the signed area of the polygon.
#     A negative value indicates a clockwise points definition.
#     A positive value indicates a counter-clockwise points definition.
#     It's the mathematical opposite because the y-axis is inverted.
#     WARNING, does not work with self-intersecting polygons, unexpected behavior.
#     """
#     area = 0.0
#     n = self.count()
#     for i in range(n):
#         current_point = self[i]
#         next_point = self[(i + 1) % n]
#         area += (next_point.x() - current_point.x()) * (next_point.y() + current_point.y())
#
#     return area / 2
#
#
# def QPolygonF_area(self: QPolygonF) -> float:
#     return abs(QPolygonF_signed_area(self))
#
#
# QPolygonF.signed_area = QPolygonF_signed_area
# QPolygonF.area = QPolygonF_area


class MovePolygon(Polygon):
    _main: bool

    @property
    def main(self) -> bool:
        return self._main

    def signed_area(self) -> float:
        """
        Return the signed area of the polygon.
        A negative value indicates a clockwise points definition.
        A positive value indicates a counter-clockwise points definition.
        It's the mathematical opposite because the y-axis is inverted.
        WARNING, does not work with self-intersecting polygons, unexpected behavior.
        """
        area = 0.0

        for i in range(len(self)):
            current_point = self[i]
            next_point = self[i + 1]
            area += (next_point.x - current_point.x) * (next_point.y + current_point.y)

        return area / 2


    @property
    def clockwise(self) -> bool:
        """
        Return True if polygon points are defined in clockwise order.
        """
        # area = self.signed_area()
        # assert area != 0.0
        return self.signed_area() <= 0

    @clockwise.setter
    def clockwise(self, value: bool) -> None:
        if self.clockwise == value:
            return
        else:
            self.reverse()

    # def angle_at(self, point_index):
    #     u = self[point_index - 1] - self[point_index]
    #     v = self[point_index + 1] - self[point_index]
    #     theta = acos((u.x*v.x + u.y*v.y) / (u.length() * v.length()))
    #     if u.x * v.y - u.y * v.x > 0:
    #         theta = 2*pi - theta
    #     return theta * 180 / pi

    # @timeit
    # def QPolygonF(self) -> QPolygonF:
    #     return QPolygonF([QPointF(p.x, p.y) for p in self])

    # def SPolygon(self) -> SPolygon:
    #     return SPolygon([QPointF(p.x, p.y) for p in self])

    def boundaries(self):
        n = len(self)
        rop = []
        for i in range(n):
            current_point = self[i]
            next_point = self[(i + 1) % n]
            rop.append(QLineF(current_point.x, current_point.y, next_point.x, next_point.y))
        return rop


class MainArea(MovePolygon):
    _main = True


class Obstacle(MovePolygon):
    _main = False


class Sublayer(RWStreamable):

    def __init__(self, main: MainArea, obstacles: [Obstacle]) -> None:
        self.main = main
        self.obstacles = obstacles
        # Segments seem to be an optimization for the pathfinder, probably no longer necessary today
        # The pathfinder works well without segments
        # self.segment_list = segment_list
        # self.boundaries = None
        # self.build_boundaries()
        # self.allow_path = None
        # self.build_allow_path()
        # self.multi_poly = SMultiPolygon([o.spf for o in obstacles])

    def __iter__(self) -> Iterator[MovePolygon]:
        return iter([self.main] + self.obstacles)

    def __getitem__(self, index: int) -> MovePolygon:
        if index == 0:
            return self.main
        else:
            return self.obstacles[index - 1]

    def __len__(self) -> int:
        return 1 + len(self.obstacles)

    # @property
    # def boundaries(self):
    #     if self._boundaries is None:
    #         self._boundaries = []
    #         for area in self:
    #             self._boundaries += area.boundaries()
    #     return self._boundaries

    # def build_boundaries(self):
    #     self.boundaries = []
    #     for area in self:
    #         self.boundaries += area.boundaries()


    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        main = stream.read(MainArea)
        nb_segment = stream.read(UShort)
        segment_list = [stream.read(Segment) for _ in range(nb_segment)]
        nb_obstacle = stream.read(UShort)
        obstacles = [stream.read(Obstacle) for _ in range(nb_obstacle)]

        return cls(main, obstacles)

    def to_stream(self, substream: WriteStream) -> None:
        substream.write(self.main)

        substream.write(UShort(0))  # always write zero segments
        # nb_segment = UShort(len(self.segment_list))
        # substream.write(nb_segment)
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
        inter = self.main.qpf.intersected(poly)
        inter_area = inter.area()
        if (poly_area - inter_area) <= 0.1:
            # poly is in main
            for obstacle in self.obstacles:
                inter = obstacle.qpf.intersected(poly)
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
    def __init__(self, sublayer_list):
        self.sublayer_list = sublayer_list

    def __iter__(self):
        return iter(self.sublayer_list)

    def __getitem__(self, item: int) -> Sublayer:
        return self.sublayer_list[item]

    def __len__(self):
        return len(self.sublayer_list)

    @property
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
        stream.write(UShort(self.total_area))
        nb_sublayer = UShort(len(self.sublayer_list))
        stream.write(nb_sublayer)
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

        self.pathfinder = substream.read(PathFinder, move=self)

    def _save(self, substream: WriteStream) -> None:
        substream.write(Version(self._version))
        nb_layer = len(self)
        substream.write(UShort(nb_layer))
        for layer in self:
            substream.write(layer)

        substream.write(self.pathfinder)
