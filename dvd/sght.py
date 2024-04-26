
from common import *

from .section import Section, section_list



class Sight(Section):

    section = section_list[3]  # SGHT

    def _build(self):
        self._stream.read_raw()


