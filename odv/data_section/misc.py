from odv.common import *
from odv.odv_object import OdvObject

from odv.section import Section


class Misc(Section, OdvObject):
    _section_id = 0
    _section_version = 6

    def _load(self, substream: ReadStream, level) -> None:
        # Unk
        self.unk0 = substream.read(Bytes, 1)

        # wind direction and speed
        # affect Doc's balloon, but not the dotted preview
        self.wind_vector = [substream.read(Short), substream.read(Short)]

        # 4 alert colors
        self.color1 = substream.read(UInt)  # 96fa64(00) green
        self.color2 = substream.read(UInt)  # ffc800(00) orange
        self.color3 = substream.read(UInt)  # ff5000(00) red
        # NPC actor colors are initialized with a 4ᵉ color on 3 bytes : ffa0ff pînk

        # next, init of civilian colors with three colors on 3 bytes :
        # afffaf light green
        # a0f8ff (9fbf) very close to previous blue/cyan
        # 618eff dark blue

        # Unk
        self.unk1 = substream.read(Bytes, 1)

        # Vision cone standard length (muwStandardViewPolygonRadius)
        # does not apply to all enemies, perhaps some have non-standard viewing angles
        self.view_length = substream.read(UShort)

        # Hearing factor affects sound perception distance
        # Min at L22 (0.75) and max at L13 (1.5)
        self.hearing_factor = substream.read(Float)

        # Night boolean
        # impact length of the vision cone, sprite darkening
        self.night = substream.read(UChar)

        # Unk
        self.unk2 = substream.read(Bytes, 1)

        # Probably a color
        self.c = substream.read(UInt)  # 40404000 for L00
        # (self.c >> 0x13) & 0x1f | (self.c >> 5) & 0x7e0 | (self.c << 8) & 0xf800


        # Only L22 (with rain) has a tail [650, 1000]
        # thunder with rain, integers [a,b] control flash frequency
        # regular if a == b
        #   [1000, 1000] => ~50s
        #   [ 100,  100] => ~ 5s
        #   maybe a number of ticks, at 20tick/s
        # no flash if b < a
        # some randomization else
        #   [100, 10000] => between 7s and 17s

        if substream.read(UChar) == 1:
            self.tail = [substream.read(UShort), substream.read(UShort)]
        else:
            self.tail = []

    def _save(self, substream: WriteStream) -> None:
        substream.write(self.unk0)
        # print(f"write {self.wind_vector}")
        substream.write(Short(self.wind_vector[0]))
        substream.write(Short(self.wind_vector[1]))
        substream.write(self.color1)
        substream.write(self.color2)
        substream.write(self.color3)
        substream.write(self.unk1)
        print(f"View length = {self.view_length}")
        substream.write(UShort(self.view_length))
        substream.write(Float(self.hearing_factor))
        substream.write(UChar(self.night))
        substream.write(self.unk2)
        substream.write(self.c)
        print(f"Tail = {self.tail}")
        if self.tail == []:
            substream.write(UChar(0))
        else:
            substream.write(UChar(1))
            substream.write(UShort(self.tail[0]))
            substream.write(UShort(self.tail[1]))


"""
all data per level:
L00: 32   0f00 f9ff   96fa6400 ffc80000 ff500000   32   f401 (500)   9a99593f (0.85)   00   46   40404000   00
L01: 32   0000 0000   96fa6400 ffc80000 ff500000   32   0002 (512)   0000803f (1.00)   00   1e   29211800   00
L02: 32   0000 0000   96fa6400 ffc80000 ff500000   32   0002 (512)   0000803f (1.00)   00   1e   21080000   00
L03: 32   0000 0000   96fa6400 ffc80000 ff500000   32   0002 (512)   0000803f (1.00)   00   00   39312100   00
L04: 32   0000 0000   96fa6400 ffc80000 ff500000   32   0002 (512)   0000803f (1.00)   00   1e   31291800   00
L05: 0f   0900 fcff   96fa6400 ffc80000 ff500000   03   0002 (512)   0000803f (1.00)   00   00   39292100   00
L06: 3c   0400 0200   96fa6400 ffc80000 ff500000   30   0002 (512)   3333b33f (1.40)   01   4b   00000000   00
L07: 32   0000 0000   96fa6400 ffc80000 ff500000   32   0002 (512)   0000803f (1.00)   00   00   29211800   00
L08: 32   1100 fbff   96fa6400 ffc80000 ff500000   32   0002 (512)   0000803f (1.00)   00   00   4f372f00   00
L09: 32   0000 0000   96fa6400 ffc80000 ff500000   32   0002 (512)   9a99993f (1.20)   01   3c   00000000   00
L10: 32   f6ff 1000   96fa6400 ffc80000 ff500000   32   0002 (512)   0000803f (1.00)   00   1e   47363600   00
L11: 32   0e00 0200   96fa6400 ffc80000 ff500000   32   0002 (512)   cdccac3f (1.35)   00   00   00000000   00
L12: 32   e6ff 0c00   96fa6400 ffc80000 ff500000   32   0002 (512)   0000803f (1.00)   00   00   29211800   00
L13: 32   f7ff ffff   96fa6400 ffc80000 ff500000   32   0002 (512)   0000c03f (1.50)   01   32   00000000   00
L14: 32   0000 0000   96fa6400 ffc80000 ff500000   32   c201 (450)   0000c03f (1.50)   01   3c   00000000   00
L15: 32   0a00 0200   96fa6400 ffc80000 ff500000   33   0002 (512)   0000803f (1.00)   00   1e   29212100   00
L16: 3c   1200 0300   96fa6400 ffc80000 ff500000   32   0002 (512)   cdccac3f (1.35)   01   3c   00141400   00
L17: 46   0e00 0800   96fa6400 ffc80000 ff500000   32   0002 (512)   6666a63f (1.30)   01   41   00000000   00
L18: 32   0500 feff   96fa6400 ffc80000 ff500000   32   0002 (512)   0000803f (1.00)   00   1e   39211000   00
L19: 32   c0ff d5ff   96fa6400 ffc80000 ff500000   32   0002 (512)   0000803f (1.00)   00   1e   472d1300   00
L20: 32   0000 0000   96fa6400 ffc80000 ff500000   32   0002 (512)   0000803f (1.00)   00   1e   48270f00   00
L21: 32   0000 0000   96fa6400 ffc80000 ff500000   32   0002 (512)   0000803f (1.00)   00   00   29211800   00
L22: 32   0000 0000   96fa6400 ffc80000 ff500000   32   0002 (512)   0000403f (0.75)   00   01   20202000   01 8a02 e803
L23: 32   0a00 faff   96fa6400 ffc80000 ff500000   32   0002 (512)   0000803f (1.00)   00   1e   301b0f00   00
L24: 32   0000 0000   96fa6400 ffc80000 ff500000   32   0002 (512)   0000803f (1.00)   00   00   16070700   00
L25: 32   0000 0000   96fa6400 ffc80000 ff500000   00   0100 (  1)   0000803f (1.00)   00   1e   47251200   00
"""
