import hashlib
import os
import re

from scb.scb_parser import ScbParser
from settings import *
from config import CONFIG

from dvd import DvdParser
from dvm import DvmParser

from common import copy, InvalidHashError


def original_name(index, root=None):
    if root is None:
        name = []
    else:
        name = [root]
    if index == 0:
        name.append("demo")
    name.append("data")
    name.append("levels")
    name.append(f"level_{index:02}")
    return str(os.path.join(*name))


class Level(object):
    def __init__(self, abs_name, index=None):
        self.abs_name = abs_name  # absolute filename without extension
        if index is None:
            try:
                m = re.findall(r"level_(\d\d)", self.abs_name)
                self.index = int(m[-1])
            except IndexError:
                self.index = -1
        else:
            self.index = index

        self._dvd = None
        self._dvm = None
        self._scb = None
        # self._stf = None

    @property
    def dvd(self):
        if self._dvd is None:
            self._dvd = DvdParser(self.abs_name + ".dvd")
        return self._dvd

    @property
    def scb(self):
        if self._scb is None:
            self._scb = ScbParser(self.abs_name + ".scb")
        return self._scb

    @property
    def dvm(self):
        if self._dvm is None:
            try:
                self._dvm = DvmParser(self.abs_name + ".dvm")
            except FileNotFoundError as e:
                if 0 <= self.index <= 25 and CONFIG.automatically_load_original_dvm is True:
                    self._dvm = DvmParser(original_name(self.index, root=CONFIG.backup_path) + ".dvm")
                else:
                    raise e
        return self._dvm

    def file_hashes(self):
        hashes = []
        # dvd, dvm and scb files
        for ext in LEVEL_EXTENSIONS[:3]:
            with open(self.abs_name + "." + ext, "rb") as f:
                hashes.append(hashlib.file_digest(f, 'sha256').hexdigest().lower())
        # stf file
        temp = [self.abs_name[:-8], "briefing", f"d00bs{self.index:02}"]
        with open(os.path.join(*temp), "rb") as f:
            hashes.append(hashlib.file_digest(f, 'sha256').hexdigest().lower())
        # return tuple of 4 hashes
        return tuple(hashes)

    def is_original(self):
        return self.file_hashes() == ORIGINAL_LEVEL_HASH[self.index]
        # hashes = ORIGINAL_LEVEL_HASH[self.index]
        # if (h := self.dvd.hash()) != hashes[0]:
        #     print(f"dvd hash {h} should be {hashes[0]}")
        #     return False
        # if (h := self.dvm.hash()) != hashes[1]:
        #     print(f"dvm hash {h} should be {hashes[0]}")
        #     return False
        # # if self.scb.hash() == hashes[2]:
        # #     return False
        # # if self.stf.hash() == hashes[3]:
        # #     return False
        # return True

    def backup(self):
        assert CONFIG.installation_path in self.abs_name
        if self.is_original() is False:
            raise InvalidHashError()
        source = self.abs_name
        destination = self.abs_name.replace(CONFIG.installation_path, CONFIG.backup_path)
        copy(f"{source}.dvd", f"{destination}.dvd")
        copy(f"{source}.dvm", f"{destination}.dvm")
        copy(f"{source}.scb", f"{destination}.scb")
        copy(f"{source[:-9]}{os.sep}briefing{os.sep}d00bs{self.index:02}",
             f"{destination[:-9]}{os.sep}briefing{os.sep}d00bs{self.index:02}")

    def restore(self):
        assert CONFIG.backup_path in self.abs_name
        assert self.is_original()
        source = self.abs_name
        destination = self.abs_name.replace(CONFIG.backup_path, CONFIG.installation_path)
        copy(f"{source}.dvd", f"{destination}.dvd")
        copy(f"{source}.dvm", f"{destination}.dvm")
        copy(f"{source}.scb", f"{destination}.scb")
        copy(f"{source[:-9]}{os.sep}briefing{os.sep}d00bs{self.index:02}",
             f"{destination[:-9]}{os.sep}briefing{os.sep}d00bs{self.index:02}")

    def insert_in_game(self):
        source = self.abs_name
        destination = original_name(self.index, root=CONFIG.installation_path)

        if self._dvd is None:
            copy(f"{source}.dvd", f"{destination}.dvd")
            print("DVD: copy", end="")
        else:
            self.dvd.save_to_file(f"{destination}.dvd")
            print("DVD: save", end="")
        print(f"to {destination}.dvd")

        if self._dvm is None:
            # copy(f"{source}.dvm", f"{destination}.dvm")
            # print("DVM: copy", end="")
            pass
        else:
            self.dvm.save_to_file(f"{destination}.dvm")
            print("DVM: save", end="")
        print(f"to {destination}.dvm")

        if self._scb is None:
            copy(f"{source}.scb", f"{destination}.scb")
            print("SCB: copy", end="")
        else:
            self.scb.save_to_file(f"{destination}.scb")
            print("SCB: save", end="")
        print(f"to {destination}.scb")


class BackupedLevel(Level):
    def __init__(self, index):
        assert 0 <= index <= 25
        super().__init__(original_name(index, root=CONFIG.backup_path), index)


class InstalledLevel(Level):
    def __init__(self, index):
        assert 0 <= index <= 25
        super().__init__(original_name(index, root=CONFIG.installation_path), index)
