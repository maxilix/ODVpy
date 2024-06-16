import time
from functools import reduce
from math import acos, pi

from PyQt6.QtCore import QLineF, QPointF, QRectF, QSize
from PyQt6.QtGui import QPainterPath, QPolygonF, QPolygon

from common import *


class LinkViability(RWStreamable):

    def __init__(self,
                 start_viabilities: list[UChar],
                 end_viabilities: list[UChar]):
        self.start_viabilities = start_viabilities
        self.end_viabilities = end_viabilities

    @classmethod
    def from_stream(cls, stream: ReadStream):
        start_reduce = stream.read(UChar)
        if start_reduce == 255:
            # 0xff is read
            # the corresponding link is totally unavailable
            return cls([], [])
        else:
            end_reduce = stream.read(UChar)

            n1 = stream.read(UShort)
            start_viabilities = [stream.read(UChar) for _ in range(n1)]
            # assert all([u in [1, 2, 4, 8] for u in start_viabilities])
            # assert start_reduce == reduce(lambda x, y: x | y, start_viabilities)

            n2 = stream.read(UShort)
            # assert n1 == n2
            end_viabilities = [stream.read(UChar) for _ in range(n2)]
            # assert all([u in [1, 2, 4, 8] for u in end_viabilities])
            # assert end_reduce == reduce(lambda x, y: x | y, end_viabilities)
            return cls(start_viabilities, end_viabilities)

    def to_stream(self, stream: WriteStream) -> None:
        if self.start_viabilities == [] and self.end_viabilities == []:
            stream.write(UChar(255))
        else:
            start_reduce = UChar(reduce(lambda x, y: x | y, self.start_viabilities))
            stream.write(start_reduce)
            end_reduce = UChar(reduce(lambda x, y: x | y, self.end_viabilities))
            stream.write(end_reduce)
            n1 = UShort(len(self.start_viabilities))
            stream.write(n1)
            for u in self.start_viabilities:
                stream.write(u)
            n2 = UShort(len(self.end_viabilities))
            stream.write(n2)
            for u in self.end_viabilities:
                stream.write(u)


class PathLink(RWStreamable):

    def __init__(self,
                 start_cp_indexes,
                 start_position,
                 end_cp_indexes,
                 end_position,
                 length,
                 global_link_viability_index_list,
                 link_viability):
        self.start_cp_indexes = start_cp_indexes
        self.start_position = start_position
        self.end_cp_indexes = end_cp_indexes
        self.end_position = end_position
        self.length = length
        self.global_link_viability_index_list = global_link_viability_index_list
        self.link_viability = link_viability

    @classmethod
    def from_stream(cls, stream):
        indexes1 = tuple(stream.read(UShort) for _ in range(4))
        indexes2 = tuple(stream.read(UShort) for _ in range(4))
        length = stream.read(UFloat)
        nb_pathfinder = stream.read(UShort)
        global_link_viability_index_list = [stream.read(UShort) for _ in range(nb_pathfinder)]
        return cls(indexes1, None, indexes2, None, length, global_link_viability_index_list, [])

    def to_stream(self, stream):
        for index1 in self.start_cp_indexes:
            stream.write(index1)
        for index2 in self.end_cp_indexes:
            stream.write(index2)
        stream.write(self.length)
        unk_obj_index_list_length = UShort(len(self.global_link_viability_index_list))
        stream.write(unk_obj_index_list_length)
        for link_viability_index in self.global_link_viability_index_list:
            stream.write(link_viability_index)

    def QLineF(self):
        p1 = self.start_position.QPointF()
        p2 = self.end_position.QPointF()
        return QLineF(p1, p2)


class CrossingPoint(RWStreamable):

    def __init__(self,
                 accesses,
                 position,
                 vector_to_next,
                 vector_from_previous,
                 link_path_index_list):
        self.accesses = accesses
        self.position = position
        self.vector_to_next = vector_to_next
        self.vector_from_previous = vector_from_previous
        self.path_link_index_list = link_path_index_list

    # def __iter__(self):
    #     return iter(self.path_link_list)
    #
    # def __getitem__(self, item):
    #     return self.path_link_list[item]
    #
    # def __len__(self):
    #     # assert (len(self.path_link_list) == len(self.global_path_link_index_list))
    #     return len(self.path_link_list)

    @classmethod
    def from_stream(cls, stream):
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
        # note:
        # 4 msb are always zero
        # 0x0f = 0b00001111 cannot be possible

        position = stream.read(UPoint)

        vector_to_next = stream.read(Point)
        vector_from_previous = stream.read(Point)

        nb_path_link = stream.read(UShort)
        path_link_index_list = [stream.read(UShort) for _ in range(nb_path_link)]
        return cls(accesses, position, vector_to_next, vector_from_previous, path_link_index_list)

    def to_stream(self, stream):
        nb_pathfinder = UShort(len(self.accesses))  # w
        stream.write(nb_pathfinder)
        for access in self.accesses:
            stream.write(access)
        stream.write(self.position)
        stream.write(self.vector_to_next)
        stream.write(self.vector_from_previous)

        nb_path_link = UShort(len(self.path_link_index_list))
        stream.write(nb_path_link)
        for path_link_index in self.path_link_index_list:
            stream.write(path_link_index)

    def QPointF(self):
        return QPointF(self.position.x + 0.5, self.position.y + 0.5)


class PathFinders(RWStreamable):

    def __init__(self, element_size_list, crossing_point_list, path_link_list, link_viability_list):
        self.element_size_list = element_size_list
        self.crossing_point_list = crossing_point_list
        self.path_link_list = path_link_list
        self.link_viability_list = link_viability_list

    @classmethod
    def from_stream(cls, stream: ReadStream):
        nb_pathfinder = stream.read(UShort)
        element_size_list = [[stream.read(UFloat), stream.read(UFloat)] for _ in range(nb_pathfinder)]

        # part 1 : crossing points
        nb_layer = stream.read(UShort)
        crossing_point_list = []

        for layer_index in range(nb_layer):
            crossing_point_list.append([])
            nb_sublayer = stream.read(UShort)
            for sublayer_index in range(nb_sublayer):
                crossing_point_list[layer_index].append([])
                nb_area = stream.read(UShort)
                for area_index in range(nb_area):
                    crossing_point_list[layer_index][sublayer_index].append([])
                    nb_crossing_point = stream.read(UShort)
                    for crossing_point_index in range(nb_crossing_point):
                        crossing_point_list[layer_index][sublayer_index][area_index].append(stream.read(CrossingPoint))

        # part 2 : path links
        nb_path_link = stream.read(UShort)
        path_link_list = [stream.read(PathLink) for _ in range(nb_path_link)]

        # part 3 : link viability
        nb_link_viability = stream.read(UShort)
        link_viability_list = [stream.read(LinkViability) for _ in range(nb_link_viability)]

        return cls(element_size_list, crossing_point_list, path_link_list, link_viability_list)

    def to_stream(self, substream: WriteStream):
        nb_pathfinder = UShort(len(self.element_size_list))
        substream.write(nb_pathfinder)
        for element in self.element_size_list:
            substream.write(element[0])
            substream.write(element[1])

        nb_layer = UShort(len(self.crossing_point_list))
        substream.write(nb_layer)
        for layer in self.crossing_point_list:
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

        nb_path_link = UShort(len(self.path_link_list))
        substream.write(nb_path_link)
        for path_link in self.path_link_list:
            substream.write(path_link)

        nb_link_viability = UShort(len(self.link_viability_list))
        substream.write(nb_link_viability)
        for link_viability in self.link_viability_list:
            substream.write(link_viability)

    @classmethod
    def build_from_motion(cls, motion, element_size_list):
        element_size_list = [[UFloat(6.0), UFloat(3.0)],
                             [UFloat(11.0), UFloat(6.0)],
                             [UFloat(19.0), UFloat(11.0)]]

        crossing_point_list = []

        for i, layer in enumerate(motion):
            crossing_point_list.append([])
            for j, sublayer in enumerate(layer):
                crossing_point_list[i].append([])
                crossing_point_list[i][j].append(cls.cp_list_from_move_area(sublayer.main))
                for k, area in enumerate(sublayer):
                    crossing_point_list[i][j].append(cls.cp_list_from_move_area(area))

        for i, layer in enumerate(motion):
            for j, sublayer in enumerate(layer):
                sublayer_QPainterPath = sublayer.allow_QPainterPath()
                for k in range(len(sublayer) + 1):
                    # t = time.time()
                    # print(f"{i}, {j}, {k} : {len(crossing_point_list[i][j][k])}cps ", end="")
                    for cp in crossing_point_list[i][j][k]:
                        cls.accesses_definition(cp, element_size_list, sublayer_QPainterPath)
                    # print(f"{time.time() - t:.2f}s")


        return cls(element_size_list, crossing_point_list, [], [])

    @staticmethod
    def cp_list_from_move_area(move_area):
        # assure que les point sont parcouru dans le bon ordre
        # cad si l'on marche sur la frontiere, la zone inaxessible est a droite
        move_area.clockwise = not move_area.main  # renverse l'ordre des points si necessaire

        cp_list = []
        for point_index in range(len(move_area)):
            u = move_area[point_index - 1] - move_area[point_index]  # vector to previous
            v = move_area[point_index + 1] - move_area[point_index]  # vector to next
            theta = acos((u.x * v.x + u.y * v.y) / (u.length() * v.length()))
            if u.x * v.y - u.y * v.x > 0:
                theta = 2 * pi - theta
            if theta < pi:
                # this point is a crossing point
                cp_list.append(CrossingPoint([],
                                             move_area[point_index],
                                             v,
                                             -u,
                                             []))
        move_area.clockwise = True  # engine need clockwise definition  TODO really needed ?
        return cp_list

    # @staticmethod
    # def area_of_QPainterPath(path: QPainterPath, precision: int = 10000) -> float:
    #     """
    #     QPainterPath area calculation
    #     https://stackoverflow.com/questions/20282579/calculating-the-fill-area-of-qpainterpath
    #     """
    #     points = [(point.x(), point.y()) for point in (path.pointAtPercent(i / precision) for i in range(precision))]
    #     points.append(points[0])
    #
    #     return 0.5 * abs(reduce(
    #         lambda sum, i: sum + (points[i][0] * points[i + 1][1] - points[i + 1][0] * points[i][1]),
    #         range(len(points) - 1),
    #         0
    #     ))

    @staticmethod
    def area(polygon: QPolygon | QPolygonF) -> float:
        area = 0.0
        n = len(polygon)

        for i in range(n):
            current_point = polygon[i]
            next_point = polygon[(i + 1) % n]
            area += (next_point.x() - current_point.x()) * (next_point.y() + current_point.y())

        return abs(area / 2)

    @staticmethod
    def rect_at(point: UPoint, w: (float, float), direction: int) -> QRectF:
        assert direction in [1, 2, 4, 8]
        if direction & 0b1001:
            x = point.x - w[0]
        else:
            x = point.x
        if direction & 0b0011:
            y = point.y - w[1]
        else:
            y = point.y
        return QRectF(x, y, w[0], w[1])

    @classmethod
    def accesses_definition(cls, cp, element_size_list, sublayer_QPainterPath):

        for element_size in element_size_list:
            access = 0
            for direction in [1, 2, 4, 8]:
                r = QPainterPath()
                r.addRect(cls.rect_at(cp.position, element_size, direction))

                inter = sublayer_QPainterPath.intersected(r)
                polygons = inter.toFillPolygons()
                if len(polygons) == 1:
                    a = element_size[0]*element_size[1] - cls.area(polygons[0])
                    if cp.position == UPoint(2022,368):
                        print(cp.position, direction, element_size, a)
                    if a <= 0.05:
                        access += direction
            cp.accesses.append(access)

