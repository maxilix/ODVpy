from functools import reduce

from PyQt6.QtCore import QRectF, Qt, QPointF, QMarginsF
from PyQt6.QtGui import QPolygonF, QPen, QBrush, QPainterPath, QPainter, QPolygon
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QApplication


def area(polygon: QPolygon | QPolygonF) -> float:
    rop = 0.0
    n = len(polygon)

    for i in range(n):
        current_point = polygon[i]
        next_point = polygon[(i + 1) % n]
        rop += (next_point.x() - current_point.x()) * (next_point.y() + current_point.y())

    return abs(rop / 2)




def rect_at(point: QPointF, w: (float, float), direction: int) -> QPolygonF:
    assert direction in [1, 2, 4, 8]
    if direction & 0b1001:
        x = point.x() - w[0]
    else:
        x = point.x()
    if direction & 0b0011:
        y = point.y() - w[1]
    else:
        y = point.y()
    return QPolygonF(QRectF(x, y, w[0], w[1]))


p1 = []
p1.append(QPointF(100, 100))
p1.append(QPointF(200, 100))
p1.append(QPointF(200, 150))
p1.append(QPointF(150, 150))  #
p1.append(QPointF(150, 200))
p1.append(QPointF(100, 200))
poly1 = QPolygonF(p1 + p1[:1])

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
poly2 = QPolygonF(p2 + p2[:1])

# path = QPainterPath()
# path.addPolygon(triangle1)
# path.addPolygon(triangle2)
# path.closeSubpath()
#
# rectangle = QPainterPath()
# rectangle.addRect(rect_at(p1[0], (400, 400), 4))
#
# i = path.intersected(rectangle)
# polys = i.toFillPolygons()
# print(polys)
# for poly in polys:
#     for point in poly:
#         print(point)
#     print()
main = poly1
main_bb_marge = QPolygonF(poly1.boundingRect().marginsAdded(QMarginsF(10, 10, 10, 10)))
main_obstacle = main_bb_marge.subtracted(poly1)

rectangle = rect_at(p1[0], (50, 50), 4)
i = main.united(rectangle)
print(area(i), area(poly1))

# i = main_obstacle.intersected(rectangle)
# for p in i:
#
# print(area(i))




if __name__ == '__main__':
    app = QApplication([])
    pen = QPen(Qt.GlobalColor.black)
    brush = QBrush(Qt.GlobalColor.gray)
    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, 800, 800)

    scene.addPolygon(main, Qt.GlobalColor.black, Qt.GlobalColor.gray,)
    scene.addPolygon(rectangle, Qt.GlobalColor.black, Qt.GlobalColor.darkRed)
    scene.addPolygon(i, Qt.GlobalColor.green, Qt.GlobalColor.green)

    for item in scene.items():
        item.setOpacity(0.15)


    view = QGraphicsView(scene)
    view.setGeometry(0, 0, 800, 800)

    view.show()
    app.exec()
