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

    def is_empty(self) -> bool:
        assert len(self.start_viabilities) == len(self.end_viabilities)
        return self.start_viabilities == []

    @classmethod
    def from_stream(cls, stream: ReadStream):
        end_reduced = stream.read(UChar)
        if end_reduced == 255:
            # 0xff is read
            # the corresponding link is totally unavailable
            return cls([], [])
        else:
            start_reduced = stream.read(UChar)

            n1 = stream.read(UShort)
            end_viabilities = [stream.read(UChar) for _ in range(n1)]
            # assert all([u in [1, 2, 4, 8] for u in end_viabilities])
            # assert start_reduce == reduce(lambda x, y: x | y, end_viabilities)

            n2 = stream.read(UShort)
            # assert n1 == n2
            start_viabilities = [stream.read(UChar) for _ in range(n2)]
            # assert all([u in [1, 2, 4, 8] for u in start_viabilities])
            # assert end_reduce == reduce(lambda x, y: x | y, start_viabilities)
            return cls(start_viabilities, end_viabilities)

    def to_stream(self, stream: WriteStream) -> None:
        if self.start_viabilities == [] and self.end_viabilities == []:
            stream.write(UChar(255))
        else:
            end_reduced = UChar(reduce(lambda x, y: x | y, self.end_viabilities))
            stream.write(end_reduced)

            start_reduced = UChar(reduce(lambda x, y: x | y, self.start_viabilities))
            stream.write(start_reduced)
            n1 = UShort(len(self.end_viabilities))
            stream.write(n1)
            for u in self.end_viabilities:
                stream.write(UChar(u))
            n2 = UShort(len(self.start_viabilities))
            stream.write(n2)
            for u in self.start_viabilities:
                stream.write(UChar(u))


class PathLink(RWStreamable):

    def __init__(self,
                 pathfinders,
                 start_cp_indexes,
                 end_cp_indexes,
                 length,
                 viability_index_list):
        self._pathfinders = pathfinders
        self.start_cp_indexes = start_cp_indexes
        self.end_cp_indexes = end_cp_indexes
        self.length = length
        self.viability_index_list = viability_index_list

    @classmethod
    def from_stream(cls, stream, *, pathfinders):
        indexes1 = tuple(stream.read(UShort) for _ in range(4))
        indexes2 = tuple(stream.read(UShort) for _ in range(4))
        length = stream.read(UFloat)
        nb_pathfinder = stream.read(UShort)
        viability_index_list = [stream.read(UShort) for _ in range(nb_pathfinder)]
        return cls(pathfinders, indexes1,indexes2, length, viability_index_list)

    def to_stream(self, stream):
        for index1 in self.start_cp_indexes:
            stream.write(UShort(index1))
        for index2 in self.end_cp_indexes:
            stream.write(UShort(index2))
        stream.write(UFloat(self.length))
        nb_pathfinder = UShort(len(self.viability_index_list))
        stream.write(nb_pathfinder)
        for link_viability_index in self.viability_index_list:
            stream.write(UShort(link_viability_index))

    # def QLineF(self):
    #     p1 = self.start_position.QPointF()
    #     p2 = self.end_position.QPointF()
    #     return QLineF(p1, p2)


class CrossingPoint(RWStreamable):

    def __init__(self,
                 pathfinders,
                 accesses,
                 position,
                 vector_to_next,
                 vector_from_previous,
                 link_path_index_list):
        self._pathfinders = pathfinders
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
    def line_to_previous(self):
        point = QPointF(self.position.x, self.position.y)
        previous_point = QPointF(self.position.x - self.vector_from_previous.x, self.position.y - self.vector_from_previous.y)
        return QLineF(point, previous_point)

    def line_to_next(self):
        point = QPointF(self.position.x, self.position.y)
        next_point = QPointF(self.position.x + self.vector_to_next.x, self.position.y + self.vector_to_next.y)
        return QLineF(point, next_point)

    def real_points(self, pathfinder_index, element_size) -> [QPointF]:
        rop = []
        for d in [1, 2, 4, 8]:
            if d & self.accesses[pathfinder_index]:
                if d & 0b1001:
                    x = self.position.x - element_size[0]
                else:
                    x = self.position.x + element_size[0]
                if d & 0b0011:
                    y = self.position.y - element_size[1]
                else:
                    y = self.position.y + element_size[1]
                rop.append(QPointF(x, y))
        return rop

    def real_point(self, pathfinder_index, element_size, direction) -> QPointF:
        if direction & self.accesses[pathfinder_index]:
            if direction & 0b1001:
                x = self.position.x - element_size[0]
            else:
                x = self.position.x + element_size[0]
            if direction & 0b0011:
                y = self.position.y - element_size[1]
            else:
                y = self.position.y + element_size[1]
            return QPointF(x, y)
        else:
            return QPointF()


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

        nb_path_link = UShort(len(self.path_link_index_list))
        stream.write(nb_path_link)
        for path_link_index in self.path_link_index_list:
            stream.write(UShort(path_link_index))

    # def QPointF(self):
    #     return QPointF(self.position.x + 0.5, self.position.y + 0.5)


class PathFinders(RWStreamable):

    def __init__(self, element_size_list, crossing_point_list, path_link_list, link_viability_list):
        self.element_size_list = element_size_list
        self.crossing_point_list = crossing_point_list
        self.path_link_list = path_link_list
        self.link_viability_list = link_viability_list

    def get_cp(self, indexes):
        assert len(indexes) == 4
        return self.crossing_point_list[indexes[0]][indexes[1]][indexes[2]][indexes[3]]

    def get_pl(self, index):
        return self.path_link_list[index]

    def get_viability(self, index):
        return self.link_viability_list[index]

    @classmethod
    def from_stream(cls, stream: ReadStream):
        rop = cls([],[],[],[])
        nb_pathfinder = stream.read(UShort)
        rop.element_size_list = [[stream.read(UFloat), stream.read(UFloat)] for _ in range(nb_pathfinder)]

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
        rop.path_link_list = [stream.read(PathLink, pathfinders=rop) for _ in range(nb_path_link)]

        # part 3 : link viability
        nb_link_viability = stream.read(UShort)
        rop.link_viability_list = [stream.read(LinkViability) for _ in range(nb_link_viability)]

        # return cls(element_size_list, crossing_point_list, path_link_list, link_viability_list)
        return rop

    def to_stream(self, substream: WriteStream):
        nb_pathfinder = UShort(len(self.element_size_list))
        substream.write(nb_pathfinder)
        for element in self.element_size_list:
            substream.write(element[0])
            substream.write(element[1])

        nb_layer = UShort(len(self.crossing_point_list))
        substream.write(nb_layer)
        for cp_layer in self.crossing_point_list:
            nb_cp_sublayer = UShort(len(cp_layer))
            substream.write(nb_cp_sublayer)
            for cp_sublayer in cp_layer:
                nb_cp_area = UShort(len(cp_sublayer))
                substream.write(nb_cp_area)
                for cp_area in cp_sublayer:
                    nb_crossing_point = UShort(len(cp_area))
                    substream.write(nb_crossing_point)
                    for crossing_point in cp_area:
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
        crossing_point_list = []

        # define crossing point list
        for i, layer in enumerate(motion):
            crossing_point_list.append([])
            for j, sublayer in enumerate(layer):
                crossing_point_list[i].append([])
                for k, area in enumerate(sublayer):
                    crossing_point_list[i][j].append(cls.cp_list_from_move_area(area))

        # define accesses for each crossing point
        for i, layer in enumerate(motion):
            for j, sublayer in enumerate(layer):
                # main_poly = sublayer.main.QPolygonF()
                # obstacle_poly = [obstacle.QPolygonF() for obstacle in sublayer.obstacles]
                for k in range(len(sublayer)):
                    for cp in crossing_point_list[i][j][k]:
                        cls.accesses_definition(cp, element_size_list, sublayer)

        # remove crossing point without access
        # for i, layer in enumerate(motion):
        #     for j, sublayer in enumerate(layer):
        #         for k in range(len(sublayer)):
        #             crossing_point_list[i][j][k] = [cp for cp in crossing_point_list[i][j][k] if sum(cp.accesses) > 0]

        path_link_list, viability_list = cls.generate_path_link_and_viability_lists(motion, element_size_list, crossing_point_list)

        return cls(element_size_list, crossing_point_list, path_link_list, viability_list)

    @staticmethod
    def cp_list_from_move_area(move_area):
        # TODO second implementation based on QLineF and the angle() method
        # probably more effective

        # Ensures that points are covered in the right order
        # i.e. if you walk on the border, the restricted area is on the right.
        move_area.clockwise = not move_area.main  # reverse the order of points if necessary

        cp_list = []
        for point_index in range(len(move_area)):
            # TODO do not add point at the limit of the DVM (or limit of sublayer maybe ?)
            u = move_area[point_index - 1] - move_area[point_index]  # vector to previous
            v = move_area[point_index + 1] - move_area[point_index]  # vector to next
            theta = acos((u.x * v.x + u.y * v.y) / (u.length() * v.length()))
            if u.x * v.y - u.y * v.x > 0:
                theta = 2 * pi - theta
            if theta < pi:
                # this point is a crossing point
                cp_list.append(CrossingPoint(None,
                                             [],
                                             move_area[point_index],
                                             v,
                                             -u,
                                             []))
        move_area.clockwise = True  # engine need clockwise definition  TODO really needed ?
        return cp_list


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
    def rect_at(point: Point, w: (float, float), direction: int) -> QRectF:
        assert direction in [1, 2, 4, 8]
        if direction & 0b1001:
            x = point.x - 2*w[0]
        else:
            x = point.x
        if direction & 0b0011:
            y = point.y - 2*w[1]
        else:
            y = point.y
        return QRectF(x, y, 2*w[0], 2*w[1])

    @classmethod
    def accesses_definition(cls, cp, element_size_list, sublayer):
        for element_size in element_size_list:
            access = 0
            for direction in [1, 2, 4, 8]:
                r = cls.rect_at(cp.position, element_size, direction)
                if sublayer.contains_poly(r):
                    access += direction
            cp.accesses.append(access)

    @classmethod
    def generate_path_link_and_viability_lists(cls, motion, element_size_list, crossing_point_list):
        path_link_list = []
        viability_list = [LinkViability([], [])]  # 0xff at index 0

        print("start pl generation")
        for i, layer in enumerate(motion):
            print(f"{i}")
            for j, sublayer in enumerate(layer):
                print(f"{i} {j}")
                for k1, area1 in enumerate(sublayer):
                    print(f"{i} {j} {k1}")
                    for l1, cp1 in enumerate(crossing_point_list[i][j][k1]):
                        for k2, area2 in enumerate(sublayer):
                            for l2, cp2 in enumerate(crossing_point_list[i][j][k2]):
                                pl = PathLink(None, (i,j,k2,l2), (i,j,k1,l1), cp1.position.distance(cp2.position), [])
                                for pf_index, element_size in enumerate(element_size_list):
                                    v = LinkViability([],[])
                                    combine_quarts = cls.quarts_definition(pf_index, cp1, cp2)
                                    for sq, eq in combine_quarts:
                                        line, trace_poly = cls.line_and_trace_construction_v0(cp1, sq, cp2, eq, pf_index, element_size)
                                        if sublayer.contains_poly(trace_poly):
                                            angle1_with_previous = line.angleTo(cp1.line_to_previous())
                                            angle1_with_next = cp1.line_to_next().angleTo(line)
                                            angle2_with_previous = line.angleTo(cp2.line_to_previous())
                                            angle2_with_next = cp2.line_to_next().angleTo(line)
                                            if (angle1_with_previous > 180 or angle1_with_next > 180) and (angle2_with_previous < 180 or angle2_with_next < 180):
                                                v.start_viabilities.append(eq)
                                                v.end_viabilities.append(sq)

                                    if v.is_empty() is False:
                                        viability_list.append(v)
                                        pl.viability_index_list.append(len(viability_list)-1)
                                    else:
                                        pl.viability_index_list.append(0)

                                if sum(pl.viability_index_list) > 0:
                                    path_link_list.append(pl)
                                    cp1.path_link_index_list.append(len(path_link_list)-1)
                                    pl_reverse = PathLink(None, pl.end_cp_indexes, pl.start_cp_indexes, pl.length, [])
                                    for v in pl.viability_index_list:
                                        v_reverse = LinkViability(viability_list[v].end_viabilities, viability_list[v].start_viabilities)
                                        viability_list.append(v_reverse)
                                        pl_reverse.viability_index_list.append(len(viability_list) - 1)
                                    path_link_list.append(pl_reverse)
                                    cp2.path_link_index_list.append(len(path_link_list) - 1)

        return path_link_list, viability_list



    @staticmethod
    def is_line_strictly_in_sublayer(line: QLineF, sublayer) -> bool:
        center = line.center()
        if not sublayer.allow_path.contains(center):
            # print(f"c {center.x():8.3f} {center.y():8.3f}   ", end="")
            return False

        for bound in sublayer.boundaries:
            # if line == bound or line.p1() == bound.p2() and line.p2() == bound.p1():
            #     return True
            if (i := bound.intersects(line))[0] == QLineF.IntersectionType.BoundedIntersection:
                if i[1] != line.p1() and i[1] != line.p2():
                    # print(f"i {i[1].x():8.3f} {i[1].y():8.3f}   ", end="")
                    return False
            # else:
            #     print(i[0])
        return True

    @staticmethod
    def quarts_definition(pf_index, cp1, cp2):
        if cp2.position.x == cp1.position.x and cp2.position.y > cp1.position.y:
            # case 1
            start_quarts = [4, 8]
            end_quarts = [1, 2]
        elif cp2.position.y == cp1.position.y and cp2.position.x > cp1.position.x:
            # case 2
            start_quarts = [2, 4]
            end_quarts = [1, 8]
        elif cp2.position.x > cp1.position.x and cp2.position.y > cp1.position.y:
            # case 3
            start_quarts = [2, 8]
            end_quarts = [2, 8]
        elif cp2.position.x > cp1.position.x and cp2.position.y < cp1.position.y:
            # case 4
            start_quarts = [1, 4]
            end_quarts = [1, 4]
        else:
            return []
        start_quarts = [q for q in start_quarts if cp1.accesses[pf_index] & q]
        end_quarts = [q for q in end_quarts if cp2.accesses[pf_index] & q]
        return [(s, e) for s in start_quarts for e in end_quarts]

    @staticmethod
    def line_and_trace_construction_v0(cp1: CrossingPoint, sq, cp2:CrossingPoint, eq, pf_index, element_size):
        lp1 = cp1.real_point(pf_index, element_size, sq)
        lp2 = cp2.real_point(pf_index, element_size, eq)

        tp1 = QPointF(cp1.position.x, cp1.position.y)
        width_vector = 2*(lp1-tp1)
        tp2 = tp1 + width_vector
        tp3 = tp2 + lp2 - lp1
        tp4 = tp3 - width_vector

        return QLineF(lp1, lp2), QPolygonF([tp1, tp2, tp3, tp4])

    @classmethod
    def line_and_trace_construction(cls, cp1: CrossingPoint, sq, cp2:CrossingPoint, eq, pf_index, element_size):
        rs = cls.rect_at(cp1.position, element_size, sq)
        re = cls.rect_at(cp2.position, element_size, eq)
        rop_line = QLineF(rs.center(), re.center())

        rop_trace = QPolygonF([rs.bottomLeft(), rs.bottomRight(), re.bottomRight(), re.bottomLeft()])
        rop_trace = rop_trace.united(QPolygonF([rs.topLeft(), rs.topRight(), re.topRight(), re.topLeft()]))
        rop_trace = rop_trace.united(QPolygonF([rs.bottomLeft(), re.bottomLeft(), re.topLeft(), rs.topLeft()]))
        rop_trace = rop_trace.united(QPolygonF([rs.bottomRight(), re.bottomRight(), re.topRight(), rs.topRight()]))

        # lp1 = cp1.real_point(pf_index, element_size, sq)
        # lp2 = cp2.real_point(pf_index, element_size, eq)
        #
        # tp1 = QPointF(cp1.position.x, cp1.position.y)
        # width_vector = 2*(lp1-tp1)
        # tp2 = tp1 + width_vector
        # tp3 = tp2 + lp2 - lp1
        # tp4 = tp3 - width_vector

        return rop_line, rop_trace