from common import *

from .section import Section


class Elem(Section):
    _section_name = "ELEM"
    _section_version = 28

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
