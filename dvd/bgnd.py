import bz2
from PyQt6.QtGui import QImage, QColorTransform, QColor

from common import *

from .section import Section


class Bgnd(Section):

	_name = "BGND"
	_version = 4

	def _load(self, substream: ReadStream) -> None:
		filename_size = substream.read(UShort)
		self.minimap_name = substream.read(String, filename_size)
		width = substream.read(UShort)
		height = substream.read(UShort)
		compression = substream.read(UInt)
		assert compression == 2
		size = substream.read(UInt)
		data = substream.read(Bytes, size)
		decompressed = bz2.decompress(data)
		self.minimap = QImage(decompressed, width, height, width*2, QImage.Format.Format_RGB16)

		# TODO very inefficient
		self.minimap.convertTo(QImage.Format.Format_RGBA8888)
		for x in range(self.minimap.width()):
			for y in range(self.minimap.height()):
				if self.minimap.pixelColor(x, y) == QColor(0, 251, 0, 255):  # green color at the corner
					self.minimap.setPixelColor(x, y, QColor(0, 0, 0, 0))

	def _save(self, substream: WriteStream) -> None:
		pass
		# filename_size = UShort(len(self.minimap_name))
		# substream.write(filename_size)
		# substream.write(self.minimap_name)
		# width = UShort(self.minimap.width())
		# substream.write(width)
		# height = UShort(self.minimap.height())
		# substream.write(height)
		# compression = substream.Write(UInt(2))  # compression
		# data = QImage.






