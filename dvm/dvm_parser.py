#!/usr/bin/enc python3

#import os

#import hqx
from PIL import Image, ImageDraw
from PyQt6.QtCore import QByteArray, QBuffer, QIODevice
from PyQt6.QtGui import QImage, QPainter, QPixmap
import gzip
import bz2

from common import *
from debug import *


"""
class LevelMap(Pixmap, ReadableFromStream):

	def __init__(self, width, height, data, compression):
		super().__init__(width, height, data)
		self.compression = compression

	@classmethod
	def from_stream(cls, stream):
		width = stream.read(UShort)
		height = stream.read(UShort)
		compression = stream.read(UInt)
		assert compression == 2
		size = stream.read(UInt)
		data = stream.read(Bytes, size)
		return cls(width, height, data, compression)

	def build(self):
		match self.compression:
			case 1:
				decompressed = zlib.decompress(self._data)
			case 2:
				decompressed = bz2.decompress(self._data)
			case _:
				decompressed = self._data
		self.bmp = Image.frombytes("RGB", (self.width, self.height), decompressed, "raw", "BGR;16")
		self.draw = ImageDraw.Draw(self.bmp, "RGBA")

	@Pixmap.needs
	def draw_segment(self, segment, color=GREEN, width=2):
		self.draw.line((segment.coor1.x, segment.coor1.y, segment.coor2.x, segment.coor2.y), width=width, fill=color)

	@Pixmap.needs
	def draw_cross(self, coordinate, color=BLUE, size=9):

		if size%2 == 0:
			size+=1
		s = (1-size)//2
		e = (size+1)//2

		self.draw.point((coordinate.x+s-1, coordinate.y+s  ), fill=color+"7f")
		self.draw.point((coordinate.x+s  , coordinate.y+s-1), fill=color+"7f")
		self.draw.point((coordinate.x+s-1, coordinate.y-s  ), fill=color+"7f")
		self.draw.point((coordinate.x+s  , coordinate.y-s+1), fill=color+"7f")
		for i in range(s, e):
			self.draw.point((coordinate.x+i  , coordinate.y+i  ), fill=color)
			self.draw.point((coordinate.x+i+1, coordinate.y+i  ), fill=color+"7f")
			self.draw.point((coordinate.x+i  , coordinate.y+i+1), fill=color+"7f")

			self.draw.point((coordinate.x+i  , coordinate.y-i  ), fill=color)
			self.draw.point((coordinate.x+i+1, coordinate.y-i  ), fill=color+"7f")
			self.draw.point((coordinate.x+i  , coordinate.y-i-1), fill=color+"7f")

	@Pixmap.needs
	def draw_area(self, area, color1=RED, width=2, alpha_in="2f"):
		bounding_box = [(coor.x, coor.y) for coor in area.coor_list]
		self.draw.polygon(bounding_box, fill=color1+alpha_in, outline=color1, width=width)

	def draw_mask(self, mask, color=RED, alpha_in="2f"):
		pass
		"""


class DvmParser(Parser):

	ext = "dvm"

	def __init__(self, filename):
		super().__init__(filename)

		self._width = self.stream.read(UShort)
		self._height = self.stream.read(UShort)
		compression = self.stream.read(UInt)
		assert compression == 2
		compressed_data_length = self.stream.read(UInt)
		self.compressed_data = self.stream.read(Bytes, compressed_data_length)
		self._data = bz2.decompress(self.compressed_data)
		self._level_map = None
		self._draw = None

	@property
	def level_map(self):
		if self._level_map is None:
			self._level_map = QImage(self._data, self._width, self._height, QImage.Format.Format_RGB16)
		return self._level_map

	@property
	def size(self):
		return (self._width, self._height)

	def draw(self, poly, pen, brush):
		if self._draw is None:
			self._draw = QImage(self._data, self._width, self._height, QImage.Format.Format_RGB16)

		painter = QPainter(self._draw)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)

		painter.setPen(pen)
		painter.setBrush(brush)
		painter.drawPolygon(poly)

		painter.end()
		# self._draw.save("test.png")

	def save_to_file(self, filename):
		if self._draw is None:
			data = self._data
		else:
			s = self._draw.sizeInBytes()
			data = bytes(self._draw.bits().asarray(s))
		compressed_data = Bytes(bz2.compress(data))
		compressed_data_length = UInt(len(compressed_data))

		stream = WriteStream()
		stream.write(self._width)
		stream.write(self._height)
		stream.write(UInt(2))  # compression type
		stream.write(compressed_data_length)
		stream.write(compressed_data)
		with open(filename, 'wb') as file:
			file.write(stream.get_value())
		print(f"Saved to {filename}")

	# def save_to_file(self, filename):
	# 	if self._draw is None:
	# 		data = self._data
	# 	else:
	# 		result = bytearray()
	# 		for y in range(self._height):
	# 			for x in range(self._width):
	# 				pixel = self._draw.pixel(x, y)
	# 				r5 = ((pixel & 0xFF0000) >> 19) & 0x1F
	# 				g6 = ((pixel & 0xFF00) >> 10) & 0x3F
	# 				b5 = ((pixel & 0xFF) >> 3) & 0x1F
	# 				rgb565 = ((r5 << 11) | (g6 << 5) | b5).to_bytes(2, byteorder='little')
	# 				result.extend(rgb565)
	# 		data = bytes(result)
	# 	compressed_data = Bytes(bz2.compress(data))
	# 	compressed_data_length = UInt(len(compressed_data))
	#
	# 	stream = WriteStream()
	# 	stream.write(self._width)
	# 	stream.write(self._height)
	# 	stream.write(UInt(2))  # compression type
	# 	stream.write(compressed_data_length)
	# 	stream.write(compressed_data)
	# 	with open(filename, 'wb') as file:
	# 		file.write(stream.get_value())
	# 	print(f"Saved to {filename}")
