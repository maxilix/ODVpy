from typing import Self

from common import *

from .section import Section

class DlgsTextWaveEntries(RStreamable):
    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        rop = cls()
        rop.u1 = stream.read(UInt)
        rop.u2 = stream.read(UInt)
        rop.u3 = stream.read(UInt)
        return rop

class DlgsTricks(RStreamable):
    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        rop = cls()
        rop.index = stream.read(UInt)
        nb_entry = stream.read(UInt)
        rop.entries = [stream.read(UInt) for _ in range(nb_entry)]
        return rop

class DlgsObjectives(RStreamable):
    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        rop = cls()
        rop.index = stream.read(UInt)
        nb_entry = stream.read(UInt)
        rop.entries = [stream.read(UInt) for _ in range(nb_entry)]
        return rop

class DlgsDebriefing(RStreamable):
    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        rop = cls()
        rop.index = stream.read(UInt)
        nb_entry1 = stream.read(UInt)
        rop.entries1 = [stream.read(UInt) for _ in range(nb_entry1)]
        nb_entry2 = stream.read(UInt)
        rop.entries2 = [stream.read(UInt) for _ in range(nb_entry2)]
        return rop


class Dlgs(Section):
    _section_name = "DLGS"
    _section_version = 4

    def _load(self, substream: ReadStream) -> None:
        self.index_text = substream.read(UInt)
        self.index_wave = substream.read(UInt)
        self.DlgsTextWaveEntries_list = []
        nb_i = substream.read(UInt)
        for i in range(nb_i):
            self.DlgsTextWaveEntries_list.append([])
            nb_j = substream.read(UInt)
            for j in range(nb_j):
                self.DlgsTextWaveEntries_list[i].append(substream.read(DlgsTextWaveEntries))

        self.triks = substream.read(DlgsTricks)
        self.objectives = substream.read(DlgsObjectives)
        self.debriefing = substream.read(DlgsDebriefing)

    def _save(self, substream: WriteStream) -> None:
        pass
