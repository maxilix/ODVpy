import time
from functools import reduce
from math import acos, pi
from typing import Any

from PyQt6.QtCore import QLineF, QPointF, QRectF, QSize
from PyQt6.QtGui import QPainterPath, QPolygonF, QPolygon

from common import *
from debug import timeit, T

""" length stats
Percentage of links smaller than the length L in original levels

L =  50 -> 18.9%
L = 100 -> 33.5%
L = 200 -> 53.1%
L = 300 -> 67.9%
L = 400 -> 77.3%
L = 500 -> 84.1%
L = 600 -> 88.6%
L = 700 -> 92.0%
L = 800 -> 94.2%

  0% -> L =    0.0
  1% -> L =    5.8
  2% -> L =    8.5
  3% -> L =   11.4
  4% -> L =   14.1
  5% -> L =   16.4
  6% -> L =   18.4
  7% -> L =   21.0
  8% -> L =   23.3
  9% -> L =   25.5
 10% -> L =   28.1
 11% -> L =   30.5
 12% -> L =   32.7
 13% -> L =   35.3
 14% -> L =   37.7
 15% -> L =   40.2
 16% -> L =   42.6
 17% -> L =   45.1
 18% -> L =   47.6
 19% -> L =   50.2
 20% -> L =   52.6
 21% -> L =   55.4
 22% -> L =   58.2
 23% -> L =   61.0
 24% -> L =   64.1
 25% -> L =   67.2
 26% -> L =   70.7
 27% -> L =   74.2
 28% -> L =   78.2
 29% -> L =   81.9
 30% -> L =   85.6
 31% -> L =   89.3
 32% -> L =   93.2
 33% -> L =   97.4
 34% -> L =  101.8
 35% -> L =  105.6
 36% -> L =  110.0
 37% -> L =  114.9
 38% -> L =  119.7
 39% -> L =  124.4
 40% -> L =  129.4
 41% -> L =  134.6
 42% -> L =  139.4
 43% -> L =  144.2
 44% -> L =  149.3
 45% -> L =  154.1
 46% -> L =  158.9
 47% -> L =  164.3
 48% -> L =  170.1
 49% -> L =  175.4
 50% -> L =  181.0
 51% -> L =  186.7
 52% -> L =  193.0
 53% -> L =  199.1
 54% -> L =  205.2
 55% -> L =  210.8
 56% -> L =  216.4
 57% -> L =  223.1
 58% -> L =  229.0
 59% -> L =  235.1
 60% -> L =  241.3
 61% -> L =  248.0
 62% -> L =  254.7
 63% -> L =  261.9
 64% -> L =  269.0
 65% -> L =  276.4
 66% -> L =  283.9
 67% -> L =  291.5
 68% -> L =  300.1
 69% -> L =  309.4
 70% -> L =  318.7
 71% -> L =  327.6
 72% -> L =  338.7
 73% -> L =  349.0
 74% -> L =  359.9
 75% -> L =  371.5
 76% -> L =  383.4
 77% -> L =  396.1
 78% -> L =  408.9
 79% -> L =  421.7
 80% -> L =  434.8
 81% -> L =  449.1
 82% -> L =  465.8
 83% -> L =  481.6
 84% -> L =  497.2
 85% -> L =  516.7
 86% -> L =  538.9
 87% -> L =  560.0
 88% -> L =  583.3
 89% -> L =  608.7
 90% -> L =  636.1
 91% -> L =  665.6
 92% -> L =  698.2
 93% -> L =  739.0
 94% -> L =  787.5
 95% -> L =  840.1
 96% -> L =  897.4
 97% -> L =  966.9
 98% -> L = 1073.7
 99% -> L = 1283.0
100% -> L = 2559.0 (longest link)
"""





class Viability(RWStreamable):

    def __init__(self, t1: list[UChar | int], t2: list[UChar | int]):
        self.t1 = t1
        self.t2 = t2

    def is_empty(self) -> bool:
        assert len(self.t1) == len(self.t2)
        return self.t1 == []

    @classmethod
    def from_stream(cls, stream: ReadStream):
        end_reduced = stream.read(UChar)
        if end_reduced == 255:
            # 0xff is read
            # the corresponding link is totally unavailable
            return cls([], [])
        else:
            start_reduced = stream.read(UChar)

            n = stream.read(UShort)
            t2 = [stream.read(UChar) for _ in range(n)]

            n = stream.read(UShort)  # must be same n
            t1 = [stream.read(UChar) for _ in range(n)]

            return cls(t1, t2)

    def to_stream(self, stream: WriteStream) -> None:
        if self.is_empty():
            stream.write(UChar(255))
        else:
            t2_reduced = reduce(lambda x, y: x | y, self.t2)
            stream.write(UChar(t2_reduced))

            t1_reduced = reduce(lambda x, y: x | y, self.t1)
            stream.write(UChar(t1_reduced))

            n = len(self.t2)

            stream.write(UShort(n))
            for e in self.t2:
                stream.write(UChar(e))

            stream.write(UShort(n))
            for e in self.t1:
                stream.write(UChar(e))


class Link(RWStreamable):

    def __init__(self,
                 pathfinders: Any,  # should be a PathFinders
                 cp1_indexes: (UShort | int, UShort | int, UShort | int, UShort | int),
                 cp2_indexes: (UShort | int, UShort | int, UShort | int, UShort | int),
                 length: Float,
                 viability_index_list: [UShort | int]):
        self._pathfinders = pathfinders
        self.cp1_indexes = cp1_indexes
        self.cp1 = self._pathfinders.get_crossing_point(self.cp1_indexes)
        self.cp2_indexes = cp2_indexes
        self.cp2 = self._pathfinders.get_crossing_point(self.cp2_indexes)
        self.length = length
        self.viability_index_list = viability_index_list

    @classmethod
    def from_stream(cls, stream, *, pathfinders):
        indexes2 = tuple(stream.read(UShort) for _ in range(4))
        indexes1 = tuple(stream.read(UShort) for _ in range(4))
        length = stream.read(Float)
        nb_pathfinder = stream.read(UShort)
        viability_index_list = [stream.read(UShort) for _ in range(nb_pathfinder)]
        return cls(pathfinders, indexes1, indexes2, length, viability_index_list)

    def to_stream(self, stream):
        for index in self.cp2_indexes:
            stream.write(UShort(index))
        for index in self.cp1_indexes:
            stream.write(UShort(index))
        stream.write(Float(self.length))
        nb_pathfinder = len(self.viability_index_list)
        stream.write(UShort(nb_pathfinder))
        for viability_index in self.viability_index_list:
            stream.write(UShort(viability_index))

    def potential_direction_combination(self, pf_index):
        # if self.cp2.x == self.cp1.x and self.cp2.y > self.cp1.y:
        #     # case 1
        #     start_quarts = [4, 8]
        #     end_quarts = [1, 2]
        # elif self.cp2.y == self.cp1.y and self.cp2.x > self.cp1.x:
        #     # case 2
        #     start_quarts = [2, 4]
        #     end_quarts = [1, 8]
        # elif self.cp2.x > self.cp1.x and self.cp2.y > self.cp1.y:
        #     # case 3
        #     start_quarts = [2, 8]
        #     end_quarts = [2, 8]
        # elif self.cp2.x > self.cp1.x and self.cp2.y < self.cp1.y:
        #     # case 4
        #     start_quarts = [1, 4]
        #     end_quarts = [1, 4]
        # else:
        #     return []
        # start_quarts = [q for q in start_quarts if self.cp1.accesses[pf_index] & q]
        # end_quarts = [q for q in end_quarts if self.cp2.accesses[pf_index] & q]
        # # if self.cp1.x == 860 and self.cp1.y == 534 and self.cp2.x == 896 and self.cp2.y == 700:
        # #     print(start_quarts, end_quarts, [(s, e) for s in start_quarts for e in end_quarts])
        pass

    @timeit
    def filter_combine_quarts(self, pf_index):
        combine_quarts = [(sq, eq)
                          for sq in [1, 2, 4, 8] if self.cp1.accesses[pf_index] & sq
                          for eq in [1, 2, 4, 8] if self.cp2.accesses[pf_index] & eq]
        # if pf_index == 0 and self.cp1.x == 827 and self.cp1.y == 712 and self.cp2.x == 860 and self.cp2.y == 534:
        #     print(f"{list(combine_quarts)}")
        #     exit()
        rop = []
        for sq, eq in combine_quarts:
            c1 = self.cp1.point_at(pf_index, sq)
            c2 = self.cp2.point_at(pf_index, eq)
            line = QLineF(c1, c2)

            a = line.angle()
            if a == 0:
                if sq in [1, 8] and eq in [2, 4]:
                    rop.append((line, sq, eq))
                continue
            if 0 < a < 90:
                if sq in [1, 4] and eq in [1, 4]:
                    rop.append((line, sq, eq))
                continue
            if a == 90:
                if sq in [8, 4] and eq in [1, 2]:
                    rop.append((line, sq, eq))
                continue
            if 90 < a < 180:
                if sq in [2, 8] and eq in [2, 8]:
                    rop.append((line, sq, eq))
                continue
            if a == 180:
                if sq in [2, 4] and eq in [1, 8]:
                    rop.append((line, sq, eq))
                continue
            if 180 < a < 270:
                if sq in [1, 4] and eq in [1, 4]:
                    rop.append((line, sq, eq))
                continue
            if a == 270:
                if sq in [1, 2] and eq in [4, 8]:
                    rop.append((line, sq, eq))
                continue
            if 270 < a < 360:
                if sq in [2, 8] and eq in [2, 8]:
                    rop.append((line, sq, eq))
                continue
        return rop

    @timeit
    def line_and_trace(self, pf_index, sq, eq):
        c1 = self.cp1.point_at(pf_index, sq)
        c2 = self.cp2.point_at(pf_index, eq)

        line = QLineF(c1, c2)

        # define 4 vectors to direction
        size = self._pathfinders.size_list[pf_index]
        v1 = QPointF(-size[0], -size[1])
        v2 = QPointF(size[0], -size[1])
        v4 = QPointF(size[0], size[1])
        v8 = QPointF(-size[0], size[1])

        a = line.angle()
        if a == 0:
            return line, QPolygonF([c1 + v4, c1 + v2, c2 + v1, c2 + v8])
        if 0 < a < 90:
            return line, QPolygonF([c1 + v4, c1 + v1, c2 + v1, c2 + v4])
        if a == 90:
            return line, QPolygonF([c1 + v2, c1 + v1, c2 + v8, c2 + v4])
        if 90 < a < 180:
            return line, QPolygonF([c1 + v2, c1 + v8, c2 + v8, c2 + v2])
        if a == 180:
            return line, QPolygonF([c2 + v4, c2 + v2, c1 + v1, c1 + v8])
        if 180 < a < 270:
            return line, QPolygonF([c2 + v4, c2 + v1, c1 + v1, c1 + v4])
        if a == 270:
            return line, QPolygonF([c2 + v2, c2 + v1, c1 + v8, c1 + v4])
        if 270 < a < 360:
            return line, QPolygonF([c2 + v2, c2 + v8, c1 + v8, c1 + v2])

        raise Exception("code should be inaccessible")

    @timeit
    def is_pertinent_link(self, pf_index, sq, eq) -> bool:
        c1 = self.cp1.point_at(pf_index, sq)
        c2 = self.cp2.point_at(pf_index, eq)

        line = QLineF(c1, c2)
        a = line.angle()

        p = line.angleTo(self.cp1.line_to_previous())
        n = self.cp1.line_to_next().angleTo(line)

        # if pf_index == 0 and self.cp1.x == 860 and self.cp1.y == 534 and self.cp2.x == 896 and self.cp2.y == 700:
        #     print("\n", sq, a, p, n)

        if sq == 1:
            start_condition = (0 <= a < 90 and p > 180 or 180 < a <= 270 and n > 180)
        elif sq == 2:
            start_condition = (270 <= a < 360 and p > 180 or 90 < a <= 180 and n > 180)
        elif sq == 4:
            start_condition = (180 <= a < 270 and p > 180 or 0 < a <= 90 and n > 180)
        else:  #sq == 8:
            start_condition = (90 <= a < 180 and p > 180 or (270 < a < 360 or a == 0) and n > 180)

        if start_condition is False:
            return False

        p = (line.angleTo(self.cp2.line_to_previous()) + 180) % 360
        n = (self.cp2.line_to_next().angleTo(line) + 180) % 360

        # if pf_index == 0 and self.cp1.x == 860 and self.cp1.y == 534 and self.cp2.x == 896 and self.cp2.y == 700:
        #     print("\n", eq, a, p, n)

        if eq == 1:
            end_condition = (180 <= a < 270 and p > 180 or 0 < a <= 90 and n > 180)
        elif eq == 2:
            end_condition = (90 <= a < 180 and p > 180 or (270 < a < 360 or a == 0) and n > 180)
        elif eq == 4:
            end_condition = (0 <= a < 90 and p > 180 or 180 < a <= 270 and n > 180)
        else:  #eq == 8:
            end_condition = (270 <= a < 360 and p > 180 or 90 < a <= 180 and n > 180)

        return end_condition


class CrossingPoint(RWStreamable):

    def __init__(self,
                 pathfinders: Any,  # should be a PathFinders
                 accesses: [UChar | int],
                 point: QPointF,
                 vector_to_next: QPointF,
                 vector_from_previous: QPointF,
                 link_index_list: [UShort | int]):
        self._pathfinders = pathfinders
        self.accesses = accesses
        self.point = point
        self.vector_to_next = vector_to_next
        self.vector_from_previous = vector_from_previous
        self.link_index_list = link_index_list

    @property
    def x(self):
        return self.point.x()

    @property
    def y(self):
        return self.point.y()

    @timeit
    def line_to_previous(self) -> QLineF:
        return QLineF(self.point, self.point - self.vector_from_previous)

    @timeit
    def line_to_next(self) -> QLineF:
        return QLineF(self.point, self.point + self.vector_to_next)

    @timeit
    def rebuild_accesses(self, sublayer):
        self.accesses = []
        for pf_index in range(len(self._pathfinders)):
            access = 0
            size = self._pathfinders.size_list[pf_index]

            # direction 1: NW
            r = QPolygonF(QRectF(self.x - 2 * size[0], self.y - 2 * size[1], 2 * size[0], 2 * size[1]))
            if sublayer.contains(r):
                access += 1

            # direction 2: NE
            r = QPolygonF(QRectF(self.x, self.y - 2 * size[1], 2 * size[0], 2 * size[1]))
            if sublayer.contains(r):
                access += 2

            # direction 4: SE
            r = QPolygonF(QRectF(self.x, self.y, 2 * size[0], 2 * size[1]))
            if sublayer.contains(r):
                access += 4

            # direction 8: SW
            r = QPolygonF(QRectF(self.x - 2 * size[0], self.y, 2 * size[0], 2 * size[1]))
            if sublayer.contains(r):
                access += 8

            self.accesses.append(access)

    @timeit
    def as_access(self, pf_index=None) -> bool:
        if pf_index is None:
            return sum(self.accesses) > 0
        else:
            return self.accesses[pf_index] > 0

    @timeit
    def point_at(self, pf_index, direction) -> QPointF:
        size = self._pathfinders.size_list[pf_index]
        if direction & 0b1001:
            x = self.x - size[0]
        else:
            x = self.x + size[0]
        if direction & 0b0011:
            y = self.y - size[1]
        else:
            y = self.y + size[1]
        return QPointF(x, y)

    @classmethod
    def from_stream(cls, stream, *, pathfinders):
        nb_pathfinder = stream.read(UShort)
        accesses = [stream.read(UChar) for _ in range(nb_pathfinder)]
        # each access (in accesses) define if obstacles are present around the point
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
        # notes:
        #   4 msb are always zero
        #   0x0f = 0b00001111 cannot be possible

        point = stream.read(QPointF)

        vector_to_next = stream.read(QPointF)
        vector_from_previous = stream.read(QPointF)

        nb_path_link = stream.read(UShort)
        path_link_index_list = [stream.read(UShort) for _ in range(nb_path_link)]
        return cls(pathfinders, accesses, point, vector_to_next, vector_from_previous, path_link_index_list)

    def to_stream(self, stream):
        nb_pathfinder = UShort(len(self.accesses))  # w
        stream.write(nb_pathfinder)
        for access in self.accesses:
            stream.write(UChar(access))
        stream.write(self.point)
        stream.write(self.vector_to_next)
        stream.write(self.vector_from_previous)

        nb_path_link = UShort(len(self.link_index_list))
        stream.write(nb_path_link)
        for path_link_index in self.link_index_list:
            stream.write(UShort(path_link_index))


class PathFinder(RWStreamable):
    size_list: list[tuple[float, float]] = []
    crossing_point_list: list[list[list[list[CrossingPoint]]]] = []
    link_list: list[Link] = []
    viability_list: list[Viability] = []

    # def __init__(self, motion, size_list, crossing_point_list, link_list, viability_list):
    #     self._motion = motion
    #     self.size_list = size_list
    #     self.crossing_point_list = crossing_point_list
    #     self.link_list = link_list
    #     self.viability_list = viability_list

    def __len__(self):
        return len(self.size_list)

    def get_crossing_point(self, indexes):
        assert len(indexes) == 4
        return self.crossing_point_list[indexes[0]][indexes[1]][indexes[2]][indexes[3]]

    def get_link(self, index):
        return self.link_list[index]

    def get_viability(self, index):
        return self.viability_list[index]

    @classmethod
    def from_stream(cls, stream: ReadStream):
        rop = cls()

        nb_pathfinder = stream.read(UShort)
        rop.size_list = [[stream.read(Float), stream.read(Float)] for _ in range(nb_pathfinder)]

        # part 1 : crossing points
        nb_layer = stream.read(UShort)
        rop.crossing_point_list = []

        for layer_index in range(nb_layer):
            rop.crossing_point_list.append([])
            nb_sublayer = stream.read(UShort)
            for sublayer_index in range(nb_sublayer):
                rop.crossing_point_list[layer_index].append([])
                nb_area = stream.read(UShort)
                for area_index in range(nb_area):
                    rop.crossing_point_list[layer_index][sublayer_index].append([])
                    nb_crossing_point = stream.read(UShort)
                    for crossing_point_index in range(nb_crossing_point):
                        rop.crossing_point_list[layer_index][sublayer_index][area_index].append(
                            stream.read(CrossingPoint, pathfinders=rop))

        # part 2 : path links
        nb_path_link = stream.read(UShort)
        rop.link_list = [stream.read(Link, pathfinders=rop) for _ in range(nb_path_link)]

        # part 3 : link viability
        nb_link_viability = stream.read(UShort)
        rop.viability_list = [stream.read(Viability) for _ in range(nb_link_viability)]

        # return cls(element_size_list, crossing_point_list, path_link_list, link_viability_list)
        return rop

    def to_stream(self, substream: WriteStream):
        nb_pathfinder = len(self.size_list)
        substream.write(UShort(nb_pathfinder))
        for size in self.size_list:
            substream.write(Float(size[0]))
            substream.write(Float(size[1]))

        nb_layer = len(self.crossing_point_list)
        substream.write(UShort(nb_layer))
        for cp_layer in self.crossing_point_list:
            nb_sublayer = len(cp_layer)
            substream.write(UShort(nb_sublayer))
            for cp_sublayer in cp_layer:
                nb_area = len(cp_sublayer)
                substream.write(UShort(nb_area))
                for cp_area in cp_sublayer:
                    nb_crossing_point = len(cp_area)
                    substream.write(UShort(nb_crossing_point))
                    for crossing_point in cp_area:
                        substream.write(crossing_point)

        nb_link = len(self.link_list)
        substream.write(UShort(nb_link))
        for link in self.link_list:
            substream.write(link)

        nb_viability = len(self.viability_list)
        substream.write(UShort(nb_viability))
        for viability in self.viability_list:
            substream.write(viability)

    def rebuild_v2(self, motion):
        from odv.pathfinder_generation import PathFinderFactory

        factory = PathFinderFactory(self.size_list, motion)
        factory.generate()
        self.crossing_point_list = factory.new_pathfinder.crossing_point_list.copy()
        # print([cp.point for cp in  self.crossing_point_list[0][0][103]])
        self.link_list = factory.new_pathfinder.link_list.copy()
        self.viability_list = factory.new_pathfinder.viability_list.copy()

    @timeit
    def rebuild_v1(self):


        self.rebuild_crossing_point_list()
        print(
            f"nb_cb = {sum([sum([sum([len(cp_l) for cp_l in area_l]) for area_l in sublayer_l]) for sublayer_l in self.crossing_point_list])}")

        # print(f"as = {sum([sum([sum([sum([sum(cp.accesses) for cp in cp_l]) for cp_l in area_l]) for area_l in sublayer_l]) for sublayer_l in self.crossing_point_list])}")
        # print(f"ac = {[[[[cp.accesses for cp in cp_l] for cp_l in area_l] for area_l in sublayer_l] for sublayer_l in self.crossing_point_list]}")

        self.rebuild_link_list()
        print(f"nb_link = {len(self.link_list)}")

        print("\n  times:")
        for k in T:
            print(f"{T[k]:6.2f} {k}")

    @timeit
    def rebuild_crossing_point_list(self):
        print("rebuilding crossing point list - ...", end="")
        self.crossing_point_list = []

        # define crossing point list
        for i, layer in enumerate(self._motion):
            self.crossing_point_list.append([])
            for j, main_area in enumerate(layer):
                self.crossing_point_list[i].append([])
                self.crossing_point_list[i][j].append([])
                self.rebuild_crossing_point_of(i, j, 0)
                for k, obstacle in enumerate(main_area):
                    self.crossing_point_list[i][j].append([])
                    self.rebuild_crossing_point_of(i, j, k+1)


        # define accesses for each crossing point
        for i, layer in enumerate(self._motion):
            for j, main_area in enumerate(layer):
                for cp in self.crossing_point_list[i][j][0]:
                    cp.rebuild_accesses(main_area)
                for k, obstacle in enumerate(main_area):
                    for cp in self.crossing_point_list[i][j][k+1]:
                        cp.rebuild_accesses(main_area)

        # clear inaccessible crossing point
        # for i, layer in enumerate(self._motion):
        #     for j, sublayer in enumerate(layer):
        #         for k, _ in enumerate(sublayer):
        #             self.crossing_point_list[i][j][k] = [cp for cp in self.crossing_point_list[i][j][k]
        #                                                  if cp.as_access()]
        # print("\b\b\bDone")

    @timeit
    def rebuild_crossing_point_of(self, i, j, k):
        self.crossing_point_list[i][j][k] = []

        if k == 0:  # main area
            point_list = [p for p in self._motion[i][j].poly]
            point_list.reverse()
        else:
            point_list = [p for p in self._motion[i][j][k-1].poly]

        n = len(point_list)
        for m, p in enumerate(point_list):
            theta = QLineF(p, point_list[(m - 1) % n]).angleTo(QLineF(p, point_list[(m + 1) % n]))
            if theta < 180:
                # this point is a crossing point
                self.crossing_point_list[i][j][k].append(CrossingPoint(self,
                                                                       [],
                                                                       p,
                                                                       point_list[(m + 1) % n] - p,
                                                                       p - point_list[(m - 1) % n],
                                                                       []))

    @timeit
    def rebuild_link_list(self):
        self.tl=[]
        print("rebuilding link list - 00.0%", end="")
        nb_cp = sum([sum([sum([len(cp_l) for cp_l in area_l]) for area_l in sublayer_l]) for sublayer_l in
                     self.crossing_point_list])
        i_cp = 0

        self.link_list = []
        self.viability_list = [Viability([], [])]  # 0xff at index 0

        for i, layer in enumerate(self._motion):
            for j, sublayer in enumerate(layer):
                for k1, area1 in enumerate(sublayer):
                    for l1, cp1 in enumerate(self.crossing_point_list[i][j][k1]):
                        print(f"\b\b\b\b\b{i_cp / nb_cp * 100:4.1f}%", end="")
                        i_cp += 1
                        for k2, area2 in enumerate(sublayer):
                            for l2, cp2 in enumerate(self.crossing_point_list[i][j][k2]):
                                if (cp2.x == cp1.x and cp2.y > cp1.y or
                                    cp2.y == cp1.y and cp2.x > cp1.x or
                                    cp2.x > cp1.x and cp2.y > cp1.y or
                                    cp2.x > cp1.x and cp2.y < cp1.y) is False:
                                    continue

                                link = Link(self, (i, j, k1, l1), (i, j, k2, l2), cp1.point.distance(cp2.point),
                                            [])
                                for pf_index in range(len(self)):
                                    viability = Viability([], [])
                                    # combine_quarts = link.potential_direction_combination(pf_index)
                                    # if pf_index == 0 and cp1.x == 860 and cp1.y == 534 and cp2.x == 896 and cp2.y == 700:
                                    #     print(combine_quarts)
                                    # print(cp1.accesses[0], cp2.accesses[0])
                                    # exit()

                                    combine_quarts = link.filter_combine_quarts(pf_index)
                                    # if pf_index == 0 and cp1.x == 827 and cp1.y == 712 and cp2.x == 860 and cp2.y == 534:
                                    #     print(f"{combine_quarts}")
                                    #     exit()

                                    for _, sq, eq in combine_quarts:
                                        if link.is_pertinent_link(pf_index, sq, eq):
                                            _, trace = link.line_and_trace(pf_index, sq, eq)
                                            self.tl.append((cp1.point_at(pf_index, sq), cp2.point_at(pf_index, eq)))
                                            if sublayer.contains(trace):
                                                viability.t1.append(eq)
                                                viability.t2.append(sq)

                                    if viability.is_empty() is False:
                                        self.viability_list.append(viability)
                                        link.viability_index_list.append(len(self.viability_list) - 1)
                                    else:
                                        link.viability_index_list.append(0)

                                if sum(link.viability_index_list) > 0:  # if at least one viability has been appended
                                    self.link_list.append(link)
                                    cp1.link_index_list.append(len(self.link_list) - 1)
                                    reversed_link = Link(self, link.cp2_indexes, link.cp1_indexes, link.length, [])
                                    for viability in link.viability_index_list:
                                        reversed_viability = Viability(self.viability_list[viability].t2,
                                                                       self.viability_list[viability].t1)
                                        self.viability_list.append(reversed_viability)
                                        reversed_link.viability_index_list.append(len(self.viability_list) - 1)
                                    self.link_list.append(reversed_link)
                                    cp2.link_index_list.append(len(self.link_list) - 1)
        print(f"{len(self.tl)=}")

        print("\b\b\b\b\bDone")



