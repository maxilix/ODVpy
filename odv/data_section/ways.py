from typing import Self

from common import *
from config import CONFIG
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

"""
nb_patrol=25
   nb_waypoint=21
      15 : 0100   02 0500   0100   64 0a00   0300 07 fa 00
      0 : 
      15 : 01000105000100640a000300074b00
      0 : 
      0 : 
      20 : 010002050001004b0a000800058403ee02071e00
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      16 : 01000105000100320a00040007320000
      0 : 
      0 : 
      0 : 
      0 : 
      17 : 01000105000100640a0005000811003200
   nb_waypoint=8
      15 : 01000205000100640a000300075000
      36 : 01000105000200140d0050120003000203001000054c04520307320005ee02e803074b00
      21 : 01000105000100640a0009000578055802075e0100
      15 : 01000205000100640a000300020100
      0 : 
      0 : 
      0 : 
      17 : 01000105000100640a000500080400e803
   nb_waypoint=6
      16 : 01000205000100640a00040007640000
      0 : 
      0 : 
      0 : 
      23 : 010000050002004b0d001912000300074b000300072300
      27 : 01000005000200320d003213000400073200000600071900020000
   nb_waypoint=17
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
   nb_waypoint=1
      15 : 01000005000100640a0003000a0500
   nb_waypoint=11
      31 : 01000205000100640a001300074b00050c06a901071e000590060702074600
      0 : 
      28 : 01000105000100640a00100005630504010723000598069400072800
      15 : 01000205000100640a000300073c00
      20 : 01000105000100300a00080005cf05e100072800
      0 : 
      0 : 
      20 : 01000105000100640a00080005bb052f00072800
      0 : 
      28 : 01000205000100640a0010000516050900074b0005cd052400073200
      15 : 01000105000100640a000300072c01
   nb_waypoint=67
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      20 : 01000005000100640a00080006f0002104079600
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      28 : 01000005000100640a00100005f0001a04071e0005f000d304072800
      20 : 01000005000100640a00080005f0001a04073c00
      20 : 01000005000100640a00080005f0001a04073c00
      28 : 01000005000100640a001000059600f60407190005f0001f04079600
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      20 : 01000005000100640a000800059a04a801076400
      0 : 
      0 : 
      15 : 01000005000100640a000300076400
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
   nb_waypoint=8
      20 : 01000005000100640a000800055c084204076400
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      20 : 01000005000100640a000800055c084204076400
   nb_waypoint=10
      20 : 01000205000100640a0008000732000811007d00
      0 : 
      0 : 
      0 : 
      0 : 
      42 : 0200010800021b0002003210003215000300073200040007320000010064200008000514058200072300
      0 : 
      0 : 
      0 : 
      15 : 01000105000100640a000300075000
   nb_waypoint=42
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      20 : 01000105000100640a000800080c003200073200
      15 : 01000005000100640a000300075a00
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      23 : 01000005000100320a000b0007370005f109db01073c00
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      26 : 01000105000100640a000e00076e0005cf06ef01073c00020000
   nb_waypoint=3
      15 : 01000005000100640a000300074b00
      20 : 01000005000100640a00080005a4063f02075e01
      15 : 01000005000100640a000300076400
   nb_waypoint=2
      15 : 01000205000100640a00030007c800
      20 : 01000005000100640a000800054e078e03079600
   nb_waypoint=3
      23 : 01000205000100640a000b00055c08cc01074b00020200
      15 : 01000005000100640a00030007c800
      20 : 01000005000100640a0008000520087201074b00
   nb_waypoint=1
      26 : 01000005000100640a000e0007fa0005a40617020796000a0600
   nb_waypoint=24
      20 : 01000005000100640a00080005a4061202076400
      0 : 
      0 : 
      0 : 
      0 : 
      20 : 01000005000100320a000800055807ea01074100
      0 : 
      0 : 
      0 : 
      0 : 
      20 : 01000005000100640a00080005d6061c02074b00
      20 : 01000005000100640a000800057b077003075000
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      20 : 01000005000100640a00080005dc059501074b00
      0 : 
      0 : 
      0 : 
      15 : 01000005000100640a000300020000
   nb_waypoint=23
      20 : 01000005000100320a00080005bd061c02074b00
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      20 : 01000005000100320a00080005d0077e04073c00
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      20 : 01000005000100640a00080005bc02bc02079600
      0 : 
      0 : 
      0 : 
      0 : 
      0 : 
      15 : 01000105000100640a000300020000
   nb_waypoint=4
      18 : 01000005000100640a0006000a0b00079600
      18 : 01000005000100640a0006000a0e00077d00
      18 : 01000005000100640a0006000a0300076400
      21 : 01000005000100640a0009000a0800077d00020000
   nb_waypoint=1
      0 : 
   nb_waypoint=3
      24 : 01000105000100640a000c00073c00050203b603071e0000
      20 : 010002050001004b0a00080005e2048403073c00
      21 : 01000205000100640a00090005a406f401074b0000
   nb_waypoint=1
      0 : 
   nb_waypoint=1
      0 : 
   nb_waypoint=1
      0 : 
   nb_waypoint=1
      0 : 
   nb_waypoint=1
      0 : 
   nb_waypoint=1
      0 : 
"""

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
        # print(f"   {nb_waypoint=}")
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
