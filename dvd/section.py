from abc import ABC, abstractmethod

from common import *

# 20 dvd sections in order
section_list = ["MISC",
                "BGND",
                "MOVE",
                "SGHT",
                "MASK",
                "WAYS",
                "ELEM",
                "FXBK",
                "MSIC",
                "SND ",
                "PAT ",
                "BOND",
                "MAT ",
                "LIFT",
                "AI  ",
                "BUIL",
                "SCRP",
                "JUMP",
                "CART",
                "DLGS"]


class Section(RWStreamable):

    _name: str
    _version: int

    def __init__(self, name, data):
        self._name = name
        self._data = data
        self._loaded = False
        # log.info(f"Section {self.section} initialized.")

    @classmethod
    def from_stream(cls, stream):
        name = stream.read(String, 4)
        try:
            assert name == cls._name
        except AssertionError:
            raise ValueError(f"Name mismatch: {name} and {cls._name}")
        size = stream.read(UInt)
        version = stream.read(Version)
        try:
            assert version == cls._version
        except AssertionError:
            raise ValueError(f"{cls._name} version mismatch: {version} and {cls._version}")
        data = stream.read(Bytes, size - 4)  # minus version size
        return cls(name, data)

    def load(self):
        substream = ReadStream(self._data)
        self._load(substream)
        next_byte = substream.read(Bytes, 1)
        assert next_byte == b''
        self._loaded = True
        # log.info(f"Section {self.section} loaded")

    @abstractmethod
    def _load(self, substream: ReadStream) -> None:
        # must read (and create) self state from substream
        # can raise an error
        pass

    def to_stream(self, stream):
        if self._loaded:
            self.save()  # update self._data
        stream.write(String(self._name))
        stream.write(UInt(len(self._data) + 4))  # plus version size
        stream.write(Version(self._version))
        stream.write(Bytes(self._data))

    def save(self):
        substream = WriteStream()
        self._save(substream)
        new_data = substream.get_value()
        if new_data == b'':
            # assume _save() do nothing, self._data dont change
            pass
        else:
            self._data = new_data

    @abstractmethod
    def _save(self, substream: WriteStream) -> None:
        # must write self state in substream
        pass

    @property
    def loaded(self):
        return self._loaded
