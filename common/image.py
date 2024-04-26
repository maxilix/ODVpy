
import gzip
import bz2

from abc import ABC, abstractmethod
from PIL import Image, ImageDraw

from . import RWStreamable, UShort, UInt, Padding, Bytes


class Pixel(RWStreamable):

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
		r8 = (r5g6b5 >> 11) * 8
		g8 = ((r5g6b5 >> 5) & 0x3F) * 4
		b8 = (r5g6b5 & 0x1F) * 8
		return cls(r8, g8, b8)


class Pixmap(ABC):

	@staticmethod
	def needs(func):
		def wrapper(self, *arg, **kwargs):
			if self.bmp is None:
				self.build()
			func(self, *arg, **kwargs)
		return wrapper

	def __init__(self, width, height, data):
		self._width = width
		self._height = height
		self._data = data
		self._bmp = None

	@property
	def width(self):
		return self._width

	@property
	def height(self):
		return self._height

	@abstractmethod
	def build(self, *arg, **kwargs):
		pass

	def unbuild(self):
		self.bmp = None
		if hasattr(self, "draw"):
			self.draw = None

	@needs
	def show(self):
		self.bmp.show()

	@needs
	def save(self, filename):
		self.bmp.save(filename)


# class Mask(Pixmap):
#
# 	def build(self):
# 		self.bmp = Image.new("1", (self.width, self.height), self.data)
# 		self.draw = ImageDraw.Draw(self.bmp)
#
# 	@Pixmap.needs
# 	def draw_area(self, area, state):
# 		bounding_box = [(coor.x, coor.y) for coor in area.coor_list]
# 		try:
# 			self.draw.polygon(bounding_box, fill=state, outline=state)
#
# 		except Exception as e:
# 			print(f"{bounding_box=}")
#
# 	def allow(self, area):
# 		self.draw_area(area, True)
#
# 	def disallow(self, area):
# 		self.draw_area(area, False)

