from common import *

from odv.section import Section


class Mat(Section):
    _section_id = 12
    _section_version = 4

    def _load(self, substream: ReadStream, level) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
