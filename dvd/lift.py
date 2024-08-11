from typing import Self, Iterator

from common import *

from .section import Section


class LiftEntry(RWStreamable):
    def __init__(self, lift_global_id, lift_type, under_global_id, under_layer_id, under_gateway, over_global_id, over_layer_id, over_gateway, shape,
                 perspective) -> None:
        # each global id (lift, under and over) refer to the MOVE global id

        self.lift_global_id = lift_global_id
        # the lift area hasn't layer_id because lifts layer is always the last layer
        self.lift_type = lift_type

        self.under_global_id = under_global_id
        self.under_layer_id = under_layer_id
        self.under_gateway = under_gateway

        self.over_global_id = over_global_id
        self.over_layer_id = over_layer_id
        self.over_gateway = over_gateway

        self.shape = shape
        self.perspective = perspective

    def __str__(self):
        return f"{self.lift_global_id} T{self.lift_type} - A1 {self.under_global_id} {self.under_layer_id} - A2 {self.over_global_id} {self.over_layer_id} - {len(self.shape)}"

    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        lift_global_id = stream.read(UShort)
        lift_type = stream.read(UChar)
        # 0: ????
        # 1: stair
        # 2: ladder
        # 3: wall

        under_global_id = stream.read(UShort)
        under_layer_id = stream.read(UShort)  # layer id

        over_global_id = stream.read(UShort)
        over_layer_id = stream.read(UShort)  # layer id

        shape = stream.read(QPolygonF)

        under_gateway = stream.read(Gateway)
        over_gateway = stream.read(Gateway)

        perspective = stream.read(UShort)
        return cls(lift_global_id, lift_type, under_global_id, under_layer_id, under_gateway, over_global_id, over_layer_id, over_gateway, shape, perspective)

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(UShort(self.lift_global_id))
        stream.write(UChar(self.lift_type))

        stream.write(UShort(self.under_global_id))
        stream.write(UShort(self.under_layer_id))  # layer id

        stream.write(UShort(self.over_global_id))
        stream.write(UShort(self.over_layer_id))  # layer id

        stream.write(self.shape)

        stream.write(self.under_gateway)
        stream.write(self.over_gateway)

        stream.write(UShort(self.perspective))


class Lift(Section):
    _section_name = "LIFT"
    _section_version = 2



    def __iter__(self) -> Iterator[LiftEntry]:
        return iter(self.lift_list)

    def __getitem__(self, index: int) -> LiftEntry:
        return self.lift_list[index]

    def __len__(self) -> int:
        return len(self.lift_list)


    def _load(self, substream: ReadStream) -> None:
        # tail = substream.read_raw()
        # print(tail.hex())
        # exit()
        nb_lift = substream.read(UShort)
        self.lift_list = [substream.read(LiftEntry) for _ in range(nb_lift)]
        # self.tail = substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        nb_lift = len(self.lift_list)
        substream.write(UShort(nb_lift))
        for lift_entry in self.lift_list:
            substream.write(lift_entry)
