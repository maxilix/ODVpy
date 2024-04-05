from common import *
from dvd import DvdParser
from settings import *

dvd = DvdParser(original_level_filename(0) + ".dvd")

dvd._move.print_structured_data()