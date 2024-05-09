import hashlib

from common import *
from config import CONFIG
from dvd import DvdParser
from odv.level import Level
from settings import *



CONFIG.load()


# for level_index in range(26):

# filename_we = original_level_filename_we(level_index)
level = Level("./empty_level_02")

motion = level.dvd.move

# print(motion[0][0][103][1].point)
# motion[0][0][103][1].point = Coordinate(1000, 300)
# r = []
# for layer in motion:
#     for sublayer in layer:
#         for area in sublayer:
#             for cp in area:
#                 r.append(cp.unk_short)
#
# rr = [0,0,0,0]
# for i in range(0, 4):
#     t = [e[i] for e in r if e[i] < 32767]
#     rr[i] = sum(t)/len(t)
#
# print(rr)

# print(motion[0][0][103][1].unk_short)

# level.dvd.save_to_file("test_level_02.dvd")
# level.insert_in_game()

