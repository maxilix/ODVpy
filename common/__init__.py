from PyQt6.QtGui import QPolygonF

from .exception import *
from .rw_stream import RStreamable, WStreamable, RWStreamable, ReadStream, WriteStream
from .rw_base import Bytes, Char, UChar, Short, UShort, Int, UInt, UFloat, String
from .rw_object import Version, Padding
from .rw_object import UPoint, Point, Segment, Polygon
from .image import Pixmap, Pixel
from .parser import Parser
from .utils import *

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
    return abs(QPolygonF_signed_area(self))


QPolygonF.signed_area = QPolygonF_signed_area
QPolygonF.area = QPolygonF_area