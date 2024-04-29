from abc import ABC
from struct import unpack, pack

from .rw_stream import RWStreamable
from .exception import ReadingError, NegativeUnsignedError, TooBigError


class Bytes(bytes, RWStreamable):

    @classmethod
    def from_stream(cls, stream, length=None):
        if length is None:
            raise ReadingError(f"length must be specified when reading {cls.__name__}")
        raw_bytes = stream.read_raw(length)
        # stream.debug_print(raw_bytes.hex())
        return raw_bytes

    def to_stream(self, stream):
        stream.write_raw(self)


# class Bool(bool, RWStreamable):
#
#     @classmethod
#     def from_stream(cls, stream):
#         raw_bytes = stream.read_raw(1)
#         assert raw_bytes == b'\x00' or raw_bytes == b'\x01'
#         # stream.debug_print(raw_bytes.hex())
#         return raw_bytes == b'\x01'  # return a boolean
#
#     def to_stream(self, stream):
#         if self is True:
#             stream.write_raw(b'\x01')
#         else:
#             stream.write_raw(b'\x00')


class ULittleEndianNumber(int, RWStreamable):
    length = 0  # must be defined by inheriting objects

    def __new__(cls, value):
        if value < 0:
            raise NegativeUnsignedError(f"{cls.__name__} cannot be negative")
        elif value >= 2 ** (8 * cls.length):
            raise TooBigError(f"{cls.__name__} cannot be greater than {2 ** (8 * cls.length) - 1}")
        else:
            return super().__new__(cls, value)

    @classmethod
    def from_stream(cls, stream):
        raw_bytes = stream.read_raw(cls.length)
        # stream.debug_print(raw_bytes.hex())
        return cls.from_bytes(raw_bytes, byteorder="little", signed=False)

    def to_stream(self, stream):
        raw_bytes = self.to_bytes(self.length, byteorder="little", signed=False)
        stream.write_raw(raw_bytes)


class UChar(ULittleEndianNumber):
    length = 1


class UShort(ULittleEndianNumber):
    length = 2


class UInt(ULittleEndianNumber):
    length = 4


class UFloat(float, RWStreamable):

    def __new__(cls, value):
        if value < 0:
            raise NegativeUnsignedError(f"{cls.__name__} cannot be negative")
        else:
            super().__new__(cls, value)

    @classmethod
    def from_stream(cls, stream):
        raw_bytes = stream.read_raw(4)
        # stream.debug_print(raw_bytes.hex())
        return cls(unpack('f', raw_bytes)[0])

    def to_stream(self, stream):
        raw_bytes = pack('f', self)
        stream.write_raw(raw_bytes)


class String(str, RWStreamable):

    @classmethod
    def from_stream(cls, stream, length=None):
        if length is None:
            raise ReadingError("length must be specified when reading String")
        raw_bytes = stream.read_raw(length)
        # stream.debug_print(raw_bytes.hex())
        return cls(object=raw_bytes, encoding='latin1')

    def to_stream(self, stream):
        raw_bytes = self.encode("latin1")
        stream.write_raw(raw_bytes)


# class Array(RWStreamable):
#     @classmethod
#     def from_stream(cls, stream, object_type=None, *, comment=None, in_line=False):
#         assert issubclass(object_type, RWStreamable)
#         size = stream.read(UShort)
#         if comment is not None:
#             stream.debug_comment(comment)
#         if in_line is True:
#             stream.debug_new_space()
#         else:
#             stream.debug_indent(+1)
#         rop = [stream.read(object_type) for _ in range(size)]
#         if in_line is True:
#             stream.debug_new_space()
#         else:
#             stream.debug_indent(-1)
#         return rop
