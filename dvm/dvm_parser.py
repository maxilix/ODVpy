import bz2
from typing import Self

from PyQt6.QtGui import QImage

from common import *
from odv.odv_object import OdvBase


class LevelMap(OdvBase):
	def __init__(self, width, height, data, filename):
		super().__init__()
		self._filename = filename
		self._width = width
		self._height = height
		self._data = data
		self._image = None
		self.modified = False

	@property
	def width(self):
		return self._width

	@property
	def height(self):
		return self._height

	@property
	def filename(self):
		return self._filename

	@property
	def image(self):
		if self._image is None:
			self._image = QImage(self._data, self._width, self._height, QImage.Format.Format_RGB16)
		return self._image

	@image.setter
	def image(self, new_image: QImage):
		self._image = new_image
		self._width = self._image.width()
		self._height = self._image.height()
		self.modified = True

	@classmethod
	def from_stream(cls, stream: ReadStream, *, filename) -> Self:
		width = stream.read(UShort)
		height = stream.read(UShort)
		compression = stream.read(UInt)
		assert compression == 2
		compressed_data_length = stream.read(UInt)
		compressed_data = stream.read(Bytes, compressed_data_length)
		data = bz2.decompress(compressed_data)
		return cls(width, height, data, filename)

	def to_stream(self, stream: WriteStream) -> None:
		if self.modified:
			s = self.image.sizeInBytes()
			data = bytes(self.image.bits().asarray(s))
		else:
			data = self._data

		compressed_data = bz2.compress(data)
		compressed_data_length = len(compressed_data)

		stream.write(UShort(self._width))
		stream.write(UShort(self._height))
		stream.write(UInt(2))  # compression type
		stream.write(UInt(compressed_data_length))
		stream.write(Bytes(compressed_data))







class DvmParser(Parser):

	ext = "dvm"

	def __init__(self, filename):
		super().__init__(filename)
		self._level_map = self.stream.read(LevelMap, filename=filename)

	@property
	def level_map(self) -> LevelMap:
		return self._level_map

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
		self._level_map.image = QImage(image_path).convertedTo(QImage.Format.Format_RGB16)

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
		stream.write(self._level_map)
		with open(filename, 'wb') as file:
			file.write(stream.get_value())
		print(f"Saved to {filename}")

	# def extract_to_bmp(self, filename):
	# 	self._level_map.save(filename)


