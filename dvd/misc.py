from common import *

from .section import Section


class Misc(Section):
    _name = "MISC"
    _version = 6

    def _load(self, substream):
        assert substream.read(Version) == self._version

        self.b0 = substream.read(Bytes, 1)
        self.f = [substream.read(Short), substream.read(Short)]
        # cast on int32_t, then on float, and divided by 10
        # and used to create a vector ( possibly [x,y] )

        # 4 alert color
        self.color1 = substream.read(UInt)  # 96fa64(00) green
        self.color2 = substream.read(UInt)  # ffc800(00) orange
        self.color3 = substream.read(UInt)  # ff5000(00) red
        # NPC actor colors are initialized with a 4ᵉ color on 3 bytes : ffa0ff pînk

        # next, init of civilian colors with three colors on 3 bytes :
        # afffaf light green
        # a0f8ff (9fbf) very close to previous blue/cyan
        # 618eff dark blue

        self.b1 = substream.read(Bytes, 1)
        self.muwStandardViewPolygonRadius = substream.read(UShort)
        self.hearing_factor = substream.read(Float)
        self.night = substream.read(UChar)  # impact length of the vision cone, sprite darkening
        self.b2 = substream.read(Bytes, 1)

        self.c = substream.read(UInt)  # 40404000 for L00
        # (self.c >> 0x13) & 0x1f | (self.c >> 5) & 0x7e0 | (self.c << 8) & 0xf800

        if substream.read(UChar) == 1:
            self.tail = [substream.read(UShort), substream.read(UShort)]
        else:
            self.tail = []

    def _save(self, substream):
        substream.write(Version(6))
        substream.write(self.b0)
        substream.write(self.f[0])
        substream.write(self.f[1])
        substream.write(self.color1)
        substream.write(self.color2)
        substream.write(self.color3)
        substream.write(self.b1)
        substream.write(self.muwStandardViewPolygonRadius)
        substream.write(self.hearing_factor)
        substream.write(self.night)
        substream.write(self.b2)
        substream.write(self.c)
        if self.tail == []:
            substream.write(UChar(0))
        else:
            substream.write(UChar(1))
            substream.write(self.tail[0])
            substream.write(self.tail[1])


"""
all data per level:
L00: 06000000 32 0f00 f9ff 96fa6400 ffc80000 ff500000 32 f401 9a99593f 00 46 40404000 00
L01: 06000000 32 0000 0000 96fa6400 ffc80000 ff500000 32 0002 0000803f 00 1e 29211800 00
L02: 06000000 32 0000 0000 96fa6400 ffc80000 ff500000 32 0002 0000803f 00 1e 21080000 00
L03: 06000000 32 0000 0000 96fa6400 ffc80000 ff500000 32 0002 0000803f 00 00 39312100 00
L04: 06000000 32 0000 0000 96fa6400 ffc80000 ff500000 32 0002 0000803f 00 1e 31291800 00
L05: 06000000 0f 0900 fcff 96fa6400 ffc80000 ff500000 03 0002 0000803f 00 00 39292100 00
L06: 06000000 3c 0400 0200 96fa6400 ffc80000 ff500000 30 0002 3333b33f 01 4b 00000000 00
L07: 06000000 32 0000 0000 96fa6400 ffc80000 ff500000 32 0002 0000803f 00 00 29211800 00
L08: 06000000 32 1100 fbff 96fa6400 ffc80000 ff500000 32 0002 0000803f 00 00 4f372f00 00
L09: 06000000 32 0000 0000 96fa6400 ffc80000 ff500000 32 0002 9a99993f 01 3c 00000000 00
L10: 06000000 32 f6ff 1000 96fa6400 ffc80000 ff500000 32 0002 0000803f 00 1e 47363600 00
L11: 06000000 32 0e00 0200 96fa6400 ffc80000 ff500000 32 0002 cdccac3f 00 00 00000000 00
L12: 06000000 32 e6ff 0c00 96fa6400 ffc80000 ff500000 32 0002 0000803f 00 00 29211800 00
L13: 06000000 32 f7ff ffff 96fa6400 ffc80000 ff500000 32 0002 0000c03f 01 32 00000000 00
L14: 06000000 32 0000 0000 96fa6400 ffc80000 ff500000 32 c201 0000c03f 01 3c 00000000 00
L15: 06000000 32 0a00 0200 96fa6400 ffc80000 ff500000 33 0002 0000803f 00 1e 29212100 00
L16: 06000000 3c 1200 0300 96fa6400 ffc80000 ff500000 32 0002 cdccac3f 01 3c 00141400 00
L17: 06000000 46 0e00 0800 96fa6400 ffc80000 ff500000 32 0002 6666a63f 01 41 00000000 00
L18: 06000000 32 0500 feff 96fa6400 ffc80000 ff500000 32 0002 0000803f 00 1e 39211000 00
L19: 06000000 32 c0ff d5ff 96fa6400 ffc80000 ff500000 32 0002 0000803f 00 1e 472d1300 00
L20: 06000000 32 0000 0000 96fa6400 ffc80000 ff500000 32 0002 0000803f 00 1e 48270f00 00
L21: 06000000 32 0000 0000 96fa6400 ffc80000 ff500000 32 0002 0000803f 00 00 29211800 00
L22: 06000000 32 0000 0000 96fa6400 ffc80000 ff500000 32 0002 0000403f 00 01 20202000 01 8a02 e803
L23: 06000000 32 0a00 faff 96fa6400 ffc80000 ff500000 32 0002 0000803f 00 1e 301b0f00 00
L24: 06000000 32 0000 0000 96fa6400 ffc80000 ff500000 32 0002 0000803f 00 00 16070700 00
L25: 06000000 32 0000 0000 96fa6400 ffc80000 ff500000 00 0100 0000803f 00 1e 47251200 00
"""
