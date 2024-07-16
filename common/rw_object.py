from PyQt6.QtCore import QPointF, QLineF
from PyQt6.QtGui import QPolygonF

from .rw_base import Bytes, Short, UShort, UInt
from .rw_stream import RWStreamable, ReadStream
from .exception import PaddingError

X_MAX_OFFICIAL = 2944
Y_MAX_OFFICIAL = 2368


class Version(UInt):
    # def __init__(self, data: int):
    #     assert isinstance(data, int)
    #     self.data = data
    # @classmethod
    # def from_stream(cls, stream):
    #     rop = stream.read(UInt)
    #     # stream.debug_comment("version")
    #     # stream.debug_new_line()
    #     return rop
    #
    # def to_stream(self, stream):
    #     stream.write(UInt(self.data))
    pass


class Padding(Bytes):
    def __new__(cls, data: int | bytes):
        if isinstance(data, bytes):
            return super().__new__(cls, data)
        elif isinstance(data, int):
            return super().__new__(cls, b'\x00' * data)
        else:
            raise Exception("Padding must be described as a pattern of bytes or a length of zeros.")

    @classmethod
    def from_stream(cls, stream, length=None, *, pattern=None):
        padding = super().from_stream(stream, length)
        if pattern is None and padding != b'\x00' * length:
            raise PaddingError(f"zero padding expected instead of : {padding}", padding=padding)
        elif pattern is not None and padding != pattern:
            raise PaddingError(f"{pattern} padding expected instead of : {padding}", padding=padding)
        # stream.debug_comment(f"Padding {padding.hex()}")
        return padding

    def to_stream(self, stream):
        super().to_stream(stream)


class Gateway(RWStreamable):
    def __init__(self, p_in: QPointF, p_mid: QPointF, p_out: QPointF):
        self.p_in = p_in
        self.p_mid = p_mid
        self.p_out = p_out

    @classmethod
    def from_stream(cls, stream):
        p_in = stream.read(QPointF)
        p_mid = stream.read(QPointF)
        p_out = stream.read(QPointF)
        return cls(p_in, p_mid, p_out)

    def to_stream(self, stream):
        stream.write(self.p_in)
        stream.write(self.p_mid)
        stream.write(self.p_out)


# class Point(RWStreamable):
#     integer_type = Short
#
#     def __init__(self, x: int, y: int):
#         if not (isinstance(x, int) and isinstance(y, int)):
#             raise TypeError("Point must be couple of integer")
#         self.x = self.integer_type(x)
#         self.y = self.integer_type(y)
#
#     @classmethod
#     def from_stream(cls, stream: ReadStream):
#         x = stream.read(cls.integer_type)
#         y = stream.read(cls.integer_type)
#         # stream.debug_new_space()
#         return cls(x, y)
#
#     def to_stream(self, stream):
#         stream.write(self.x)
#         stream.write(self.y)
#
#     def distance(self, other):
#         if other is None:
#             return (self.x ** 2 + self.y ** 2) ** 0.5
#         else:
#             return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
#
#     def length(self):
#         return self.distance(other=None)
#
#     def __eq__(self, other):
#         return self.x == other.x and self.y == other.y
#
#     def __add__(self, other):
#         return Point(self.x + other.x, self.y + other.y)
#
#     def __sub__(self, other):
#         return Point(self.x - other.x, self.y - other.y)
#
#     def __neg__(self):
#         return Point(-self.x, -self.y)
#
#     def __repr__(self):
#         return f"<{type(self).__name__} {str(self)}>"
#
#     def __str__(self):
#         return f"({self.x}, {self.y})"
#
#
# class UPoint(Point):
#     integer_type = UShort
#
#
# class Segment(RWStreamable):
#
#     def __init__(self, coor1: UPoint, coor2: UPoint):
#         if not (isinstance(coor1, UPoint) and isinstance(coor1, UPoint)):
#             raise TypeError("Segment must be Coordinate to Coordinate")
#         self.coor1 = coor1
#         self.coor2 = coor2
#
#     @classmethod
#     def from_stream(cls, stream: ReadStream):
#         coor1 = stream.read(UPoint)
#         coor2 = stream.read(UPoint)
#         # stream.debug_new_line()
#         return cls(coor1, coor2)
#
#     def to_stream(self, stream):
#         stream.write(self.coor1)
#         stream.write(self.coor2)
#
#     def __repr__(self):
#         return f"<Segment {str(self)}>"
#
#     def __str__(self):
#         return f"{self.coor1} -> {self.coor2}"
#
#
# class Polygon(RWStreamable):
#     def __init__(self, point_list=None):
#         # if not (isinstance(point_list, list) and all(isinstance(c, UPoint) for c in point_list)):
#         #     raise TypeError("Area must be a list of UPoint")
#         # assert point_list[0] != point_list[-1]
#         if point_list is None:
#             self._point_list = []
#         else:
#             self._point_list = point_list
#         self.poly = QPolygonF([QPointF(p.x, p.y) for p in self._point_list])
#
#     def __iter__(self):
#         # return iter(self._point_list)
#         return iter(self.poly)
#
#     def __getitem__(self, index: int):
#         # return self._point_list[index % len(self)]
#         return self.poly[index % len(self)]
#         # p = self._point_list[index % len(self)]
#         # return QPointF(p.x, p.y)
#
#     def __len__(self):
#         # return len(self._point_list)
#         return len(self.poly)
#
#     def reverse(self):
#         self._point_list.reverse()
#
#     def index(self, point):
#         return self._point_list.index(point)
#
#     def to_stream(self, stream):
#         nb_point = len(self._point_list)
#         stream.write(UShort(nb_point))
#         for point in self._point_list:
#             stream.write(point)
#
#     def boundaries(self):
#         n = len(self)
#         rop = []
#         for i in range(n):
#             current_point = self[i]
#             next_point = self[(i + 1) % n]
#             rop.append(QLineF(current_point.x, current_point.y, next_point.x, next_point.y))
#         return rop
#
#     @classmethod
#     def from_stream(cls, stream: ReadStream):
#         poly = stream.read(QPolygonF)
#         for point in poly:
#             print(point)
#         exit()
#         nb_point = stream.read(UShort)
#         point_list = [stream.read(UPoint) for _ in range(nb_point)]
#         # point_list = stream.read(Array, Coordinate, comment="area", in_line=True)
#         # stream.debug_new_line()
#         return cls(point_list)
