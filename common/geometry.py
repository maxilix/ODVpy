from . import RWStreamable, UShort, ReadStream


class Coordinate(RWStreamable):

    def __init__(self, x: int, y: int):
        if not (isinstance(x, int) and isinstance(y, int)):
            raise TypeError("Coordinate must be (int, int)")
        self.x = x
        self.y = y

    @classmethod
    def from_stream(cls, stream: ReadStream):
        x = stream.read(UShort)
        y = stream.read(UShort)
        stream.new_space()
        return cls(x, y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"<Coordinate {self}>"

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
        # stream.comment("Area")
        nb_coor = stream.read(UShort)
        stream.new_space()
        coor_list = [stream.read(Coordinate) for _ in range(nb_coor)]
        # stream.new_line()
        return cls(coor_list)
