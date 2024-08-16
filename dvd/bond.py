from typing import Self, Iterator

from PyQt6.QtCore import QPoint

from common import *
from odv.odv_object import OdvObject, OdvRoot, OdvLeaf
from .move import Layer, Move

from .section import Section


class BondLine(OdvLeaf):
    line: QLineF
    left_id: UShort
    right_id: UShort
    layer: Layer

    # def __init__(self, parent), p1: QPointF, p2: QPointF, left_id, right_id, layer) -> None:
    #     super().__init__(parent)
    #     self.p1 = p1
    #     self.p2 = p2
    #     self.left_id = left_id
    #     self.right_id = right_id
    #     self.layer = layer

    # @property
    # def layer(self):
    #     return self._layer.i
    #
    # @layer_id.setter
    # def layer_id(self, layer_id):
    #     self._layer = self.parent.move[layer_id]

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent) -> Self:
        rop = cls(parent)
        rop.line = stream.read(QLineF)
        rop.left_id = stream.read(UShort)
        rop.right_id = stream.read(UShort)
        rop.layer = parent.move[stream.read(UShort)]
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(self.line)
        stream.write(UShort(self.left_id))
        stream.write(UShort(self.right_id))
        stream.write(UShort(self.layer.i))


class Bond(Section, OdvRoot):
    _section_name = "BOND"
    _section_version = 2

    _move: Move

    @property
    def move(self):
        return self._move

    def _load(self, substream: ReadStream, *, move) -> None:
        self._move = move
        nb_bond_line = substream.read(UShort)
        for _ in range(nb_bond_line):
            self.add_child(substream.read(BondLine, parent=self))

    def _save(self, substream: WriteStream) -> None:
        nb_bond_line = len(self)
        substream.write(UShort(nb_bond_line))
        for bond_line in self:
            substream.write(bond_line)
