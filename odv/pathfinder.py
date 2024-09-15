import time
from functools import reduce
from math import acos, pi
from typing import Any

import numpy as np
import shapely
from shapely import Polygon as ShapelyPolygon, is_valid_reason
from shapely.affinity import translate

from common import *
from debug import timeit, T

def oriented_angle_1(v1: np.array) -> float:
    rad_angle = np.arctan2(v1[1], v1[0])
    return np.round(np.degrees(- rad_angle), 1) % 360

def oriented_angle_2(v1: np.array, v2: np.array) -> float:
    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    rad_angle = np.copysign(np.arccos(np.clip(cos_theta, -1.0, 1.0)), v1[0] * v2[1] - v1[1] * v2[0])
    return np.round(np.degrees(- rad_angle), 1) % 360
    # the minus, here       ---^---
    # comes from the inversion of the y-axis between math and computer science conventions


def rect_at(x, y, size, direction):
    rop = ShapelyPolygon([(x - size[0], y - size[1]),
                          (x + size[0], y - size[1]),
                          (x + size[0], y + size[1]),
                          (x - size[0], y + size[1]),
                          (x - size[0], y - size[1])])
    if direction & 0b1001:
        rop = translate(rop, -size[0], 0)  # West
    else:
        rop = translate(rop, size[0], 0)  # East
    if direction & 0b0011:
        rop = translate(rop, 0, -size[1])  # Nort
    else:
        rop = translate(rop, 0, +size[1])  # South
    return rop


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
                 point: Point,
                 vector_to_next: Point,
                 vector_from_previous: Point,
                 link_index_list: [UShort | int]):
        self._pathfinders = pathfinders
        self.accesses = accesses
        self.point = point
        self.vector_to_next = vector_to_next
        self.vector_from_previous = vector_from_previous
        self.link_index_list = link_index_list

    @property
    def x(self):
        return self.point.x

    @property
    def y(self):
        return self.point.y

    # @timeit
    # def line_to_previous(self):
    #     return QLineF(self.point, self.point - self.vector_from_previous)
    #
    # @timeit
    # def line_to_next(self):
    #     return QLineF(self.point, self.point + self.vector_to_next)





    @timeit
    def point_at(self, pf_index, direction):
        size = self._pathfinders.size_list[pf_index]
        if direction & 0b1001:
            x = self.x - size[0]
        else:
            x = self.x + size[0]
        if direction & 0b0011:
            y = self.y - size[1]
        else:
            y = self.y + size[1]
        return Point(x, y)

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

        point = stream.read(Point)

        vector_to_next = stream.read(Point)
        vector_from_previous = stream.read(Point)

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

    def __init__(self, motion, size_list, crossing_point_list, link_list, viability_list):
        self._motion = motion
        self.size_list = size_list
        # ( 3.0,  2.0)   monkey
        # ( 6.0,  3.0)   standing human
        # (11.0,  6.0)   crawling human
        # (19.0, 11.0)   horses
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
    def from_stream(cls, stream: ReadStream, *, move: Any):
        rop = cls(move, [], [], [], [])

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

    @timeit
    def rebuild(self):
        """
          1.08 rebuild_crossing_point_list
         54.41 rebuild_link_list

         48.68 contains_v1
         16.13 QPolygonF_signed_area
          3.23 line_and_trace
          1.07 rebuild_accesses
          1.04 potential_direction_combination
        """

        self.build_shapely_polygons()
        self.rebuild_crossing_point_list()
        print(f"nb_cb = {sum([sum([sum([len(cp_l) for cp_l in area_l]) for area_l in sublayer_l]) for sublayer_l in self.crossing_point_list])}")

        self.rebuild_link_list()
        print(f"nb_link = {len(self.link_list)}")

        print("\n  times:")
        for k in T:
            print(f"{T[k]:6.2f} {k}")

    @timeit
    def build_shapely_polygons(self):
        # build oriented and valid shapely polygon 3D list
        #   poly.is_ccw has strange behavior on invalid polygons.
        #   Although the game engine accepts self-intersecting polygons,
        #   the pathfinder construction rejects them for greater control.

        self.shapely_polygons: list[list[list[Polygon]]] = []
        for layer in self._motion:
            # print(layer)
            self.shapely_polygons.append([])
            for main_area in layer:
                # print(main_area)
                self.shapely_polygons[-1].append([])
                sp = ShapelyPolygon(main_area.poly)
                if not sp.is_valid:
                    print(f"Invalid {main_area} polygon: {is_valid_reason(sp)}")
                    return
                if sp.exterior.is_ccw:  # main polygon must be defined counter-clockwise
                    self.shapely_polygons[-1][-1].append(sp.reverse())
                else:
                    self.shapely_polygons[-1][-1].append(sp)
                for obstacle in main_area:
                    sp = ShapelyPolygon(obstacle.poly)
                    if not sp.is_valid:
                        print(f"Invalid {obstacle} polygon: {is_valid_reason(sp)}")
                        return
                    if sp.exterior.is_ccw:  # obstacle polygons must be defined clockwise
                        self.shapely_polygons[-1][-1].append(sp)
                    else:
                        self.shapely_polygons[-1][-1].append(sp.reverse())

    @timeit
    def rebuild_crossing_point_list(self):
        print("rebuilding crossing point list - ...", end="")
        self.crossing_point_list = []
        for i, pll in enumerate(self.shapely_polygons):
            self.crossing_point_list.append([])
            for j, pl in enumerate(pll):
                self.crossing_point_list[i].append([])
                for k, p in enumerate(pl):
                    self.crossing_point_list[i][j].append([])
                    # 1 - define crossing point list
                    self.rebuild_crossing_point_list_of(i, j, k)
                    # 2 - build accesses
                    for l, cp in enumerate(self.crossing_point_list[i][j][k]):
                        self.rebuild_accesses(i,j,k,l)
                    # 3 - remove cp with complete no access
                    self.crossing_point_list[i][j][k] = [cp for cp in self.crossing_point_list[i][j][k] if sum(cp.accesses) > 0]

        print("\b\b\bDone")

    @timeit
    def rebuild_crossing_point_list_of(self, i, j, k):
        self.crossing_point_list[i][j][k] = []
        # coords = [Point(*p) for p in self.shapely_polygons[i][j][k].exterior.coords[:-1]]  # the last point is the same as the first one
        coords = np.array(self.shapely_polygons[i][j][k].exterior.coords[:-1])  # the last point is the same as the first one
        # if k!=0:print("obstacle",i,j,k)
        n = len(coords)
        for m, p in enumerate(coords):
            # get the angle of the non-movable side area at the current point
            theta = oriented_angle_2(coords[m - 1] - p, coords[(m + 1) % n] - p)
            # if k!=0:print(theta, " ", end="")
            if theta < 180:
                # this point is a crossing point
                self.crossing_point_list[i][j][k].append(CrossingPoint(self,
                                                                       [],
                                                                       Point(*p),
                                                                       Point(*(coords[(m + 1) % n] - p)),
                                                                       Point(*(p - coords[(m - 1) % n])),
                                                                       []))
                # if k!=0:print("ok", end="")
            # if k!=0:print()



    @timeit
    def rebuild_accesses(self, i, j, k, l):
        cp = self.crossing_point_list[i][j][k][l]
        for size in self.size_list:
            access = 0
            for d in [1,2,4,8]:
                r = rect_at(cp.x, cp.y, size, d)
                a = self.shapely_polygons[i][j][0].intersection(r).area
                if a < 4*size[0]*size[1] - 0.01:
                    # the area of intersection with the main polygon is smaller than the area of the rectangle
                    continue
                if k != 0 and self.shapely_polygons[i][j][k].intersection(r).area > 0.01:
                    # intersection with the obstacle of which the cp is part
                    continue
                if any(shapely.area(shapely.intersection(r, self.shapely_polygons[i][j][1:])) > 0.01):
                    # intersection with at least one obstacle
                    continue
                access += d
            cp.accesses.append(access)

        # print(i,j,k,l,cp.x,cp.y,cp.accesses)

    @timeit
    def main_area_contain(self, i, j, polygon:ShapelyPolygon):
        a = self.shapely_polygons[i][j][0].intersection(polygon).area
        if a < polygon.area - 0.01:
            # the area of intersection with the main polygon is smaller than the area of the polygon
            return False
        # if k != 0 and self.shapely_polygons[i][j][k].intersection(r).area > 0.01:
        #     # intersection with the obstacle of which the cp is part
        #     continue
        if any(shapely.area(shapely.intersection(polygon, self.shapely_polygons[i][j][1:])) > 0.01):
            # intersection with at least one obstacle
            return False
        return True


    @timeit
    def traces(self,pf_index,i,j,k1,l1,k2,l2):
        cp1 = self.crossing_point_list[i][j][k1][l1]
        cp2 = self.crossing_point_list[i][j][k2][l2]
        combine_quarts = [(sq, eq)
                          for sq in [1, 2, 4, 8] if cp1.accesses[pf_index] & sq
                          for eq in [1, 2, 4, 8] if cp2.accesses[pf_index] & eq]

        rop = []
        for sq, eq in combine_quarts:
            c1 = cp1.point_at(pf_index, sq)
            c2 = cp2.point_at(pf_index, eq)
            path_vector = (c2-c1).to_nparray()
            a = oriented_angle_1(path_vector)
            # print(path_vector, a)

            if not ((a == 0        and sq in [1, 8] and eq in [2, 4]) or \
                    (0 < a < 90    and sq in [1, 4] and eq in [1, 4]) or \
                    (a == 90       and sq in [8, 4] and eq in [1, 2]) or \
                    (90 < a < 180  and sq in [2, 8] and eq in [2, 8]) or \
                    (a == 180      and sq in [2, 4] and eq in [1, 8]) or \
                    (180 < a < 270 and sq in [1, 4] and eq in [1, 4]) or \
                    (a == 270      and sq in [1, 2] and eq in [4, 8]) or \
                    (270 < a < 360 and sq in [2, 8] and eq in [2, 8])):
                # this combination of quarters is irrelevant depending on the angle
                continue

            p = oriented_angle_2(path_vector, (-cp1.vector_from_previous).to_nparray())
            n = oriented_angle_2(cp1.vector_to_next.to_nparray(), path_vector)
            if not ((sq == 1 and (0 <= a < 90 and p > 180 or 180 < a <= 270 and n > 180)) or \
                    (sq == 2 and (270 <= a < 360 and p > 180 or 90 < a <= 180 and n > 180)) or \
                    (sq == 4 and (180 <= a < 270 and p > 180 or 0 < a <= 90 and n > 180)) or \
                    (sq == 8 and (90 <= a < 180 and p > 180 or (270 < a < 360 or a == 0) and n > 180))):
                # start condition failed
                continue

            p = (oriented_angle_2(path_vector, (-cp2.vector_from_previous).to_nparray()) + 180) % 360
            n = (oriented_angle_2(cp2.vector_to_next.to_nparray(), path_vector) + 180) % 360
            if not ((eq == 1 and (180 <= a < 270 and p > 180 or 0 < a <= 90 and n > 180)) or \
                    (eq == 2 and (90 <= a < 180 and p > 180 or (270 < a < 360 or a == 0) and n > 180)) or \
                    (eq == 4 and (0 <= a < 90 and p > 180 or 180 < a <= 270 and n > 180)) or \
                    (eq == 8 and (270 <= a < 360 and p > 180 or 90 < a <= 180 and n > 180))):
                # end condition failed
                continue

            # compute the trace
            # define 4 vectors to direction
            size = self.size_list[pf_index]
            v1 = Point(-size[0], -size[1])
            v2 = Point(size[0], -size[1])
            v4 = Point(size[0], size[1])
            v8 = Point(-size[0], size[1])
            if a == 0:
                rop.append((ShapelyPolygon([c1 + v4, c1 + v2, c2 + v1, c2 + v8]), eq, sq))
            elif 0 < a < 90:
                rop.append((ShapelyPolygon([c1 + v4, c1 + v1, c2 + v1, c2 + v4]), eq, sq))
            elif a == 90:
                rop.append((ShapelyPolygon([c1 + v2, c1 + v1, c2 + v8, c2 + v4]), eq, sq))
            elif 90 < a < 180:
                rop.append((ShapelyPolygon([c1 + v2, c1 + v8, c2 + v8, c2 + v2]), eq, sq))
            elif a == 180:
                rop.append((ShapelyPolygon([c2 + v4, c2 + v2, c1 + v1, c1 + v8]), eq, sq))
            elif 180 < a < 270:
                rop.append((ShapelyPolygon([c2 + v4, c2 + v1, c1 + v1, c1 + v4]), eq, sq))
            elif a == 270:
                rop.append((ShapelyPolygon([c2 + v2, c2 + v1, c1 + v8, c1 + v4]), eq, sq))
            elif 270 < a < 360:
                rop.append((ShapelyPolygon([c2 + v2, c2 + v8, c1 + v8, c1 + v2]), eq, sq))
            else:
                raise Exception("code should be inaccessible")

        return rop



    @timeit
    def rebuild_link_list(self):
        print("rebuilding link list - 00.0%", end="")
        nb_cp = sum([sum([sum([len(cp_l) for cp_l in area_l]) for area_l in sublayer_l]) for sublayer_l in
                     self.crossing_point_list])
        i_cp = 0

        self.link_list = []
        self.viability_list = [Viability([], [])]  # 0xff at index 0

        for i, cp_lll in enumerate(self.crossing_point_list):
            for j, cp_ll in enumerate(cp_lll):
                for k1, cp1_l in enumerate(cp_ll):
                    for l1, cp1 in enumerate(cp1_l):
                        print(f"\b\b\b\b\b{i_cp / nb_cp * 100:4.1f}%", end="")
                        i_cp += 1
                        for k2, cp2_l in enumerate(cp_ll):
                            for l2, cp2 in enumerate(cp2_l):
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

                                    # if pf_index == 0 and cp1.x == 827 and cp1.y == 712 and cp2.x == 860 and cp2.y == 534:
                                    #     print(f"{combine_quarts}")
                                    #     exit()

                                    for trace, sq, eq in self.traces(pf_index,i,j,k1,l1,k2,l2):
                                        if self.main_area_contain(i,j,trace):
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
                        # print("ici")
                        # exit()
        print("\b\b\b\b\bDone")
