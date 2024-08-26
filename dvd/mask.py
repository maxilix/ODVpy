import math
from typing import Self

from PyQt6.QtGui import QImage

from common import *
from odv.odv_object import OdvLeaf, OdvRoot

from .section import Section


class MaskImage(OdvLeaf):
    flag: UShort
    point_list_1: list[QPointF] = []
    point_list_2: list[QPointF] = []
    u4: UShort = 0
    layer_id: int
    position: QPointF
    y: UShort

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent, layer_id) -> Self:
        rop = cls(parent)
        rop.layer_id = layer_id
        
        rop.flag = stream.read(UChar)
        if rop.flag & 1:
            nb_point = stream.read(UShort)
            rop.point_list_1 = [stream.read(QPointF) for _ in range(nb_point)]
        if rop.flag & 2:
            nb_point = stream.read(UShort)
            rop.point_list_2 = [stream.read(QPointF) for _ in range(nb_point)]
        if rop.flag & 16:
            rop.u4 = stream.read(UShort)

        rop.position = stream.read(QPointF)
        width = stream.read(UShort)
        height = stream.read(UShort)

        mask_length = stream.read(UShort)
        mask_stream = ReadStream(stream.read(Bytes, mask_length))
        data = b''
        for line_index in range(height):
            line_length = mask_stream.read(UChar)
            line_stream = ReadStream(mask_stream.read(Bytes, line_length))
            while descriptor := line_stream.read(UChar):
                c = descriptor & 128
                n = descriptor & 127
                if c:
                    # read 1 Byte and copy it n times
                    data += line_stream.read(Bytes, 1) * n
                else:
                    # read n Bytes
                    data += line_stream.read(Bytes, n)
            assert len(line_stream.read_raw()) == 0

        assert len(mask_stream.read_raw()) == 0

        rop.image = QImage(data, width, height, math.ceil(width/8), QImage.Format.Format_Mono)
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        # TODO write Mask
        pass

        

class Mask(Section, OdvRoot):
    _section_name = "MASK"
    _section_version = 4


    def _load(self, substream: ReadStream):
        nb_layer = substream.read(UShort)
        for layer_id in range(nb_layer):
            nb_mask = substream.read(UShort)
            for mask_index in range(nb_mask):
                self.add_child(substream.read(MaskImage, parent=self, layer_id=layer_id))

    def _save(self, substream: WriteStream) -> None:
        substream.write(UShort(0))


