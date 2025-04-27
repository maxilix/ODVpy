from common import *
from odv.odv_object import OdvObject

from .section import Section


class MaskEntry(OdvObject):
    flag: UShort
    point_list_1: list[QPointF] = []
    point_list_2: list[QPointF] = []
    u4: UShort = 0
    layer_id: int
    position: QPointF
    y: UShort
    maskimage: MaskImage

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
        rop.maskimage = stream.read(MaskImage)

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
        stream.write(self.maskimage)




        

class Mask(Section):
    _section_name = "MASK"
    _section_version = 4


    def _load(self, substream: ReadStream):
        self.nb_layer = substream.read(UShort)
        print(f"mask layer = {self.nb_layer}")
        for layer_id in range(self.nb_layer):
            nb_mask = substream.read(UShort)
            for mask_index in range(nb_mask):
                self.add_child(substream.read(MaskEntry, parent=self, layer_id=layer_id))

    def _save(self, substream: WriteStream) -> None:
        # mask_tab = [[] for _ in range(self.nb_layer)]
        # for mask_entry in self:
        #     mask_tab[mask_entry.layer_id].append(mask_entry)
        #
        # substream.write(UShort(len(mask_tab)))
        # for mask_list in mask_tab:
        #     substream.write(UShort(len(mask_list)))
        #     for mask_entry in mask_list:
        #         substream.write(mask_entry)

        substream.write(UShort(1))
        substream.write(UShort(len(self)))
        for mask_entry in self:
            substream.write(mask_entry)



