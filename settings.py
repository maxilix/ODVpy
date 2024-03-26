
import os


TRANSPARENTS = [(0, 248, 0), (0, 0, 248)]
TRANSPARENT_GREEN = TRANSPARENTS[0]
TRANSPARENT_BLUE = TRANSPARENTS[1]

GAME_PATH = "../Desperados Wanted Dead or Alive"


def original_level_filename(index):
    assert 0 <= index <= 25
    filename = GAME_PATH
    if index == 0:
        filename += f"{os.sep}demo"
    filename += f"{os.sep}data{os.sep}levels{os.sep}level_{index:02}"
    return filename
