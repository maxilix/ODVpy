from typing import Self

from common import *

from .section import Section


class DoorAccess(RWStreamable):
    def __init__(self, point: QPointF, area_global_id: int | UShort, layer_id: int | UShort) -> None:
        self.point = point
        self.area_global_id = area_global_id
        self.layer_id = layer_id

    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        point = stream.read(QPointF)
        area_global_id = stream.read(UShort)
        layer_id = stream.read(UShort)
        return cls(point, area_global_id, layer_id)

    def to_stream(self, stream: WriteStream) -> None:
        pass

    def __str__(self):
        return f"{self.layer_id}:{self.area_global_id} {self.point}"


class Door(RWStreamable):
    def __init__(self, door_type, unk0, locked, unlockable, unk1, unk2, unk3, unk4, unk5, unk6, shape, accesses, unk7, unk8) -> None:
        self.door_type = door_type
        self.unk0 = unk0
        self.locked = locked
        self.unlockable = unlockable
        self.unk1 = unk1
        self.unk2 = unk2
        self.unk3 = unk3
        self.unk4 = unk4
        self.unk5 = unk5
        self.unk6 = unk6
        self.shape = shape
        self.accesses = accesses
        self.unk7 = unk7
        self.unk8 = unk8


    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        door_type = stream.read(UChar)
        unk0 = stream.read(UChar)
        locked = stream.read(UChar)
        unlockable = stream.read(UChar)
        unk1 = stream.read(UChar)
        unk2 = stream.read(UChar)
        unk3 = stream.read(UChar)
        unk4 = stream.read(UChar)
        unk5 = stream.read(UChar)
        unk6 = stream.read(UChar)

        shape = stream.read(QPolygonF)
        nb_access = stream.read(UShort)
        assert nb_access == 3
        accesses = [stream.read(DoorAccess) for _ in range(nb_access)]

        unk7 = stream.read(UShort)
        if unk7 != 0xffff:
            unk8 = (stream.read(UChar), stream.read(UChar))
            print(f"from {accesses[0]}   to {accesses[2]}  {unk7} {unk8}")
        else:
            unk8 = None

        return cls(door_type, unk0, locked, unlockable, unk1, unk2, unk3, unk4, unk5, unk6, shape, accesses, unk7, unk8)

    def to_stream(self, stream: WriteStream) -> None:
        pass


class Building(RWStreamable):
    def __init__(self, unk1, characters_id_list, door_list) -> None:
        self.unk1 = unk1
        self.characters_id_list = characters_id_list
        self.door_list = door_list

    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        unk1 = stream.read(UShort)
        nb_characters = stream.read(UShort)
        character_id_list = [stream.read(UShort) for _ in range(nb_characters)]
        nb_doors = stream.read(UShort)
        door_list = [stream.read(Door) for _ in range(nb_doors)]
        return cls(unk1, character_id_list, door_list)

    def to_stream(self, stream: WriteStream) -> None:
        pass


class Buil(Section):
    _section_name = "BUIL"
    _section_version = 4

    def _load(self, substream: ReadStream) -> None:
        nb_building = substream.read(UShort)
        self.building_list = [substream.read(Building) for _ in range(nb_building)]

        nb_special_door = substream.read(UShort)
        self.special_door_list = [substream.read(Door) for _ in range(nb_special_door)]

    def _save(self, substream: WriteStream) -> None:
        pass
