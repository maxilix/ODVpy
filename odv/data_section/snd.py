from common import *

from odv.section import Section


class Snd(Section):
    _section_name = "SND "
    _section_version = 7

    def _load(self, substream: ReadStream) -> None:
        substream.read_raw()

    def _save(self, substream: WriteStream) -> None:
        pass
