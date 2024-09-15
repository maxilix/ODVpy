from functools import reduce
from typing import Self, Any

from common import *
from odv.odv_object import OdvRoot, OdvObject, OdvLeaf
from odv.pathfinder import PathFinder
from .section import Section





#
# class Viability(RWStreamable):
#     t1: list[int]
#     t2: list[int]
#
#     def is_empty(self) -> bool:
#         assert len(self.t1) == len(self.t2)
#         return self.t1 == []
#
#     @classmethod
#     def from_stream(cls, stream: ReadStream):
#         rop = cls()
#         end_reduced = stream.read(UChar)
#         if end_reduced == 255:
#             # 0xff is read
#             # the corresponding link is totally unavailable
#             rop.t2 = []
#             rop.t1 = []
#         else:
#             start_reduced = stream.read(UChar)
#             n = stream.read(UShort)
#             rop.t2 = [stream.read(UChar) for _ in range(n)]
#             n = stream.read(UShort)  # must be same n
#             rop.t1 = [stream.read(UChar) for _ in range(n)]
#
#         return rop
#
#     def to_stream(self, stream: WriteStream) -> None:
#         if self.is_empty():
#             stream.write(UChar(255))
#         else:
#             t2_reduced = reduce(lambda x, y: x | y, self.t2)
#             stream.write(UChar(t2_reduced))
#
#             t1_reduced = reduce(lambda x, y: x | y, self.t1)
#             stream.write(UChar(t1_reduced))
#
#             n = len(self.t2)
#
#             stream.write(UShort(n))
#             for e in self.t2:
#                 stream.write(UChar(e))
#
#             stream.write(UShort(n))
#             for e in self.t1:
#                 stream.write(UChar(e))
#
#
# class Link(RWStreamable):
#
#     def __init__(self,
#                  pathfinders: Any,  # should be a PathFinders
#                  cp1_indexes: (UShort | int, UShort | int, UShort | int, UShort | int),
#                  cp2_indexes: (UShort | int, UShort | int, UShort | int, UShort | int),
#                  length: Float,
#                  viability_index_list: [UShort | int]):
#         self._pathfinders = pathfinders
#         self.cp1_indexes = cp1_indexes
#         self.cp1 = self._pathfinders.get_crossing_point(self.cp1_indexes)
#         self.cp2_indexes = cp2_indexes
#         self.cp2 = self._pathfinders.get_crossing_point(self.cp2_indexes)
#         self.length = length
#         self.viability_index_list = viability_index_list
#
#     @classmethod
#     def from_stream(cls, stream, *, pathfinders):
#         indexes2 = tuple(stream.read(UShort) for _ in range(4))
#         indexes1 = tuple(stream.read(UShort) for _ in range(4))
#         length = stream.read(Float)
#         nb_pathfinder = stream.read(UShort)
#         viability_index_list = [stream.read(UShort) for _ in range(nb_pathfinder)]
#         return cls(pathfinders, indexes1, indexes2, length, viability_index_list)
#
#     def to_stream(self, stream):
#         for index in self.cp2_indexes:
#             stream.write(UShort(index))
#         for index in self.cp1_indexes:
#             stream.write(UShort(index))
#         stream.write(Float(self.length))
#         nb_pathfinder = len(self.viability_index_list)
#         stream.write(UShort(nb_pathfinder))
#         for viability_index in self.viability_index_list:
#             stream.write(UShort(viability_index))
#
#
#
#
# class CrossingPoint(RWStreamable):
#
#     def __init__(self,
#                  pathfinders: Any,  # should be a PathFinders
#                  accesses: [UChar | int],
#                  point: Point,
#                  vector_to_next: Point,
#                  vector_from_previous: Point,
#                  link_index_list: [UShort | int]):
#         self._pathfinders = pathfinders
#         self.accesses = accesses
#         self.point = point
#         self.vector_to_next = vector_to_next
#         self.vector_from_previous = vector_from_previous
#         self.link_index_list = link_index_list
#
#     @classmethod
#     def from_stream(cls, stream, *, pathfinders):
#         nb_pathfinder = stream.read(UShort)
#         accesses = [stream.read(UChar) for _ in range(nb_pathfinder)]
#         # each access (in accesses) define if obstacles are present around the point
#         # X=0 if obstacle is presente in the quarter
#         # X=1 if no obstacle in the quarter
#         #
#         #    NW      |      NE
#         #      ___X  |  __X_
#         #     _______|_______
#         #            |
#         #      X___  |  _X__
#         #    SW      |      SE
#         #
#         # notes:
#         #   4 msb are always zero
#         #   0x0f = 0b00001111 cannot be possible
#
#         point = stream.read(Point)
#
#         vector_to_next = stream.read(Point)
#         vector_from_previous = stream.read(Point)
#
#         nb_link = stream.read(UShort)
#         link_index_list = [stream.read(UShort) for _ in range(nb_link)]
#         return cls(pathfinders, accesses, point, vector_to_next, vector_from_previous, link_index_list)
#
#     def to_stream(self, stream):
#         nb_pathfinder = UShort(len(self.accesses))  # w
#         stream.write(nb_pathfinder)
#         for access in self.accesses:
#             stream.write(UChar(access))
#         stream.write(self.point)
#         stream.write(self.vector_to_next)
#         stream.write(self.vector_from_previous)
#
#         nb_link = UShort(len(self.link_index_list))
#         stream.write(nb_link)
#         for link_index in self.link_index_list:
#             stream.write(UShort(link_index))
#
#
# class PathFinder(RWStreamable):
#
#     def __init__(self, motion, size_list, crossing_point_list, link_list, viability_list):
#         self._motion = motion
#         self.size_list = size_list
#         self.crossing_point_list = crossing_point_list
#         self.link_list = link_list
#         self.viability_list = viability_list
#
#     def __len__(self):
#         return len(self.size_list)
#
#     def get_crossing_point(self, indexes):
#         assert len(indexes) == 4
#         return self.crossing_point_list[indexes[0]][indexes[1]][indexes[2]][indexes[3]]
#
#     def get_link(self, index):
#         return self.link_list[index]
#
#     def get_viability(self, index):
#         return self.viability_list[index]
#
#     @classmethod
#     def from_stream(cls, stream: ReadStream, *, move: Any):
#         rop = cls(move, [], [], [], [])
#
#         nb_pathfinder = stream.read(UShort)
#         rop.size_list = [[stream.read(Float), stream.read(Float)] for _ in range(nb_pathfinder)]
#
#         # part 1 : crossing points
#         nb_layer = stream.read(UShort)
#         rop.crossing_point_list = []
#
#         for layer_index in range(nb_layer):
#             rop.crossing_point_list.append([])
#             nb_sublayer = stream.read(UShort)
#             for sublayer_index in range(nb_sublayer):
#                 rop.crossing_point_list[layer_index].append([])
#                 nb_area = stream.read(UShort)
#                 for area_index in range(nb_area):
#                     rop.crossing_point_list[layer_index][sublayer_index].append([])
#                     nb_crossing_point = stream.read(UShort)
#                     for crossing_point_index in range(nb_crossing_point):
#                         rop.crossing_point_list[layer_index][sublayer_index][area_index].append(
#                             stream.read(CrossingPoint, pathfinders=rop))
#
#         # part 2 : path links
#         nb_path_link = stream.read(UShort)
#         rop.link_list = [stream.read(Link, pathfinders=rop) for _ in range(nb_path_link)]
#
#         # part 3 : link viability
#         nb_link_viability = stream.read(UShort)
#         rop.viability_list = [stream.read(Viability) for _ in range(nb_link_viability)]
#
#         # return cls(element_size_list, crossing_point_list, path_link_list, link_viability_list)
#         return rop
#
#     def to_stream(self, substream: WriteStream):
#         nb_pathfinder = len(self.size_list)
#         substream.write(UShort(nb_pathfinder))
#         for size in self.size_list:
#             substream.write(Float(size[0]))
#             substream.write(Float(size[1]))
#
#         nb_layer = len(self.crossing_point_list)
#         substream.write(UShort(nb_layer))
#         for cp_layer in self.crossing_point_list:
#             nb_sublayer = len(cp_layer)
#             substream.write(UShort(nb_sublayer))
#             for cp_sublayer in cp_layer:
#                 nb_area = len(cp_sublayer)
#                 substream.write(UShort(nb_area))
#                 for cp_area in cp_sublayer:
#                     nb_crossing_point = len(cp_area)
#                     substream.write(UShort(nb_crossing_point))
#                     for crossing_point in cp_area:
#                         substream.write(crossing_point)
#
#         nb_link = len(self.link_list)
#         substream.write(UShort(nb_link))
#         for link in self.link_list:
#             substream.write(link)
#
#         nb_viability = len(self.viability_list)
#         substream.write(UShort(nb_viability))
#         for viability in self.viability_list:
#             substream.write(viability)
#
#
#
#
#
#
#






class Obstacle(OdvLeaf):
    poly: Polygon

    def __str__(self):
        return f"Obstacle {self.parent.main_area_id + self.i + 1}"

    # @property
    # def poly(self) -> Polygon:
    #     return self._poly
    #
    # @poly.setter
    # def poly(self, poly: Polygon):
    #     # check if poly is clockwise
    #     if poly.signed_area() <= 0:
    #         # clockwise
    #         self._poly = poly
    #     else:
    #         # counter-clockwise
    #         self._poly = Polygon(poly[::-1])

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent):
        rop = cls(parent)
        rop.poly = stream.read(Polygon)
        return rop

    def to_stream(self, stream: WriteStream):
        stream.write(self.poly)


class MainArea(OdvObject):
    poly: Polygon

    def __str__(self):
        return f"Main area {self.main_area_id}"

    @property
    def main_area_id(self):
        rop = 0
        for layer_index in range(self.parent.i):
            rop += self.parent.parent[layer_index].total_area()
        for mainArea_index in range(self.i):
            rop += 1 + len(self.parent[mainArea_index])
        return rop

    # @property
    # def poly(self) -> Polygon:
    #     return self._poly
    #
    # @poly.setter
    # def poly(self, poly: Polygon):
    #     # check if poly is clockwise
    #     if poly.signed_area() <= 0:
    #         # clockwise
    #         self._poly = poly
    #     else:
    #         # counter-clockwise
    #         self._poly = Polygon(poly[::-1])

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent) -> Self:
        rop = cls(parent)
        rop.poly = stream.read(Polygon)
        nb_segment = stream.read(UShort)
        segment_list = [stream.read(Line) for _ in range(nb_segment)]
        nb_obstacle = stream.read(UShort)
        for _ in range(nb_obstacle):
            rop.add_child(stream.read(Obstacle, parent=rop))
        return rop

    def to_stream(self, substream: WriteStream) -> None:
        substream.write(self.poly)

        substream.write(UShort(0))  # always write zero segments
        # nb_segment = len(self.segment_list)
        # substream.write(UShort(nb_segment))
        # for segment in self.segment_list:
        #     substream.write(segment)

        nb_obstacle = len(self)
        substream.write(UShort(nb_obstacle))
        for obstacle in self:
            substream.write(obstacle)

    # @property
    # def path(self):
    #     if self._path is None:
    #         self._path = QPainterPath()
    #         self._path.addPolygon(self.main.poly)
    #         self._path.closeSubpath()
    #         for obstacle in self.obstacles:
    #             negative = QPainterPath()
    #             negative.addPolygon(obstacle.poly)
    #             negative.closeSubpath()
    #             self._path -= negative
    #     return self._path

    # @timeit
    # def contains(self, poly: Polygon) -> bool:
    #     poly_area = poly.area()
    #     inter = self.poly.intersected(poly)
    #     inter_area = inter.area()
    #     if (poly_area - inter_area) <= 0.1:
    #         # poly is in main
    #         for obstacle in self :
    #             inter = obstacle.poly.intersected(poly)
    #             if inter.isEmpty():
    #                 continue
    #             inter_area = inter.area()
    #             if inter_area > 0.1:
    #                 # obstacle intersects poly
    #                 return False
    #         return True
    #     else:
    #         return False


class Layer(OdvObject):

    def total_area(self) -> int:
        return sum([(len(main_area) + 1) for main_area in self])

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent) -> Self:
        rop = cls(parent)
        # total_area is rebuilt on demand
        total_area = stream.read(UShort)
        nb_main_area = stream.read(UShort)
        for _ in range(nb_main_area):
            rop.add_child(stream.read(MainArea, parent=rop))
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(UShort(self.total_area()))
        nb_main_area = len(self)
        stream.write(UShort(nb_main_area))
        for main_area in self:
            stream.write(main_area)


class Move(Section, OdvRoot):
    _section_name = "MOVE"
    _section_version = 1

    def main_area(self, index: int):
        i = 0
        while (ta_i := self[i].total_area()) <= index:
            i += 1
            index -= ta_i
        j = 0
        while (ta_j := (1 + len(self[i][j]))) <= index:
            j += 1
            index -= ta_j
        assert index == 0
        rop = self[i][j]
        return rop

    def main_area_iterator(self, *, include_None):
        class MAI:
            def __iter__(subself):
                if include_None:
                    return iter([None] + [ma for layer in self for ma in layer])
                else:
                    return iter(ma for layer in self for ma in layer)
            def __getitem__(self, item):
                return list(iter(self))[item]
            def __len__(self):
                return len(list(iter(self)))
        return MAI()

    def _load(self, substream: ReadStream) -> None:
        nb_layer = substream.read(UShort)
        for _ in range(nb_layer):
            self.add_child(substream.read(Layer, parent=self))
        self.pathfinder = substream.read(PathFinder, move=self)

    def _save(self, substream: WriteStream) -> None:
        nb_layer = len(self)
        substream.write(UShort(nb_layer))
        for layer in self:
            substream.write(layer)

        # self.pathfinder.rebuild()
        substream.write(self.pathfinder)
