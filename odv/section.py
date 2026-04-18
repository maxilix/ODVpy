from abc import abstractmethod

from common import *
from game_data import *


class Section(RWStreamable):

    _section_name: str
    _section_version: int

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = data
        self._loaded = False
        # log.info(f"Section {self.section} initialized.")

    def __str__(self):
        return f"{self._section_name} Section"

    @property
    def version(self):
        return self._section_version

    @property
    def fullname(self):
        return SECTION_FULLNAME[self._section_name]

    @classmethod
    def from_stream(cls, stream):
        name = stream.read(String, 4)
        if name != cls._section_name:
            raise ValueError(f"Name mismatch: {name} and {cls._section_name}")
        size = stream.read(UInt)
        version = stream.read(Version)
        if version != cls._section_version:
            raise ValueError(f"{cls._section_name} version mismatch: {version} and {cls._section_version}")
        data = stream.read(Bytes, size - 4)  # minus version size
        return cls(data)

    def load(self, **kwargs):
        substream = ReadStream(self._data)
        self._load(substream, **kwargs)
        next_byte = substream.read(Bytes, 1)
        assert next_byte == b''
        self._loaded = True
        print(f"Section {self._section_name} loaded")

    @abstractmethod
    def _load(self, substream: ReadStream, **kwargs) -> None:
        # must read (and create) self state from substream
        # can raise an error
        pass

    def to_stream(self, stream):
        if self._loaded:
            self.save()  # update self._data
        stream.write(String(self._section_name))
        stream.write(UInt(len(self._data) + 4))  # plus version size
        stream.write(Version(self._section_version))
        stream.write(Bytes(self._data))

    def save(self):
        substream = WriteStream()
        self._save(substream)
        new_data = substream.get_value()
        if new_data == b'':
            # assume _save() do nothing, self._data don't change
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
