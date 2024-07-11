from common import *

from .section import Section


class Scrp(Section):
    _name = "SCRP"
    _version = 1

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
