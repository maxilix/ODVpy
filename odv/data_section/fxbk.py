from common import *

from odv.section import Section


class Fxbk(Section):
    _section_id = 7
    _section_version = 3

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
