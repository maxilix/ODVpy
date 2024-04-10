
import sys
import io

from . import ReadStream

# ─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼


class Indent(object):
    def __init__(self):
        self._value = 0

    def __iadd__(self, other):
        assert isinstance(other, int)
        assert other > 0
        self._value += other
        return self

    def __isub__(self, other):
        assert isinstance(other, int)
        assert other > 0
        assert self._value >= other
        self._value -= other
        return self

    def __str__(self):
        rop = " │  " * max((self._value - 1), 0)
        if self._value > 0:
            rop += " ├─ "
        return rop




class Printer(object):

    def __init__(self, data):
        self._stream = ReadStream(data)
        self._output_stream = io.StringIO()
        self._indent = 0

    def _write(self, raw_string):
        self._output_stream.write(raw_string)

    def _write_indent(self):
        self._write(" │  " * max((self._indent-1), 0))
        if self._indent > 0:
            self._write(" ├─ ")

    def write_line(self, line):
        self._write_indent()
        self._write(line)
        self._write("\n")

    def indent(self):
        self._indent += 1

    def unindent(self):
        assert self._indent > 0
        self._write(" │  " * max((self._indent-1), 0))
        if self._indent > 0:
            self._write(" ├─ ")

        self._indent -= 1

    # def new_group(self, object_to_read, description):
    #     self._write(group_name)



    def print_all(self):
        print(self._output_stream)
