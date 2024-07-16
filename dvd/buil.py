from typing import Self

from common import *

from .section import Section


class DoorAccess(RWStreamable):
    def __init__(self, point: QPointF, z: int | UShort, layer_id: int | UShort) -> None:
        self.point = point
        self.z = z
        self.layer_id = layer_id

    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        point = stream.read(QPointF)
        z = stream.read(UShort)
        layer_id = stream.read(UShort)
        return cls(point, z, layer_id)

    def to_stream(self, stream: WriteStream) -> None:
        pass


class Door(RWStreamable):
    def __init__(self) -> None:
        pass

    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        door_type = stream.read(UChar)
        unk = stream.read(UChar)
        locked = stream.read(UChar)
        unlockable = stream.read(UChar)
        unk = stream.read(UChar)
        unk = stream.read(UChar)
        unk = stream.read(UChar)
        unk = stream.read(UChar)
        unk = stream.read(UChar)
        unk = stream.read(UChar)

        shape = stream.read(QPolygonF)
        nb_access = stream.read(UShort)
        assert nb_access == 3
        accesses = [stream.read(DoorAccess) for _ in range(nb_access)]

        unk_last = stream.read(UShort)
        if unk_last != 0xffff:
            unk = stream.read(UChar)
            unk = stream.read(UChar)

        return cls()

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
        door_list = [stream.read(UShort) for _ in range(nb_doors)]
        return cls(unk1, character_id_list, door_list)

    def to_stream(self, stream: WriteStream) -> None:
        pass


class Buil(Section):
    _name = "BUIL"
    _version = 4

    def _load(self, substream: ReadStream) -> None:
        nb_building = substream.read(UShort)
        self.building_list = [substream.read(Building) for _ in range(nb_building)]

        nb_special_door = substream.read(UShort)
        self.special_door_list = [substream.read(Door) for _ in range(nb_special_door)]

    def _save(self, substream: WriteStream) -> None:
        pass
