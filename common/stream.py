#!/usr/bin/enc python3



import io
#import sys
import logging as log

from abc import ABC, abstractmethod
from struct import pack, unpack


from . import PaddingError




class ReadableFromStream(ABC):

	@classmethod
	@abstractmethod
	def from_stream(cls, stream, *arg, **kwarg):
		pass


class Bytes(ReadableFromStream):
	@classmethod
	def from_stream(cls, stream, length):
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


class UChar(ReadableFromStream):
	@classmethod
	def from_stream(cls, stream):
		raw_bytes = stream.read_raw(1)
		return int.from_bytes(raw_bytes, byteorder="little", signed=False)


class UShort(ReadableFromStream):
	@classmethod
	def from_stream(cls, stream):
		raw_bytes = stream.read_raw(2)
		return int.from_bytes(raw_bytes, byteorder="little", signed=False)


class UInt(ReadableFromStream):
	@classmethod
	def from_stream(cls, stream):
		raw_bytes = stream.read_raw(4)
		return int.from_bytes(raw_bytes, byteorder="little", signed=False)


class UFloat(ReadableFromStream):
	@classmethod
	def from_stream(cls, stream):
		return unpack('f', stream.read_raw(4))[0]


class String(ReadableFromStream):
	@classmethod
	def from_stream(cls, stream, length):
		raw_bytes = stream.read_raw(length)
		while raw_bytes != b'' and raw_bytes[-1] == 0:
			raw_bytes = raw_bytes[:-1]
		return raw_bytes.decode("latin1").replace(" ", "_")


class Padding(ReadableFromStream):
	@classmethod
	def from_stream(cls, stream, length, *, pattern=None):
		padding = stream.read_raw(length)
		if pattern is None and padding != b'\x00'*length:
			raise PaddingError(f"zero padding expected insteed of : {padding}", padding=padding)
		elif pattern is not None and padding != pattern:
			raise PaddingError(f"{pattern} padding expected insteed of : {padding}", padding=padding)


class ByteStream:

	def __init__(self, data):
		self._io = io.BytesIO(data)

	@classmethod
	def from_file(cls, filename):       
		fd = open(filename, "rb")
		rop = cls(fd.read())
		fd.close()
		return rop

	def tell(self):
		return self._io.tell()

	def read_raw(self, length=None):
		return self._io.read(length)

	def print(self, length, group_length=None):
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
