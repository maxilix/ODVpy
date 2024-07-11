from common import *

from .section import Section


class Buil(Section):
    _name = "BUIL"
    _version = 4

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
