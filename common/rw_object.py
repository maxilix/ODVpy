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


class Point(RWStreamable):
    integer_type = Short

    def __init__(self, x: int, y: int):
        if not (isinstance(x, int) and isinstance(y, int)):
            raise TypeError("Point must be couple of integer")
        self.x = self.integer_type(x)
        self.y = self.integer_type(y)

    @classmethod
    def from_stream(cls, stream: ReadStream):
        x = stream.read(cls.integer_type)
        y = stream.read(cls.integer_type)
        # stream.debug_new_space()
        return cls(x, y)

    def to_stream(self, stream):
        stream.write(self.x)
        stream.write(self.y)

    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"<{type(self).__name__} {str(self)}>"

    def __str__(self):
        return f"({self.x}, {self.y})"


class UPoint(Point):
    integer_type = UShort


class Segment(RWStreamable):

    def __init__(self, coor1: UPoint, coor2: UPoint):
        if not (isinstance(coor1, UPoint) and isinstance(coor1, UPoint)):
            raise TypeError("Segment must be Coordinate to Coordinate")
        self.coor1 = coor1
        self.coor2 = coor2

    @classmethod
    def from_stream(cls, stream: ReadStream):
        coor1 = stream.read(UPoint)
        coor2 = stream.read(UPoint)
        # stream.debug_new_line()
        return cls(coor1, coor2)

    def to_stream(self, stream):
        stream.write(self.coor1)
        stream.write(self.coor2)

    def __repr__(self):
        return f"<Segment {str(self)}>"

    def __str__(self):
        return f"{self.coor1} -> {self.coor2}"


class Area(RWStreamable):
    def __init__(self, point_list):
        if not (isinstance(point_list, list) and all(isinstance(c, UPoint) for c in point_list)):
            raise TypeError("Area must be a list of Coordinate")
        self.point_list = point_list

    def __iter__(self):
        return iter(self.point_list)

    def __getitem__(self, item):
        return self.point_list[item]

    def __len__(self):
        return len(self.point_list)

    def index(self, point):
        return self.point_list.index(point)

    def to_stream(self, stream):
        nb_point = UShort(len(self.point_list))
        stream.write(nb_point)
        for point in self.point_list:
            stream.write(point)

    @classmethod
    def from_stream(cls, stream: ReadStream):
        nb_point = stream.read(UShort)
        point_list = [stream.read(UPoint) for _ in range(nb_point)]
        # point_list = stream.read(Array, Coordinate, comment="area", in_line=True)
        # stream.debug_new_line()
        return cls(point_list)
