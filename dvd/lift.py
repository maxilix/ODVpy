from common import *

from .section import Section


class Lift(Section):
    _name = "LIFT"
    _version = 2

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
