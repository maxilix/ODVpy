
import io

from abc import ABC, abstractmethod
from struct import pack, unpack

from .exception import PaddingError, ReadingTypeError


class ReadableFromStream(ABC):

	@classmethod
	@abstractmethod
	def from_stream(cls, stream):
		pass


class Bytes(ReadableFromStream):
	@classmethod
	def from_stream(cls, stream, length=None):
		if length is None:
			raise ReadingTypeError("length must be specified when reading Bytes")
		raw_bytes = stream.read_raw(length)
		return raw_bytes


class Bool(ReadableFromStream):
	@classmethod
	def from_stream(cls, stream):
		raw_bytes = stream.read_raw(1)
		if raw_bytes == b'\x00':
			return False
		elif raw_bytes == b'\x01':
			return True
		else:
			raise


class ULittleEndianNumber(ReadableFromStream):
	length = None  # must be defined by inheriting objects

	@classmethod
	def from_stream(cls, stream):
		raw_bytes = stream.read_raw(cls.length)
		return int.from_bytes(raw_bytes, byteorder="little", signed=False)


class UChar(ULittleEndianNumber):
	length = 1


class UShort(ULittleEndianNumber):
	length = 2


class UInt(ULittleEndianNumber):
	length = 4


class UFloat(ReadableFromStream):
	@classmethod
	def from_stream(cls, stream):
		return unpack('f', stream.read_raw(4))[0]


class String(ReadableFromStream):
	@classmethod
	def from_stream(cls, stream, length=None):
		if length is None:
			raise ReadingTypeError("length must be specified when reading String")
		raw_bytes = stream.read_raw(length)
		while raw_bytes != b'' and raw_bytes[-1] == 0:
			raw_bytes = raw_bytes[:-1]
		return raw_bytes.decode("latin1").replace(" ", "_")


class Padding(ReadableFromStream):
	@classmethod
	def from_stream(cls, stream, length=None, *, pattern=None):
		if length is None:
			raise ReadingTypeError("length must be specified when reading Padding")
		padding = stream.read_raw(length)
		if pattern is None and padding != b'\x00'*length:
			raise PaddingError(f"zero padding expected instead of : {padding}", padding=padding)
		elif pattern is not None and padding != pattern:
			raise PaddingError(f"{pattern} padding expected instead of : {padding}", padding=padding)


class ReadStream(object):

	def __init__(self, data):
		self._bytes_stream_in = io.BytesIO(data)
		self._str_stream_out = io.StringIO("")

	@classmethod
	def from_file(cls, filename):       
		fd = open(filename, "rb")
		data = fd.read()
		fd.close()
		return cls(data)

	def tell(self):
		return self._bytes_stream_in.tell()

	def read_raw(self, length=None):
		return self._bytes_stream_in.read(length)

	def p_print(self, length, group_length=None):
		if type(length) is not int:
			length = length.length
		hex_string = self.read_raw(length).hex()
		if group_length is None:
			print(hex_string, end='')
		else:
			for i, c in enumerate(hex_string):
				if i != 0 and i % (group_length*2) == 0:
					print(" ", end='')
				print(c, end='')
		print(" ", end='')
		return hex_string

	def read(self, object_type, *arg, **kwarg):
		return object_type.from_stream(self, *arg, **kwarg)

	def skip(self, object_type, *arg, **kwarg):
		self.read(object_type, *arg, **kwarg)
