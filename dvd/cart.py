from typing import Self

from common import *
from odv.odv_object import OdvObject, OdvObjectIterable

from .section import Section

class MobileElement(OdvObject):

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent) -> Self:
        rop = cls(parent)

        return rop

    def to_stream(self, stream: WriteStream) -> None:
        pass



class Cart(Section, OdvObjectIterable):
    _section_name = "CART"
    _section_version = 5

    def _load(self, substream: ReadStream) -> None:
        tail = substream.read_raw().hex(" ", 1)
        print(tail)
        exit()
        nb_mobile = substream.read(UShort)
        for _ in range(nb_mobile):
            self.add_child(substream.read(MobileElement, parent=self))


    def _save(self, substream: WriteStream) -> None:
        pass


"""
L1 and L7
01 00

06 
00 01 10 07 00 4c 65 76 65 6c 30 31 18 00 4c 65 76 65 6c 20 30 31 20 2d 20 77 61 67 6f 6e 20 63 68 61 72 62 6f 6e cd fe 44 ff 00 00 00 01
01 01 10 07 00 4c 65 76 65 6c 30 31 0f 00 4c 65 76 65 6c 20 30 31 20 2d 20 6c 6f 63 6f 27 ff 54 ff 00 00 00 01
01 01 10 07 00 4c 65 76 65 6c 30 31 15 00 4c 65 76 65 6c 20 30 31 20 2d 20 6c 6f 63 6f 20 72 6f 75 65 73 3b ff 9f ff 00 00 00 01
01 01 10 07 00 4c 65 76 65 6c 30 31 12 00 4c 65 76 65 6c 20 30 31 20 2d 20 77 61 67 6f 6e 20 31 c4 fd b9 fe 00 00 00 01
01 01 10 07 00 4c 65 76 65 6c 30 31 12 00 4c 65 76 65 6c 20 30 31 20 2d 20 77 61 67 6f 6e 20 32 1f fd 6b fe 00 00 00 01
01 01 10 07 00 4c 65 76 65 6c 30 31 12 00 4c 65 76 65 6c 20 30 31 20 2d 20 77 61 67 6f 6e 20 33 9c fc 51 fe 00 00 00 01

01 05 00 04 00 ba 99 35 c3 90 c6 de c2 00 00 00 
00 00 00 80 42 80 ca ed bf e2 63 e7 c1 00 00 00 
00 00 00 58 42 18 af 0e c2 f8 a8 95 c0 00 00 00 
00 00 00 58 42 eb 69 57 c3 28 48 ae c2 00 00 00 
00 00 00 80 42 eb 69 57 c3 00 00 00 00 90 c6 de c2 00 00 00 00 00 00 80 42 00 00 00 00 00 01 01 00 00 00 00 80 3f 00 00 80 3f 64 00 00 00 00 04 00 c9 10 89 c3 10 88 1d c3 00 00 00 00 00 00 00 42 08 cf 3c c3 ce 8e ec c2 00 00 00 00 00 00 00 42 2f da 64 c3 40 49 b3 c2 00 00 00 00 00 00 00 42 5c 16 9d c3 49 e5 00 c3 00 00 00 00 00 00 00 42 5c 16 9d c3 00 00 00 00 10 88 1d c3 00 00 00 00 00 00 00 42 00 00 00 00 00 01 01 00 00 00 00 80 3f 00 00 80 3f 64 00 00 00 00 04 00 37 69 05 c4 1c 20 8a c3 00 00 00 00 00 00 40 42 ac b9 8d c3 26 02 24 c3 00 00 00 00 00 00 40 42 a1 70 a1 c3 f0 17 07 c3 00 00 00 00 00 00 40 42 b2 44 0f c4 02 56 77 c3 00 00 00 00 00 00 40 42 b2 44 0f c4 00 00 00 00 1c 20 8a c3 00 00 00 00 00 00 40 42 00 00 00 00 00 01 01 00 00 00 00 80 3f 00 00 80 3f 64 00 00 00 00 04 00 c6 64 2f c4 09 14 ac c3 00 00 00 00 00 00 68 42 10 0c 0a c4 8c bf 88 c3 00 00 00 00 00 00 68 42 22 25 12 c4 86 f7 7a c3 00 00 00 00 00 00 68 42 d8 7d 37 c4 40 d0 a0 c3 00 00 00 00 00 00 68 42 d8 7d 37 c4 00 00 00 00 09 14 ac c3 00 00 00 00 00 00 68 42 00 00 00 00 00 01 01 00 00 00 00 80 3f 00 00 80 3f 64 00 00 00 00 04 00 cb 69 4e c4 23 a0 c7 c3 00 00 00 00 00 00 14 42 e8 12 35 c4 2a 10 b0 c3 00 00 00 00 00 00 54 42 21 ae 3c c4 71 4c a5 c3 00 00 00 00 00 00 54 42 04 05 56 c4 6a dc bc c3 00 00 00 00 00 00 14 42 04 05 56 c4 00 00 00 00 23 a0 c7 c3 00 00 00 00 00 00 54 42 00 00 00 00 00 01 01 00 00 00 00 80 3f 00 00 80 3f 64 00 00 00 00 05 00 9d fc 82 fe bd fc 6d fe e9 ff d5 ff 00 00 00 00 cd ff f7 ff 01 ca ff 95 ff 4f 00 00 00 04 00 00 00 ff ff 01 0f 00 00 00 00 00 00 00



L10
0100 
01 00 01 10 14 00 4c 65 76 65 6c 31 30 5f 42 69 67 20 47 61 74 74 6c 69 6e 67 0c 
                                       00 42 69 67 20 47 41 54 54 4c 49 4e 47 bb                               
ff b4 ff 22 00 01 01 01 00 00 04 00 f6 ff f2 ff 07 00 f2 ff 09 00 fc ff f3 ff fd ff 00 00 00 4a 00 03 00 ff ff 00 30 00

"""