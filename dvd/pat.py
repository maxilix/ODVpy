from common import *

from .section import Section


class Pat(Section):
    _name = "PAT "
    _version = 10

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
