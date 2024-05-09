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
        self.unk_tab1 = unk_tab1
        self.unk_tab2 = unk_tab2

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
        if self.unk_tab1 == [] and self.unk_tab2 == []:
            stream.write(UChar(255))
        else:
            u1 = UChar(reduce(lambda x, y: x | y, self.unk_tab1))
            stream.write(u1)
            u2 = UChar(reduce(lambda x, y: x | y, self.unk_tab2))
            stream.write(u2)
            n1 = UShort(len(self.unk_tab1))
            stream.write(n1)
            for u in self.unk_tab1:
                stream.write(u)
            n2 = UShort(len(self.unk_tab2))
            stream.write(n2)
            for u in self.unk_tab2:
                stream.write(u)



class PathLink(RWStreamable):

    def __init__(self, indexes1, point1, indexes2, point2, unk_int, global_unk_obj_index_list, unk_obj_list):
        self.indexes1 = indexes1
        self.point1 = point1
        self.indexes2 = indexes2
        self.point2 = point2
        self.unk_int = unk_int
        self.global_unk_obj_index_list = global_unk_obj_index_list
        self.unk_obj_list = unk_obj_list

    def get_other(self, indexes):
        if indexes == self.indexes1:
            return self.indexes2
        elif indexes == self.indexes2:
            return self.indexes1
        else:
            raise IndexError(f"Link has no {indexes}")

    @classmethod
    def from_stream(cls, stream, *, w=None):
        indexes1 = tuple(stream.read(UShort) for _ in range(4))
        indexes2 = tuple(stream.read(UShort) for _ in range(4))
        unk_int = stream.read(UInt)
        # last bytes of unk_int is in [0, 63, 64, 65, 66, 67, 68, 69]
        nb_unk_obj = stream.read(UShort)  # w again
        assert w is None or w == nb_unk_obj
        global_unk_obj_index_list = [stream.read(UShort) for _ in range(nb_unk_obj)]
        return cls(indexes1, None, indexes2, None, unk_int, global_unk_obj_index_list, [])

    def to_stream(self, stream):
        for index1 in self.indexes1:
            stream.write(index1)
        for index2 in self.indexes2:
            stream.write(index2)
        stream.write(self.unk_int)
        unk_obj_index_list_length = UShort(len(self.global_unk_obj_index_list))
        stream.write(unk_obj_index_list_length)
        for unk_obj_index in self.global_unk_obj_index_list:
            stream.write(unk_obj_index)

    def QLineF(self):
        p1 = self.point1.QPointF()
        p2 = self.point2.QPointF()
        return QLineF(p1, p2)


class CrossingPoint(RWStreamable):

    def __init__(self, unk_char, point, unk_short, global_link_path_index_list, path_link_list):
        self.unk_char = unk_char
        self.point = point
        self.unk_short = unk_short  # 4 length tab
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
    def from_stream(cls, stream, *, w=None):
        nb_bytes = stream.read(UShort)  # w again
        assert w is None or w == nb_bytes
        unk_char = [stream.read(UChar) for _ in range(nb_bytes)]
        for byte in unk_char:
            assert byte in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # never 15

        point = stream.read(Coordinate)
        # read as 8 UChar (hypothetical)
        # b1 = [stream.read(UChar) for _ in range(8)]
        # 00000 or 11111 on 5 first bits
        # flags ? on the 3 last bits
        # 0    00000000
        # 1    00000001
        # 2    00000010
        # 3    00000011
        # 4    00000100
        # 5    ________  never appear in official level
        # 6    00000110
        # 7    00000111

        # 248  11111000
        # 249  11111001
        # 250  11111010
        # 251  11111011
        # 252  11111100
        # 253  11111101
        # 254  11111110
        # 255  11111111
        # assert b1[1] in [0, 1, 2, 3, 4,    6, 7,       248,      250, 251, 252, 253, 254, 255]
        # assert b1[3] in [0, 1, 2, 3,       6,               249, 250, 251, 252, 253, 254, 255]
        # assert b1[5] in [0, 1, 2, 3, 4,    6, 7,       248,      250, 251, 252, 253, 254, 255]
        # assert b1[7] in [0, 1, 2, 3,       6,               249, 250, 251, 252, 253, 254, 255]

        # read as 4 UShort (same as decompiler)
        unk_short = [stream.read(UShort) for _ in range(4)]

        nb_link_path = stream.read(UShort)
        global_link_path_index_list = [stream.read(UShort) for _ in range(nb_link_path)]
        return cls(unk_char, point, unk_short, global_link_path_index_list, [])

    def to_stream(self, stream):
        nb_bytes = UShort(len(self.unk_char))  # w
        stream.write(nb_bytes)
        for char in self.unk_char:
            stream.write(char)
        stream.write(self.point)
        for short in self.unk_short:
            stream.write(short)
        nb_link_path = UShort(len(self.global_path_link_index_list))
        stream.write(nb_link_path)
        for path_link_index in self.global_path_link_index_list:
            stream.write(path_link_index)



    def QPointF(self):
        return QPointF(self.point.x + 0.5, self.point.y + 0.5)


class MoveArea(RWStreamable):
    def __init__(self, area, crossing_point_list=None, main=False):
        self.area = area
        if crossing_point_list is None:
            self.crossing_point_list = []
        else:
            self.crossing_point_list = crossing_point_list
        self.main = main

    def is_main(self):
        return self.main

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

    def QPolygonF(self):
        return QPolygonF([QPointF(p.x + 0.5, p.y + 0.5) for p in self.area.coor_list])


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

    def __iter__(self):
        return iter(self.layer_list)

    def __getitem__(self, item):
        return self.layer_list[item]

    def __len__(self):
        return len(self.layer_list)

    def _load(self, stream):
        version = stream.read(Version)
        assert version == 1

        # part 1 : movable areas and obstacles
        nb_layer = stream.read(UShort)
        self.layer_list = [stream.read(Layer) for _ in range(nb_layer)]

        # part 2 : pathfinder
        self.w = stream.read(UShort)  # this number appears several times in the section
        self.w_list = [stream.read(UInt) for _ in range(2 * self.w)]

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
                    area.crossing_point_list = [stream.read(CrossingPoint, w=self.w) for _ in range(nb_crossing_point)]

        # part 2.2 : path links
        max_index = max([max(cp.global_path_link_index_list) if len(cp.global_path_link_index_list) > 0 else 0
                         for layer in self
                         for sublayer in layer
                         for area in sublayer
                         for cp in area
                         ])
        nb_path_link = stream.read(UShort)
        assert nb_path_link == max_index + 1
        self.global_path_link_list = [stream.read(PathLink, w=self.w) for _ in range(nb_path_link)]
        for layer in self:
            for sublayer in layer:
                for area in sublayer:
                    for cp in area:
                        cp.path_link_list = [self.global_path_link_list[index] for index in cp.global_path_link_index_list]
        for path_link in self.global_path_link_list:
            i1, j1, k1, l1 = path_link.indexes1
            path_link.point1 = self[i1][j1][k1][l1]
            assert path_link not in iter(path_link.point1)
            i2, j2, k2, l2 = path_link.indexes2
            path_link.point2 = self[i2][j2][k2][l2]
            assert path_link in iter(path_link.point2)

        # part 2.3 : unknown last object
        max_index = max([max(path_link.global_unk_obj_index_list)
                         for path_link in self.global_path_link_list
                         ])
        self.nb_unk_obj = stream.read(UShort)
        assert self.nb_unk_obj == max_index + 1
        self.global_unk_obj_list = [stream.read(UnkLastObject) for _ in range(self.nb_unk_obj)]
        for path_link in self.global_path_link_list:
            path_link.unk_obj_list = [self.global_unk_obj_list[index] for index in path_link.global_unk_obj_index_list]

    def _save(self, substream):
        substream.write(Version(1))
        nb_layer = UShort(len(self))
        substream.write(nb_layer)
        for layer in self:
            substream.write(layer)
        substream.write(self.w)
        for element in self.w_list:
            substream.write(element)
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
        nb_path_link = UShort(len(self.global_path_link_list))
        substream.write(nb_path_link)
        for path_link in self.global_path_link_list:
            substream.write(path_link)
        nb_unk_obj = UShort(len(self.global_unk_obj_list))
        substream.write(nb_unk_obj)
        for unk_obj in self.global_unk_obj_list:
            substream.write(unk_obj)




    def print(self, file=sys.stdout):
        for i, layer in enumerate(self.layer_list):
            print(f"Layer {i}", file=file)
            print(f"  total_area={layer.total_area}", file=file)
            for j, sublayer in enumerate(layer):
                print(f"  Sublayer {j}", file=file)
                print(f"    nb_point_in_main_area={len(sublayer.area_list[0])}", file=file)
                print(f"    nb_segment={len(sublayer.segment_list)}", file=file)
                print(f"    nb_excluded_area={len(sublayer.area_list[1:])}", file=file)
                for excluded_area in sublayer[1:]:
                    print(f"      nb_point_in_excluded_area = {len(excluded_area)}", file=file)

    def get_path_link(self, index):
        return self.global_path_link_list[index]
