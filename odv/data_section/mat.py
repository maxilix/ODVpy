from common import *

from odv.section import Section


class Mat(Section):
    _section_name = "MAT "
    _section_version = 4

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
