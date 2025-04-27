from typing import Self

from common import *
from common import ReadStream
from odv.odv_object import OdvObject
from .move import MainArea, Move

from .section import Section

class JumpStart(RWStreamable):
    p: QPointF
    u1: Short
    u2: Short
    u3: Short

    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        rop = cls()
        rop.p = stream.read(QPointF)
        # offsets to draw jump line
        # u1 and u2 of the order of the jump height (in pixel)
        # u3 often close to zero, may be some kind of x offset
        rop.u1 = stream.read(Short)
        rop.u2 = stream.read(Short)
        rop.u3 = stream.read(Short)
        return rop

    def to_stream(self, stream):
        stream.write(self.p)
        stream.write(Short(self.u1))
        stream.write(Short(self.u2))
        stream.write(Short(self.u3))


class JumpArea(OdvObject):
    move: Move
    roof_main_area: MainArea
    ground_main_area: MainArea
    landing_polygon: QPolygonF
    jump_start_list: list[JumpStart]

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent, move) -> Self:
        rop = cls(parent)
        rop.move = move

        layer_id = stream.read(UShort)
        rop.roof_main_area = move.main_area(stream.read(UShort))
        assert rop.roof_main_area.parent.i == layer_id

        nb_point = stream.read(UShort)
        rop.jump_start_list = [stream.read(JumpStart) for _ in range(nb_point)]

        layer_id = stream.read(UShort)
        rop.ground_main_area = move.main_area(stream.read(UShort))
        assert rop.ground_main_area.parent.i == layer_id

        rop.landing_polygon = stream.read(QPolygonF)

        return rop

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(UShort(self.roof_main_area.parent.i))  # layer id
        stream.write(UShort(self.roof_main_area.main_area_id))
        n = len(self.jump_start_list)
        stream.write(UShort(n))
        for jump_start in self.jump_start_list:
            stream.write(jump_start)
        stream.write(UShort(self.ground_main_area.parent.i))  # layer id
        stream.write(UShort(self.ground_main_area.main_area_id))
        stream.write(self.landing_polygon)



class Jump(Section):
    _section_name = "JUMP"
    _section_version = 1

    move: Move

    def _load(self, substream: ReadStream, *, move) -> None:
        self.move = move
        nb_jump_area = substream.read(UShort)
        for _ in range(nb_jump_area):
            self.add_child(substream.read(JumpArea, parent=self, move=move))

    def _save(self, substream: WriteStream) -> None:
        nb_jump_area = len(self)
        substream.write(UShort(nb_jump_area))
        for jump_area in self:
            substream.write(jump_area)
