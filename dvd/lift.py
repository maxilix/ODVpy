from typing import Self

from common import *
from odv.odv_object import OdvRoot, OdvLeaf
from .move import MainArea, Move
from .section import Section


class LiftArea(OdvLeaf):
    move: Move
    lift_type: UChar
    main_area: MainArea
    main_area_under: MainArea
    gateway_under: Gateway
    main_area_over: MainArea
    gateway_over: Gateway
    # shape: QPolygonF
    perspective: UShort


    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent, move) -> Self:
        rop = cls(parent)
        rop.move = move

        rop.main_area = move.get_by_global(stream.read(UShort))
        rop.lift_type = stream.read(UChar)
        # 0: ????
        # 1: stair
        # 2: ladder
        # 3: wall

        rop.main_area_under = move.get_by_global(stream.read(UShort))
        under_layer_id = stream.read(UShort)  # layer id

        rop.main_area_over = move.get_by_global(stream.read(UShort))
        over_layer_id = stream.read(UShort)  # layer id

        shape = stream.read(QPolygonF)  # seems useless, isn't always defined

        rop.gateway_under = stream.read(Gateway)
        rop.gateway_over = stream.read(Gateway)

        rop.perspective = stream.read(UShort)
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(UShort(self.main_area.global_id))
        stream.write(UChar(self.lift_type))

        stream.write(UShort(self.main_area_under.global_id))
        stream.write(UShort(self.main_area_under.parent.i))  # layer id

        stream.write(UShort(self.main_area_over.global_id))
        stream.write(UShort(self.main_area_over.parent.i))  # layer id

        # stream.write(self.shape)
        stream.write(UShort(0))  # write null polygon as shape

        stream.write(self.gateway_under)
        stream.write(self.gateway_over)

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
