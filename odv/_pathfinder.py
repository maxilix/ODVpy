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



p1 = QPointF(150, 150)
p2 = QPointF(200, 100)
p3 = QPointF(200, 150)

p4 = QPointF(150, 400)
p5 = QPointF(150, 500)
p6 = QPointF(200, 300)

r1 = rect_at(QPointF(100,100), (200,100),4)
r1_p = [r1.topLeft(), r1.topRight(), r1.bottomRight(), r1.bottomLeft()]

r2 = rect_at(QPointF(200,400), (200,100),4)
r2_p = [r2.topLeft(), r2.topRight(), r2.bottomRight(), r2.bottomLeft()]

c1 = r1.center()
c2 = r2.center()
match QLineF(c1, c2).angle():
    case 0:
        return

bb = r1.united(r2)
if bb.topLeft() == r1.topLeft():
    p = QPolygonF([r1.topLeft(), r1.topRight()])



# r = QRectF()
# print(isinstance(r, QPolygonF))
# exit()

# b = boundaries(poly1)
#
# line1 = QLineF(QPointF(100, 400), QPointF(100, 100))
# line2 = QLineF(QPointF(200, 100), QPointF(500, 100))
#
#
# print(line1)


if __name__ == '__main__':
    app = QApplication([])
    pen = QPen(Qt.GlobalColor.black)
    pen.setWidthF(3)

    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, 800, 800)

    scene.addPolygon(poly1)
    scene.addPolygon(poly2)
    scene.addPolygon(poly3)
    # for b_line in b:
    #     scene.addLine(b_line, Qt.GlobalColor.green)
    # scene.addLine(line1, pen)
    # scene.addLine(line2, pen)
    # for item in scene.items():
    #     item.setOpacity(0.15)
    # scene.addPath(line_path, Qt.GlobalColor.green, Qt.GlobalColor.green)
    # scene.addPath(i, Qt.GlobalColor.red, Qt.GlobalColor.red)



    view = QGraphicsView(scene)
    view.setGeometry(0, 0, 800, 800)

    view.show()
    app.exec()
