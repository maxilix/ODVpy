from typing import Self

from PyQt6.QtCore import QPoint

from common import *

from .section import Section


class BondLink(RWStreamable):

    def __init__(self, p1: QPointF, p2: QPointF, left_id, right_id, layer_id) -> None:
        self.p1 = p1
        self.p2 = p2
        self.left_id = left_id
        self.right_id = right_id
        self.layer_id = layer_id

    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        p1 = stream.read(QPointF)
        p2 = stream.read(QPointF)
        left_id = stream.read(UShort)
        right_id = stream.read(UShort)
        layer_id = stream.read(UShort)
        return cls(p1, p2, left_id, right_id, layer_id)

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(self.p1)
        stream.write(self.p2)
        stream.write(Bytes(self.left_id))
        stream.write(UShort(self.right_id))
        stream.write(UShort(self.layer_id))


class Bond(Section):
    _name = "BOND"
    _version = 2

    def _load(self, substream: ReadStream) -> None:
        nb_bond = substream.read(UShort)
        self.bond_list = [substream.read(BondLink) for _ in range(nb_bond)]

        # self.raw = substream.read_raw()
        # self.hraw = self.raw.hex().upper()

    def _save(self, substream: WriteStream) -> None:
        nb_bond = len(self.bond_list)
        substream.write(UShort(nb_bond))
        for bond in self.bond_list:
            substream.write(bond)
