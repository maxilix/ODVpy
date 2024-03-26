
import os


TRANSPARENTS = [(0, 248, 0), (0, 0, 248)]
TRANSPARENT_GREEN = TRANSPARENTS[0]
TRANSPARENT_BLUE = TRANSPARENTS[1]

GAME_PATH = "../Desperados Wanted Dead or Alive"


class OriginalLevel():

    def __init__(self, level_index):
        assert 0 <= level_index <= 25
        self.index = level_index
        self.dvd = GAME_PATH
        self.dvm = GAME_PATH
        if level_index == 0:
            self.dvd += f"{os.sep}demo"
            self.dvm += f"{os.sep}demo"
        self.dvd += f"{os.sep}data{os.sep}levels{os.sep}level_{level_index:02}.dvd"
        self.dvm += f"{os.sep}data{os.sep}levels{os.sep}level_{level_index:02}.dvm"


LEVEL = [OriginalLevel(i) for i in range(26)]
