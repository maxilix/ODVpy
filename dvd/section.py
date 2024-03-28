from abc import ABC, abstractmethod

from common import *

# 20 dvd sections in order
section_list = ["MISC", "BGND", "MOVE", "SGHT", "MASK", "WAYS", "ELEM", "FXBK", "MSIC", "SND_", "PAT_", "BOND", "MAT_",
                "LIFT", "AI__", "BUIL", "SCRP", "JUMP", "CART", "DLGS"]


class Section(ReadableFromStream):

    def __init__(self, data):
        self._data = data
        self._stream = None
        # log.info(f"Section {self.section} initialized.")

    @classmethod
    def from_stream(cls, stream):
        read_section = stream.read(String, 4)
        assert read_section == cls.section
        size = stream.read(UInt)
        data = stream.read(Bytes, size)
        return cls(data)

    @abstractmethod
    def _build(self):
        pass

    def build(self):
        self._stream = ByteStream(self._data)
        self._build()
        next_byte = self._stream.read(Bytes, 1)
        assert next_byte == b''
        # log.info(f"Section {self.section} builded.")

    @property
    def built(self):
        return self._stream is not None
