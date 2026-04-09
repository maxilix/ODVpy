from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QBrush

THIN_PEN_WIDTH = 0.4
LIGHT_BRUSH_ALPHA = 32
HIGH_BRUSH_ALPHA = 96

class OdvPen(QPen):
    def __init__(self, color, width):
        super().__init__(color)
        self.setWidthF(width)
        self.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.setJoinStyle(Qt.PenJoinStyle.RoundJoin)


class OdvThinPen(OdvPen):
    def __init__(self, color):
        super().__init__(color, THIN_PEN_WIDTH)


class OdvBrush(QBrush):
    def __init__(self, color, alpha):
        color.setAlpha(alpha)
        super().__init__(color)


class OdvLightBrush(OdvBrush):
    def __init__(self, color):
        super().__init__(color, LIGHT_BRUSH_ALPHA)


class OdvHighBrush(OdvBrush):
    def __init__(self, color):
        super().__init__(color, HIGH_BRUSH_ALPHA)



from .point import GraphicPoint
from .line import GraphicLine, GraphicMultiLine, GraphicGateway
from .polygon import GraphicPolygon
from .pixmap import GraphicMap, GraphicMask
from .sight import GraphicSightObstacle
