from common import *

from odv.section import Section


class Msic(Section):
    _section_id = 8
    _section_version = 1

    def _load(self, substream: ReadStream, level) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
