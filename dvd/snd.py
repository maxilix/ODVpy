from common import *

from .section import Section


class Snd(Section):
    _name = "SND "
    _version = 7

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
