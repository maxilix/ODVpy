from typing import Self

from common import *
from odv.odv_object import OdvBase


class LevelMap(OdvBase):
	def __init__(self, image):
		super().__init__()
		self.image = image
		self.modified = False

	@property
	def width(self):
		return self.image.width

	@property
	def height(self):
		return self.image.height

	# @property
	# def image(self):
	# 	if self._image is None:
	# 		self._image = QImage(self._data, self._width, self._height, QImage.Format.Format_RGB16)
	# 	return self._image
	#
	# @image.setter
	# def image(self, new_image: QImage):
	# 	self._image = new_image
	# 	self._width = self._image.width()
	# 	self._height = self._image.height()
	# 	self.modified = True

	@classmethod
	def from_stream(cls, stream: ReadStream) -> Self:
		image = stream.read(Image)
		return cls(image)

	def to_stream(self, stream: WriteStream) -> None:
		raise NotImplemented
		if self.modified:
			s = self.image.sizeInBytes()
			data = bytes(self.image.bits().asarray(s))
		else:
			data = self._data








class DvmParser(Parser):

	ext = "dvm"

	def __init__(self, filename):
		super().__init__(filename)
		self.level_map = self.stream.read(LevelMap, filename=filename)

	# @property
	# def level_map(self) -> LevelMap:
	# 	return self._level_map

	# @property
	# def width(self):
	# 	return self._level_map._width
	#
	# @property
	# def height(self):
	# 	return self._level_map._height

	# @property
	# def data(self) -> list[int]:
	# 	return [self._data[i] + 256*self._data[i+1] for i in range(0, len(self._data), 2)]
	#
	# @data.setter
	# def data(self, data: list[int]):
	# 	assert len(data)*2 == len(self._data)
	# 	self._data = b''.join([pixel.to_bytes(2, byteorder='little') for pixel in data])
	# 	self._level_map = QImage(self._data, self._width, self._height, QImage.Format.Format_RGB16)
	# 	self.modified = True

	def change_level_map_image(self, image_path):
		self.level_map.image = Image.from_file(image_path)
		self.level_map.modified = True

	# def draw(self, poly, pen, brush):
	# 	if self._draw is None:
	# 		self._draw = QImage(self._data, self._width, self._height, QImage.Format.Format_RGB16)
	#
	# 	painter = QPainter(self._draw)
	# 	painter.setRenderHint(QPainter.RenderHint.Antialiasing)
	#
	# 	painter.setPen(pen)
	# 	painter.setBrush(brush)
	# 	painter.drawPolygon(poly)
	#
	# 	painter.end()
	# 	# self._draw.save("test.png")

	def save_to_file(self, filename):
		stream = WriteStream()
		stream.write(self.level_map)
		with open(filename, 'wb') as file:
			file.write(stream.get_value())

	# def extract_to_bmp(self, filename):
	# 	self._level_map.save(filename)


