import time
from functools import reduce
from math import acos, pi
from typing import Any

from PyQt6.QtCore import QLineF, QPointF, QRectF, QSize
from PyQt6.QtGui import QPainterPath, QPolygonF, QPolygon

from common import *
from debug import T


class Viability(RWStreamable):

    def __init__(self, t1: list[UChar | int], t2: list[UChar | int]):
        self.t1 = t1
        self.t2 = t2

    @timeit
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

    @timeit
    def potential_direction_combination(self, pf_index):
        if self.cp2.x == self.cp1.x and self.cp2.y > self.cp1.y:
            # case 1
            start_quarts = [4, 8]
            end_quarts = [1, 2]
        elif self.cp2.y == self.cp1.y and self.cp2.x > self.cp1.x:
            # case 2
            start_quarts = [2, 4]
            end_quarts = [1, 8]
        elif self.cp2.x > self.cp1.x and self.cp2.y > self.cp1.y:
            # case 3
            start_quarts = [2, 8]
            end_quarts = [2, 8]
        elif self.cp2.x > self.cp1.x and self.cp2.y < self.cp1.y:
            # case 4
            start_quarts = [1, 4]
            end_quarts = [1, 4]
        else:
            return []
        start_quarts = [q for q in start_quarts if self.cp1.accesses[pf_index] & q]
        end_quarts = [q for q in end_quarts if self.cp2.accesses[pf_index] & q]
        return [(s, e) for s in start_quarts for e in end_quarts]

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

    # def QLineF(self):
    #     p1 = self.start_position.QPointF()
    #     p2 = self.end_position.QPointF()
    #     return QLineF(p1, p2)


class CrossingPoint(RWStreamable):

    def __init__(self,
                 pathfinders: Any,  # should be a PathFinders
                 accesses: [UChar | int],
                 position,
                 vector_to_next,
                 vector_from_previous,
                 link_index_list: [UShort | int]):
        self._pathfinders = pathfinders
        self.accesses = accesses
        self.position = position
        self.vector_to_next = vector_to_next
        self.vector_from_previous = vector_from_previous
        self.link_index_list = link_index_list

    # def __iter__(self):
    #     return iter(self.path_link_list)
    #
    # def __getitem__(self, item):
    #     return self.path_link_list[item]
    #
    # def __len__(self):
    #     # assert (len(self.path_link_list) == len(self.global_path_link_index_list))
    #     return len(self.path_link_list)

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    @timeit
    def line_to_previous(self) -> QLineF:
        point = QPointF(self.position.x, self.position.y)
        previous_point = QPointF(self.position.x - self.vector_from_previous.x,
                                 self.position.y - self.vector_from_previous.y)
        return QLineF(point, previous_point)

    @timeit
    def line_to_next(self) -> QLineF:
        point = QPointF(self.position.x, self.position.y)
        next_point = QPointF(self.position.x + self.vector_to_next.x, self.position.y + self.vector_to_next.y)
        return QLineF(point, next_point)

    @timeit
    def rebuild_accesses(self, sublayer):
        self.accesses = []
        for pf_index in range(len(self._pathfinders)):
            access = 0
            size = self._pathfinders.size_list[pf_index]

            # direction 1: NW
            r = QRectF(self.x - 2 * size[0], self.y - 2 * size[1], 2 * size[0], 2 * size[1])
            if sublayer.contains_poly(r):
                access += 1

            # direction 2: NE
            r = QRectF(self.x              , self.y - 2 * size[1], 2 * size[0], 2 * size[1])
            if sublayer.contains_poly(r):
                access += 2

            # direction 4: SE
            r = QRectF(self.x              , self.y              , 2 * size[0], 2 * size[1])
            if sublayer.contains_poly(r):
                access += 4

            # direction 8: SW
            r = QRectF(self.x - 2 * size[0], self.y              , 2 * size[0], 2 * size[1])
            if sublayer.contains_poly(r):
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
        # if real and not direction & self.accesses[pf_index]:
        #     return QPointF()
        # else:
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

        position = stream.read(Point)

        vector_to_next = stream.read(Point)
        vector_from_previous = stream.read(Point)

        nb_path_link = stream.read(UShort)
        path_link_index_list = [stream.read(UShort) for _ in range(nb_path_link)]
        return cls(pathfinders, accesses, position, vector_to_next, vector_from_previous, path_link_index_list)

    def to_stream(self, stream):
        nb_pathfinder = UShort(len(self.accesses))  # w
        stream.write(nb_pathfinder)
        for access in self.accesses:
            stream.write(UChar(access))
        stream.write(self.position)
        stream.write(self.vector_to_next)
        stream.write(self.vector_from_previous)

        nb_path_link = UShort(len(self.link_index_list))
        stream.write(nb_path_link)
        for path_link_index in self.link_index_list:
            stream.write(UShort(path_link_index))

    # def QPF(self):
    #     return QPointF(self.x, self.y)


class PathFinders(RWStreamable):

    def __init__(self, motion, size_list, crossing_point_list, link_list, viability_list):
        self._motion = motion
        self.size_list = size_list
        self.crossing_point_list = crossing_point_list
        self.link_list = link_list
        self.viability_list = viability_list

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
    def from_stream(cls, stream: ReadStream, *, motion: Any):
        rop = cls(motion, [], [], [], [])

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
            substream.write(size[0])
            substream.write(size[1])

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

    @timeit
    def rebuild(self):
        self.rebuild_crossing_point_list()
        self.rebuild_link_list()
        for k in T:
            print(f"{T[k]:6.2f} {k}")

    @timeit
    def rebuild_crossing_point_list(self):
        print("rebuilding crossing point list - ...", end="")
        self.crossing_point_list = []

        # define crossing point list
        for i, layer in enumerate(self._motion):
            self.crossing_point_list.append([])
            for j, sublayer in enumerate(layer):
                self.crossing_point_list[i].append([])
                for k, area in enumerate(sublayer):
                    self.crossing_point_list[i][j].append([])
                    self.rebuild_crossing_point_of(i, j, k)

        # define accesses for each crossing point
        for i, layer in enumerate(self._motion):
            for j, sublayer in enumerate(layer):
                for k, _ in enumerate(sublayer):
                    for cp in self.crossing_point_list[i][j][k]:
                        cp.rebuild_accesses(sublayer)

        # clear inaccessible crossing point
        for i, layer in enumerate(self._motion):
            for j, sublayer in enumerate(layer):
                for k, _ in enumerate(sublayer):
                    self.crossing_point_list[i][j][k] = [cp for cp in self.crossing_point_list[i][j][k]
                                                         if cp.as_access()]
        print("\b\b\bDone")

    @timeit
    def rebuild_crossing_point_of(self, i, j, k):
        move_area = self._motion[i][j][k]
        # TODO second implementation based on QLineF and the angle() method
        # probably more efficient, but small optimization anyway

        # Ensures that points are covered in the right order
        # i.e. if you walk on the border, the restricted area is on the right.
        move_area.clockwise = not move_area.main  # reverse the order of points if necessary

        self.crossing_point_list[i][j][k] = []
        for point_index in range(len(move_area)):
            # TODO do not add point at the limit of the sublayer
            u = move_area[point_index - 1] - move_area[point_index]  # vector to previous
            v = move_area[point_index + 1] - move_area[point_index]  # vector to next
            theta = acos((u.x * v.x + u.y * v.y) / (u.length() * v.length()))
            if u.x * v.y - u.y * v.x > 0:
                theta = 2 * pi - theta
            if theta < pi:
                # this point is a crossing point
                self.crossing_point_list[i][j][k].append(CrossingPoint(self,
                                                                       [],
                                                                       move_area[point_index],
                                                                       v,
                                                                       -u,
                                                                       []))
        move_area.clockwise = True  # engine need clockwise definition  TODO really needed ?

    # @staticmethod
    # def area(polygon: QPolygon | QPolygonF) -> float:
    #     area = 0.0
    #     n = len(polygon)
    # 
    #     for i in range(n):
    #         current_point = polygon[i]
    #         next_point = polygon[(i + 1) % n]
    #         area += (next_point.x() - current_point.x()) * (next_point.y() + current_point.y())
    # 
    #     return abs(area / 2)

    @timeit
    def rebuild_link_list(self):
        print("rebuilding link list - 00.0%", end="")
        nb_cp = sum([sum([sum([len(cp_l) for cp_l in area_l]) for area_l in sublayer_l]) for sublayer_l in self.crossing_point_list])
        i_cp = 0

        self.link_list = []
        self.viability_list = [Viability([], [])]  # 0xff at index 0

        for i, layer in enumerate(self._motion):
            for j, sublayer in enumerate(layer):
                for k1, area1 in enumerate(sublayer):
                    for l1, cp1 in enumerate(self.crossing_point_list[i][j][k1]):
                        print(f"\b\b\b\b\b{i_cp/nb_cp*100:4.1f}%", end="")
                        i_cp += 1
                        for k2, area2 in enumerate(sublayer):
                            for l2, cp2 in enumerate(self.crossing_point_list[i][j][k2]):
                                link = Link(self, (i, j, k1, l1), (i, j, k2, l2), cp1.position.distance(cp2.position),
                                            [])
                                for pf_index in range(len(self)):
                                    viability = Viability([], [])
                                    combine_quarts = link.potential_direction_combination(pf_index)
                                    # if cp1.x == 860 and cp1.y == 534 and cp2.x == 941 and cp2.y == 513:
                                    #     print(combine_quarts)
                                    #     exit()

                                    for sq, eq in combine_quarts:
                                        line, trace = link.line_and_trace(pf_index, sq, eq)
                                        # if cp1.x == 860 and cp1.y == 534 and cp2.x == 941 and cp2.y == 513:
                                        #     print(sublayer.contains_poly(trace))


                                        if sublayer.contains_poly(trace):
                                            angle1_with_previous = line.angleTo(cp1.line_to_previous())
                                            angle1_with_next = cp1.line_to_next().angleTo(line)
                                            angle2_with_previous = line.angleTo(cp2.line_to_previous())
                                            angle2_with_next = cp2.line_to_next().angleTo(line)
                                            # if cp1.x == 860 and cp1.y == 534 and cp2.x == 941 and cp2.y == 513:
                                            #     print(f"to {cp2.x} {cp2.y}, {angle1_with_previous}, {angle1_with_next}, {angle2_with_previous}, {angle2_with_next}")
                                            #     exit()

                                            if (angle1_with_previous > 180 or angle1_with_next > 180) and (
                                                    angle2_with_previous < 180 or angle2_with_next < 180):
                                                viability.t1.append(sq)
                                                viability.t2.append(eq)

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
        print("\b\b\b\b\bDone")


    # @staticmethod
    # def is_line_strictly_in_sublayer(line: QLineF, sublayer) -> bool:
    #     center = line.center()
    #     if not sublayer.allow_path.contains(center):
    #         # print(f"c {center.x():8.3f} {center.y():8.3f}   ", end="")
    #         return False
    # 
    #     for bound in sublayer.boundaries:
    #         # if line == bound or line.p1() == bound.p2() and line.p2() == bound.p1():
    #         #     return True
    #         if (i := bound.intersects(line))[0] == QLineF.IntersectionType.BoundedIntersection:
    #             if i[1] != line.p1() and i[1] != line.p2():
    #                 # print(f"i {i[1].x():8.3f} {i[1].y():8.3f}   ", end="")
    #                 return False
    #         # else:
    #         #     print(i[0])
    #     return True

    # @staticmethod
    # def quarts_definition(pf_index, cp1, cp2):
    #     if cp2.position.x == cp1.position.x and cp2.position.y > cp1.position.y:
    #         # case 1
    #         start_quarts = [4, 8]
    #         end_quarts = [1, 2]
    #     elif cp2.position.y == cp1.position.y and cp2.position.x > cp1.position.x:
    #         # case 2
    #         start_quarts = [2, 4]
    #         end_quarts = [1, 8]
    #     elif cp2.position.x > cp1.position.x and cp2.position.y > cp1.position.y:
    #         # case 3
    #         start_quarts = [2, 8]
    #         end_quarts = [2, 8]
    #     elif cp2.position.x > cp1.position.x and cp2.position.y < cp1.position.y:
    #         # case 4
    #         start_quarts = [1, 4]
    #         end_quarts = [1, 4]
    #     else:
    #         return []
    #     start_quarts = [q for q in start_quarts if cp1.accesses[pf_index] & q]
    #     end_quarts = [q for q in end_quarts if cp2.accesses[pf_index] & q]
    #     return [(s, e) for s in start_quarts for e in end_quarts]

    # @staticmethod
    # def line_and_trace_construction(cp1: CrossingPoint, sq, cp2: CrossingPoint, eq, pf_index, element_size):
    #     c1 = cp1.real_point(pf_index, element_size, sq)
    #     c2 = cp2.real_point(pf_index, element_size, eq)
    #     line = QLineF(c1, c2)
    #
    #     # define 4 vectors to direction
    #     v1 = QPointF(-element_size[0], -element_size[1])
    #     v2 = QPointF(element_size[0], -element_size[1])
    #     v4 = QPointF(element_size[0], element_size[1])
    #     v8 = QPointF(-element_size[0], element_size[1])
    #
    #     a = line.angle()
    #     if a == 0:
    #         return line, QPolygonF([c1 + v4, c1 + v2, c2 + v1, c2 + v8])
    #     if 0 < a < 90:
    #         return line, QPolygonF([c1 + v4, c1 + v1, c2 + v1, c2 + v4])
    #     if a == 90:
    #         return line, QPolygonF([c1 + v2, c1 + v1, c2 + v8, c2 + v4])
    #     if 90 < a < 180:
    #         return line, QPolygonF([c1 + v2, c1 + v8, c2 + v8, c2 + v2])
    #     if a == 180:
    #         return line, QPolygonF([c2 + v4, c2 + v2, c1 + v1, c1 + v8])
    #     if 180 < a < 270:
    #         return line, QPolygonF([c2 + v4, c2 + v1, c1 + v1, c1 + v4])
    #     if a == 270:
    #         return line, QPolygonF([c2 + v2, c2 + v1, c1 + v8, c1 + v4])
    #     if 270 < a < 360:
    #         return line, QPolygonF([c2 + v2, c2 + v8, c1 + v8, c1 + v2])
    #
    #     raise Exception("code should be inaccessible")
