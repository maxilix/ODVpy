import hashlib

from common import *
from config import CONFIG
from dvd import DvdParser
from odv.level import Level
from settings import *



CONFIG.load()


for level_index in range(25):

    level = Level(f"/home/maxe/PycharmProjects/Desperados Wanted Dead or Alive/data/levels/level_{level_index+1:02}")
    motion = level.dvd.move

    r = []
    for layer in motion:
        for sublayer in layer:
            for area in sublayer:
                for cp in area:
                    r.append(cp.unk_short)

    rr = [0,0,0,0]
    for i in range(0, 4):

        t = [e[i] for e in r]
        rr[i] = round(sum(t)/len(t),1)

    print(rr)

