from typing import Self, Iterator

from PyQt6.QtCore import QPoint

from common import *
from odv.odv_object import OdvObject, OdvRoot, OdvLeaf
from .move import Layer, Move

from .section import Section


class BondLine(OdvLeaf):
    move: Move
    line: QLineF
    left_id: UShort
    right_id: UShort
    layer: Layer

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent, move) -> Self:
        rop = cls(parent)
        rop.move = move
        rop.line = stream.read(QLineF)
        rop.left_id = stream.read(UShort)
        rop.right_id = stream.read(UShort)
        rop.layer = move[stream.read(UShort)]
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(self.line)
        stream.write(UShort(self.left_id))
        stream.write(UShort(self.right_id))
        stream.write(UShort(self.layer.i))


class Bond(Section, OdvRoot):
    _section_name = "BOND"
    _section_version = 2

    move: Move

    def _load(self, substream: ReadStream, *, move) -> None:
        self.move = move
        nb_bond_line = substream.read(UShort)
        for _ in range(nb_bond_line):
            self.add_child(substream.read(BondLine, parent=self, move=move))

    def _save(self, substream: WriteStream) -> None:
        nb_bond_line = len(self)
        substream.write(UShort(nb_bond_line))
        for bond_line in self:
            substream.write(bond_line)
