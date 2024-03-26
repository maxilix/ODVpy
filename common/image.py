
import gzip
import bz2

from abc import ABC, abstractmethod
from PIL import Image, ImageDraw

from . import ReadableFromStream, UShort, UInt, Padding, Bytes


class Pixel(ReadableFromStream):

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
		r = (r5g6b5 >> 11) * 8
		g = ((r5g6b5 >> 5) & 0x3F) * 4
		b = (r5g6b5 & 0x1F) * 8
		return cls(r, g, b)


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


class Mask(Pixmap):

	def build(self):
		self.bmp = Image.new("1", (self.width, self.height), self.data)
		self.draw = ImageDraw.Draw(self.bmp)

	@Pixmap.needs
	def draw_area(self, area, state):
		bounding_box = [(coor.x, coor.y) for coor in area.coor_list]
		try:
			self.draw.polygon(bounding_box, fill=state, outline=state)
			
		except Exception as e:
			print(f"{bounding_box=}")

	def allow(self, area):
		self.draw_area(area, True)

	def disallow(self, area):
		self.draw_area(area, False)


"""
class Ellipse(Bitmap):

	def __init__(self, x_radius, y_radius, outline_color=None, width=1, fill_color=None):
		total_width = x_radius*2 + width + 1
		total_height = y_radius*2 + width + 1
		data = {"outline_color":outline_color, "fill_color":fill_color, "width":width}
		super().__init__(total_width, total_height, data)

	def build(self):
		radius = self.data["radius"]
		width = self.data["width"]
		center = self.width//2
		self.bmp = Image.new('RGBA', (self.width, self.height), color=(0,0,0,0))
		draw = ImageDraw.Draw(self.bmp, "RGBA")
		draw.ellipse([(0, 0), (total_width, total_height)], fill=None, outline=None, width=1)
		
		for y in range(self.height):
			nb_transparent_pixel = stream.read(UShort)
			nb_total_pixel = stream.read(UShort)
			for x in range(self.width):
				if nb_total_pixel == 65535 or x > nb_total_pixel:
					break
				elif x < nb_transparent_pixel:
					continue
				else:
					pixel = stream.read(Pixel)
					self.bmp.putpixel((x+x_offset,y+y_offset), pixel.to_rgb())
"""
