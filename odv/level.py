import hashlib
from pathlib import Path
from typing import List

from config import Config
from game_data import *
from odv.common import copy, InvalidHashError, ReadStream, WriteStream, Bytes, RWStreamable, original_filename, \
    guess_level_index
from .data_section import *
from .section import Section


class Dvd(RWStreamable):
    _sections: List[Section|None]

    def __init__(self):
        self._sections = [None]*NB_SECTION

    @classmethod
    def from_stream(cls, stream: ReadStream):
        rop = cls()
        rop._sections = [stream.read(section_types[i]) for i in range(NB_SECTION)]
        return rop

    def to_stream(self, stream: WriteStream):
        for i in range(NB_SECTION):
            stream.write(self._sections[i])

    def __iter__(self):
        return iter(self._sections)

    def __getitem__(self, index: int):
        return self._sections[index]

    def __len__(self) -> int:
        return len(self._sections)



class Scb(RWStreamable):
    _tail: Bytes|bytes

    def __init__(self):
        self._tail = b''

    @classmethod
    def from_stream(cls, stream: ReadStream):
        rop = cls()
        rop._tail = stream.read_raw()
        return rop

    def to_stream(self, stream: WriteStream):
        stream.write(Bytes(self._tail))




class Level(object):
    base_path: Path
    index: int
    data: Dvd
    script: Scb


    def __init__(self, filename: Path|str|None = None):
        if filename is None:
            self.base_path = Path()
            self.index = -1
            self.data = Dvd()
            self.script = Scb()
        else:
            self.base_path = Path(filename).with_suffix("")  # remove extension
            self.index = guess_level_index(self.base_path)
            if self.index == -1:
                print("[Level] Level index cannot be guessed.")

            dvd_stream = ReadStream.from_file(self.base_path.with_suffix(".dvd"))
            self.data = dvd_stream.read(Dvd)

            scb_stream = ReadStream.from_file(self.base_path.with_suffix(".scb"))
            self.script = scb_stream.read(Scb)

    @property
    def valid(self):
        return 0 <= self.index <= 25

    def file_hashes(self):
        hashes = []
        # dvd, dvm and scb files
        for ext in LEVEL_EXTENSIONS[:3]:
            with open(self.base_path.with_suffix(ext), "rb") as f:
                hashes.append(hashlib.file_digest(f, 'sha256').hexdigest().lower())
        # stf file
        with open(self.base_path.parent / "briefing" / f"d00bs{self.index:02}", "rb") as f:
            hashes.append(hashlib.file_digest(f, 'sha256').hexdigest().lower())
        # return tuple of 4 hashes
        return tuple(hashes)

    def is_original(self):
        return self.file_hashes() == ORIGINAL_LEVEL_HASH[self.index]

    def export(self, destination: Path|None = None):
        if destination is None:
            destination = Config.installation_path
        destination.parent.mkdir(parents=True, exist_ok=True)

        dvd_stream = WriteStream()
        dvd_stream.write(self.data)
        with open(destination.with_suffix(".dvd"), 'wb') as file:
            file.write(dvd_stream.get_value())
        print(f"[Level Export] Dvd file saved as {destination.stem}.dvd")

        scb_stream = WriteStream()
        scb_stream.write(self.script)
        with open(destination.with_suffix(".scb"), 'wb') as file:
            file.write(scb_stream.get_value())
        print(f"[Level Export] Scb file saved as {destination.stem}.scb")

    def copy(self, source:Path, destination:Path):
        """Copy the dvd, scb, dvm, and skip save (/briefing/d00bsXX) from source to destination."""
        assert source.with_suffix(".dvd").exists()
        assert source.with_suffix(".scb").exists()
        assert source.with_suffix(".dvm").exists()
        assert (source.parent / "briefing" / f"d00bs{self.index:02}").exists()
        copy(source.with_suffix(".dvd"), destination.with_suffix(".dvd"))
        copy(source.with_suffix(".scb"), destination.with_suffix(".scb"))
        copy(source.with_suffix(".dvm"), destination.with_suffix(".dvm"))
        copy(source.parent / "briefing" / f"d00bs{self.index:02}", destination.parent / "briefing" / f"d00bs{self.index:02}")
        print(f"[Level Copy] {source} --> {destination}")

    def _relocated(self, from_root: Path, to_root: Path) -> Path:
        """Return base_path rebased from from_root to to_root."""
        assert self.base_path.is_relative_to(from_root), (
            f"{self.base_path} is not relative to {from_root}"
        )
        return to_root / self.base_path.relative_to(from_root)

    def backup(self):
        if not self.is_original():
            raise InvalidHashError("Cannot backup a modified level — restore the original first.")
        self.copy(self.base_path, self._relocated(Config.installation_path, Config.backup_path))

    def restore(self):
        if not self.is_original():
            raise InvalidHashError("Cannot restore a modified level — backup the original first.")
        self.copy(self.base_path, self._relocated(Config.backup_path, Config.installation_path))

    def insert_in_game(self, as_index: int = -1):
        if as_index == -1:
            as_index = self.index
        destination = original_filename(as_index, root=Config.installation_path)
        self.export(destination)



class BackedUpLevel(Level):
    def __init__(self, index):
        super().__init__(original_filename(index, Config.backup_path))



class InstalledLevel(Level):
    def __init__(self, index):
        super().__init__(original_filename(index, Config.installation_path))
