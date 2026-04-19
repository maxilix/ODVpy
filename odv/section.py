from abc import abstractmethod

from common import *
from game_data import *


class Section(RWStreamable):

    _section_id: int
    _section_version: int
    _section_dependencies = []

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = data
        self._loaded = False
        # log.info(f"Section {self.section} initialized.")

    def __str__(self):
        return f"{SECTION_FLAG[self._section_id]} Section"

    @property
    def version(self):
        return self._section_version

    @property
    def fullname(self):
        return SECTION_FULLNAME[self._section_id]

    @classmethod
    def from_stream(cls, stream):
        flag = stream.read(String, 4)
        if flag != SECTION_FLAG[cls._section_id]:
            raise ValueError(f"Flag mismatch: {flag} and {SECTION_FLAG[cls._section_id]}")
        size = stream.read(UInt)
        version = stream.read(Version)
        if version != cls._section_version:
            raise ValueError(f"{SECTION_FLAG[cls._section_id]} version mismatch: {version} and {cls._section_version}")
        data = stream.read(Bytes, size - 4)  # minus version size
        return cls(data)

    def load(self, level):
        substream = ReadStream(self._data)
        self._load(substream, level)
        next_byte = substream.read(Bytes, 1)
        assert next_byte == b''
        self._loaded = True
        print(f"Section {SECTION_FLAG[self._section_id]} loaded")

    @abstractmethod
    def _load(self, substream: ReadStream, level) -> None:
        # must read (and create) self state from substream
        # can raise an error
        pass

    def to_stream(self, stream):
        if self._loaded:
            self.save()  # update self._data
        stream.write(String(SECTION_FLAG[self._section_id]))
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
