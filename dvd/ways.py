from common import *

from .section import Section


class Ways(Section):
    _name = "WAYS"
    _version = 1

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
