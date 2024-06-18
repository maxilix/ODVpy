from functools import reduce

from PyQt6.QtCore import QRectF, Qt, QPointF, QMarginsF, QLineF
from PyQt6.QtGui import QPolygonF, QPen, QBrush, QPainterPath, QPainter, QPolygon, QGradient, QLinearGradient, QColor
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QApplication


def area(polygon: QPolygon | QPolygonF) -> float:
    rop = 0.0
    n = len(polygon)

    for i in range(n):
        current_point = polygon[i]
        next_point = polygon[(i + 1) % n]
        rop += (next_point.x() - current_point.x()) * (next_point.y() + current_point.y())

    return abs(rop / 2)




def rect_at(point: QPointF, w: (float, float), direction: int) -> QRectF:
    assert direction in [1, 2, 4, 8]
    if direction & 0b1001:
        x = point.x() - w[0]
    else:
        x = point.x()
    if direction & 0b0011:
        y = point.y() - w[1]
    else:
        y = point.y()
    return QRectF(x, y, w[0], w[1])

def boundaries(poly: QPolygon | QPolygonF) -> [QLineF]:
    # assert poly.isClosed()
    n = len(poly) - poly.isClosed()
    rop = []
    for i in range(n):
        current_point = poly[i]
        next_point = poly[(i + 1) % n]
        rop.append(QLineF(current_point, next_point))
    return rop

p1 = []
p1.append(QPointF(100, 100))
p1.append(QPointF(200, 100))
p1.append(QPointF(200, 150))
p1.append(QPointF(150, 150))  #
p1.append(QPointF(150, 200))
p1.append(QPointF(100, 200))
poly1 = QPolygonF(p1)# + p1[:1])
b = boundaries(poly1)

line1 = QLineF(QPointF(100, 400), QPointF(100, 100))
line2 = QLineF(QPointF(200, 100), QPointF(500, 100))


print(line1)


if __name__ == '__main__':
    app = QApplication([])
    pen = QPen(Qt.GlobalColor.black)
    pen.setWidthF(3)

    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, 800, 800)

    # for b_line in b:
    #     scene.addLine(b_line, Qt.GlobalColor.green)
    scene.addLine(line1, pen)
    scene.addLine(line2, pen)
    # for item in scene.items():
    #     item.setOpacity(0.15)
    # scene.addPath(line_path, Qt.GlobalColor.green, Qt.GlobalColor.green)
    # scene.addPath(i, Qt.GlobalColor.red, Qt.GlobalColor.red)



    view = QGraphicsView(scene)
    view.setGeometry(0, 0, 800, 800)

    view.show()
    app.exec()
