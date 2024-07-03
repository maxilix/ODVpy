from math import floor

from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPolygonF


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



def QPointF_truncated(self: QPointF) -> QPointF:
    return QPointF(floor(self.x()), floor(self.y()))


QPolygonF.signed_area = QPolygonF_signed_area
QPolygonF.area = QPolygonF_area
QPointF.truncated = QPointF_truncated
