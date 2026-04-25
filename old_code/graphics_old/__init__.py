from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QBrush
from PyQt6.QtWidgets import QGraphicsLineItem


class OdvPen(QPen):
    def __init__(self, color, width):
        super().__init__(color)
        self.setWidthF(width)
        self.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.setJoinStyle(Qt.PenJoinStyle.RoundJoin)


class OdvThinPen(OdvPen):
    def __init__(self, color):
        super().__init__(color, 0.3)


class OdvBrush(QBrush):
    def __init__(self, color, alpha):
        color.setAlpha(alpha)
        super().__init__(color)


class OdvLightBrush(OdvBrush):
    def __init__(self, color):
        super().__init__(color, 32)


class OdvHighBrush(OdvBrush):
    def __init__(self, color):
        super().__init__(color, 96)


class QGraphicsLargeLineItem(QGraphicsLineItem):
    _width_scale = 6.0

    def shape(self):
        # virtually extends the line width for click detection
        temp_line = QGraphicsLineItem(self.line())
        pen = self.pen()
        pen.setWidthF(pen.widthF() * self._width_scale)
        pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        temp_line.setPen(pen)
        return temp_line.shape()


from .point import GraphicPoint
from .line import GraphicLine, GraphicMultiLine, GraphicGateway
from .polygon import GraphicPolygon
from .pixmap import GraphicMap, GraphicMask
from .sight import GraphicSightObstacle

# TODO graphic ZValue
