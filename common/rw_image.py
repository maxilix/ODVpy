
import gzip
import bz2

import cv2
import numpy as np

from .rw_stream import RWStreamable, RStreamable
from .rw_base import UShort, UInt, Bytes


class Pixel(RStreamable):

	def __init__(self, r,g,b,a=255):
		self._r = r
		self._g = g
		self._b = b
		self._a = a

	def to_rgb(self):
		return self._r, self._g, self._b

	def to_rgba(self):
		return self._r, self._g, self._b, self._a

	@classmethod
	def from_stream(cls, stream):
		r5g6b5 = stream.read(UShort)
		#  red     green     blue
		# 00000   000 000   00000
		r8 = (r5g6b5 >> 11) * 8
		g8 = ((r5g6b5 >> 5) & 0x3F) * 4
		b8 = (r5g6b5 & 0x1F) * 8
		return cls(r8, g8, b8)


class Image(RWStreamable):
	def __init__(self, image):
		self._image = image  # numpy array stored in BGR format

	@property
	def height(self):
		return self._image.shape[0]

	@property
	def width(self):
		return self._image.shape[1]

	@property
	def data(self):
		return self._image.data

	def rgba(self):
		image_bgr = self._image
		image_rgba = np.zeros((self.height, self.width, 4), dtype=np.uint8)
		image_rgba[:, :, 0] = image_bgr[:, :, 2]
		image_rgba[:, :, 1] = image_bgr[:, :, 1]
		image_rgba[:, :, 2] = image_bgr[:, :, 0]
		image_rgba[:, :, 3] = 255
		transparency = np.array([0, 248, 0])  # Green
		mask = np.all(image_bgr == transparency, axis=-1)
		image_rgba[mask, 3] = 0
		return image_rgba

	def debug_show(self):
		cv2.imshow("", self._image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	@classmethod
	def from_file(cls, filename):
		image = cv2.imread(filename, cv2.IMREAD_COLOR)
		return cls(image)

	@classmethod
	def from_stream(cls, stream):
		width = stream.read(UShort)
		height = stream.read(UShort)
		compression = stream.read(UInt)
		size = stream.read(UInt)
		data = stream.read(Bytes, size)
		if compression == 2:
			decompressed = bz2.decompress(data)
		else:
			# to_stream always write bz2 compression
			raise NotImplemented(f"compression type {compression}")

		image_565 = np.frombuffer(decompressed, dtype=np.uint16).reshape((height, width))
		image = np.zeros((height, width, 3), dtype=np.uint8)
		image[:, :, 0] = 8*(image_565 & 0x1F)
		image[:, :, 1] = 4*((image_565 >> 5) & 0x3F)
		image[:, :, 2] = 8*((image_565 >> 11) & 0x1F)
		return cls(image)

	def to_stream(self, stream):
		stream.write(UShort(self.width))
		stream.write(UShort(self.height))
		stream.write(UInt(2))  # bz2 compression

		r_565 = (self._image[:, :, 2] >> 3) & 0x1F
		g_565 = (self._image[:, :, 1] >> 2) & 0x3F
		b_565 = (self._image[:, :, 0] >> 3) & 0x1F
		image_565 = ((r_565.astype(np.uint16) << 11) | (g_565.astype(np.uint16) << 5) | b_565)

		decompressed = image_565.tobytes()
		data = bz2.compress(decompressed)
		size = len(data)
		stream.write(UInt(size))
		stream.write(Bytes(data))