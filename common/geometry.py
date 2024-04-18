from . import RWStreamable, UShort, ReadStream

X_MAX_OFFICIAL = 2944
Y_MAX_OFFICIAL = 2368


class Coordinate(RWStreamable):

    def __init__(self, x: int, y: int):
        if not (isinstance(x, int) and isinstance(y, int)):
            raise TypeError("Coordinate must be (int, int)")
        self.x = x
        if self.x < 0 or self.x > X_MAX_OFFICIAL:
            print(f"Warning: Coordinate x={self.x}")
        self.y = y
        if self.y < 0 or self.y > Y_MAX_OFFICIAL:
            print(f"Warning: Coordinate y={self.y}")

    @classmethod
    def from_stream(cls, stream: ReadStream):
        x = stream.read(UShort)
        y = stream.read(UShort)
        # stream.debug_new_space()
        return cls(x, y)

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
