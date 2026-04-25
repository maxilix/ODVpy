from odv.common import *
from odv.data_section import Sght, Ways, Move

from odv.section import Section


class Elem(Section):
    _section_id = 6
    _section_version = 28

    move: Move
    sght: Sght
    ways: Ways

    def _load(self, substream: ReadStream, level) -> None:
        self.move = level.data[2]
        self.sght = level.data[3]
        self.ways = level.data[5]
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
