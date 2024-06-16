from functools import reduce

from PyQt6.QtCore import QRectF, Qt, QPointF
from PyQt6.QtGui import QPolygonF, QPen, QBrush, QPainterPath, QPainter
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QApplication


def area_of(path: QPainterPath, precision: int = 1000) -> float:
    """
    QPainterPath area calculation
    https://stackoverflow.com/questions/20282579/calculating-the-fill-area-of-qpainterpath
    """
    points = [(point.x(), point.y()) for point in (path.pointAtPercent(i/precision) for i in range (precision))]
    points.append(points[0])

    return 0.5 * abs(reduce(
        lambda sum, i: sum + (points[i][0] * points[i + 1][1] - points[i + 1][0] * points[i][1]),
        range (len (points) - 1),
        0
    ))


def rect_to_polygon(rect):
    # Get the corner points of the rectangle
    top_left = rect.topLeft()
    top_right = rect.topRight()
    bottom_right = rect.bottomRight()
    bottom_left = rect.bottomLeft()

    # Create a QPolygonF from the corner points
    polygon = QPolygonF([top_left, top_right, bottom_right, bottom_left])

    return polygon


def rect_at(point: QPointF, w: (float, float), direction: int) -> QRectF:
    if direction & 0b1001:
        x = point.x() - w[0]
    else:
        x = point.x()
    if direction & 0b0011:
        y = point.y() - w[1]
    else:
        y = point.y()
    return QRectF(x, y, w[0], w[1])


p1 = []
p1.append(QPointF(100, 100))
p1.append(QPointF(200, 100))
p1.append(QPointF(200, 150))
p1.append(QPointF(150, 150))  #
p1.append(QPointF(150, 200))
p1.append(QPointF(100, 200))
triangle1 = QPolygonF(p1 + p1[:1])

p2 = []
p2.append(QPointF(300, 300))
p2.append(QPointF(600, 300))
p2.append(QPointF(600, 600))
p2.append(QPointF(350, 600))  #
p2.append(QPointF(350, 550))
p2.append(QPointF(550, 550))
p2.append(QPointF(550, 350))
p2.append(QPointF(350, 350))
p2.append(QPointF(350, 600))  #
p2.append(QPointF(300, 600))
triangle2 = QPolygonF(p2 + p2[:1])

path = QPainterPath()
path.addPolygon(triangle1)
path.addPolygon(triangle2)
path.closeSubpath()

rectangle = QPainterPath()
rectangle.addRect(rect_at(p1[0], (400, 400), 4))

i = path.intersected(rectangle)
polys = i.toFillPolygons()
print(polys)
for poly in polys:
    for point in poly:
        print(point)
    print()





if __name__ == '__main__':
    app = QApplication([])
    pen = QPen(Qt.GlobalColor.black)
    brush = QBrush(Qt.GlobalColor.gray)
    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, 800, 800)

    scene.addPath(path, Qt.GlobalColor.black, Qt.GlobalColor.gray)
    scene.addPath(rectangle, Qt.GlobalColor.black, Qt.GlobalColor.darkRed)

    for item in scene.items():
        item.setOpacity(0.15)

    scene.addPath(i, Qt.GlobalColor.green, Qt.GlobalColor.green)

    view = QGraphicsView(scene)
    view.setGeometry(0, 0, 800, 800)

    view.show()
    app.exec()
