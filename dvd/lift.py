from typing import Self

from common import *
from odv.odv_object import OdvRoot, OdvLeaf
from .move import MainArea, Move
from .section import Section


class LiftArea(OdvLeaf):
    move: Move
    lift_type: UChar
    main_area: MainArea
    main_area_below: MainArea
    gateway_below: Gateway
    main_area_above: MainArea
    gateway_above: Gateway
    # shape: QPolygonF
    perspective: UShort


    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent, move) -> Self:
        rop = cls(parent)
        rop.move = move

        rop.main_area = move.main_area(stream.read(UShort))
        rop.lift_type = stream.read(UChar)
        # 0: ????
        # 1: stair
        # 2: ladder
        # 3: wall

        rop.main_area_below = move.main_area(stream.read(UShort))
        under_layer_id = stream.read(UShort)  # layer id

        rop.main_area_above = move.main_area(stream.read(UShort))
        over_layer_id = stream.read(UShort)  # layer id

        shape = stream.read(QPolygonF)  # seems useless, isn't always defined

        rop.gateway_below = stream.read(Gateway)
        rop.gateway_above = stream.read(Gateway)

        rop.perspective = stream.read(UShort)
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(UShort(self.main_area.main_area_id))
        stream.write(UChar(self.lift_type))

        stream.write(UShort(self.main_area_below.main_area_id))
        stream.write(UShort(self.main_area_below.parent.i))  # layer id

        stream.write(UShort(self.main_area_above.main_area_id))
        stream.write(UShort(self.main_area_above.parent.i))  # layer id

        # stream.write(self.shape)
        stream.write(UShort(0))  # write null polygon as shape

        stream.write(self.gateway_below)
        stream.write(self.gateway_above)

        stream.write(UShort(self.perspective))


class Lift(Section, OdvRoot):
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
