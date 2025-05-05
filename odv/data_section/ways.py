from common import *

from odv.section import Section


class Ways(Section):
    _section_name = "WAYS"
    _section_version = 1

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
