import io

from abc import ABC, abstractmethod
from struct import pack, unpack

from .exception import PaddingError, ReadingTypeError

INDENT_SIZE = 5


class RWStreamable(ABC):
    @classmethod
    @abstractmethod
    def from_stream(cls, stream):
        pass

    # @classmethod
    # @abstractmethod
    # def to_stream(cls, stream):
    #     pass


class Bytes(RWStreamable):
    @classmethod
    def from_stream(cls, stream, length=None):
        if length is None:
            raise ReadingTypeError("length must be specified when reading Bytes")
        raw_bytes = stream.read_raw(length)
        stream.write(raw_bytes.hex())
        return raw_bytes


class Bool(RWStreamable):
    @classmethod
    def from_stream(cls, stream):
        raw_bytes = stream.read_raw(1)
        assert raw_bytes == b'\x00' or raw_bytes == b'\x01'
        stream.write(raw_bytes.hex())
        return raw_bytes == b'\x01'  # return a boolean


class ULittleEndianNumber(RWStreamable):
    length = None  # must be defined by inheriting objects

    @classmethod
    def from_stream(cls, stream):
        raw_bytes = stream.read_raw(cls.length)
        stream.write(raw_bytes.hex())
        return int.from_bytes(raw_bytes, byteorder="little", signed=False)


class UChar(ULittleEndianNumber):
    length = 1


class UShort(ULittleEndianNumber):
    length = 2


class UInt(ULittleEndianNumber):
    length = 4


class UFloat(RWStreamable):
    @classmethod
    def from_stream(cls, stream):
        raw_bytes = stream.read_raw(4)
        stream.write(raw_bytes.hex())
        return unpack('f', raw_bytes)[0]


class String(RWStreamable):
    @classmethod
    def from_stream(cls, stream, length=None):
        if length is None:
            raise ReadingTypeError("length must be specified when reading String")
        raw_bytes = stream.read_raw(length)
        while raw_bytes != b'' and raw_bytes[-1] == 0:
            raw_bytes = raw_bytes[:-1]
        stream.write(raw_bytes.hex())
        return raw_bytes.decode("latin1").replace(" ", "_")


class Padding(RWStreamable):
    @classmethod
    def from_stream(cls, stream, length=None, *, pattern=None):
        if length is None:
            raise ReadingTypeError("length must be specified when reading Padding")
        padding = stream.read_raw(length)
        if pattern is None and padding != b'\x00' * length:
            raise PaddingError(f"zero padding expected instead of : {padding}", padding=padding)
        elif pattern is not None and padding != pattern:
            raise PaddingError(f"{pattern} padding expected instead of : {padding}", padding=padding)
        stream.comment(f"Padding {padding.hex()}")



class ReadStream(object):

    def __init__(self, data):
        self._bytes_stream_in = io.BytesIO(data)
        self._str_stream_out = io.StringIO("")
        self._indent = 0
        self._new_line_indented = True

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

    # def p_print(self, length, group_length=None):
    # 	if type(length) is not int:
    # 		length = length.length
    # 	hex_string = self.read_raw(length).hex()
    # 	if group_length is None:
    # 		print(hex_string, end='')
    # 	else:
    # 		for i, c in enumerate(hex_string):
    # 			if i != 0 and i % (group_length*2) == 0:
    # 				print(" ", end='')
    # 			print(c, end='')
    # 	print(" ", end='')
    # 	return hex_string

    def read(self, object_type, *arg, **kwarg):
        assert issubclass(object_type, RWStreamable)
        return object_type.from_stream(self, *arg, **kwarg)

    def write(self, hex_string: str):
        if hex_string != "":
            int(hex_string, 16)  # assert hex_string is really hexadecimal
            self._str_stream_out.write(f"{hex_string.lower()} ")
            self._new_line_indented = False

    def comment(self, string: str):
        self._str_stream_out.write(f"[{string}] ")
        self._new_line_indented = False

    def indent(self):
        assert self._new_line_indented is True
        self._indent += 1
        self._str_stream_out.write(" " * INDENT_SIZE)

    def desindent(self):
        assert self._new_line_indented is True
        assert self._indent > 0
        self._indent -= 1
        self._str_stream_out.seek(self._str_stream_out.tell() - INDENT_SIZE)

    def new_line(self):
        self._str_stream_out.write("\n")
        self._str_stream_out.write(" " * INDENT_SIZE * self._indent)
        self._new_line_indented = True

    def new_space(self):
        self._str_stream_out.write("  ")

    def save_output(self, filename):
        file = open(filename, "w")
        file.write(self._str_stream_out.getvalue())
        file.close()

# def read_array(self, object_type, *arg, **kwarg):
# 	# assert issubclass(object_type, RWStreamable)
# 	length, hex_string = self.read(UShort)
# 	self.write_line(hex_string)
# 	rop = []
# 	self._indent += 1
# 	for _ in range(length):
# 		obj, hex_string = self.read(object_type, *arg, **kwarg)
#
#
# 	return [object_type.from_stream(self, *arg, **kwarg) for _ in range(length)]
#
# def write_raw(self, raw_string):
# 	self._str_stream_out.write(raw_string)
#
# def write_line(self, line):
# 	for _ in range(self._indent):
# 		self.write_raw("     ")
# 	self.write_raw(line)

# def skip(self, object_type, *arg, **kwarg):
# 	self.read(object_type, *arg, **kwarg)
