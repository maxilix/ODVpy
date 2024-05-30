import hashlib

from common import *
from config import CONFIG
from dvd import DvdParser
from odv.level import Level, BackupedLevel, original_name
from settings import *


CONFIG.load()




# for i in range(26):
#     level = OriginalLevel(i)
#     motion = level.dvd.move
#     print(f"- L{i:02} : {len(motion.w)} flags : {[(hex(a1)[2:6], hex(a2)[2:6]) for a1, a2 in motion.w]}")
#     print(f"- L{i:02} : {len(motion.w)} flags : {[(a1, a2) for a1, a2 in motion.w]}")


# level = OriginalLevel(17)
# level = Level(CONFIG.installation_path + "/" + original_name(2))
level = Level("./empty_level_02")


motion = level.dvd.move
# t = [pl.unk_int - motion.w_list[1] for pl in motion.global_path_link_list]
# print(motion.w_list)
# print(sum(t)/len(t))
# print(max(t))

# for path_lick in motion.global_path_link_list:
#     path_lick.unk_int = UInt(2**32-1)

motion.w[0] = (UInt(0x00000000), UInt(0x40400000))
# motion.w[1] = (UInt(0x00000000), UInt(0x00000000))
# motion.w[2] = (UInt(0x00000000), UInt(0x00000000))
# motion.w = [[UInt(motion.w[0][0] * 1), UInt(motion.w[0][1] * 3)]]

# for layer in motion:
#     for sublayer in layer:
#         for area in sublayer:
#             for cp in area:
#                 cp.unk_char = cp.unk_char
#                 break

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

