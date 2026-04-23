from common import *

from odv.section import Section


class Ai(Section):
    _section_id = 14
    _section_version = 2

    def _load(self, substream: ReadStream, level) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
