from typing import Self

from common import *
from odv.data_section import Move
from odv.odv_object import OdvObjectIterable, OdvObject
from odv.section import Section

"""
Data.A.u1:
  0 = Execute in both directions
  1 = Execute when going forward
  2 = Execute when going backward

Data.B.A.u1:
  x = Chance of being executed

WaypointCommands:
  Elements:
    0x00: Unknown() // Flips single byte
    0x01: SkipWaypoint()
    0x02: GoToWaypoint(ubyte index)
    0x03: Unused()
    0x04: SetAIState(ubyte state) // Might need a "Wait" afterwards to take effect
    0x05: FaceToAndStare(ushort x, ushort y)
    0x06: GlanceAt(ushort x, ushort y)
    0x07: Wait(ushort duration)
    0x08: CheckFor(ushort id, ushort timeout) // ID skips animations (another reason to use unique IDs)
    0x09: CheckForSync(ushort id, ushort timeout, ushort friendWaypointIndex)
    0x0A: FaceTo(ubyte direction)

  Mobile Elements:
    0x80: MobileSprite1(ushort sprite) // Unk
    0x81: SetSpeed(float speed)
    0x82: Accelerate(float speedTarget, ushort atWaypoint)
    0x83: Wait(ushort duration)
    0x84: JumpToStart()
    0x85: MobileSprite2(ushort sprite) // Unk
    0x86: MobileSprite3(ushort sprite) // Unk
"""

class WaypointCommands(RStreamable):
    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        rop = cls()
        length = stream.read(UShort)
        # print(f"l{length}")
        rop.cmds = [stream.read(Bytes, 1) for _ in range(length)]
        # print(f"cmds {rop.cmds.hex()}")
        return rop


class WaypointDataA(RStreamable):
    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        rop = cls()
        rop.u1 = stream.read(UChar)
        # print(rop.u1)
        rop.u2 = stream.read(UShort)
        # print(rop.u2)
        return rop

class WaypointDataB(RStreamable):
    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        rop = cls()
        c = stream.read(UShort)

        rop.a_list = [stream.read(WaypointDataA) for _ in range(c)]
        assert all([0 <= a.u1 <= 100 for a in rop.a_list])
        assert 0 <= sum([a.u1 for a in rop.a_list]) <= 100

        # observed values for a.u2 : 10, 13, 16, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 31, 32, 33, 34, 36, 37, 39, 41, 42, 56, 58, 59, 63, 67, 76
        rop.cmds_list = [stream.read(WaypointCommands) for _ in range(c)]
        return rop

    def __len__(self):
        return 2 + 3* len(self.a_list) + 2*len(self.cmds_list) + sum([len(cmd.cmds) for cmd in self.cmds_list])


class WaypointData(RStreamable):
    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        rop = cls()
        c = stream.read(UShort)
        assert c in [1, 2]

        rop.a_list = [stream.read(WaypointDataA) for _ in range(c)]
        assert all([a.u1 in [0,1,2] for a in rop.a_list])
        if c == 2:
            assert sorted([a.u1 for a in rop.a_list]) == [1, 2]




        # observed values for a.u2 : 5, 8, 16, 18, 20, 21, 23, 26, 27, 28, 31, 34, 36, 51, 62
        rop.b_list = [stream.read(WaypointDataB) for _ in range(c)]

        if c == 1:
            assert rop.a_list[0].u2 == 5
        if c == 2:
            assert rop.a_list[0].u2 == 8
            assert rop.a_list[1].u2 == 8 + len(rop.b_list[0])


        return rop


#              [          B             ]
#      [  A  ]      [  A  ]
# 0100 02 0500 0100 64 0a00 0300 07 fa 00



#                      [                      B                          ] [                   B                   ]
#      [  A  ] [  A  ]      [  A  ] [  A  ]      [ cmd  ]      [   cmd   ]      [  A  ]      [         cmd         ]
# 0200 01 0800 02 1b00 0200 32 1000 32 1500 0300 07 32 00 0400 07 32 00 00 0100 64 2000 0800 05 14 05 82 00 07 23 00
#  0 1  2  3 4  5  6 7  8 9  a  b c  d  e f 1011 12 13 14 1516 17 18 19 1a 1b1c 1d 1e1f 20

class Waypoint(OdvObject):
    move: Move

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent, move) -> Self:
        rop = cls(parent)
        rop.move = move
        rop.point = stream.read(QPointF)  # maybe y,x instead of x,y
        rop.sector = move.sector(stream.read(UShort))
        layer_id = stream.read(UShort)
        assert rop.sector.parent.i == layer_id
        has_classname = stream.read(UChar)
        data_size = stream.read(UShort)
        if has_classname:
            rop.classname = stream.read(String, data_size)
            rop.data = None
            # print(f"      {rop.point} - {rop.classname} {layer_id} {rop.sector}")

        else:
            rop.classname = None
            if data_size > 0:
                rop.data = stream.read(WaypointData)
            else:
                rop.data = None
            # rop.data = stream.read(Bytes, data_size)
            # print(f"      {data_size} : {rop.data.hex() }")
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        pass


class Patrol(OdvObjectIterable):
    move: Move
    waypoint_list: list[Waypoint]

    def __iter__(self):
        return iter(self.waypoint_list)

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent, move) -> Self:
        rop = cls(parent)
        rop.move = move
        nb_waypoint = stream.read(UShort)
        rop.waypoint_list = [stream.read(Waypoint, parent=rop, move=move) for _ in range(nb_waypoint)]
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        nb_waypoint = len(self)
        stream.write(UShort(nb_waypoint))
        for waypoint in self.waypoint_list:
            stream.write(waypoint)




class Ways(Section, OdvObjectIterable):
    _section_name = "WAYS"
    _section_version = 1

    move: Move
    patrol_list: list[Patrol]

    def __iter__(self):
        return iter(self.patrol_list)

    def _load(self, substream: ReadStream, *, move) -> None:
        self.move = move
        nb_patrol = substream.read(UShort)
        # print(f"{nb_patrol=}")

        self.patrol_list = [substream.read(Patrol, parent=self, move=move) for _ in range(nb_patrol)]
        # assert

    def _save(self, substream: WriteStream) -> None:
        pass
