import hashlib

from common import *
from config import CONFIG
from dvd import DvdParser
from odv.level import Level
from settings import *



CONFIG.load()


# for level_index in range(26):

# filename_we = original_level_filename_we(level_index)
# level = Level("/home/maxe/PycharmProjects/Desperados Wanted Dead or Alive/data/levels/level_02")
# motion = level.dvd.move
#
# r = []
# for layer in motion:
#     for sublayer in layer:
#         for area in sublayer:
#             for cp in area:
#                 r.append(cp.unk_short)
#
# rr = [0,0,0,0]
# for i in range(0, 4):
#
#     t = [e[i] for e in r]
#     rr[i] = sum(t)/len(t)
#
# print(rr)

