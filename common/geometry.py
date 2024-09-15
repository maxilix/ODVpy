import math

import numpy as np

from .rw_stream import RWStreamable
from .rw_base import Short, UShort



class Point(RWStreamable):
    x:int
    y:int
    def __init__(self, x:int, y:int):
        self.x = math.floor(x)
        self.y = math.floor(y)

    # def __init__(self, couple:(int, int)):
    #     self.x = floor(couple[0])
    #     self.y = floor(couple[1])

    def distance(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f"({self.x} {self.y})"

    def __repr__(self):
        return f"({self.x} {self.y})"

    def __iter__(self):
        yield self.x
        yield self.y

    @classmethod
    def from_stream(cls, stream):
        x = stream.read(Short)
        y = stream.read(Short)
        return cls(x, y)

    def to_stream(self, stream):
        stream.write(Short(self.x))
        stream.write(Short(self.y))

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def to_nparray(self):
        return np.array([self.x, self.y])


class Vector(Point):

    def angle_to(self, other):
        v1 = np.array([self.x, self.y])
        v2 = np.array([other.x, other.y])
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        cos_angle = dot_product / (norm_v1 * norm_v2)
        angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
        return np.degrees(angle)


class Line(RWStreamable):
    p1: Point
    p2: Point

    def __init__(self, p1:Point, p2:Point):
        self.p1 = p1
        self.p2 = p2

    def __iter__(self):
        yield self.p1
        yield self.p2

    @classmethod
    def from_stream(cls, stream):
        p1 = stream.read(Point)
        p2 = stream.read(Point)
        return cls(p1, p2)

    def to_stream(self, stream):
        stream.write(self.p1)
        stream.write(self.p2)

    # def to_vector(self):
    #     return Vector(self.p2.x - self.p1.x, self.p2.y - self.p1.y)

    # def angle_to(self, other):
    #     return self.to_vector().angle_to(other.to_vector())



class Gateway(RWStreamable):
    def __init__(self, p1:Point, p2:Point, p3:Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __iter__(self):
        yield self.p1
        yield self.p2
        yield self.p3

    # def truncated(self):
    #     return Gateway(self.p1.truncated(), self.p2.truncated(), self.p3.truncated())

    @classmethod
    def from_stream(cls, stream):
        p1 = stream.read(Point)
        p2 = stream.read(Point)
        p3 = stream.read(Point)
        return cls(p1, p2, p3)

    def to_stream(self, stream):
        stream.write(self.p1)
        stream.write(self.p2)
        stream.write(self.p3)



class MultiLine(RWStreamable):
    p_list: list[Point]

    def __init__(self, p_list: list[Point]):
        self.p_list = p_list

    def __iter__(self):
        return iter(self.p_list)

    def __len__(self):
        return len(self.p_list)

    def __getitem__(self, index):
        return self.p_list[index]

    @classmethod
    def from_stream(cls, stream):
        n = stream.read(UShort)
        p_list = [stream.read(Point) for _ in range(n)]
        return cls(p_list)

    def to_stream(self, stream):
        stream.write(UShort(len(self)))
        for p in self.p_list:
            stream.write(p)


class Polygon(MultiLine):

    def __getitem__(self, index):
        return super().__getitem__(index % len(self))

    # def angle_at(self, index):
    #     v1 = self[index-1] - self[index]
    #     v2 = self[index+1] - self[index]
    #     return v1.angle_to(v2)
