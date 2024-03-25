#!/usr/bin/enc python3



WHITE = "#ffffff"
RED   = "#ff0000"
GREEN = "#00ff00"
BLUE  = "#0000ff"




from .exception import PaddingError
from .stream import ReadableFromStream, Bytes, Bool, UChar, UShort, UInt, String, Padding, ByteStream
from .parser import Parser
from .geometry import Coordinate, Segment, Area
from .image import Pixmap, Pixel, Mask
