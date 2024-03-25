#!/usr/bin/enc python3


TRANSPARENTS = [(0, 248, 0), (0, 0, 248)]
TRANSPARENT_GREEN = TRANSPARENTS[0]
TRANSPARENT_BLUE = TRANSPARENTS[1]

GAME_PATH = "../Desperados Wanted Dead or Alive"
LOG_FILENAME = "./.log"


class OriginalLevel():

    def __init__(self, level_index):
        assert 0 <= level_index <= 25
        self.index = level_index
        self.dvd = GAME_PATH
        self.dvm = GAME_PATH
        if level_index == 0:
            self.dvd += "/demo"
            self.dvm += "/demo"
        self.dvd += f"/data/levels/level_{level_index:02}.dvd"
        self.dvm += f"/data/levels/level_{level_index:02}.dvm"


LEVEL = [OriginalLevel(i) for i in range(26)]
