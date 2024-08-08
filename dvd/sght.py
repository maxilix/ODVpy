from common import *

from .section import Section


class Sght(Section):

    _name = "SGHT"
    _version = 6

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass


