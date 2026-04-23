from abc import abstractmethod

from common import *
from game_data import *


class Section(RWStreamable):

    _section_id: int
    _section_version: int

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

    @classmethod
    def from_file(cls, filename):
        # TODO "with open(filename, 'wb') as file" and try
        # TODO implement and handle spécific error
        # TODO probably remove seek from ReadStream
        stream = ReadStream.from_file(filename)
        while True:
            flag = stream.read(String, 4)
            if flag == "":
                raise ValueError(f"Flag {SECTION_FLAG[cls._section_id]} unfound.")
            if flag == SECTION_FLAG[cls._section_id]:
                stream.seek(-4, os.SEEK_CUR)  # return at the flag position
                return cls.from_stream(stream)
            else:
                print(f"[Section {flag}] passed.")
                size = stream.read(UInt)
                stream.seek(size, os.SEEK_CUR)

    def load(self, level):
        if not self.loaded:
            [level.data[dependence].load(level) for dependence in SECTION_DEPENDENCIES[self._section_id]]
            substream = ReadStream(self._data)
            self._load(substream, level)
            next_byte = substream.read(Bytes, 1)
            assert next_byte == b''
            self._loaded = True
            print(f"[Section {SECTION_FLAG[self._section_id]}] loaded.")

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

    def to_file(self, filename):
        stream = WriteStream()
        self.to_stream(stream)
        with open(filename, 'wb') as file:
            file.write(stream.get_value())

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
