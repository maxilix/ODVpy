from common import *

from odv.section import Section


class Pat(Section):
    _section_id = 10
    _section_version = 10

    def _load(self, substream: ReadStream, level) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
