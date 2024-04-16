
# from .exception import PaddingError
from .stream import RWStreamable, Bytes, Bool, UChar, UShort, UInt, String, Padding, ReadStream, Version, Array
from .parser import Parser
from .geometry import Coordinate, Segment, Area
from .image import Pixmap, Pixel, Mask
from .printer import Printer, Indent

# WHITE = "#ffffff"
# RED = "#ff0000"
# GREEN = "#00ff00"
# BLUE = "#0000ff"


def p_print(*args):
    print(*args, end="")


def p_indent(i):
    print()
    p_print(" │  " * max(i - 1, 0))
    if i > 0:
        p_print(" ├─ ")


def p_title(title):
    p_print(f" ───── {title} ─────")


def hs_to_i(hex_string):
    if hex_string == "":
        return 0
    else:
        return int(hex_string[:2], 16) + hs_to_i(hex_string[2:]) * 256
