from typing import Self

from common import *
from odv.odv_object import OdvObject, OdvObjectIterable

from odv.section import Section


class MaskEntry(OdvObject):
    flag: UShort
    point_list_1: list[QPointF] = []
    point_list_2: list[QPointF] = []
    u4: UShort = 0
    position: QPointF
    mask_image: MaskImage

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent) -> Self:
        rop = cls(parent)
        
        rop.flag = stream.read(UChar)
        # observed values
        # 9     0000 1001
        # 10    0000 1010
        # 11    0000 1011
        # 12    0000 1100
        # 13    0000 1101
        # 14    0000 1110
        # 15    0000 1111
        # 26    0001 1010
        # 27    0001 1011
        # 30    0001 1110
        # 31    0001 1111

        if rop.flag & 1:
            nb_point_f1 = stream.read(UShort)
            assert nb_point_f1 > 1
            rop.point_list_1 = [stream.read(QPointF) for _ in range(nb_point_f1)]
        if rop.flag & 2:
            nb_point_f2 = stream.read(UShort)
            assert nb_point_f2 > 1
            rop.point_list_2 = [stream.read(QPointF) for _ in range(nb_point_f2)]
        if rop.flag & 4:
            pass
        if rop.flag & 8:
            pass
        if rop.flag & 16:
            rop.u4 = stream.read(UShort)
            # observed values:
            #  0, 3, 4, 6, 7, 8, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23, 24, 25, 27, 28, 32, 33, 35, 36, 37, 38, 39, 41,
            #  42, 43, 44, 45, 46, 49, 50, 51, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 73, 75,
            #  76, 78, 79, 80, 81, 82, 85, 86, 89, 90, 91, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103, 105, 107, 109, 110,
            #  112, 113, 114, 116, 118, 119, 120, 122, 123, 124, 125, 126, 127, 129, 130, 131, 132, 133, 134, 137, 138, 141,
            #  142, 143, 144, 147, 149, 150, 151, 154, 155, 156, 158, 160, 161, 163, 165, 166, 167, 168, 170, 171, 172, 173,
            #  175, 177, 182, 183, 184, 185, 187, 188, 191, 193, 195, 196, 197, 198, 199, 200, 203, 205, 207, 208, 209, 210,
            #  211, 212, 213, 214, 216, 217, 218, 219, 220, 222, 224, 225, 226, 227, 228, 230, 232, 233, 234, 236, 237, 238,
            #  239, 243, 246, 248, 250, 251, 252, 254, 255, 256, 257, 258, 259, 260, 261, 263, 266, 267, 268, 269, 270, 271,
            #  274, 276, 278, 279, 280, 281, 283, 285, 290, 291, 293, 294, 295, 296, 297, 298, 300, 301, 302, 303, 304, 305,
            #  306, 311, 313, 318, 319, 320, 326, 332, 333, 334, 335, 336, 345, 346, 347, 348, 349, 352, 353, 354, 355, 356,
            #  361, 368, 369, 370, 371, 377, 379, 380, 382, 390, 391, 392, 393, 394, 395, 396, 402, 403, 404, 405, 406, 407,
            #  409, 410, 411, 412, 415, 435, 441, 442, 444, 445, 453, 464, 469, 470, 496, 505, 509, 510, 542, 558, 559, 568,
            #  569, 575, 576, 577, 597, 614, 645

        rop.position = stream.read(QPointF)
        rop.mask_image = stream.read(MaskImage)
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(UChar(self.flag))
        if self.flag & 1:
            stream.write(UShort(len(self.point_list_1)))
            for p in self.point_list_1:
                stream.write(p)
        if self.flag & 2:
            stream.write(UShort(len(self.point_list_2)))
            for p in self.point_list_2:
                stream.write(p)
        if self.flag & 16:
            stream.write(UShort(self.u4))

        stream.write(self.position)
        stream.write(self.mask_image)



class MaskLayer(OdvObjectIterable):
    mask_entry_list: list[MaskEntry]

    def __iter__(self):
        return iter(self.mask_entry_list)

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent) -> Self:
        rop = cls(parent)
        nb_mask_entry = stream.read(UShort)
        rop.mask_entry_list = [stream.read(MaskEntry, parent=rop) for _ in range(nb_mask_entry)]
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        nb_mask_entry = len(self.mask_entry_list)
        stream.write(UShort(nb_mask_entry))
        for mask_entry in self.mask_entry_list:
            stream.write(mask_entry)



class Mask(Section, OdvObjectIterable):
    _section_name = "MASK"
    _section_version = 4

    layer_list = list[MaskLayer]

    def __iter__(self):
        return iter(self.layer_list)

    def _load(self, substream: ReadStream):
        nb_layer = substream.read(UShort)
        self.layer_list = [substream.read(MaskLayer, parent=self) for _ in range(nb_layer)]

    def _save(self, substream: WriteStream) -> None:
        nb_layer = len(self.layer_list)
        substream.write(UShort(nb_layer))
        for layer in self.layer_list:
            substream.write(layer)
