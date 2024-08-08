import hashlib

from PyQt6.QtCore import QBuffer, QByteArray, QRectF, QLineF, QPointF, QSizeF
from PyQt6.QtGui import QColor, QPen, QBrush, QImage, qRgb, qRed, qGreen, qBlue, QPolygonF, QVector2D, QPixmap
from PyQt6.QtWidgets import QLabel, QApplication

from common import *
from config import CONFIG
from dvd import DvdParser
from dvd.bond import BondLink
from dvd.move import Obstacle, Sublayer
from odv.level import Level, BackupedLevel, InstalledLevel
from odv.pathfinder import PathFinder, CrossingPoint
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

"""
L00 
nb_cb = 781
nb_link = 7676
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


def is_line_strictly_in_sublayer(line: QLineF, sublayer: Sublayer) -> bool:

    center = line.center()
    if not sublayer.allow_path.contains(center):
        print(f"c {center.x():8.3f} {center.y():8.3f}   ", end="")
        return False

    for bound in sublayer.boundaries:
        # if line == bound or line.p1() == bound.p2() and line.p2() == bound.p1():
        #     return True
        if (i := bound.intersects(line))[0] == QLineF.IntersectionType.BoundedIntersection:
            if i[1] != line.p1() and i[1] != line.p2():
                print(f"i {i[1].x():8.3f} {i[1].y():8.3f}   ", end="")
                return False
        # else:
        #     print(i[0])
    return True


# level = Level("./dev/empty_level/empty_level_19")
# level = Level("../Missions/03_Red_River/level_03")
# level = Level("../Missions/00_All_Character/level_00")
# level = InstalledLevel(2)
level = BackupedLevel(0)
level.dvm.load_another_image("../Missions/Level_28.png")
# for level_index in range(26):
#     print(f"Level {level_index}")

# move = level.dvd.move

# buil = level.dvd.buil
# print(len(buil.building_list), len(buil.special_door_list))
# for sd in buil.special_door_list:
#     print(sd.accesses[0].point, sd.accesses[0].area_global_id, sd.accesses[0].layer_id)
#     print(sd.accesses[1].point, sd.accesses[1].area_global_id, sd.accesses[1].layer_id)
#     print(sd.accesses[2].point, sd.accesses[2].area_global_id, sd.accesses[2].layer_id)
#     print()

# exit()


# for sublayer in motion[0]:
#     for area in sublayer.obstacles:
#         level.dvm.draw(area.poly, QPen(QColor(255, 90, 40, 128)), QBrush(QColor(255, 90, 40, 32)))



level.insert_in_game()
