from typing import Self

from common import *
from odv.odv_object import OdvObject
from .move import Layer, Move
from .section import Section
from .sght import Sght, SightObstacle


class BondLine(OdvObject):
    move: Move
    sght: Sght
    line: QLineF
    sight_obstacle_1: SightObstacle
    sight_obstacle_2: SightObstacle
    layer: Layer

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent, move, sght) -> Self:
        rop = cls(parent)
        rop.move = move
        rop.sght = sght
        rop.line = stream.read(QLineF)
        rop.sight_obstacle_1 = sght.walkable_sight(stream.read(UShort))
        rop.sight_obstacle_2 = sght.walkable_sight(stream.read(UShort))

        rop.layer = move[stream.read(UShort)]
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(self.line)
        stream.write(UShort(self.sight_obstacle_1.walkable_sight_id))
        stream.write(UShort(self.sight_obstacle_2.walkable_sight_id))
        stream.write(UShort(self.layer.i))


class Bond(Section):
    _section_name = "BOND"
    _section_version = 2

    move: Move
    sght: Sght

    def _load(self, substream: ReadStream, *, move, sght) -> None:
        self.move = move
        self.sght = sght
        nb_bond_line = substream.read(UShort)
        for _ in range(nb_bond_line):
            self.add_child(substream.read(BondLine, parent=self, move=move, sght=sght))

    def _save(self, substream: WriteStream) -> None:
        nb_bond_line = len(self)
        substream.write(UShort(nb_bond_line))
        for bond_line in self:
            substream.write(bond_line)
