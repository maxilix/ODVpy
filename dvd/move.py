import sys
from functools import reduce
from io import StringIO

from PyQt6.QtCore import QPointF, QPoint, QLineF
from PyQt6.QtGui import QPolygonF, QPainterPath

from common import *
from debug import hxs

from .section import Section




class UnkLastObject(RWStreamable):

    def __init__(self, unk_tab1, unk_tab2):
        self.t1 = unk_tab1
        self.t2 = unk_tab2

    def is_ff(self) -> bool :
        return self.t1 == []

    @classmethod
    def from_stream(cls, stream):
        u1 = stream.read(UChar)
        if u1 == 255:  # 0xff is read
            return cls([], [])
        else:
            u2 = stream.read(UChar)

            n1 = stream.read(UShort)
            l1 = [stream.read(UChar) for _ in range(n1)]
            assert all([u in [1, 2, 4, 8] for u in l1])
            assert u1 == reduce(lambda x, y: x | y, l1)

            n2 = stream.read(UShort)
            assert n1 == n2
            l2 = [stream.read(UChar) for _ in range(n2)]
            assert all([u in [1, 2, 4, 8] for u in l2])
            assert u2 == reduce(lambda x, y: x | y, l2)
            return cls(l1, l2)

    def to_stream(self, stream):
        if self.t1 == [] and self.t2 == []:
            stream.write(UChar(255))
        else:
            u1 = UChar(reduce(lambda x, y: x | y, self.t1))
            stream.write(u1)
            u2 = UChar(reduce(lambda x, y: x | y, self.t2))
            stream.write(u2)
            n1 = UShort(len(self.t1))
            stream.write(n1)
            for u in self.t1:
                stream.write(u)
            n2 = UShort(len(self.t2))
            stream.write(n2)
            for u in self.t2:
                stream.write(u)


class PathLink(RWStreamable):

    def __init__(self, indexes1, point1, indexes2, point2, link_length, global_unk_obj_index_list, unk_obj):
        self.indexes1 = indexes1
        self.point1 = point1
        self.indexes2 = indexes2
        self.point2 = point2
        self.link_length = link_length
        self.global_unk_obj_index_list = global_unk_obj_index_list
        self.unk_obj = unk_obj

    def get_other(self, indexes):
        if indexes == self.indexes1:
            return self.indexes2
        elif indexes == self.indexes2:
            return self.indexes1
        else:
            raise IndexError(f"Link has no {indexes}")

    @classmethod
    def from_stream(cls, stream, *, nb_w=None):
        indexes1 = tuple(stream.read(UShort) for _ in range(4))
        indexes2 = tuple(stream.read(UShort) for _ in range(4))
        link_length = stream.read(UFloat)
        nb_unk_obj = stream.read(UShort)  # w again
        assert nb_w is None or nb_w == nb_unk_obj
        global_unk_obj_index_list = [stream.read(UShort) for _ in range(nb_unk_obj)]
        return cls(indexes1, None, indexes2, None, link_length, global_unk_obj_index_list, [])

    def to_stream(self, stream):
        for index1 in self.indexes1:
            stream.write(index1)
        for index2 in self.indexes2:
            stream.write(index2)
        stream.write(self.link_length)
        unk_obj_index_list_length = UShort(len(self.global_unk_obj_index_list))
        stream.write(unk_obj_index_list_length)
        for unk_obj_index in self.global_unk_obj_index_list:
            stream.write(unk_obj_index)

    def QLineF(self):
        p1 = self.point1.QPointF()
        p2 = self.point2.QPointF()
        return QLineF(p1, p2)


class CrossingPoint(RWStreamable):

    def __init__(self, unk_char, point, previous_point, next_point, global_link_path_index_list, path_link_list):
        self.unk_char = unk_char
        self.point = point
        self.previous_point = previous_point
        self.next_point = next_point
        self.global_path_link_index_list = global_link_path_index_list
        self.path_link_list = path_link_list

    def __iter__(self):
        return iter(self.path_link_list)

    def __getitem__(self, item):
        return self.path_link_list[item]

    def __len__(self):
        # assert (len(self.path_link_list) == len(self.global_path_link_index_list))
        return len(self.path_link_list)

    @classmethod
    def from_stream(cls, stream, *, nb_w=None):
        nb_bytes = stream.read(UShort)  # w again
        assert nb_w is None or nb_w == nb_bytes
        unk_char = [stream.read(UChar) for _ in range(nb_bytes)]
        # unk_char[0] define the position of area around the point, as a flag:
        # X=0 if obstacle is presente in the quarter
        # X=1 if no obstacle in the quarter
        #
        #    NW      |      NE
        #      ___X  |  __X_
        #     _______|_______
        #            |
        #      X___  |  _X__
        #    SW      |      SE
        #
        # 0x0f = 0b00001111 cannot be possible

        point = stream.read(UPoint)

        next_point = point + stream.read(Point)
        previous_point = point - stream.read(Point)

        nb_path_link = stream.read(UShort)
        global_path_link_index_list = [stream.read(UShort) for _ in range(nb_path_link)]
        return cls(unk_char, point, previous_point, next_point, global_path_link_index_list, [])

    def to_stream(self, stream):
        nb_bytes = UShort(len(self.unk_char))  # w
        stream.write(nb_bytes)
        for char in self.unk_char:
            stream.write(char)
        stream.write(self.point)
        stream.write(self.next_point - self.point)
        stream.write(self.point - self.previous_point)

        nb_path_link = UShort(len(self.global_path_link_index_list))
        stream.write(nb_path_link)
        for path_link_index in self.global_path_link_index_list:
            stream.write(path_link_index)

    def QPointF(self):
        return QPointF(self.point.x + 0.5, self.point.y + 0.5)


class MoveArea(RWStreamable):
    def __init__(self, area: Area, crossing_point_list=None, main=False):
        self.area = area
        if crossing_point_list is None:
            self.crossing_point_list = []
        else:
            self.crossing_point_list = crossing_point_list
        self._main = main

    """
    def check(self):
        # check if previous vector (resp. next vector) of each crossing point
        # really refer to the previous (resp. next) point of the area.
        for cp in self.crossing_point_list:
            if cp.previous_point not in self.previous_of(cp.point):
                print(f"{cp.point=}")
                print(f"{self.area.point_list=}")
                print(f"previous failed: {cp.previous_point} {self.previous_of(cp.point)}")
                print()
            if cp.next_point not in self.next_of(cp.point):
                print(f"{cp.point=}")
                print(f"{self.area.point_list=}")
                print(f"next failed: {cp.next_point} {self.next_of(cp.point)}")
                print()

    def next_of(self, point, incr=1):
        n = len(self.area)
        if self._main:
            incr = -incr
        return [self.area[(i + incr) % n] for i in range(n) if self.area[i] == point]

    def previous_of(self, point):
        return self.next_of(point, incr=-1)
    """

    @property
    def main(self):
        return self._main

    def __iter__(self):
        return iter(self.crossing_point_list)

    def __getitem__(self, item):
        return self.crossing_point_list[item]

    def __len__(self):
        return len(self.crossing_point_list)

    @classmethod
    def from_stream(cls, stream, main=False):
        move_area = stream.read(Area)
        return cls(move_area, [], main)

    def to_stream(self, stream):
        stream.write(self.area)

    def QPolygonF(self) -> QPolygonF:
        return QPolygonF([QPointF(p.x + 0.5, p.y + 0.5) for p in self.area.point_list])


class Sublayer(RWStreamable):

    def __init__(self, area_list, segment_list):
        self.area_list = area_list  # [main_area] + obstacle_list
        self.segment_list = segment_list

    def __iter__(self):
        return iter(self.area_list)

    def __getitem__(self, item):
        return self.area_list[item]

    def __len__(self):
        return len(self.area_list)

    @classmethod
    def from_stream(cls, stream):
        main_area = stream.read(MoveArea, main=True)
        # stream.debug_new_line()

        nb_segment = stream.read(UShort)
        segment_list = [stream.read(Segment) for _ in range(nb_segment)]
        # segment_list = stream.read(Array, Segment, comment="nb segment")

        nb_obstacle = stream.read(UShort)
        obstacle_list = [stream.read(MoveArea) for _ in range(nb_obstacle)]
        # sub_area_list = stream.read(Array, Area, comment="nb excluded area")

        return cls([main_area] + obstacle_list, segment_list)

    def to_stream(self, stream):
        stream.write(self.area_list[0])  # main_area
        nb_segment = UShort(len(self.segment_list))
        stream.write(nb_segment)
        for segment in self.segment_list:
            stream.write(segment)
        nb_obstacle = UShort(len(self.area_list) - 1)
        stream.write(nb_obstacle)
        for obstacle in self.area_list[1:]:
            stream.write(obstacle)

    def QPainterPath(self):
        positive = QPainterPath()
        positive.addPolygon(self.area_list[0].QPolygonF())
        positive.closeSubpath()
        for move_area in self.area_list[1:]:
            negative = QPainterPath()
            negative.addPolygon(move_area.QPolygonF())
            negative.closeSubpath()
            positive -= negative
        return positive


class Layer(RWStreamable):
    def __init__(self, total_area, sublayer_list):
        self.total_area = total_area
        self.sublayer_list = sublayer_list

    def __iter__(self):
        return iter(self.sublayer_list)

    def __getitem__(self, item):
        return self.sublayer_list[item]

    def __len__(self):
        return len(self.sublayer_list)

    @classmethod
    def from_stream(cls, stream):
        total_area = stream.read(UShort)
        # stream.debug_comment("nb total area")
        # stream.debug_new_line()

        nb_sublayer = stream.read(UShort)
        sublayer_list = [stream.read(Sublayer) for _ in range(nb_sublayer)]
        # sublayer_list = stream.read(Array, Sublayer, comment="nb sublayer")

        return cls(total_area, sublayer_list)

    def to_stream(self, stream):
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
        self.element_size = None
        self.general_link_list = None
        self.link_context_list = None

    def __iter__(self):
        return iter(self.layer_list)

    def __getitem__(self, item):
        return self.layer_list[item]

    def __len__(self):
        return len(self.layer_list)

    def _load(self, stream, only_areas=False):
        self.load_areas(stream)
        self.loaded_areas = True
        if only_areas is False:
            self.load_pathfinder(stream)
            self. loaded_pathfinder = True

    def load_areas(self, stream):
        version = stream.read(Version)
        assert version == 1

        # part 1 : movable areas and obstacles
        nb_layer = stream.read(UShort)
        self.layer_list = [stream.read(Layer) for _ in range(nb_layer)]

    def load_pathfinder(self, stream):
        # part 2 : pathfinder
        nb_pathfinder = stream.read(UShort)  # this number appears several times in the section
        # self.w = [[stream.read(UInt), stream.read(UInt)] for _ in range(nb_pathfinder)]
        self.element_size = [[stream.read(UFloat), stream.read(UFloat)] for _ in range(nb_pathfinder)]

        # part 2.1 : crossing points
        nb_layer = stream.read(UShort)
        assert nb_layer == len(self.layer_list)
        for layer in self:
            nb_sublayer = stream.read(UShort)
            assert nb_sublayer == len(layer)
            for sublayer in layer:
                nb_area = stream.read(UShort)
                assert nb_area == len(sublayer)
                for area in sublayer:
                    nb_crossing_point = stream.read(UShort)
                    area.crossing_point_list = [stream.read(CrossingPoint, nb_w=len(self.element_size)) for _ in range(nb_crossing_point)]

        # part 2.2 : path links
        max_index = max([max(cp.global_path_link_index_list) if len(cp.global_path_link_index_list) > 0 else 0
                         for layer in self
                         for sublayer in layer
                         for area in sublayer
                         for cp in area
                         ])
        nb_path_link = stream.read(UShort)
        assert nb_path_link == max_index + 1
        self.general_link_list = [stream.read(PathLink, nb_w=len(self.element_size)) for _ in range(nb_path_link)]
        for layer in self:
            for sublayer in layer:
                for area in sublayer:
                    for cp in area:
                        cp.path_link_list = [self.general_link_list[index] for index in
                                             cp.global_path_link_index_list]
        for path_link in self.general_link_list:
            i1, j1, k1, l1 = path_link.indexes1
            path_link.point1 = self[i1][j1][k1][l1]
            assert path_link not in iter(path_link.point1)
            i2, j2, k2, l2 = path_link.indexes2
            path_link.point2 = self[i2][j2][k2][l2]
            assert path_link in iter(path_link.point2)

        # part 2.3 : unknown last object
        max_index = max([max(path_link.global_unk_obj_index_list)
                         for path_link in self.general_link_list
                         ])
        nb_unk_obj = stream.read(UShort)
        assert nb_unk_obj == max_index + 1
        self.link_context_list = [stream.read(UnkLastObject) for _ in range(nb_unk_obj)]
        for path_link in self.general_link_list:
            path_link.unk_obj = [self.link_context_list[index] for index in path_link.global_unk_obj_index_list]

    def _save(self, substream):
        substream.write(Version(1))
        nb_layer = UShort(len(self))
        substream.write(nb_layer)
        for layer in self:
            substream.write(layer)

        nb_w = UShort(len(self.element_size))
        substream.write(nb_w)
        for element in self.element_size:
            substream.write(element[0])
            substream.write(element[1])
        substream.write(nb_layer)
        for layer in self:
            nb_sublayer = UShort(len(layer))
            substream.write(nb_sublayer)
            for sublayer in layer:
                nb_area = UShort(len(sublayer))
                substream.write(nb_area)
                for area in sublayer:
                    nb_crossing_point = UShort(len(area))
                    substream.write(nb_crossing_point)
                    for crossing_point in area:
                        substream.write(crossing_point)

        nb_path_link = UShort(len(self.general_link_list))
        substream.write(nb_path_link)
        for path_link in self.general_link_list:
            substream.write(path_link)
        nb_unk_obj = UShort(len(self.link_context_list))
        substream.write(nb_unk_obj)
        for unk_obj in self.link_context_list:
            substream.write(unk_obj)

    def get_ff_index(self):
        for i, uo in enumerate(self.link_context_list):
            if uo.is_ff():
                return i

