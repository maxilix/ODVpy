from functools import reduce
from typing import Any

from PyQt6.QtCore import QRectF

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


@timeit
def signed_double_area(poly: QPolygonF) -> float:
    """
    Return the signed area of the polygon.
    A negative value indicates a clockwise points definition.
    A positive value indicates a counter-clockwise points definition.
    It's the mathematical opposite because the y-axis is inverted.
    WARNING, does not work with self-intersecting polygons, unexpected behavior.
    """
    area = 0.0
    n = poly.count()
    for i in range(n):
        current_point = poly[i - 1]
        next_point = poly[i]
        area += (next_point.x() - current_point.x()) * (next_point.y() + current_point.y())
    return area

def is_simple(poly: QPolygonF) -> (bool,str):
    for point in poly:
        if (c:=poly.count(point)) > 1:
            return False, f"{point} appear {c} times."
    return True, ""

def is_self_intersected(poly: QPolygonF) -> (bool,str):
    line_list = [QLineF(poly[i-1], poly[i]) for i in range(-1, poly.count())]
    for line in line_list:
        for inter in [line.intersects(l) for l in line_list if l != line]:
            if inter[0] == QLineF.IntersectionType.BoundedIntersection and inter[1] != line.p1() and inter[1] != line.p2():
                return True, f"self-intersection at {inter[1]}"
    return False, ""

def is_clockwise(poly: QPolygonF) -> bool:
    """
    WARNING, does not work with self-intersecting polygons, unexpected behavior.
    """
    return signed_double_area(poly) < 0.0


class Viability(RWStreamable):

    def __init__(self, t1: list[UChar | int], t2: list[UChar | int]):
        self.t1 = t1
        self.t2 = t2

    def is_empty(self) -> bool:
        assert len(self.t1) == len(self.t2)
        return self.t1 == []

    @classmethod
    def from_stream(cls, stream: ReadStream, **kwargs):
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
                 cp1_indexes: (UShort | int, UShort | int, UShort | int, UShort | int),
                 cp2_indexes: (UShort | int, UShort | int, UShort | int, UShort | int),
                 length: Float,
                 viability_index_list: list[UShort | int]):
        self.cp1_indexes = cp1_indexes
        self.cp2_indexes = cp2_indexes
        self.length = length
        self.viability_index_list = viability_index_list

    @classmethod
    def from_stream(cls, stream, **kwargs):
        indexes2 = tuple(stream.read(UShort) for _ in range(4))
        indexes1 = tuple(stream.read(UShort) for _ in range(4))
        length = stream.read(Float)
        nb_pathfinder = stream.read(UShort)
        viability_index_list = [stream.read(UShort) for _ in range(nb_pathfinder)]
        return cls(indexes1, indexes2, length, viability_index_list)

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


class CrossingPoint(RWStreamable):

    def __init__(self,
                 # pathfinders: Any,  # should be a PathFinders
                 accesses: list[UChar | int],
                 point: QPointF,
                 vector_to_next: QPointF,
                 vector_from_previous: QPointF,
                 link_index_list: list[UShort | int]):
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

    @classmethod
    def from_stream(cls, stream, **kwargs):
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
        return cls(accesses, point, vector_to_next, vector_from_previous, path_link_index_list)

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
    polygon_list: list[list[list[QPolygonF]]] = []
    size_vectors: list[dict] = []
    size_list: list[tuple[float, float]] = []
    crossing_point_list: list[list[list[list[CrossingPoint]]]] = []
    link_list: list[Link] = []
    viability_list: list[Viability] = []

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
    def from_stream(cls, stream: ReadStream, **kwargs):
        rop = cls()

        nb_pathfinder = stream.read(UShort)
        rop.size_list = [(stream.read(Float), stream.read(Float)) for _ in range(nb_pathfinder)]

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
                            stream.read(CrossingPoint))

        # part 2 : path links
        nb_path_link = stream.read(UShort)
        rop.link_list = [stream.read(Link) for _ in range(nb_path_link)]

        # part 3 : link viability
        nb_link_viability = stream.read(UShort)
        rop.viability_list = [stream.read(Viability) for _ in range(nb_link_viability)]

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
    def rebuild(self, motion, /, max_link_length=46340, print_times=False):
        """
        rebuild all pathfinders from motion (polygons definition)
        max_link_length=46340 is the diagonal of a (2**15-1, 2**15-1) map,
            where 2**15-1 is the max of a Short

        note: max_link_length=300 generate about 2/3 of smallest original links
            this test limit saves a factor of 10 in execution
        """
        self.size_vectors = [{1: QPointF(-s[0], -s[1]),
                              2: QPointF(+s[0], -s[1]),
                              4: QPointF(+s[0], +s[1]),
                              8: QPointF(-s[0], +s[1])} for s in self.size_list]
        self.polygon_list = []

        print("Verifying polygons definition...", end="")
        self._build_polygons(motion)
        print("\b\b Done.")

        print("Evaluating docking point location...", end="")
        self._rebuild_crossing_points()
        print("\b\b Done.")
        print(f"  {sum([sum([sum([len(cp_l) for cp_l in area_l]) for area_l in sublayer_l]) for sublayer_l in self.crossing_point_list])} docking point found.")

        print("Generating links...", end="")
        self._rebuild_links(max_link_length)
        print("\b\b Done.")
        print(f"  {len(self.link_list)} links generated.")

        if print_times:
            print("\n  times:")
            for k in T:
                print(f"{T[k]:6.2f} {k}")


    @timeit
    def _build_polygons(self, motion):
        """
        Build oriented QPolygonF 3d list
        Although the game engine accepts self-intersecting polygons,the pathfinder construction
            rejects them for greater control.
        """

        def _check_and_add(poly: QPolygonF, clockwise: bool):
            if (r := is_self_intersected(poly))[0]:
                print(r[1])
                return False
            if not (r := is_simple(poly))[0]:
                print(r[1])
                return False
            if is_clockwise(poly) == clockwise:  # main polygon must be defined counter-clockwise
                self.polygon_list[-1][-1].append(poly)
            else:
                self.polygon_list[-1][-1].append(QPolygonF(poly[::-1]))

        for layer in motion:
            self.polygon_list.append([])
            for main_area in layer:
                self.polygon_list[-1].append([])
                # main polygon must be defined counter-clockwise
                if _check_and_add(QPolygonF(main_area.area), clockwise=False) is False:
                    return False
                for obstacle in main_area:
                    # obstacle polygons must be defined clockwise
                    if _check_and_add(QPolygonF(obstacle.area), clockwise=True) is False:
                        return False


    @timeit
    def _rebuild_crossing_points(self):
        """
        rebuild all the crossing point list
        """

        self.crossing_point_list = []
        for i, pll in enumerate(self.polygon_list):
            self.crossing_point_list.append([])
            for j, pl in enumerate(pll):
                self.crossing_point_list[i].append([])
                for k, p in enumerate(pl):
                    self.crossing_point_list[i][j].append([])
                    # 1 - define crossing point list of polygon i j k
                    self._rebuild_crossing_points_of(i, j, k)
                    # 2 - build accesses
                    for l, cp in enumerate(self.crossing_point_list[i][j][k]):
                        self._rebuild_accesses_of(i, j, k, l)
                    # 3 - remove cp with complete no access
                    self.crossing_point_list[i][j][k] =\
                        [cp for cp in self.crossing_point_list[i][j][k] if sum(cp.accesses) > 0]

    @timeit
    def _rebuild_crossing_points_of(self, i, j, k):
        self.crossing_point_list[i][j][k] = []
        poly = self.polygon_list[i][j][k]
        n = poly.count()
        for index in range(poly.count()):
            pp = poly[index - 1]        # previous point
            cp = poly[index]            # current point
            np = poly[(index + 1) % n]  # next point
            theta = QLineF(cp, pp).angleTo(QLineF(cp, np))

            if theta < 180:  # this point is a crossing point
                self.crossing_point_list[i][j][k].append(CrossingPoint([],
                                                                       cp,
                                                                       np - cp,
                                                                       cp - pp,
                                                                       []))

    @timeit
    def _rebuild_accesses_of(self, i, j, k, l):

        def rect_at(x, y, s, direction):
            rop = QRectF(x, y, 2 * s[0], 2 * s[1])  # South-East by default
            if direction & 0b1001:
                rop = rop.translated(-2 * s[0], 0)  # go to West
            if direction & 0b0011:
                rop = rop.translated(0, -2 * s[1])  # go to Nort
            return QPolygonF(rop)

        cp = self.crossing_point_list[i][j][k][l]
        for size in self.size_list:
            access = 0
            dqa = 8*size[0]*size[1]  # double of quarter rectangle
            for d in [1,2,4,8]:
                r = rect_at(cp.x, cp.y, size, d)
                if dqa - abs(signed_double_area(self.polygon_list[i][j][0].intersected(r))) > 0.2:
                    # the area of intersection with the main polygon is smaller than the area of the rectangle
                    continue
                if k != 0 and abs(signed_double_area(self.polygon_list[i][j][k].intersected(r))) > 0.2:
                    # intersection with the obstacle of which the docking point is part
                    continue
                touch_other_obstacles = False
                for obstacle_poly in self.polygon_list[i][j][1:]:#k] + self.polygon_list[i][j][k+1:]:
                    if abs(signed_double_area(obstacle_poly.intersected(r))) > 0.2:
                        # intersection with another obstacle
                        touch_other_obstacles = True
                        break
                if touch_other_obstacles:
                    continue
                access += d
            cp.accesses.append(access)


    @timeit
    def does_main_area_contain(self, i, j, poly: QPolygonF):
        if abs(signed_double_area(poly)) - abs(signed_double_area(self.polygon_list[i][j][0].intersected(poly))) > 0.2:
            # the area of intersection with the main polygon is smaller than the area of the polygon
            return False
        for obstacle_poly in self.polygon_list[i][j][1:]:
            if abs(signed_double_area(obstacle_poly.intersected(poly))) > 0.2:
                # intersection with another obstacle
                return False
        return True


    @timeit
    def _get_traces(self, pf_index, i, j, k1, l1, k2, l2):
        cp1 = self.crossing_point_list[i][j][k1][l1]
        cp2 = self.crossing_point_list[i][j][k2][l2]
        combine_quarts = [(sq, eq) for sq in [1, 2, 4, 8] if cp1.accesses[pf_index] & sq
                                   for eq in [1, 2, 4, 8] if cp2.accesses[pf_index] & eq]

        rop = []
        for sq, eq in combine_quarts:
            c1 = cp1.point + self.size_vectors[pf_index][sq]
            c2 = cp2.point + self.size_vectors[pf_index][eq]
            path_vector = QLineF(c1, c2)
            a = path_vector.angle()

            if not ((a == 0 and sq in [1, 8] and eq in [2, 4]) or
                    (0 < a < 90 and sq in [1, 4] and eq in [1, 4]) or
                    (a == 90 and sq in [8, 4] and eq in [1, 2]) or
                    (90 < a < 180 and sq in [2, 8] and eq in [2, 8]) or
                    (a == 180 and sq in [2, 4] and eq in [1, 8]) or
                    (180 < a < 270 and sq in [1, 4] and eq in [1, 4]) or
                    (a == 270 and sq in [1, 2] and eq in [4, 8]) or
                    (270 < a < 360 and sq in [2, 8] and eq in [2, 8])):
                # this combination of quarters is irrelevant depending on the angle
                continue

            p = path_vector.angleTo(QLineF(QPointF(0,0), -cp1.vector_from_previous))
            n = QLineF(QPointF(0,0), cp1.vector_to_next).angleTo(path_vector)
            if not ((sq == 1 and (0 <= a < 90 and p > 180 or 180 < a <= 270 and n > 180)) or
                    (sq == 2 and (270 <= a < 360 and p > 180 or 90 < a <= 180 and n > 180)) or
                    (sq == 4 and (180 <= a < 270 and p > 180 or 0 < a <= 90 and n > 180)) or
                    (sq == 8 and (90 <= a < 180 and p > 180 or (270 < a < 360 or a == 0) and n > 180))):
                # start condition failed
                continue

            p = (path_vector.angleTo(QLineF(QPointF(0,0), -cp2.vector_from_previous)) + 180) % 360
            n = (QLineF(QPointF(0,0), cp2.vector_to_next).angleTo(path_vector) + 180) % 360
            if not ((eq == 1 and (180 <= a < 270 and p > 180 or 0 < a <= 90 and n > 180)) or
                    (eq == 2 and (90 <= a < 180 and p > 180 or (270 < a < 360 or a == 0) and n > 180)) or
                    (eq == 4 and (0 <= a < 90 and p > 180 or 180 < a <= 270 and n > 180)) or
                    (eq == 8 and (270 <= a < 360 and p > 180 or 90 < a <= 180 and n > 180))):
                # end condition failed
                continue

            # compute the trace
            v1 = self.size_vectors[pf_index][1]
            v2 = self.size_vectors[pf_index][2]
            v4 = self.size_vectors[pf_index][4]
            v8 = self.size_vectors[pf_index][8]
            if a == 0:
                rop.append((QPolygonF([c1 + v4, c1 + v2, c2 + v1, c2 + v8]), sq, eq))
            elif 0 < a < 90:
                rop.append((QPolygonF([c1 + v4, c1 + v1, c2 + v1, c2 + v4]), sq, eq))
            elif a == 90:
                rop.append((QPolygonF([c1 + v2, c1 + v1, c2 + v8, c2 + v4]), sq, eq))
            elif 90 < a < 180:
                rop.append((QPolygonF([c1 + v2, c1 + v8, c2 + v8, c2 + v2]), sq, eq))
            elif a == 180:
                rop.append((QPolygonF([c2 + v4, c2 + v2, c1 + v1, c1 + v8]), sq, eq))
            elif 180 < a < 270:
                rop.append((QPolygonF([c2 + v4, c2 + v1, c1 + v1, c1 + v4]), sq, eq))
            elif a == 270:
                rop.append((QPolygonF([c2 + v2, c2 + v1, c1 + v8, c1 + v4]), sq, eq))
            elif 270 < a < 360:
                rop.append((QPolygonF([c2 + v2, c2 + v8, c1 + v8, c1 + v2]), sq, eq))
            else:
                raise Exception(f"code should be inaccessible (a={a})")

        return rop

    @timeit
    def _rebuild_links(self, max_link_length):
        self.link_list = []
        self.viability_list = [Viability([], [])]  # 0xff at index 0

        for i, cp_lll in enumerate(self.crossing_point_list):
            for j, cp_ll in enumerate(cp_lll):
                for k1, cp1_l in enumerate(cp_ll):
                    for l1, cp1 in enumerate(cp1_l):
                        for k2, cp2_l in enumerate(cp_ll):
                            for l2, cp2 in enumerate(cp2_l):
                                if QLineF(cp1.point, cp2.point).length() > max_link_length:
                                    continue
                                if (cp2.x == cp1.x and cp2.y > cp1.y or
                                    cp2.y == cp1.y and cp2.x > cp1.x or
                                    cp2.x > cp1.x and cp2.y > cp1.y or
                                    cp2.x > cp1.x and cp2.y < cp1.y) is False:
                                    continue

                                link = Link((i, j, k1, l1),
                                            (i, j, k2, l2),
                                            QLineF(cp1.point, cp2.point).length(),
                                            [])

                                for pf_index in range(len(self)):
                                    viability = Viability([], [])
                                    for trace, sq, eq in self._get_traces(pf_index, i, j, k1, l1, k2, l2):
                                        if self.does_main_area_contain(i, j, trace):
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
                                    reversed_link = Link(link.cp2_indexes, link.cp1_indexes, link.length, [])
                                    for viability in link.viability_index_list:
                                        reversed_viability = Viability(self.viability_list[viability].t2,
                                                                       self.viability_list[viability].t1)
                                        self.viability_list.append(reversed_viability)
                                        reversed_link.viability_index_list.append(len(self.viability_list) - 1)
                                    self.link_list.append(reversed_link)
                                    cp2.link_index_list.append(len(self.link_list) - 1)
