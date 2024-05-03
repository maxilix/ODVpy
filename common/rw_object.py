from .rw_base import Bytes, UShort, UInt
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


class Coordinate(RWStreamable):

    def __init__(self, x: int, y: int):
        if not (isinstance(x, int) and isinstance(y, int)):
            raise TypeError("Coordinate must be (int, int)")
        self.x = UShort(x)
        if self.x < 0 or self.x > X_MAX_OFFICIAL:
            print(f"Warning: Coordinate x={self.x}")
        self.y = UShort(y)
        if self.y < 0 or self.y > Y_MAX_OFFICIAL:
            print(f"Warning: Coordinate y={self.y}")

    @classmethod
    def from_stream(cls, stream: ReadStream):
        x = stream.read(UShort)
        y = stream.read(UShort)
        # stream.debug_new_space()
        return cls(x, y)

    def to_stream(self, stream):
        stream.write(self.x)
        stream.write(self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"<Coordinate {str(self)}>"

    def __str__(self):
        return f"({self.x}, {self.y})"


class Segment(RWStreamable):

    def __init__(self, coor1: Coordinate, coor2: Coordinate):
        if not (isinstance(coor1, Coordinate) and isinstance(coor1, Coordinate)):
            raise TypeError("Segment must be Coordinate to Coordinate")
        self.coor1 = coor1
        self.coor2 = coor2

    @classmethod
    def from_stream(cls, stream: ReadStream):
        coor1 = stream.read(Coordinate)
        coor2 = stream.read(Coordinate)
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
    def __init__(self, coor_list):
        if not (isinstance(coor_list, list) and all(isinstance(c, Coordinate) for c in coor_list)):
            raise TypeError("Area must be a list of Coordinate")
        self.coor_list = coor_list

    @classmethod
    def from_stream(cls, stream: ReadStream):
        nb_coor = stream.read(UShort)
        coor_list = [stream.read(Coordinate) for _ in range(nb_coor)]
        # coor_list = stream.read(Array, Coordinate, comment="area", in_line=True)
        # stream.debug_new_line()
        return cls(coor_list)

    def to_stream(self, stream):
        nb_coor = UShort(len(self.coor_list))
        stream.write(nb_coor)
        for coor in self.coor_list:
            stream.write(coor)
