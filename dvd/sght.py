from typing import Self

from common import *
from odv.odv_object import OdvLeaf, OdvRoot
from .move import Move, Sector
from .section import Section


class SightLine(RWStreamable):
    def __init__(self, x, y, z_bottom, z_top):
        self.x = x
        self.y = y
        self.z_bottom = z_bottom
        self.z_top = z_top

    def length(self):
        assert self.z_bottom <= self.z_top
        return self.z_top - self.z_bottom

    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        x = stream.read(Float)
        y = stream.read(Float)
        z_bottom = stream.read(Float)
        z_top = stream.read(Float)
        return cls(x, y, z_bottom, z_top)

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(Float(self.x))
        stream.write(Float(self.y))
        stream.write(Float(self.z_bottom))
        stream.write(Float(self.z_top))


class SightObstacle(OdvLeaf):
    move: Move
    vline_list: list[SightLine]
    main_area: Sector | None
    unk_char_1: UChar
    unk_char_2: UChar
    unk_char_3: UChar
    unk_char_4: UChar

    def volume_shape(self):
        pass

    def __str__(self):
        if self.main_area is None:
            return super().__str__()
        else:
            return f"{super().__str__()} - {self.walkable_sight_id}"

    @property
    def walkable_sight_id(self):
        return list(self.parent.walkable_sight_iterator()).index(self)

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent, move) -> Self:
        rop = cls(parent)
        rop.move = move

        nb_vline = stream.read(UShort)
        rop.vline_list = [stream.read(SightLine) for _ in range(nb_vline)]
        assert len(rop.vline_list) >= 3

        min_x = stream.read(Float)
        assert min_x == min(vl.x for vl in rop.vline_list)

        min_z_bottom = stream.read(Float)
        assert round(min_z_bottom, 5) == round(min(vl.z_bottom for vl in rop.vline_list), 5)
        # 2 round error : one in L18 and one in L21

        min_y = stream.read(Float)
        assert min_y == min(vl.y for vl in rop.vline_list)

        max_x = stream.read(Float)
        assert max_x == max(vl.x for vl in rop.vline_list)

        max_z_top = stream.read(Float)
        assert max_z_top == max(vl.z_top for vl in rop.vline_list)

        max_y = stream.read(Float)
        assert max_y == max(vl.y for vl in rop.vline_list)

        has_main_area_above = stream.read(UChar)
        if has_main_area_above:
            layer_id = stream.read(UShort)
            rop.main_area = move.main_area(stream.read(UShort))
            assert rop.main_area.parent.i == layer_id
        else:
            rop.main_area = None

        rop.unk_char_1 = stream.read(UChar)
        rop.unk_char_2 = stream.read(UChar)
        rop.unk_char_3 = stream.read(UChar)
        rop.unk_char_4 = stream.read(UChar)
        # unk_char_i == 1, 0, 1, 0   ==>   the obstacle is roughly defined and contains sub-obstacles


        unk_float_1 = stream.read(Float)
        assert unk_float_1 == 1.0
        unk_float_2 = stream.read(Float)
        assert unk_float_2 == 1.0
        unk_char_5 = stream.read(UChar)
        assert unk_char_5 == 100
        unk_int_1 = stream.read(UInt)
        assert unk_int_1 == 0
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        nb_sight_vline = len(self.vline_list)
        stream.write(UShort(nb_sight_vline))
        for vl in self.vline_list:
            stream.write(vl)

        stream.write(Float(min(vl.x for vl in self.vline_list)))
        stream.write(Float(min(vl.z_bottom for vl in self.vline_list)))
        stream.write(Float(min(vl.y for vl in self.vline_list)))
        stream.write(Float(max(vl.x for vl in self.vline_list)))
        stream.write(Float(max(vl.z_top for vl in self.vline_list)))
        stream.write(Float(max(vl.y for vl in self.vline_list)))

        if self.main_area is not None:
            stream.write(UChar(1))
            stream.write(UShort(self.main_area.parent.i))
            stream.write(UShort(self.main_area.main_area_id))
        else:
            stream.write(UChar(0))

        stream.write(UChar(self.unk_char_1))
        stream.write(UChar(self.unk_char_2))
        stream.write(UChar(self.unk_char_3))
        stream.write(UChar(self.unk_char_4))
        stream.write(Float(1.0))
        stream.write(Float(1.0))
        stream.write(UChar(100))
        stream.write(UInt(0))


class GroundSight(object):
    walkable_sight_id = 0
    def __str__(self):
        return "Ground Sight"


class Sght(Section, OdvRoot):
    _section_name = "SGHT"
    _section_version = 6

    move: Move

    def walkable_sight(self, index):
        return self.walkable_sight_iterator()[index]

    def walkable_sight_iterator(self):
        class WSI:
            def __iter__(subself):
                return iter([self.ground_sight] + [s for s in self if s.main_area is not None])
            def __getitem__(self, item):
                return list(iter(self))[item]
            def __len__(self):
                return len(list(iter(self)))
        return WSI()

    def _load(self, substream: ReadStream, * , move) -> None:
        self.move = move
        self.ground_sight = GroundSight()
        nb_sight_obstacle = substream.read(UShort)
        for _ in range(nb_sight_obstacle):
            self.add_child(substream.read(SightObstacle, parent=self, move=move))

    def _save(self, substream: WriteStream) -> None:
        nb_sight_obstacle = len(self)
        substream.write(UShort(nb_sight_obstacle))
        for sight_obstacle in self:
            substream.write(sight_obstacle)

