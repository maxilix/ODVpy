from abc import ABC, abstractmethod

from common import *

# 20 dvd sections in order
section_list = ["MISC", "BGND", "MOVE", "SGHT", "MASK", "WAYS", "ELEM", "FXBK", "MSIC", "SND ", "PAT ", "BOND", "MAT ",
                "LIFT", "AI  ", "BUIL", "SCRP", "JUMP", "CART", "DLGS"]


class Section(RWStreamable):

    section_index = None  # must be defined by inheriting objects

    def __init__(self, name, data):
        self._name = name
        self._data = data
        self._loaded = False
        # log.info(f"Section {self.section} initialized.")

    @classmethod
    def from_stream(cls, stream):
        name = stream.read(String, 4)
        assert name == section_list[cls.section_index]
        size = stream.read(UInt)
        data = stream.read(Bytes, size)
        return cls(name, data)

    def to_stream(self, stream):
        if self._loaded:
            self.save()  # update self._data
            stream.write(self._name)
            stream.write(UInt(len(self._data)))
            stream.write(self._data)

    def load(self, **kwargs):
        substream = ReadStream(self._data)
        self._load(substream, **kwargs)
        # next_byte = substream.read(Bytes, 1)
        # assert next_byte == b''
        self._loaded = True
        # log.info(f"Section {self.section} built")

    @abstractmethod
    def _load(self, substream, **kwargs):
        # must read (and create) self state from substream
        # must set self._loaded
        pass

    def save(self):
        substream = WriteStream()
        self._save(substream)
        new_data = substream.get_value()
        if new_data == b'':
            # assume _save() do nothing, self._data dont change
            pass
        else:
            self._data = Bytes(new_data)

    @abstractmethod
    def _save(self, substream):
        # must write self state in substream
        pass

    @property
    def loaded(self):
        return self._loaded
