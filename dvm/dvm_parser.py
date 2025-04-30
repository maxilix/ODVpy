from typing import Self

from common import *
from odv.odv_object import OdvBase


class LevelMap(OdvBase):
	def __init__(self, image):
		super().__init__()
		self.image = image
		# self.modified = False  #todo del-it

	@property
	def width(self):
		return self.image.width

	@property
	def height(self):
		return self.image.height

	@classmethod
	def from_stream(cls, stream: ReadStream) -> Self:
		image = stream.read(Image)
		return cls(image)

	def to_stream(self, stream: WriteStream) -> None:
		stream.write(self.image)


class DvmParser(Parser):

	ext = "dvm"

	def __init__(self, filename):
		super().__init__(filename)
		self.level_map = self.stream.read(LevelMap)

	def save_to_file(self, filename):
		stream = WriteStream()
		stream.write(self.level_map)
		with open(filename, 'wb') as file:
			file.write(stream.get_value())



