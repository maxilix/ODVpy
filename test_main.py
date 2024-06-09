import hashlib

from PyQt6.QtCore import QBuffer, QByteArray
from PyQt6.QtGui import QColor, QPen, QBrush, QImage, qRgb, qRed, qGreen, qBlue

from common import *
from config import CONFIG
from dvd import DvdParser
from odv.level import Level, BackupedLevel, InstalledLevel
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


# for i in range(26):
#     level = BackupedLevel(i)
#     # motion = level.dvd.move
#     # print(f"L{i:02}   ", end="")
#     # l = [pl.link_length for pl in motion.global_path_link_list]
#     # print(f"{min(l):6.3f} {max(l):8.3f}")
#     misc = level.dvd.misc
#     print(hex(misc.c))
#
# exit()







level = Level("./dev/empty_level/empty_level_02")
# level = Level("../Missions/DemoMod_L00/level_00")
# level = InstalledLevel(2)
# level = BackupedLeve  l(5)

motion = level.dvd.move
# t = [pl.unk_int - motion.w_list[1] for pl in motion.global_path_link_list]
# print(motion.w_list)
# print(sum(t)/len(t))
# print(max(t))


# for v in motion.w:
#     print(v)
# exit()

# motion[0][0][103][2][5].unk_obj_list[0].t1 = []
# motion[0][0][103][2][5].unk_obj_list[0].t1 = []
# motion[0][0][103][2][5].unk_obj_list[0].t2 = []
# motion[0][0][103][10][11].unk_obj_list[0].t1 = []
# motion[0][0][103][10][11].unk_obj_list[0].t2 = []
# motion[0][0][103][10][12].unk_obj_list[0].t1 = []
# motion[0][0][103][10][12].unk_obj_list[0].t2 = []
# motion[0][0][41][4][6].unk_obj_list[0].t1 = []
# motion[0][0][41][4][6].unk_obj_list[0].t2 = []

index = motion.get_ff_index()
motion.global_unk_obj_list[0].t1 = [UChar(1)]
motion.global_unk_obj_list[0].t2 = [UChar(1)]

for i, layer in enumerate(motion):
    for j, sublayer in enumerate(layer):
        for k, area in enumerate(sublayer):
            for l, cp in enumerate(area):
                for m, pl in enumerate(cp):
                    pl.global_unk_obj_index_list[0] = UShort(0)

#
# exit()

# motion.w = [[UFloat(6.0),  UFloat(3.0)],
#             [UFloat(11.0), UFloat(6.0)],
#             [UFloat(3.0),  UFloat(2.0)],
#             [UFloat(19.0), UFloat(11.0)]]


# motion.w[0] = [UFloat(1.0), UFloat(1.0)]
# motion.w[1] = [UFloat(25.0), UFloat(25.0)]
# motion.w[2] = [UFloat(11.0), UFloat(6.0)]
# motion.w[2] = [UFloat(40.0), UFloat(30.0)]
# motion.w[3] = [UFloat(40.0), UFloat(30.0)]

for sublayer in motion[0]:
    for area in sublayer[1:]:
        poly = area.QPolygonF()
        level.dvm.draw(poly, QPen(QColor(255, 0, 0)), QBrush(QColor(255, 0, 0, 64)))

# for layer in motion[1:-1]:
#     for sublayer in layer:
#         poly = sublayer[0].QPolygonF()
#         level.dvm.draw(poly, QPen(QColor(160, 200, 40)), QBrush(QColor(160, 200, 40, 64)))


# for layer in motion:
#     for sublayer in layer:
#         for area in sublayer:
#             for cp in area:
#                 cp.unk_char = [cp.unk_char[0],
#                                cp.unk_char[1],
#                                cp.unk_char[0],
#                                cp.unk_char[2]]


# for pl in motion.global_path_link_list:
#     pl.global_unk_obj_index_list = pl.global_unk_obj_index_list

# for unk_obj in motion.global_unk_obj_list:
#     n = len(unk_obj.unk_tab1)
#     unk_obj.unk_tab1 = [UChar(4)]*n
#     unk_obj.unk_tab2 = [UChar(4)]*n


# cp = motion[0][0][102][1]
# cp.unk_char = [UChar(9), UChar(6), UChar(6)]
# for w0, w1 in motion.w:
#     print(f"{bin(w0)[2:].zfill(32)}   {bin(w1)[2:].zfill(32)}")

level.insert_in_game()

