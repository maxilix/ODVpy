#!/usr/bin/enc python3
"""

"""
import bz2
from PIL import Image

from common import *

from .section import Section, section_list





class LevelMiniMap(Pixmap, ReadableFromStream):

	@classmethod
	def from_stream(cls, stream):
		width = stream.read(UShort)
		height = stream.read(UShort)
		compression = stream.read(UInt)
		assert compression == 2
		size = stream.read(UInt)
		data = stream.read(Bytes, size)
		return cls(width, height, data)

	def build(self):
		decompressed = bz2.decompress(self.data)
		self.bmp = Image.frombytes("RGB", (self.width, self.height), decompressed, "raw", "BGR;16")








class MiniMap(Section):

	section = section_list[1] # BGND

	def build(self):
		stream = ByteStream(self.data)

		version = stream.read(UInt)
		assert version == 4
		filename_size = stream.read(UShort)
		self.filename = stream.read(String, filename_size)
		self.minimap = stream.read(LevelMiniMap)

		super().build(stream)



