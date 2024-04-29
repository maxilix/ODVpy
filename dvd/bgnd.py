

import bz2
from PIL import Image
from PyQt6.QtGui import QImage


from common import *

from .section import Section


# class LevelMiniMap(Pixmap, ReadableFromStream):
#
# 	@classmethod
# 	def from_stream(cls, stream):
# 		width = stream.read(UShort)
# 		height = stream.read(UShort)
# 		compression = stream.read(UInt)
# 		assert compression == 2
# 		size = stream.read(UInt)
# 		data = stream.read(Bytes, size)
# 		return cls(width, height, data)
#
# 	def build(self):
# 		decompressed = bz2.decompress(self.data)
# 		self.bmp = Image.frombytes("RGB", (self.width, self.height), decompressed, "raw", "BGR;16")


class MiniMap(Section):

	section_index = 1  # BGND

	def _load(self, substream):
		version = substream.read(Version)
		assert version == 4
		filename_size = substream.read(UShort)
		self.minimap_name = substream.read(String, filename_size)
		width = substream.read(UShort)
		height = substream.read(UShort)
		compression = substream.read(UInt)
		assert compression == 2
		size = substream.read(UInt)
		data = substream.read(Bytes, size)
		decompressed = bz2.decompress(data)
		self.minimap = QImage(decompressed, width, height, QImage.Format.Format_RGB16)

	def _save(self, substream):
		pass
		# substream.write(Version(4))
		# filename_size = UShort(len(self.minimap_name))
		# substream.write(filename_size)
		# substream.write(self.minimap_name)
		# width = UShort(self.minimap.width())
		# substream.write(width)
		# height = UShort(self.minimap.height())
		# substream.write(height)
		# compression = substream.Write(UInt(2))  # compression
		# data = QImage.






