from common import *

from .section import Section


class Mat(Section):
    _name = "MAT "
    _version = 4

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
