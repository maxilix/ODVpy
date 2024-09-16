from PyQt6.QtCore import QLineF, QRectF, QPointF
from PyQt6.QtGui import QPolygonF

from debug import timeit, T
from odv.pathfinder import PathFinder, CrossingPoint, Viability, Link


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
        current_point = poly[i]
        next_point = poly[(i + 1) % n]
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









class PathFinderFactory(object):

    def __init__(self, size_list, motion, max_link_length=None):
        self.new_pathfinder = PathFinder()
        self.new_pathfinder.size_list = size_list
        self.motion = motion
        self.max_link_length = max_link_length
        self.polygon_list: list[list[list[QPolygonF]]] = []



    @timeit
    def generate(self):
        print("Verifying polygons definition...", end="")
        self.build_polygon_list()
        print("\b\b Done.")

        print("Evaluating docking point location...", end="")
        self.rebuild_crossing_point_list()
        print("\b\b Done.")
        print(f"  {sum([sum([sum([len(cp_l) for cp_l in area_l]) for area_l in sublayer_l]) for sublayer_l in self.new_pathfinder.crossing_point_list])} docking point found.")
        # print(f"as = {sum([sum([sum([sum([sum(cp.accesses) for cp in cp_l]) for cp_l in area_l]) for area_l in sublayer_l]) for sublayer_l in self.new_pathfinder.crossing_point_list])}")
        # print(f"ac = {[[[[cp.accesses for cp in cp_l] for cp_l in area_l] for area_l in sublayer_l] for sublayer_l in self.new_pathfinder.crossing_point_list]}")

        print("Generating links...", end="")
        self.rebuild_link_list()
        print("\b\b Done.")
        print(f"  {len(self.new_pathfinder.link_list)} links generated.")

        print("\n  times:")
        for k in T:
            print(f"{T[k]:6.2f} {k}")


    @timeit
    def build_polygon_list(self):
        """
        Build oriented QPolygonF 3D list
        Although the game engine accepts self-intersecting polygons,the pathfinder construction
            rejects them for greater control.
        """

        self.polygon_list: list[list[list[QPolygonF]]] = []

        def check_and_add(poly: QPolygonF, clockwise: bool):
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

        for layer in self.motion:
            self.polygon_list.append([])
            for main_area in layer:
                self.polygon_list[-1].append([])
                # main polygon must be defined counter-clockwise
                if check_and_add(QPolygonF(main_area.poly), clockwise=False) is False:
                    return False

                for obstacle in main_area:
                    # obstacle polygons must be defined clockwise
                    if check_and_add(QPolygonF(obstacle.poly), clockwise=True) is False:
                        return False


    @timeit
    def rebuild_crossing_point_list(self):
        # print("rebuilding crossing point list - ...", end="")
        self.new_pathfinder.crossing_point_list = []
        for i, pll in enumerate(self.polygon_list):
            self.new_pathfinder.crossing_point_list.append([])
            for j, pl in enumerate(pll):
                self.new_pathfinder.crossing_point_list[i].append([])
                for k, p in enumerate(pl):
                    self.new_pathfinder.crossing_point_list[i][j].append([])
                    # 1 - define crossing point list
                    self.rebuild_crossing_point_list_of(i, j, k)
                    # 2 - build accesses
                    for l, cp in enumerate(self.new_pathfinder.crossing_point_list[i][j][k]):
                        self.rebuild_accesses(i,j,k,l)
                    # 3 - remove cp with complete no access
                    # self.new_pathfinder.crossing_point_list[i][j][k] =\
                    #     [cp for cp in self.new_pathfinder.crossing_point_list[i][j][k] if sum(cp.accesses) > 0]

                    # if k == 1:
                    #     print(self.new_pathfinder.crossing_point_list[i][j][k])
                    #     exit()
        # print("\b\b\bDone")


    @timeit
    def rebuild_crossing_point_list_of(self, i, j, k):
        self.new_pathfinder.crossing_point_list[i][j][k] = []
        poly = self.polygon_list[i][j][k]
        n = poly.count()
        for index in range(poly.count()):
            pp = poly[index - 1]        # previous point
            cp = poly[index]            # current point
            np = poly[(index + 1) % n]  # next point
            theta = QLineF(cp, pp).angleTo(QLineF(cp, np))
            # print(theta)

            if theta < 180:  # this point is a crossing point
                self.new_pathfinder.crossing_point_list[i][j][k].append(CrossingPoint(self.new_pathfinder,
                                                                                      [],
                                                                                      cp,
                                                                                      np - cp,
                                                                                      cp - pp,
                                                                                      []))
                # if k!=0:print("ok", end="")
            # if k!=0:print()


    @timeit
    def rebuild_accesses(self, i, j, k, l):

        def rect_at(x, y, size, direction):
            rop = QRectF(x, y, 2*size[0], 2*size[1])  # South-East by default
            if direction & 0b1001:
                rop = rop.translated(-2 * size[0], 0)  # go to West
            if direction & 0b0011:
                rop = rop.translated(0, -2 * size[1])  # go to Nort
            return QPolygonF(rop)

        cp = self.new_pathfinder.crossing_point_list[i][j][k][l]
        for size in self.new_pathfinder.size_list:
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
    def main_area_contain(self, i, j, poly: QPolygonF):
        if abs(signed_double_area(poly)) - abs(signed_double_area(self.polygon_list[i][j][0].intersected(poly))) > 0.2:
            # the area of intersection with the main polygon is smaller than the area of the polygon
            return False
        for obstacle_poly in self.polygon_list[i][j][1:]:
            if abs(signed_double_area(obstacle_poly.intersected(poly))) > 0.2:
                # intersection with another obstacle
                return False
        return True


    @timeit
    def traces(self, pf_index, i, j, k1, l1, k2, l2):
        cp1 = self.new_pathfinder.crossing_point_list[i][j][k1][l1]
        cp2 = self.new_pathfinder.crossing_point_list[i][j][k2][l2]
        combine_quarts = [(sq, eq) for sq in [1, 2, 4, 8] if cp1.accesses[pf_index] & sq
                                   for eq in [1, 2, 4, 8] if cp2.accesses[pf_index] & eq]

        rop = []
        for sq, eq in combine_quarts:
            c1 = cp1.point_at(pf_index, sq)
            c2 = cp2.point_at(pf_index, eq)
            path_vector = QLineF(c1, c2)
            a = path_vector.angle()
            # print(path_vector, a)

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
            # define 4 vectors to direction
            size = self.new_pathfinder.size_list[pf_index]
            v1 = QPointF(-size[0], -size[1])
            v2 = QPointF(+size[0], -size[1])
            v4 = QPointF(+size[0], +size[1])
            v8 = QPointF(-size[0], +size[1])
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
                raise Exception("code should be inaccessible")

        return rop

    @timeit
    def rebuild_link_list(self):
        # self.tl = []
        # print("rebuilding link list - 00.0%", end="")
        # nb_cp = sum([sum([sum([len(cp_l) for cp_l in area_l]) for area_l in sublayer_l]) for sublayer_l in
        #              self.new_pathfinder.crossing_point_list])
        # i_cp = 0

        self.new_pathfinder.link_list = []
        self.new_pathfinder.viability_list = [Viability([], [])]  # 0xff at index 0

        for i, cp_lll in enumerate(self.new_pathfinder.crossing_point_list):
            for j, cp_ll in enumerate(cp_lll):
                for k1, cp1_l in enumerate(cp_ll):
                    for l1, cp1 in enumerate(cp1_l):
                        # print(f"\b\b\b\b\b{i_cp / nb_cp * 100:4.1f}%", end="")
                        # i_cp += 1
                        for k2, cp2_l in enumerate(cp_ll):
                            for l2, cp2 in enumerate(cp2_l):
                                if (cp2.x == cp1.x and cp2.y > cp1.y or
                                    cp2.y == cp1.y and cp2.x > cp1.x or
                                    cp2.x > cp1.x and cp2.y > cp1.y or
                                    cp2.x > cp1.x and cp2.y < cp1.y) is False:
                                    continue

                                link = Link(self.new_pathfinder,
                                            (i, j, k1, l1),
                                            (i, j, k2, l2),
                                            QLineF(cp1.point, cp2.point).length(),
                                            [])

                                for pf_index in range(len(self.new_pathfinder)):
                                    viability = Viability([], [])
                                    for trace, sq, eq in self.traces(pf_index,i,j,k1,l1,k2,l2):
                                        # self.tl.append((cp1.point_at(pf_index, sq), cp2.point_at(pf_index, eq)))
                                        if self.main_area_contain(i,j,trace):
                                            viability.t1.append(eq)
                                            viability.t2.append(sq)

                                    if viability.is_empty() is False:
                                        self.new_pathfinder.viability_list.append(viability)
                                        link.viability_index_list.append(len(self.new_pathfinder.viability_list) - 1)
                                    else:
                                        link.viability_index_list.append(0)

                                if sum(link.viability_index_list) > 0:  # if at least one viability has been appended
                                    self.new_pathfinder.link_list.append(link)
                                    cp1.link_index_list.append(len(self.new_pathfinder.link_list) - 1)
                                    reversed_link = Link(self.new_pathfinder, link.cp2_indexes, link.cp1_indexes, link.length, [])
                                    for viability in link.viability_index_list:
                                        reversed_viability = Viability(self.new_pathfinder.viability_list[viability].t2,
                                                                       self.new_pathfinder.viability_list[viability].t1)
                                        self.new_pathfinder.viability_list.append(reversed_viability)
                                        reversed_link.viability_index_list.append(len(self.new_pathfinder.viability_list) - 1)
                                    self.new_pathfinder.link_list.append(reversed_link)
                                    cp2.link_index_list.append(len(self.new_pathfinder.link_list) - 1)
        # print(f"{len(self.tl)=}")
        # print("\b\b\b\b\bDone")


