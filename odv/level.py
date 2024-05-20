import hashlib
import re

from PyQt6.QtWidgets import QMessageBox

from qt.common.simple_messagebox import QErrorBox
from settings import *
from config import CONFIG

from dvd import DvdParser
from dvm import DvmParser

from common import copy


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
        # self._scb = None
        self._dvm = None

    @property
    def dvd(self):
        if self._dvd is None:
            self._dvd = DvdParser(self.abs_name + ".dvd")
        return self._dvd

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
        assert self.is_original()
        source = self.abs_name
        destination = self.abs_name.replace(CONFIG.installation_path, CONFIG.backup_path)
        copy(f"{source}.dvd", f"{destination}.dvd")
        # copy(f"{source}.dvm", f"{destination}.dvm")
        # copy(f"{source}.scb", f"{destination}.scb")
        # copy(f"{source[:-8]}{os.sep}briefing{os.sep}b00bs{self.index:02}",
        #      f"{destination[:-8]}{os.sep}briefing{os.sep}b00bs{self.index:02}")

    def restore(self):
        assert CONFIG.backup_path in self.abs_name
        assert self.is_original()
        source = self.abs_name
        destination = self.abs_name.replace(CONFIG.backup_path, CONFIG.installation_path)
        copy(f"{source}.dvd", f"{destination}.dvd")
        # copy(f"{source}.dvm", f"{destination}.dvm")
        # scb and stf

    def insert_in_game(self):
        self.dvd.save_to_file(original_name(self.index, root=CONFIG.installation_path) + ".dvd")

        # self.dvm.save_to_file(os.path.join(CONFIG.installation_path, original_name(self.index)))


class OriginalLevel(Level):
    def __init__(self, index):
        assert 0 <= index <= 25
        super().__init__(original_name(index, root=CONFIG.backup_path), index)
