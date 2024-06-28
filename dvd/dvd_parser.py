
from common import Parser, WriteStream, Bytes
from .misc import Misc
from .bgnd import Bgnd
from .move import Move
from .sght import Sght
from .mask import Mask


class DvdParser(Parser):

	ext = "dvd"

	def __init__(self, filename):
		super().__init__(filename)

		# Must be read in order
		self._misc = self.stream.read(Misc)
		self._bgnd = self.stream.read(Bgnd)
		self._move = self.stream.read(Move)
		self._sght = self.stream.read(Sght)
		self._mask = self.stream.read(Mask)
		self._tail = self.stream.read_raw()  # read all

	def save_to_file(self, filename):
		stream = WriteStream()
		stream.write(self._misc)
		stream.write(self._bgnd)
		stream.write(self._move)
		stream.write(self._sght)
		stream.write(self._mask)
		stream.write(Bytes(self._tail))
		with open(filename, 'wb') as file:
			file.write(stream.get_value())
		print(f"Saved to {filename}")

	@property
	def misc(self):
		if self._misc.loaded is False:
			self._misc.load()
		return self._misc

	@property
	def bgnd(self):
		if self._bgnd.loaded is False:
			self._bgnd.load()
		return self._bgnd

	@property
	def move(self):
		if self._move.loaded is False:
			self._move.load()
		return self._move




