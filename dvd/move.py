import sys

from PyQt6.QtCore import QPointF, QPoint, QLineF
from PyQt6.QtGui import QPolygonF, QPainterPath

from common import *

from .section import Section, section_list


class PathLink(RWStreamable):

    def __init__(self, indexes1, point1, indexes2, point2, unk, unk_obj_index_list, unk_obj_list):
        self.indexes1 = indexes1
        self.point1 = point1
        self.indexes2 = indexes2
        self.point2 = point2
        self.unk = unk
        self.unk_obj_index_list = unk_obj_index_list
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
        unk = stream.read(Bytes, 4)
        assert unk[3] in [0, 63, 64, 65, 66, 67, 68, 69]
        unk_obj_index_list_length = stream.read(UShort)  # w again
        assert w is None or w == unk_obj_index_list_length
        unk_obj_index_list = [stream.read(UShort) for _ in range(unk_obj_index_list_length)]
        return cls(indexes1, None, indexes2, None, unk, unk_obj_index_list, [])

    def QLineF(self, motion):
        i1, j1, k1, l1 = self.indexes1
        i2, j2, k2, l2 = self.indexes2
        p1 = motion[i1][j1][k1][l1].QPointF()
        p2 = motion[i2][j2][k2][l2].QPointF()
        return QLineF(p1, p2)


class CrossingPoint(RWStreamable):

    def __init__(self, b0, point, b1, link_path_index_list, path_link_list):
        self.b0 = b0
        self.point = point
        self.b1 = b1
        self.path_link_global_index_list = link_path_index_list
        self.path_link_list = path_link_list

    def __iter__(self):
        return iter(self.path_link_global_index_list)

    def __getitem__(self, item):
        return self.path_link_global_index_list[item]

    def __len__(self):
        assert (len(self.path_link_list) == len(self.path_link_global_index_list))
        return len(self.path_link_global_index_list)

    @classmethod
    def from_stream(cls, stream, *, w=None):
        nb_bytes = stream.read(UShort)  # w again
        assert w is None or w == nb_bytes
        b0 = [stream.read(UChar) for _ in range(nb_bytes)]
        for byte in b0:
            assert byte in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # never 15

        coor = stream.read(Coordinate)
        b1 = [stream.read(UChar) for _ in range(8)]
        # unknown b1
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
        assert b1[1] in [0, 1, 2, 3, 4,    6, 7,       248,      250, 251, 252, 253, 254, 255]
        assert b1[3] in [0, 1, 2, 3,       6,               249, 250, 251, 252, 253, 254, 255]
        assert b1[5] in [0, 1, 2, 3, 4,    6, 7,       248,      250, 251, 252, 253, 254, 255]
        assert b1[7] in [0, 1, 2, 3,       6,               249, 250, 251, 252, 253, 254, 255]
        nb_link_path = stream.read(UShort)
        link_path_index_list = [stream.read(UShort) for _ in range(nb_link_path)]
        return cls(b0, coor, b1, link_path_index_list, [])

    def QPointF(self):
        return QPointF(self.point.x + 0.5, self.point.y + 0.5)


class MoveArea(RWStreamable):
    def __init__(self, area, crossing_point_list):
        self.area = area
        self.crossing_point_list = crossing_point_list

    def __iter__(self):
        return iter(self.crossing_point_list)

    def __getitem__(self, item):
        return self.crossing_point_list[item]

    def __len__(self):
        return len(self.crossing_point_list)

    @classmethod
    def from_stream(cls, stream):
        move_area = stream.read(Area)
        return cls(move_area, [])

    def QPolygonF(self):
        return QPolygonF([QPointF(p.x + 0.5, p.y + 0.5) for p in self.area.coor_list])


class Sublayer(RWStreamable):

    def __init__(self, area_list, segment_list):
        self.area_list = area_list
        self.segment_list = segment_list

    def __iter__(self):
        return iter(self.area_list)

    def __getitem__(self, item):
        return self.area_list[item]

    def __len__(self):
        return len(self.area_list)

    @classmethod
    def from_stream(cls, stream):
        main_area = stream.read(MoveArea)
        # stream.debug_new_line()

        nb_segment = stream.read(UShort)
        segment_list = [stream.read(Segment) for _ in range(nb_segment)]
        # segment_list = stream.read(Array, Segment, comment="nb segment")

        nb_excluded_area = stream.read(UShort)
        excluded_area_list = [stream.read(MoveArea) for _ in range(nb_excluded_area)]
        # sub_area_list = stream.read(Array, Area, comment="nb excluded area")

        return cls([main_area] + excluded_area_list, segment_list)

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


class Motion(Section):
    section = section_list[2]  # MOVE

    def __iter__(self):
        return iter(self.layer_list)

    def __getitem__(self, item):
        return self.layer_list[item]

    def __len__(self):
        return len(self.layer_list)

    def _build(self, stream):
        version = stream.read(Version)
        assert version == 1

        nb_layer = stream.read(UShort)
        self.layer_list = [stream.read(Layer) for _ in range(nb_layer)]
        # self.layer_list = self._stream.read(Array, Layer, comment="nb layer")

        self.w = stream.read(UShort)  # this number appears several times in the section
        # self._stream.debug_comment("w")
        # self._stream.debug_new_line()

        stream.read(Padding, 2)
        self.empty_flag = []
        while True:
            flag = stream.read(Bytes, 2).hex()
            nb_layer = stream.read(UShort)
            if nb_layer == 0:
                self.empty_flag.append(flag)
                continue
            else:
                self.active_flag = flag
                assert nb_layer == len(self.layer_list)
                for layer in self:
                    nb_sublayer = stream.read(UShort)
                    assert nb_sublayer == len(layer)
                    for sublayer in layer:
                        nb_area = stream.read(UShort)
                        assert nb_area == len(sublayer)
                        for area in sublayer:
                            nb_crossing_point = stream.read(UShort)
                            area.crossing_point_list = [stream.read(CrossingPoint, w=self.w) for _ in
                                                        range(nb_crossing_point)]
                break

        max_index = max([max(cp.path_link_global_index_list) if len(cp.path_link_global_index_list) > 0 else 0
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
                        cp.path_link_list = [self.global_path_link_list[index] for index in cp.path_link_global_index_list]

        max_index = max([max(path_link.unk_obj_index_list)
                         for path_link in self.global_path_link_list
                         ])
        self.nb_unk_obj = stream.read(UShort)
        assert self.nb_unk_obj == max_index + 1
        # print(f"{nb_unk_obj=}")
        self.before_ff = []
        self.ff_index = 0
        while True:
            temp = stream.read(Bytes, 1)
            if not temp:
                raise Exception("unable to find FF in the last part")
            if temp != b'\xff':
                self.before_ff.append(temp)
                self.ff_index += 1
            else:
                break

        assert len(self.before_ff) % 8 == 0

        # print(f"{len(self.before_ff)=}")
        self.tail = stream.read_raw()  # must read list of unk_obj TODO
        assert len(self.tail) % 4 == 0
        for byte in self.tail:
            assert byte in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # never 15

        # print(f"len tail = {len(self.tail)}")

        # === stat on tail ===
        # proportion = [round(self.tail.count(i)/len(self.tail), 4) for i in range(16)]
        # print(proportion)

        # === stat on cp b0 ===
        l = [o for layer in self for sublayer in layer for area in sublayer for cp in area for o in cp.b0]
        proportion = [round(l.count(i)/len(l), 4) for i in range(16)]
        print(proportion)




        # print("motion built")

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
        return self.global_path_link_list[index]
