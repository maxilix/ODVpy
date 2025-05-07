import hashlib
import os
import re


from .data_section import *
from settings import *
from config import CONFIG



from common import copy, InvalidHashError, ReadStream


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

data_section_type = [Misc,
                     Bgnd,
                     Move,
                     Sght,
                     Mask,
                     Ways,
                     Elem,
                     Fxbk,
                     Msic,
                     Snd,
                     Pat,
                     Bond,
                     Mat,
                     Lift,
                     Ai,
                     Buil,
                     Scrp,
                     Jump,
                     Cart,
                     Dlgs]

class Level(object):
    def __init__(self, abs_filename, index=None):
        self.abs_filename = abs_filename  # absolute filename without extension
        if index is None:
            try:
                m = re.findall(r"level_(\d\d)", self.abs_filename)
                self.index = int(m[-1])
            except IndexError:
                self.index = -1
        else:
            self.index = index

        self._dvd_filename = self.abs_filename + ".dvd"
        stream = ReadStream.from_file(self._dvd_filename)
        # for i in range(20):

        self.data = dict()
        self.data["MISC"] = stream.read(Misc)
        self.data["MISC"].load()
        self.data["BGND"] = stream.read(Bgnd)
        self.data["BGND"].load(abs_filename=self.abs_filename)
        self.data["MOVE"] = stream.read(Move)
        self.data["MOVE"].load()
        self.data["SGHT"] = stream.read(Sght)
        self.data["SGHT"].load(move=self.data["MOVE"])



    # @property
    # def scb(self):
    #     if self._scb is None:
    #         self._scb = ScbParser(self.abs_name + ".scb")
    #     return self._scb

    # @property
    # def dvm(self):
    #     if self._dvm is None:
    #         try:
    #             self._dvm = DvmParser(self.abs_name + ".dvm")
    #         except FileNotFoundError as e:
    #             if 0 <= self.index <= 25 and CONFIG.automatically_load_original_dvm is True:
    #                 self._dvm = DvmParser(original_name(self.index, root=CONFIG.backup_path) + ".dvm")
    #             else:
    #                 raise e
    #     return self._dvm

    def file_hashes(self):
        hashes = []
        # dvd, dvm and scb files
        for ext in LEVEL_EXTENSIONS[:3]:
            with open(self.abs_filename + "." + ext, "rb") as f:
                hashes.append(hashlib.file_digest(f, 'sha256').hexdigest().lower())
        # stf file
        temp = [self.abs_filename[:-8], "briefing", f"d00bs{self.index:02}"]
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
        assert CONFIG.installation_path in self.abs_filename
        if self.is_original() is False:
            raise InvalidHashError()
        source = self.abs_filename
        destination = self.abs_filename.replace(CONFIG.installation_path, CONFIG.backup_path)
        copy(f"{source}.dvd", f"{destination}.dvd")
        copy(f"{source}.dvm", f"{destination}.dvm")
        copy(f"{source}.scb", f"{destination}.scb")
        copy(f"{source[:-9]}{os.sep}briefing{os.sep}d00bs{self.index:02}",
             f"{destination[:-9]}{os.sep}briefing{os.sep}d00bs{self.index:02}")

    def restore(self):
        assert CONFIG.backup_path in self.abs_filename
        assert self.is_original()
        source = self.abs_filename
        destination = self.abs_filename.replace(CONFIG.backup_path, CONFIG.installation_path)
        copy(f"{source}.dvd", f"{destination}.dvd")
        copy(f"{source}.dvm", f"{destination}.dvm")
        copy(f"{source}.scb", f"{destination}.scb")
        copy(f"{source[:-9]}{os.sep}briefing{os.sep}d00bs{self.index:02}",
             f"{destination[:-9]}{os.sep}briefing{os.sep}d00bs{self.index:02}")

    def insert_in_game(self):
        source = self.abs_filename
        destination = original_name(self.index, root=CONFIG.installation_path)

        if self._dvd is None:
            copy(f"{source}.dvd", f"{destination}.dvd")
            print(f"DVD: copy to {destination}.dvd")
        else:
            self.dvd.save_to_file(f"{destination}.dvd")
            print(f"DVD: save to {destination}.dvd")

        if self._dvm is None:
            try:
                copy(f"{source}.dvm", f"{destination}.dvm")
                print(f"DVM: copy to {destination}.dvm")
            except FileNotFoundError as e:
                pass
        else:
            self.dvm.save_to_file(f"{destination}.dvm")
            print(f"DVM: save to {destination}.dvm")

        if self._scb is None:
            copy(f"{source}.scb", f"{destination}.scb")
            print(f"SCB: copy to {destination}.scb")
        else:
            self.scb.save_to_file(f"{destination}.scb")
            print(f"SCB: save to {destination}.scb")


class BackupedLevel(Level):
    def __init__(self, index):
        assert 0 <= index <= 25
        super().__init__(original_name(index, root=CONFIG.backup_path), index)


class InstalledLevel(Level):
    def __init__(self, index):
        assert 0 <= index <= 25
        super().__init__(original_name(index, root=CONFIG.installation_path), index)
