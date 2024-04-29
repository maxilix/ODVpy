
"""
all data per level:
                                                                                 nuit
     [version] [    unk0    ] [            same            ] [     unk1      ] 3f TF [       unk2              ]
L00: 0600 0000 32 0f 00 f9 ff 96 fa64 00ff c800 00ff 5000 00 32 f4 01 9a 99 59 3f 00 46 40 40 40 00 06 				demo   jour
L01: 0600 0000 32 00 00 00 00 96 fa64 00ff c800 00ff 5000 00 32 00 02 00 00 80 3f 00 1e 29 21 18 00 00 				tuto   jour     id07
L02: 0600 0000 32 00 00 00 00 96 fa64 00ff c800 00ff 5000 00 32 00 02 00 00 80 3f 00 1e 21 08 00 00 00 				       soir
L03: 0600 0000 32 00 00 00 00 96 fa64 00ff c800 00ff 5000 00 32 00 02 00 00 80 3f 00 00 39 31 21 00 00 				tuto nuit/matin
L04: 0600 0000 32 00 00 00 00 96 fa64 00ff c800 00ff 5000 00 32 00 02 00 00 80 3f 00 1e 31 29 18 00 00 				       jour
L05: 0600 0000 0f 09 00 fc ff 96 fa64 00ff c800 00ff 5000 00 03 00 02 00 00 80 3f 00 00 39 29 21 00 00 				tuto soir/nuit
L06: 0600 0000 3c 04 00 02 00 96 fa64 00ff c800 00ff 5000 00 30 00 02 33 33 b3 3f 01 4b 00 00 00 00 00 				       nuit
L07: 0600 0000 32 00 00 00 00 96 fa64 00ff c800 00ff 5000 00 32 00 02 00 00 80 3f 00 00 29 21 18 00 00 				tuto   jour     id01
L08: 0600 0000 32 11 00 fb ff 96 fa64 00ff c800 00ff 5000 00 32 00 02 00 00 80 3f 00 00 4f 37 2f 00 00 				     jour/soir
L09: 0600 0000 32 00 00 00 00 96 fa64 00ff c800 00ff 5000 00 32 00 02 9a 99 99 3f 01 3c 00 00 00 00 00 				       nuit
L10: 0600 0000 32 f6 ff 10 00 96 fa64 00ff c800 00ff 5000 00 32 00 02 00 00 80 3f 00 1e 47 36 36 00 00 				       jour     id14?
L11: 0600 0000 32 0e 00 02 00 96 fa64 00ff c800 00ff 5000 00 32 00 02 cd cc ac 3f 00 00 00 00 00 00 00 				       soir                      0 building
L12: 0600 0000 32 e6 ff 0c 00 96 fa64 00ff c800 00ff 5000 00 32 00 02 00 00 80 3f 00 00 29 21 18 00 00 				       jour
L13: 0600 0000 32 f7 ff ff ff 96 fa64 00ff c800 00ff 5000 00 32 00 02 00 00 c0 3f 01 32 00 00 00 00 00 				       nuit
L14: 0600 0000 32 00 00 00 00 96 fa64 00ff c800 00ff 5000 00 32 c2 01 00 00 c0 3f 01 3c 00 00 00 00 00 				tuto   nuit     id10?
L15: 0600 0000 32 0a 00 02 00 96 fa64 00ff c800 00ff 5000 00 33 00 02 00 00 80 3f 00 1e 29 21 21 00 00 				       jour     id16
L16: 0600 0000 3c 12 00 03 00 96 fa64 00ff c800 00ff 5000 00 32 00 02 cd cc ac 3f 01 3c 00 14 14 00 00 				       nuit     id15
L17: 0600 0000 46 0e 00 08 00 96 fa64 00ff c800 00ff 5000 00 32 00 02 66 66 a6 3f 01 41 00 00 00 00 00 				       nuit
L18: 0600 0000 32 05 00 fe ff 96 fa64 00ff c800 00ff 5000 00 32 00 02 00 00 80 3f 00 1e 39 21 10 00 00 				       jour     id21
L19: 0600 0000 32 c0 ff d5 ff 96 fa64 00ff c800 00ff 5000 00 32 00 02 00 00 80 3f 00 1e 47 2d 13 00 00 				     jour/soir           vent
L20: 0600 0000 32 00 00 00 00 96 fa64 00ff c800 00ff 5000 00 32 00 02 00 00 80 3f 00 1e 48 27 0f 00 00 				tuto jour/soir
L21: 0600 0000 32 00 00 00 00 96 fa64 00ff c800 00ff 5000 00 32 00 02 00 00 80 3f 00 00 29 21 18 00 00 				       soir     id18
L22: 0600 0000 32 00 00 00 00 96 fa64 00ff c800 00ff 5000 00 32 00 02 00 00 40 3f 00 01 20 20 20 00 01 8a 02 e8 03 	       soir              pluie
L23: 0600 0000 32 0a 00 fa ff 96 fa64 00ff c800 00ff 5000 00 32 00 02 00 00 80 3f 00 1e 30 1b 0f 00 00 				     matin/jour 
L24: 0600 0000 32 00 00 00 00 96 fa64 00ff c800 00ff 5000 00 32 00 02 00 00 80 3f 00 00 16 07 07 00 00 				      (jour?)            grotte
L25: 0600 0000 32 00 00 00 00 96 fa64 00ff c800 00ff 5000 00 00 01 00 00 00 80 3f 00 1e 47 25 12 00 00 				      (jour?)            grotte


same (96fa6400ffc80000ff500000) to base 10 : 150 250 100 0 255 200 0 0 255 80 0 0

level_map size : 
L00 00 0a (2560) x 40 06 (1600)
L01 40 08 (2112) x 40 04 (1088)
L02 40 06 (1600) x 40 09 (2368)
L03 80 07 (1920) x 80 03 (896)
L04 00 0a (2560) x 80 05 (1408)
L05 00 05 (1280) x 00 03 (768)
L06 40 09 (2368) x 80 07 (1920)
L07 40 08 (2112) x 40 04 (1088)
L08 c0 08 (2240) x 40 06 (1600)
L09 40 06 (1600) x c0 05 (1472)
L10 40 06 (1600) x c0 08 (2240)
L11 00 05 (1280) x 40 09 (2368)
L12 c0 08 (2240) x c0 06 (1728)
L13 40 09 (2368) x c0 06 (1728)
L14 40 06 (1600) x 80 05 (1408)
L15 c0 08 (2240) x 40 06 (1600)
L16 c0 08 (2240) x 40 06 (1600)
L17 40 06 (1600) x 00 04 (1024)
L18 00 0a (2560) x c0 06 (1728)
L19 00 05 (1280) x c0 08 (2240)
L20 00 05 (1280) x 00 03 (768)
L21 00 0a (2560) x c0 06 (1728)
L22 80 09 (2432) x 00 07 (1792)
L23 80 09 (2432) x 40 07 (1856)
L24 80 0b (2944) x 80 06 (1664)
L25 00 04 (1024) x c0 03 (960)

"""

from common import *

from .section import Section


class Miscellaneous(Section):
    section_index = 0  # MISC

    def _load(self, substream):
        version = substream.read(Version)
        assert version == 6
        self.unk0 = substream.read(Bytes, 5)
        substream.read(Padding, 12, pattern=b'\x96\xfa\x64\x00\xff\xc8\x00\x00\xff\x50\x00\x00')
        self.unk1 = substream.read(Bytes, 6)
        substream.read(Padding, 1, pattern=b'\x3f')
        self.night = substream.read(UChar)  # length of the vision cone, sound sensitivity, sprite darkening
        # WARNING stream.read_raw() should not be used, because it read all and Section.load() checks whether the
        # entire substream has been consumed.
        # if you know what you're reading, you should know the length of the reading
        self.unk2 = Bytes(substream.read_raw())  # 10 bytes for level 22, 6 bytes for others, WHY?

    def _save(self, substream):
        substream.write(Version(6))
        substream.write(self.unk0)
        substream.write(Padding(b'\x96\xfa\x64\x00\xff\xc8\x00\x00\xff\x50\x00\x00'))
        substream.write(self.unk1)
        substream.write(Padding(b'\x3f'))
        substream.write(self.night)
        substream.write(self.unk2)

