from common import *

from .section import Section


class Cart(Section):
    _section_name = "CART"
    _section_version = 5

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
