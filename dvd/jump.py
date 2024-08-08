from common import *

from .section import Section


class Jump(Section):
    _name = "JUMP"
    _version = 1

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
