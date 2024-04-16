from common import *
from dvd import DvdParser
from settings import *

for level_index in range(1):
    dvd = DvdParser(original_level_filename(level_index) + ".dvd")

    print(f"  L{level_index:02} ", end="")
    motion = dvd.move
    assert motion.built
    motion._stream.debug_save(f"./extracted/section/move/{level_index}.data")
    # print(len(motion.before_ff))
    # print(bin(len(motion.before_ff))[2:].zfill(8))
    # print(motion.empty_flag, motion.active_flag)
    # print(len(motion.tail))
    # print(10*sum([sum(cp.b0) for layer in motion for sublayer in layer for area in sublayer for cp in area]))


    # print("  Done\n")
    print()

print("Done")
