from PyQt6.QtCore import QPointF, QLineF
from PyQt6.QtGui import QPolygonF, QPainterPath

from common import *
from odv.pathfinder import PathFinders
from .section import Section
from math import acos, pi


class MovePolygon(Polygon):
    _main: bool

    @property
    def main(self):
        return self._main

    def signed_area(self):
        """
        Return the signed area of the polygon.
        A negative value indicates a clockwise points definition.
        A positive value indicates a counter-clockwise points definition.
        """
        area = 0.0

        for i in range(len(self)):
            current_point = self[i]
            next_point = self[i + 1]
            area += (next_point.x - current_point.x) * (next_point.y + current_point.y)

        return area / 2

    @property
    def clockwise(self):
        area = self.signed_area()
        assert area != 0.0
        return self.signed_area() < 0

    @clockwise.setter
    def clockwise(self, value: bool):
        if self.clockwise == value:
            return
        else:
            self.reverse()

    def angle_at(self, point_index):
        u = self[point_index - 1] - self[point_index]
        v = self[point_index + 1] - self[point_index]
        theta = acos((u.x*v.x + u.y*v.y) / (u.length() * v.length()))
        if u.x * v.y - u.y * v.x > 0:
            theta = 2*pi - theta
        return theta * 180 / pi


    def QPolygonF(self) -> QPolygonF:
        return QPolygonF([QPointF(p.x + 0.5, p.y + 0.5) for p in self])

    def reversed_QPolygonF(self) -> QPolygonF:
        return QPolygonF([QPointF(p.x + 0.5, p.y + 0.5) for p in reversed(self)])


class MainArea(MovePolygon):
    _main = True


class Obstacle(MovePolygon):
    _main = False

    # def __init__(self, area: Polygon):
    #     self.area = area

    # def check(self):
    #     # check if previous vector (resp. next vector) of each crossing point
    #     # really refer to the previous (resp. next) point of the area.
    #     for cp in self.crossing_point_list:
    #         if cp.previous_point not in self.previous_of(cp.point):
    #             print(f"{cp.point=}")
    #             print(f"{self.area.point_list=}")
    #             print(f"previous failed: {cp.previous_point} {self.previous_of(cp.point)}")
    #             print()
    #         if cp.next_point not in self.next_of(cp.point):
    #             print(f"{cp.point=}")
    #             print(f"{self.area.point_list=}")
    #             print(f"next failed: {cp.next_point} {self.next_of(cp.point)}")
    #             print()
    #
    # def next_of(self, point, incr=1):
    #     n = len(self.area)
    #     if self._main:
    #         incr = -incr
    #     return [self.area[(i + incr) % n] for i in range(n) if self.area[i] == point]
    #
    # def previous_of(self, point):
    #     return self.next_of(point, incr=-1)

    # @classmethod
    # def from_stream(cls, stream):
    #     move_area = stream.read(Polygon)
    #     return cls(move_area)
    #
    # def to_stream(self, stream):
    #     stream.write(self.area)


class Sublayer(RWStreamable):

    def __init__(self, main, obstacle_list):
        self.main = main
        self.obstacle_list = obstacle_list
        # self.segment_list = segment_list

    def __iter__(self):
        return iter(self.obstacle_list)

    def __getitem__(self, item: int) -> Obstacle:
        return self.obstacle_list[item]

    def __len__(self):
        return len(self.obstacle_list)

    @classmethod
    def from_stream(cls, stream: ReadStream):
        main = stream.read(MainArea)
        nb_segment = stream.read(UShort)
        segment_list = [stream.read(Segment) for _ in range(nb_segment)]
        nb_obstacle = stream.read(UShort)
        obstacle_list = [stream.read(Obstacle) for _ in range(nb_obstacle)]

        return cls(main, obstacle_list)

    def to_stream(self, substream: WriteStream):
        substream.write(self.main)

        substream.write(UShort(0))  # always write zero segments
        # nb_segment = UShort(len(self.segment_list))
        # substream.write(nb_segment)
        # for segment in self.segment_list:
        #     substream.write(segment)

        nb_obstacle = UShort(len(self.obstacle_list))
        substream.write(nb_obstacle)
        for obstacle in self.obstacle_list:
            substream.write(obstacle)

    def QPainterPath(self):
        positive = QPainterPath()
        positive.addPolygon(self.main.QPolygonF())
        positive.closeSubpath()
        for obstacle in self.obstacle_list:
            negative = QPainterPath()
            negative.addPolygon(obstacle.QPolygonF())
            negative.closeSubpath()
            positive -= negative
        return positive


class Layer(RWStreamable):
    def __init__(self,
                 total_area,
                 sublayer_list):
        self.total_area = total_area  # is not yet dynamic TODO
        self.sublayer_list = sublayer_list

    def __iter__(self):
        return iter(self.sublayer_list)

    def __getitem__(self, item: int) -> Sublayer:
        return self.sublayer_list[item]

    def __len__(self):
        return len(self.sublayer_list)

    @classmethod
    def from_stream(cls, stream: ReadStream):
        total_area = stream.read(UShort)
        nb_sublayer = stream.read(UShort)
        sublayer_list = [stream.read(Sublayer) for _ in range(nb_sublayer)]
        return cls(total_area, sublayer_list)

    def to_stream(self, stream: WriteStream):
        stream.write(self.total_area)
        nb_sublayer = UShort(len(self.sublayer_list))
        stream.write(nb_sublayer)
        for sublayer in self.sublayer_list:
            stream.write(sublayer)


class Motion(Section):
    section_index = 2  # MOVE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loaded_areas = False
        self.layer_list = []

        self.loaded_pathfinder = False
        self.pathfinders = None

    def __iter__(self):
        return iter(self.layer_list)

    def __getitem__(self, item: int) -> Layer:
        return self.layer_list[item]

    def __len__(self):
        return len(self.layer_list)

    def _load(self, stream: ReadStream, only_areas: bool = False):
        self.load_areas(stream)
        if only_areas is False:
            self.load_pathfinder(stream)

    def load_areas(self, stream: ReadStream):
        version = stream.read(Version)
        assert version == 1

        nb_layer = stream.read(UShort)
        self.layer_list = [stream.read(Layer) for _ in range(nb_layer)]
        self.loaded_areas = True

    def load_pathfinder(self, stream: ReadStream):
        self.pathfinders = stream.read(PathFinders)
        self.loaded_pathfinder = True

    def _save(self, substream: WriteStream):
        if self.loaded_areas is False or self.loaded_pathfinder is False:
            return
        substream.write(Version(1))
        nb_layer = UShort(len(self))
        substream.write(nb_layer)
        for layer in self:
            substream.write(layer)

        substream.write(self.pathfinders)
