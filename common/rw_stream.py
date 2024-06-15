import io
import os

from abc import ABC, abstractmethod



class RStreamable(ABC):
    @classmethod
    @abstractmethod
    def from_stream(cls, stream):
        pass


class WStreamable(ABC):
    @abstractmethod
    def to_stream(self, stream):
        pass


class RWStreamable(RStreamable, WStreamable, ABC):
    pass


# INDENT_SIZE = 5


class ReadStream(object):

    # @staticmethod
    # def debug(func):
    #     def wrapper(self, *arg, **kwargs):
    #         if self.debug is True:
    #             func(self, *arg, **kwargs)
    #     return wrapper

    def __init__(self, data):
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

    def get_value(self):
        return self._input.getvalue()

    def read_raw(self, length=None):
        return self._input.read(length)

    def read(self, object_type, *arg, **kwarg):
        assert issubclass(object_type, RStreamable)
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


class WriteStream(object):
    def __init__(self):
        self._output = io.BytesIO()
        # self.debug = debug
        # if self.debug is True:
        #     self._debug_output = io.StringIO("")
        #     self._debug_indent = 0
        #     self._debug_line_is_empty = True

    def to_file(self, filename: str):
        fd = open(filename, "wb")
        fd.write(self._output.getvalue())
        fd.close()
        return

    def get_value(self):
        return self._output.getvalue()

    def write_raw(self, data: bytes):
        assert isinstance(data, bytes)
        self._output.write(data)

    def write(self, element):
        assert isinstance(element, WStreamable)
        element.to_stream(self)