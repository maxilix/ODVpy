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
    y: UShort
    mask_image: MaskImage

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent) -> Self:
        rop = cls(parent)
        
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
