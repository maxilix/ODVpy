
from common import *

from .section import Section, section_list



class Sight(Section):

    section_index = 3  # SGHT

    def _load(self, substream):
        substream.read_raw()

    def _save(self, substream):
        pass


