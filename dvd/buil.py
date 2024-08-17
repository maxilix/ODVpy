from typing import Self

from common import *
from odv.odv_object import OdvRoot, OdvObject, OdvLeaf
from .move import Move, MainArea

from .section import Section


# class DoorAccess(RWStreamable):
#     def __init__(self, point: QPointF, area_global_id: int | UShort, layer_id: int | UShort) -> None:
#         self.point = point
#         self.area_global_id = area_global_id
#         self.layer_id = layer_id
#
#     @classmethod
#     def from_stream(cls, stream: ReadStream) -> Self:
#         point = stream.read(QPointF)
#         area_global_id = stream.read(UShort)
#         layer_id = stream.read(UShort)
#         return cls(point, area_global_id, layer_id)
#
#     def to_stream(self, stream: WriteStream) -> None:
#         stream.write(self.point)
#         stream.write(UShort(self.area_global_id))
#         stream.write(UShort(self.layer_id))
#
#     def __str__(self):
#         return f"{self.point} {self.layer_id}:{self.area_global_id}"

class Door(OdvLeaf):
    move: Move
    door_type: UChar
    unk0: UChar
    locked: UChar
    unlockable: UChar
    unk1: UChar
    unk2: UChar
    unk3: UChar
    unk4: UChar
    unk5: UChar
    unk6: UChar
    shape: QPolygonF
    p_in: QPointF
    main_area_in: MainArea
    p_mid: QPointF
    p_out: QPointF
    main_area_out: MainArea
    unk7: UShort
    unk8: None or (UChar, UChar)

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent, move) -> Self:
        rop = cls(parent)
        rop.move = move
        rop.door_type = stream.read(UChar)
        # print(f"{rop.door_type=}")
        rop.unk0 = stream.read(UChar)
        # print(f"{rop.unk0=}")
        rop.locked = stream.read(UChar)
        # print(f"{rop.locked=}")
        rop.unlockable = stream.read(UChar)
        # print(f"{rop.unlockable=}")
        rop.unk1 = stream.read(UChar)
        # print(f"{rop.unk1=}")
        rop.unk2 = stream.read(UChar)
        # print(f"{rop.unk2=}")
        rop.unk3 = stream.read(UChar)
        # print(f"{rop.unk3=}")
        rop.unk4 = stream.read(UChar)
        # print(f"{rop.unk4=}")
        rop.unk5 = stream.read(UChar)
        # print(f"{rop.unk5=}")
        rop.unk6 = stream.read(UChar)
        # print(f"{rop.unk6=}")
        rop.shape = stream.read(QPolygonF)
        # print(f"{rop.shape=}")
        nb_access = stream.read(UShort)
        assert nb_access == 3

        rop.p_in = stream.read(QPointF)
        rop.main_area_in = move.get_by_global(stream.read(UShort))
        layer_id_in = stream.read(UShort)
        assert rop.main_area_in.parent.i == layer_id_in

        rop.p_mid = stream.read(QPointF)
        main_area_mid = move.get_by_global(stream.read(UShort))
        layer_id_mid = stream.read(UShort)
        assert main_area_mid.parent.i == layer_id_mid

        rop.p_out = stream.read(QPointF)
        rop.main_area_out = move.get_by_global(stream.read(UShort))
        layer_id_out = stream.read(UShort)
        assert rop.main_area_out.parent.i == layer_id_out

        rop.unk7 = stream.read(UShort)
        if rop.unk7 != 0xffff:
            rop.unk8 = (stream.read(UChar), stream.read(UChar))
            assert rop.unk8[0] in [0,1]
            assert rop.unk8[1] in [0,1]
            assert sum(rop.unk8) == 1
        else:
            rop.unk8 = (0, 0)

        return rop

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(UChar(self.door_type))
        stream.write(UChar(self.unk0))
        stream.write(UChar(self.locked))
        stream.write(UChar(self.unlockable))
        stream.write(UChar(self.unk1))
        stream.write(UChar(self.unk2))
        stream.write(UChar(self.unk3))
        stream.write(UChar(self.unk4))
        stream.write(UChar(self.unk5))
        stream.write(UChar(self.unk6))
        stream.write(self.shape)
        stream.write(UShort(3))  # nb access
        stream.write(self.p_in)
        stream.write(UShort(self.main_area_in.global_id))
        stream.write(UShort(self.main_area_in.parent.i))
        stream.write(self.p_mid)
        stream.write(UShort(self.main_area_in.global_id))  # rewrite main_area in global_id
        stream.write(UShort(self.main_area_in.parent.i))  # rewrite layer id of main_area in
        stream.write(self.p_out)
        stream.write(UShort(self.main_area_out.global_id))
        stream.write(UShort(self.main_area_out.parent.i))


        stream.write(UShort(self.unk7))
        if self.unk7 != 0xffff:
            stream.write(UChar(self.unk8[0]))
            stream.write(UChar(self.unk8[1]))


class Building(OdvObject):
    move: Move
    unk1: UShort
    character_id_list: list[UShort]

    # door_list: list[Door] is child

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


class Buildings(OdvRoot):
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


class SpecialDoors(OdvRoot):
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
