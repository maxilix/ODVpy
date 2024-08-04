from typing import Self, Iterator

from PyQt6.QtCore import QPoint

from common import *

from .section import Section


class BondLink(RWStreamable):
    has_graphic = True

    def __init__(self, parent, p1: QPointF, p2: QPointF, left_id, right_id, layer) -> None:
        self.parent = parent
        self.p1 = p1
        self.p2 = p2
        self.left_id = left_id
        self.right_id = right_id
        self.layer = layer

    def __str__(self):
        return f"Bond {self.i}"
    @property
    def i(self):
        return self.parent.bond_list.index(self)

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent, move) -> Self:
        p1 = stream.read(QPointF)
        p2 = stream.read(QPointF)
        left_id = stream.read(UShort)
        right_id = stream.read(UShort)
        layer = move[stream.read(UShort)]
        return cls(parent, p1, p2, left_id, right_id, layer)

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(self.p1)
        stream.write(self.p2)
        stream.write(UShort(self.left_id))
        stream.write(UShort(self.right_id))
        stream.write(UShort(self.layer.i))


class Bond(Section):
    _name = "BOND"
    _version = 2

    def __iter__(self) -> Iterator[BondLink]:
        return iter(self.bond_list)

    def __getitem__(self, index: int) -> BondLink:
        return self.bond_list[index]

    def __len__(self) -> int:
        return len(self.bond_list)

    def _load(self, substream: ReadStream, *, move) -> None:
        nb_bond = substream.read(UShort)
        self.bond_list = [substream.read(BondLink, parent=self, move=move) for _ in range(nb_bond)]

    def _save(self, substream: WriteStream) -> None:
        nb_bond = len(self.bond_list)
        substream.write(UShort(nb_bond))
        for bond in self.bond_list:
            substream.write(bond)
