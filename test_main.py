import hashlib

from common import *
from config import CONFIG
from dvd import DvdParser
from settings import *
import backup

from dev.utils import print_original_hash_dict


CONFIG.load()


for level_index in range(26):

    filename_we = original_level_filename_we(level_index)
    dvd = DvdParser(filename_we + ".dvd")
    sd1 = dvd._move._data
    # print(len(sd1))
    motion = dvd.move
    motion.save()
    motion.load()
    sd2 = dvd._move._data
    # print(len(sd2))
    assert sd1 == sd2


    pass
    # with open(filename, 'rb') as file:
    #     print(f"\"{hashlib.file_digest(file, 'sha256').hexdigest()}\",")



    # print("---------------------------------------------------")
    # print(f"  L{level_index:02} ")
    # assert motion.built
    # print(motion.empty_flag, motion.active_flag)

    # print(len(motion.before_ff))
    # print(motion.before_ff)
    # print(f"      size={len(motion.tail) + len(motion.before_ff) + 1:>6}")
    # print(f"nb_unk_obj={motion.nb_unk_obj:>6}")
    # print(f" sum_of_b0={sum([sum(cp.b0) for layer in motion for sublayer in layer for area in sublayer for cp in area]):>6}")
    # print()
    # print(f"len before ff / 8 = {len(motion.before_ff)/8}")
    # print(f"len after ff / 4  = {len(motion.tail)/4}")
    # print(f"len after ff / nb_unk_obj = {len(motion.tail)/motion.nb_unk_obj}")
    # print()
    # print(f"    w={motion.w}")
    # nb_cp = len([cp for layer in motion for sublayer in layer for area in sublayer for cp in area])
    # print(f"nb_cp={nb_cp}")
    # print(f"times={motion.w*nb_cp}")



    # print("  Done\n")
    # print()

# print("Done")
