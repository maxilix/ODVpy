from common import *

from .section import Section


class Pat(Section):
    _section_name = "PAT "
    _section_version = 10

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
