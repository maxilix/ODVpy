import hashlib

from common import *
from config import CONFIG
from dvd import DvdParser
from settings import *
import backup

from dev.utils import print_original_hash_dict


CONFIG.load()


# for level_index in range(26):

# filename_we = original_level_filename_we(level_index)
filename_we = ("./level_02")
dvd = DvdParser(filename_we + ".dvd")

motion = dvd.move

