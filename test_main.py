import hashlib

from PyQt6.QtCore import QBuffer, QByteArray
from PyQt6.QtGui import QColor, QPen, QBrush, QImage, qRgb, qRed, qGreen, qBlue, QPolygonF, QVector2D

from common import *
from config import CONFIG
from dvd import DvdParser
from dvd.move import Obstacle
from odv.level import Level, BackupedLevel, InstalledLevel
from odv.pathfinder import PathFinders
from settings import *

CONFIG.load()

"""
w[0] = obstacle avoidance distance, on foot
     = [x distance, y distance]
     
w[3] or w[4] = obstacle avoidance distance, on horseback
             = [x distance, y distance]
             
             
        human                    monkey       horse      

L00   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L01   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L02   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L03   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L04   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L05   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L06   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L07   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L08   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L09   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L10   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L11   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L12   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L13   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L14   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L15   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L16   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L17   [6.0, 3.0]  [11.0, 6.0]  [3.0, 2.0]  [19.0, 11.0]
L18   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L19   [6.0, 3.0]  [11.0, 6.0] 
L20   [6.0, 3.0]  [11.0, 6.0]  [3.0, 2.0]  [19.0, 11.0]
L21   [6.0, 3.0]  [11.0, 6.0]  [3.0, 2.0]  [19.0, 11.0]
L22   [6.0, 3.0]  [11.0, 6.0]  [3.0, 2.0]  [19.0, 11.0]
L23   [6.0, 3.0]  [11.0, 6.0]  [3.0, 2.0]  [19.0, 11.0]
L24   [6.0, 3.0]  [11.0, 6.0]  [3.0, 2.0]
L25   [6.0, 3.0]  [11.0, 6.0] 
"""


def draw_obstacle_on_dvm(level, layer_index=0):
    if level.dvd.move.loaded_areas is False:
        level.dvd.move.load(only_areas=True)
    pen = QPen(QColor(255, 0, 0, 128))
    pen.setWidthF(0.5)
    brush = QBrush(QColor(255, 0, 0, 32))
    for sublayer in level.dvd.move[layer_index]:
        for obstacle in sublayer:
            level.dvm.draw(obstacle.QPolygonF(), pen, brush)


def signed_area(polygon: QPolygonF):
    area = 0.0
    num_points = polygon.size()

    for i in range(num_points):
        current_point = QVector2D(polygon[i])
        next_point = QVector2D(polygon[(i + 1) % num_points])
        area += (next_point.x() - current_point.x()) * (next_point.y() + current_point.y())

    print(area)
    return area <= 0.0


# level = Level("./dev/empty_level/empty_level_02")
# level = Level("../Missions/DemoMod_L00/level_00")
# level = InstalledLevel(2)
# for level_index in range(1):

level = BackupedLevel(6)
level.dvd.move.load()
motion = level.dvd.move
# print(len(motion))

# for layer in motion:
#     for sublayer in layer:
#         assert sublayer.main.clockwise
#         for obstacle in sublayer:
#             assert obstacle.clockwise

# o = motion[0][0].main
# o = Obstacle([UPoint(0, 0),
#               UPoint(1, 0),
#               UPoint(1, 1),
#               UPoint(0, 1), ])
# o.clockwise = False
# for i in range(len(o)):
#     print(o[i], o.angle_at(i))


pf1 = motion.pathfinders
pf2 = PathFinders.build_from_motion(motion, [])

for i in range(len(pf1.crossing_point_list)):
    for j in range(len(pf1.crossing_point_list[i])):
        for k in range(len(pf1.crossing_point_list[i][j])):
            # assert len(pf1.crossing_point_list[i][j][k]) == len(pf2.crossing_point_list[i][j][k])
            for cp1_index in range(len(pf1.crossing_point_list[i][j][k])):
                cp2_index = [c.position for c in pf2.crossing_point_list[i][j][k]].index(pf1.crossing_point_list[i][j][k][cp1_index].position)
                cp1 = pf1.crossing_point_list[i][j][k][cp1_index]
                cp2 = pf2.crossing_point_list[i][j][k][cp2_index]
                assert cp1.position == cp2.position
                assert cp1.vector_to_next == cp2.vector_to_next
                assert cp1.vector_from_previous == cp2.vector_from_previous


                # cp1 = pf1.crossing_point_list[i][j][k][cp_index]
                # cp2 = pf2.crossing_point_list[i][j][k][cp_index]
                # if cp1.position != cp2.position:


# level.insert_in_game()
