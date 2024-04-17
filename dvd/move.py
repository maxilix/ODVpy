import sys

from PyQt6.QtCore import QPointF, QPoint, QLineF
from PyQt6.QtGui import QPolygonF, QPainterPath

from common import *

from .section import Section, section_list


class PathLink(RWStreamable):

    def __init__(self, indexes_1, indexes_2, unk, objectC_index_list):
        self.indexes_1 = indexes_1
        self.indexes_2 = indexes_2
        self.unk = unk
        self.objectC_index_list = objectC_index_list

    def get_other(self, indexes):
        if indexes == self.indexes_1:
            return self.indexes_2
        elif indexes == self.indexes_2:
            return self.indexes_1
        else:
            raise IndexError(f"Link has no {indexes}")

    @classmethod
    def from_stream(cls, stream, *, w):
        indexes_1 = tuple(stream.read(UShort) for _ in range(4))
        indexes_2 = tuple(stream.read(UShort) for _ in range(4))
        unk = stream.read(Bytes, 4)
        assert unk[3] in [0, 63, 64, 65, 66, 67, 68, 69]
        objectC_index_list_length = stream.read(UShort)  # w again
        assert objectC_index_list_length == w
        objectC_index_list = [stream.read(UShort) for _ in range(objectC_index_list_length)]
        return cls(indexes_1, indexes_2, unk, objectC_index_list)

    def QLineF(self, motion):
        i1, j1, k1, l1 = self.indexes_1
        i2, j2, k2, l2 = self.indexes_2
        p1 = motion[i1][j1][k1][l1].QPointF()
        p2 = motion[i2][j2][k2][l2].QPointF()
        return QLineF(p1, p2)


class CrossingPoint(RWStreamable):

    def __init__(self, b0, point, b1, link_path_index_list):
        self.b0 = b0
        self.point = point
        self.b1 = b1
        self.path_link_index_list = link_path_index_list

    def __iter__(self):
        return iter(self.path_link_index_list)

    def __getitem__(self, item):
        return self.path_link_index_list[item]

    def __len__(self):
        return len(self.path_link_index_list)

    @classmethod
    def from_stream(cls, stream, *, w):
        nb_bytes = stream.read(UShort)  # w again
        assert nb_bytes == w
        b0 = [stream.read(UChar) for _ in range(nb_bytes)]
        for byte in b0:
            assert byte in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]  # never 15

        coor = stream.read(Coordinate)
        b1 = [stream.read(UChar) for _ in range(8)]
        assert b1[1] in [0,1,2,3,4,6,7,248,    250,251,252,253,254,255]
        assert b1[3] in [0,1,2,3,  6,      249,250,251,252,253,254,255]
        assert b1[5] in [0,1,2,3,4,6,7,248,    250,251,252,253,254,255]
        assert b1[7] in [0,1,2,3,  6,      249,250,251,252,253,254,255]
        nb_link_path = stream.read(UShort)
        link_path_index_list = [stream.read(UShort) for _ in range(nb_link_path)]
        return cls(b0, coor, b1, link_path_index_list)

    def QPointF(self):
        return QPointF(self.point.x + 0.5, self.point.y + 0.5)


class MoveArea(object):
    def __init__(self, area, crossing_point_list=None):
        self.area = area
        if crossing_point_list is None:
            self.crossing_point_list = []
        else:
            self.crossing_point_list = crossing_point_list

    def __iter__(self):
        return iter(self.crossing_point_list)

    def __getitem__(self, item):
        return self.crossing_point_list[item]

    def __len__(self):
        return len(self.crossing_point_list)

    def set_crossing_point_list(self, crossing_point_list):
        self.crossing_point_list = crossing_point_list

    def QPolygonF(self):
        return QPolygonF([QPointF(p.x + 0.5, p.y + 0.5) for p in self.area.coor_list])


class Sublayer(RWStreamable):

    def __init__(self, area_list, segment_list):
        self.area_list = [MoveArea(area) for area in area_list]
        self.segment_list = segment_list

    def __iter__(self):
        return iter(self.area_list)

    def __getitem__(self, item):
        return self.area_list[item]

    def __len__(self):
        return len(self.area_list)

    @classmethod
    def from_stream(cls, stream):
        main_area = stream.read(Area)
        stream.debug_new_line()

        # nb_segment = stream.read(UShort)
        # stream.comment("nb segment")
        # stream.new_space()
        # segment_list = [stream.read(Segment) for _ in range(nb_segment)]
        # stream.new_line()
        segment_list = stream.read(Array, Segment, comment="nb segment")

        # nb_sub_area = stream.read(UShort)
        # stream.comment("nb sub area")
        # stream.new_line()
        # stream.indent()
        # sub_area_list = [stream.read(Area) for _ in range(nb_sub_area)]
        # stream.new_line()
        # stream.desindent()
        sub_area_list = stream.read(Array, Area, comment="nb excluded area")

        return cls([main_area] + sub_area_list, segment_list)

    def QPainterPath(self):
        positive = QPainterPath()
        positive.addPolygon(self.area_list[0].QPolygonF())
        positive.closeSubpath()
        for move_area in self.area_list[1:]:
            negative = QPainterPath()
            negative.addPolygon(move_area.QPolygonF())
            negative.closeSubpath()
            positive -= negative
        return positive  # positive.subtracted(negative)


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
        stream.debug_comment("nb total area")
        stream.debug_new_line()

        # nb_sublayer = stream.read(UShort)
        # stream.comment("nb sublayer")
        # stream.new_line()
        # stream.indent()
        # sublayer_list = [stream.read(Sublayer) for _ in range(nb_sublayer)]
        # stream.desindent()
        sublayer_list = stream.read(Array, Sublayer, comment="nb sublayer")
        # stream.new_line()
        return cls(total_area, sublayer_list)

    # def build(self, width, height):
    #     self.movable_mask = Mask(width, height, False)
    #     self.movable_mask.build()
    #     for sublayer in self.sublayer_list:
    #         self.movable_mask.allow(sublayer.allowed_area)
    #         for disallowed_area in sublayer.disallowed_area_list:
    #             self.movable_mask.disallow(disallowed_area)


class Motion(Section):
    section = section_list[2]  # MOVE

    def __iter__(self):
        return iter(self.layer_list)

    def __getitem__(self, item):
        return self.layer_list[item]

    def __len__(self):
        return len(self.layer_list)

    def _build(self):
        version = self._stream.read(Version)
        assert version == 1

        # nb_layer = self._stream.read(UShort)
        # self._stream.comment("nb layer")
        # self._stream.new_line()
        # self._stream.indent()
        # self.layer_list = [self._stream.read(Layer) for _ in range(nb_layer)]
        # self._stream.desindent()
        self.layer_list = self._stream.read(Array, Layer, comment="nb layer")

        self.w = self._stream.read(UShort)  # this number appears several times in the section
        self._stream.debug_comment("w")
        self._stream.debug_new_line()

        self._stream.read(Padding, 2)
        self.empty_flag = []
        while True:
            flag = self._stream.read(Bytes, 2)
            nb_layer = self._stream.read(UShort)
            if nb_layer == 0:
                self.empty_flag.append(flag)

                continue
            else:
                self.active_flag = flag
                assert nb_layer == len(self.layer_list)
                for layer in self:
                    nb_sublayer = self._stream.read(UShort)
                    assert nb_sublayer == len(layer)
                    for sublayer in layer:
                        nb_area = self._stream.read(UShort)
                        assert nb_area == len(sublayer)
                        for area in sublayer:
                            nb_crossing_point = self._stream.read(UShort)
                            crossing_point_list = [self._stream.read(CrossingPoint, w=self.w) for _ in range(nb_crossing_point)]
                            area.set_crossing_point_list(crossing_point_list)
                break

        max_index = max([max(cp.path_link_index_list) if len(cp.path_link_index_list) > 0 else 0
                         for layer in self
                         for sublayer in layer
                         for area in sublayer
                         for cp in area
                         ])
        nb_path_link = self._stream.read(UShort)
        assert nb_path_link == max_index + 1
        self.path_link_list = [self._stream.read(PathLink, w=self.w) for _ in range(nb_path_link)]

        max_index = max([max(path_link.objectC_index_list)
                         for path_link in self.path_link_list
                         ])
        nb_objectD = self._stream.read(UShort)
        assert nb_objectD == max_index + 1
        # print(f"{nb_objectD=}")
        self.before_ff = []
        self.ff_index = 0
        while True:
            temp = self._stream.read(Bytes, 1)
            if not temp:
                raise Exception("unable to find FF in the last part")
            if temp != b'\xff':
                self.before_ff.append(temp)
                self.ff_index += 1
            else:
                break
        # print(f"{len(self.before_ff)=}")
        self.tail = self._stream.read_raw()  # must read list of objectD TODO
        # print(f"{len(tail)=}")
        # for byte in tail:
        #     assert byte in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]  # never 15
        # proportion = [round(tail.count(i)/len(tail),4) for i in range(15)]
        # print(proportion)

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

    def get_ObjectA(self, indexes):
        return self.layer_list[indexes[0]].sublayer_list[indexes[1]].crossing_point_list_list[indexes[2]][indexes[3]]

    def get_path_link(self, index):
        return self.path_link_list[index]
