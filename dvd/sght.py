from common import *

from .section import Section


class Sght(Section):

    _name = "SGHT"

    def _load(self, substream):
        substream.read_raw()

    def _save(self, substream):
        pass


