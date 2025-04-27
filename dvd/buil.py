from typing import Self

from common import *
from odv.odv_object import OdvObject
from .move import Move, MainArea

from .section import Section

# TODO separate buildings door and special door

class Door(OdvObject):
    move: Move
    door_type: UChar
    enable: UChar
    locked: UChar
    unlockable: UChar
    unk_bool_3: UChar
    unk_bool_4: UChar
    unk_bool_5: UChar
    unk_bool_6: UChar
    unk_bool_7: UChar
    unk_bool_8: UChar
    shape: QPolygonF
    gateway: Gateway
    main_area_1: MainArea
    main_area_3: MainArea
    anim_id: UShort
    allowed_sens: (UChar, UChar)

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent, move) -> Self:
        rop = cls(parent)
        rop.move = move
        rop.door_type = stream.read(UChar)
        rop.enable = stream.read(UChar)
        rop.locked = stream.read(UChar)
        rop.unlockable = stream.read(UChar)
        rop.unk_bool_3 = stream.read(UChar)
        rop.unk_bool_4 = stream.read(UChar)
        rop.unk_bool_5 = stream.read(UChar)
        rop.unk_bool_6 = stream.read(UChar)
        rop.unk_bool_7 = stream.read(UChar)
        rop.unk_bool_8 = stream.read(UChar)
        rop.shape = stream.read(QPolygonF)
        nb_access = stream.read(UShort)
        assert nb_access == 3

        p1 = stream.read(QPointF)
        rop.main_area_1 = move.main_area(stream.read(UShort))
        layer_id_1 = stream.read(UShort)
        assert rop.main_area_1.parent.i == layer_id_1

        p2 = stream.read(QPointF)
        main_area_2 = move.main_area(stream.read(UShort))
        layer_id_2 = stream.read(UShort)
        assert main_area_2.parent.i == layer_id_2

        p3 = stream.read(QPointF)
        rop.main_area_3 = move.main_area(stream.read(UShort))
        layer_id_3 = stream.read(UShort)
        assert rop.main_area_3.parent.i == layer_id_3

        rop.gateway = Gateway(p1, p2, p3)

        rop.anim_id = stream.read(UShort)
        if rop.anim_id != 0xffff:
            rop.allowed_sens = (stream.read(UChar), stream.read(UChar))
            assert rop.allowed_sens[0] in [0, 1]
            assert rop.allowed_sens[1] in [0, 1]
            assert sum(rop.allowed_sens) == 1
        else:
            rop.allowed_sens = (0, 0)

        return rop

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(UChar(self.door_type))
        stream.write(UChar(self.enable))
        stream.write(UChar(self.locked))
        stream.write(UChar(self.unlockable))
        stream.write(UChar(self.unk_bool_3))
        stream.write(UChar(self.unk_bool_4))
        stream.write(UChar(self.unk_bool_5))
        stream.write(UChar(self.unk_bool_6))
        stream.write(UChar(self.unk_bool_7))
        stream.write(UChar(self.unk_bool_8))
        stream.write(self.shape)
        stream.write(UShort(3))  # nb access
        stream.write(self.gateway.p1)
        stream.write(UShort(self.main_area_1.main_area_id))
        stream.write(UShort(self.main_area_1.parent.i))
        stream.write(self.gateway.p2)
        stream.write(UShort(self.main_area_1.main_area_id))  # rewrite main_area_1 global id
        stream.write(UShort(self.main_area_1.parent.i))   # rewrite main_area_1 layer id
        stream.write(self.gateway.p3)
        stream.write(UShort(self.main_area_3.main_area_id))  # TODO test with main_area_1 info again for non special door
        stream.write(UShort(self.main_area_3.parent.i))   # TODO same

        stream.write(UShort(self.anim_id))
        if self.anim_id != 0xffff:
            stream.write(UChar(self.allowed_sens[0]))
            stream.write(UChar(self.allowed_sens[1]))


class Building(OdvObject):
    move: Move
    unk1: UShort
    character_id_list: list[UShort]

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent, move) -> Self:
        rop = cls(parent)
        rop.move = move
        rop.unk1 = stream.read(UShort)
        nb_characters = stream.read(UShort)
        rop.character_id_list = [stream.read(UShort) for _ in range(nb_characters)]
        nb_doors = stream.read(UShort)
        for _ in range(nb_doors):
            rop.add_child(stream.read(Door, parent=rop, move=move))
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(UShort(self.unk1))
        nb_characters = len(self.character_id_list)
        stream.write(UShort(nb_characters))
        for character_id in self.character_id_list:
            stream.write(UShort(character_id))
        nb_doors = len(self)
        stream.write(UShort(nb_doors))
        for door in self:
            stream.write(door)


class Buildings(OdvObject):
    move: Move

    @classmethod
    def from_stream(cls, stream: ReadStream, *, move) -> Self:
        rop = cls()
        rop.move = move
        nb_building = stream.read(UShort)
        for _ in range(nb_building):
            rop.add_child(stream.read(Building, parent=rop, move=move))
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        nb_building = len(self)
        stream.write(UShort(nb_building))
        for building in self:
            stream.write(building)


class SpecialDoors(OdvObject):
    move: Move

    @classmethod
    def from_stream(cls, stream: ReadStream, *, move) -> Self:
        rop = cls()
        rop.move = move
        nb_special_door = stream.read(UShort)
        for _ in range(nb_special_door):
            rop.add_child(stream.read(Door, parent=rop, move=move))
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        nb_special_door = len(self)
        stream.write(UShort(nb_special_door))
        for door in self:
            stream.write(door)


class Buil(Section):
    _section_name = "BUIL"
    _section_version = 4

    move: Move
    buildings: Buildings
    special_doors: SpecialDoors

    def _load(self, substream: ReadStream, *, move) -> None:
        self.move = move
        self.buildings = substream.read(Buildings, move=move)
        self.special_doors = substream.read(SpecialDoors, move=move)

    def _save(self, substream: WriteStream) -> None:
        substream.write(self.buildings)
        substream.write(self.special_doors)
