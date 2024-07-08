from math import floor

from PyQt6.QtCore import QPointF, QLineF
from PyQt6.QtGui import QPolygonF

from common import ReadStream, Short


# QPointF monkey patch

def QPointF_truncated(self: QPointF) -> QPointF:
    return QPointF(floor(self.x()), floor(self.y()))


def QPointF_distance(self: QPointF, other: QPointF) -> float:
    return QLineF(self, other).length()

def QPointF_from_stream(cls, stream: ReadStream):
    x = stream.read(Short)
    y = stream.read(Short)
    return cls(x, y)


def QPointF_to_stream(self, stream):
    stream.write(Short(self.x()))
    stream.write(Short(self.y()))


QPointF.truncated = QPointF_truncated
QPointF.distance = QPointF_distance
QPointF.from_stream = classmethod(QPointF_from_stream)
QPointF.to_stream = QPointF_to_stream


# QLineF monkey patch

def QLineF_from_stream(cls, stream: ReadStream):
    p1 = stream.read(QPointF)
    p2 = stream.read(QPointF)
    return cls(p1, p2)


def QLineF_to_stream(self, stream):
    stream.write(self.p1())
    stream.write(self.p2())


QLineF.from_stream = classmethod(QLineF_from_stream)
QLineF.to_stream = QLineF_to_stream


# QPolygonF monkey patch

def QPolygonF_from_stream(cls, stream: ReadStream):
    nb_point = stream.read(Short)
    return cls([stream.read(QPointF) for _ in range(nb_point)])


def QPolygonF_to_stream(self, stream):
    stream.write(Short(len(self)))
    for point in self:
        stream.write(point)



def QPolygonF_signed_area(self: QPolygonF) -> float:
    """
    Return the signed area of the polygon.
    A negative value indicates a clockwise points definition.
    A positive value indicates a counter-clockwise points definition.
    It's the mathematical opposite because the y-axis is inverted.
    WARNING, does not work with self-intersecting polygons, unexpected behavior.
    """
    area = 0.0
    n = self.count()
    for i in range(n):
        current_point = self[i]
        next_point = self[(i + 1) % n]
        area += (next_point.x() - current_point.x()) * (next_point.y() + current_point.y())

    return area / 2


def QPolygonF_area(self: QPolygonF) -> float:
    return abs(self.signed_area())

# def QPolygonF_reversed(self: QPolygonF) -> QPolygonF:
#     return QPolygonF(reversed(self))
#
# def QPolygonF_reverse(self: QPolygonF) -> None:
#     # self.swap(self.reversed())
#     for i in range(len(self)//2):
#         self.swapItemAt(i, len(self) - 1 - i)

QPolygonF.from_stream = classmethod(QPolygonF_from_stream)
QPolygonF.to_stream = QPolygonF_to_stream
QPolygonF.signed_area = QPolygonF_signed_area
QPolygonF.area = QPolygonF_area
# QPolygonF.reversed = QPolygonF_reversed
# QPolygonF.reverse = QPolygonF_reverse
