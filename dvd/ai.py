from common import *

from .section import Section


class Ai(Section):
    _name = "AI  "
    _version = 2

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
