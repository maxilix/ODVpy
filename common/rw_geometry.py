from PyQt6.QtCore import QPointF

from common import RWStreamable, UShort, ReadStream, Short


class Point(RWStreamable):


    def __init__(self, x: UShort | int, y: UShort | int):
        # if not (isinstance(x, int) and isinstance(y, int)):
        #     raise TypeError("Point must be couple of integer")
        self.x = x
        self.y = y

    @classmethod
    def from_stream(cls, stream: ReadStream, **kwargs) -> 'Point':
        x = stream.read(UShort)
        y = stream.read(UShort)
        return cls(x, y)

    def to_stream(self, stream):
        stream.write(UShort(self.x))
        stream.write(UShort(self.y))

    # def distance(self, other):
    #     if other is None:
    #         return (self.x ** 2 + self.y ** 2) ** 0.5
    #     else:
    #         return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    #
    # def length(self):
    #     return self.distance(other=None)
    #
    # def __eq__(self, other):
    #     return self.x == other.x and self.y == other.y
    #
    # def __add__(self, other):
    #     return Point(self.x + other.x, self.y + other.y)
    #
    # def __sub__(self, other):
    #     return Point(self.x - other.x, self.y - other.y)
    #
    # def __neg__(self):
    #     return Point(-self.x, -self.y)

    # def __repr__(self):
    #     return f"<{self.__class__.__name__} {str(self)}>"
    #
    # def __str__(self):
    #     return f"({self.x}, {self.y})"


class Segment(RWStreamable):

    def __init__(self, p1: Point, p2: Point):
        # if not (isinstance(coor1, UPoint) and isinstance(coor1, UPoint)):
        #     raise TypeError("Segment must be Coordinate to Coordinate")
        self.p1 = p1
        self.p2 = p2

    @classmethod
    def from_stream(cls, stream: ReadStream, **kwargs) -> 'Segment':
        p1 = stream.read(Point)
        p2 = stream.read(Point)
        # stream.debug_new_line()
        return cls(p1, p2)

    def to_stream(self, stream):
        stream.write(self.p1)
        stream.write(self.p2)

    # def __repr__(self):
    #     return f"<{self.__class__.__name__} {str(self)}>"
    #
    # def __str__(self):
    #     return f"{self.p1} -> {self.p2}"


class Gateway(RWStreamable):
    def __init__(self, p1:Point, p2:Point, p3:Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    # def __iter__(self):
    #     return iter([self.p1, self.p2, self.p3])
    #
    # def truncated(self):
    #     return Gateway(self.p1.truncated(), self.p2.truncated(), self.p3.truncated())

    @classmethod
    def from_stream(cls, stream, **kwargs) -> 'Gateway':
        p1 = stream.read(QPointF)
        p2 = stream.read(QPointF)
        p3 = stream.read(QPointF)
        return cls(p1, p2, p3)

    def to_stream(self, stream):
        stream.write(self.p1)
        stream.write(self.p2)
        stream.write(self.p3)


class Multiline(RWStreamable):
    def __init__(self, point_list:list[Point]):
        self.point_list = point_list

    @classmethod
    def from_stream(cls, stream, **kwargs) -> 'Multiline':
        nb_point = stream.read(UShort)
        return cls([stream.read(Point) for _ in range(nb_point)])

    def to_stream(self, stream):
        stream.write(UShort(len(self.point_list)))
        for point in self.point_list:
            stream.write(point)
