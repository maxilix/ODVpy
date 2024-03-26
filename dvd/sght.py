
from common import *

from .section import Section, section_list
from debug import hs_to_i, i_to_hsi


class Sight(Section):

    section = section_list[3]  # SGHT

    def _build(self):
        self._stream.read_raw()


