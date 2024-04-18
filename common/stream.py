import io
import os

from abc import ABC, abstractmethod
from struct import pack, unpack

from .exception import PaddingError, ReadingTypeError




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
        # stream.debug_print(raw_bytes.hex())
        return raw_bytes


class Bool(RWStreamable):
    @classmethod
    def from_stream(cls, stream):
        raw_bytes = stream.read_raw(1)
        assert raw_bytes == b'\x00' or raw_bytes == b'\x01'
        # stream.debug_print(raw_bytes.hex())
        return raw_bytes == b'\x01'  # return a boolean


class ULittleEndianNumber(RWStreamable):
    length = None  # must be defined by inheriting objects

    @classmethod
    def from_stream(cls, stream):
        raw_bytes = stream.read_raw(cls.length)
        # stream.debug_print(raw_bytes.hex())
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
        # stream.debug_print(raw_bytes.hex())
        return unpack('f', raw_bytes)[0]


class Version(RWStreamable):
    @classmethod
    def from_stream(cls, stream):
        rop = stream.read(UInt)
        # stream.debug_comment("version")
        # stream.debug_new_line()
        return rop


class String(RWStreamable):
    @classmethod
    def from_stream(cls, stream, length=None):
        if length is None:
            raise ReadingTypeError("length must be specified when reading String")
        raw_bytes = stream.read_raw(length)
        while raw_bytes != b'' and raw_bytes[-1] == 0:
            raw_bytes = raw_bytes[:-1]
        # stream.debug_print(raw_bytes.hex())
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
        # stream.debug_comment(f"Padding {padding.hex()}")


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


# INDENT_SIZE = 5


class ReadStream(object):

    # @staticmethod
    # def debug(func):
    #     def wrapper(self, *arg, **kwargs):
    #         if self.debug is True:
    #             func(self, *arg, **kwargs)
    #     return wrapper

    def __init__(self, data, *, debug=True):
        self._input = io.BytesIO(data)
        # self.debug = debug
        # if self.debug is True:
        #     self._debug_output = io.StringIO("")
        #     self._debug_indent = 0
        #     self._debug_line_is_empty = True

    @classmethod
    def from_file(cls, filename):
        fd = open(filename, "rb")
        data = fd.read()
        fd.close()
        return cls(data)

    def read_raw(self, length=None):
        return self._input.read(length)

    def read(self, object_type, *arg, **kwarg):
        assert issubclass(object_type, RWStreamable)
        rop = object_type.from_stream(self, *arg, **kwarg)

        return rop

    # @debug
    # def debug_print(self, hex_string: str):
    #     if hex_string != "":
    #         int(hex_string, 16)  # assert hex_string is really hexadecimal
    #         self._debug_output.write(f"{hex_string.lower()} ")
    #         self._debug_line_is_empty = False
    #
    # @debug
    # def debug_comment(self, string: str):
    #     self._debug_output.write(f"[{string}] ")
    #     self._debug_line_is_empty = False
    #
    # @debug
    # def debug_indent(self, incr: int):
    #     assert incr > 0 or incr < 0 and self._debug_indent >= -incr
    #     self.debug_new_line()
    #     self._debug_indent += incr
    #     if incr > 0:
    #         self._debug_output.write(" " * INDENT_SIZE * incr)
    #     elif incr < 0 and self._debug_indent >= -incr:
    #         self._debug_output.seek(self._debug_output.tell() + INDENT_SIZE * incr)
    #
    # @debug
    # def debug_new_line(self):
    #     if self._debug_line_is_empty is False:
    #         self._debug_line_is_empty = True
    #         self._debug_output.write("\n")
    #         self._debug_output.write(" " * INDENT_SIZE * self._debug_indent)
    #
    # @debug
    # def debug_new_space(self):
    #     self._debug_output.write("  ")
    #
    # @debug
    # def debug_save(self, filename):
    #     os.makedirs(os.path.dirname(filename), exist_ok=True)
    #     with open(filename, "w") as file:
    #         file.write(self._debug_output.getvalue())
