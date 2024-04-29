
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
		self._misc = self.stream.read(Miscellaneous)
		self._bgnd = self.stream.read(MiniMap)
		self._move = self.stream.read(Motion)
		self._sght = self.stream.read(Sight)
		self._mask = self.stream.read(Masks)

		# self.build()

	@property
	def move(self):
		if self._move.loaded is False:
			self._move.load()
		return self._move


