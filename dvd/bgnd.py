

import bz2
from PIL import Image
from PyQt6.QtGui import QImage


from common import RWStreamable, UShort, UInt, Bytes, ReadStream, String

from .section import Section, section_list


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

	section = section_list[1] # BGND

	def _build(self):
		version = self._stream.read(UInt)
		assert version == 4
		filename_size = self._stream.read(UShort)
		self.minimap_name = self._stream.read(String, filename_size)
		width = self._stream.read(UShort)
		height = self._stream.read(UShort)
		compression = self._stream.read(UInt)
		assert compression == 2
		size = self._stream.read(UInt)
		data = self._stream.read(Bytes, size)
		decompressed = bz2.decompress(data)
		self.minimap = QImage(decompressed, width, height, QImage.Format.Format_RGB16)





