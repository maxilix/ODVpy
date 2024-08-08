from typing import Self, Iterator

from PyQt6.QtCore import QPoint

from common import *
from odv.odv_object import OdvObject
from .move import Layer

from .section import Section


class BondLink(OdvObject):
    # _left_id: int
    # _right_id: int
    _layer: Layer

    def __init__(self, parent, p1: QPointF, p2: QPointF, left_id, right_id, layer_id) -> None:
        super().__init__(parent)
        self.p1 = p1
        self.p2 = p2
        self.left_id = left_id
        self.right_id = right_id
        self.layer_id = layer_id

    @property
    def layer_id(self):
        return self._layer.i

    @layer_id.setter
    def layer_id(self, layer_id):
        self._layer = self.parent.move[layer_id]

    def __str__(self):
        return f"Bond {self.i}"

    @property
    def i(self):
        return self.parent.bond_list.index(self)

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent) -> Self:
        p1 = stream.read(QPointF)
        p2 = stream.read(QPointF)
        left_id = stream.read(UShort)
        right_id = stream.read(UShort)
        layer_id = stream.read(UShort)
        return cls(parent, p1, p2, left_id, right_id, layer_id)

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(self.p1)
        stream.write(self.p2)
        stream.write(UShort(self.left_id))
        stream.write(UShort(self.right_id))
        stream.write(UShort(self.layer_id))


class Bond(Section):
    _name = "BOND"
    _version = 2

    def __iter__(self) -> Iterator[BondLink]:
        return iter(self.bond_list)

    def __getitem__(self, index: int) -> BondLink:
        return self.bond_list[index]

    def __len__(self) -> int:
        return len(self.bond_list)

    @property
    def move(self):
        return self._move

    def _load(self, substream: ReadStream, *, move) -> None:
        nb_bond = substream.read(UShort)
        self._move = move
        self.bond_list = [substream.read(BondLink, parent=self) for _ in range(nb_bond)]

    def _save(self, substream: WriteStream) -> None:
        nb_bond = len(self.bond_list)
        substream.write(UShort(nb_bond))
        for bond in self.bond_list:
            substream.write(bond)
