
from . import ReadableFromStream, UShort


class Coordinate(ReadableFromStream):

	def __init__(self, x, y):
		if not (isinstance(x, int) and isinstance(y, int)):
			raise TypeError("Coordinate must be (int, int)")
		self.x = x
		self.y = y

	@classmethod
	def from_stream(cls, stream):
		x = stream.read(UShort)
		y = stream.read(UShort)
		return cls(x, y)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __repr__(self):
		return f"<Coordinate {self}>"

	def __str__(self):
		return f"({self.x}, {self.y})"


class Segment(ReadableFromStream):

	def __init__(self, coor1, coor2):
		if not (isinstance(coor1, Coordinate) and isinstance(coor1, Coordinate)):
			raise TypeError("Segment must be Coordinate to Coordinate")
		self.coor1 = coor1
		self.coor2 = coor2

	@classmethod
	def from_stream(cls, stream):
		coor1 = stream.read(Coordinate)
		coor2 = stream.read(Coordinate)
		return cls(coor1, coor2)

	def __repr__(self):
		return f"<Segment {str(self)}>"

	def __str__(self):
		return f"{self.coor1} -> {self.coor2}"


class Area(ReadableFromStream):
	def __init__(self, coor_list):
		if not (isinstance(coor_list, list) and all(isinstance(c, Coordinate) for c in coor_list)):
			raise TypeError("Area must be a list of Coordinate")
		self.coor_list = coor_list

	@classmethod
	def from_stream(cls, stream):
		nb_coor = stream.read(UShort)
		coor_list = [stream.read(Coordinate) for _ in range(nb_coor)]
		return cls(coor_list)
