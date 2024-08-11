from common import *

from .section import Section


class Sght(Section):

    _section_name = "SGHT"
    _section_version = 6

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass


