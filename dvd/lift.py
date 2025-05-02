from typing import Self

from common import *
from odv.odv_object import OdvObjectIterable, OdvObject
from .move import Sector, Move
from .section import Section


class LiftArea(OdvObject):
    move: Move
    lift_type: UChar
    sector: Sector
    sector_below: Sector
    gateway_below: Gateway
    sector_above: Sector
    gateway_above: Gateway
    # shape: QPolygonF
    perspective: UShort


    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent, move) -> Self:
        rop = cls(parent)
        rop.move = move

        rop.sector = move.sector(stream.read(UShort))
        rop.lift_type = stream.read(UChar)
        # 0: ????
        # 1: stair
        # 2: ladder
        # 3: wall

        rop.sector_below = move.sector(stream.read(UShort))
        under_layer_id = stream.read(UShort)  # layer id

        rop.sector_above = move.sector(stream.read(UShort))
        over_layer_id = stream.read(UShort)  # layer id

        shape = stream.read(QPolygonF)  # seems useless, isn't always defined

        rop.gateway_below = stream.read(Gateway)
        rop.gateway_above = stream.read(Gateway)

        rop.perspective = stream.read(UShort)
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(UShort(self.sector.sector_id))
        stream.write(UChar(self.lift_type))

        stream.write(UShort(self.sector_below.sector_id))
        stream.write(UShort(self.sector_below.parent.i))  # layer id

        stream.write(UShort(self.sector_above.sector_id))
        stream.write(UShort(self.sector_above.parent.i))  # layer id

        # stream.write(self.shape)
        stream.write(UShort(0))  # write null polygon as shape

        stream.write(self.gateway_below)
        stream.write(self.gateway_above)

        stream.write(UShort(self.perspective))


class Lift(Section, OdvObjectIterable):
    _section_name = "LIFT"
    _section_version = 2



    def _load(self, substream: ReadStream, *, move) -> None:
        self.move = move
        nb_lift = substream.read(UShort)
        for _ in range(nb_lift):
            self.add_child(substream.read(LiftArea, parent=self, move=move))

    def _save(self, substream: WriteStream) -> None:
        nb_lift = len(self)
        substream.write(UShort(nb_lift))
        for lift_area in self:
            substream.write(lift_area)
