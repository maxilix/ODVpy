
from common import Parser
from .misc import Miscellaneous
from .bgnd import MiniMap
from .move import Motion
from .sght import Sight
from .mask import Masks


class DvdParser(Parser):

	extension = "dvd"

	def __init__(self, filename):
		super().__init__(filename)

		# Must be read in order
		self.misc = self.stream.read(Miscellaneous)
		self.bgnd = self.stream.read(MiniMap)
		self.move = self.stream.read(Motion)
		self.sght = self.stream.read(Sight)
		self.mask = self.stream.read(Masks)

		# self.build()

	def build(self):
		self.misc.build()
		self.bgnd.build()
		self.move.build()
		# self.sght.build()
		self.mask.build()
		pass
