from common import *

from .section import Section


class Jump(Section):
    _section_name = "JUMP"
    _section_version = 1

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
