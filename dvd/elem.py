from common import *

from .section import Section


class Elem(Section):
    _name = "ELEM"
    _version = 28

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
