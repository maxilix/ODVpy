from common import *

from odv.section import Section


class Fxbk(Section):
    _section_name = "FXBK"
    _section_version = 3

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
