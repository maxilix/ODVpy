import re

from PyQt6.QtWidgets import QMessageBox

from qt.common.simple_messagebox import QErrorBox
from settings import *
from config import CONFIG

from dvd import DvdParser
from dvm import DvmParser

from common import copy


def original_name(index):
    name = ""
    if index == 0:
        name += f"demo{os.sep}"
    name += f"data{os.sep}levels{os.sep}level_{index:02}"
    return name


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

    # def load(self):
    #     self.load_dvd()
    #     if self.dvd is not None:
    #         self.load_dvm()
    #
    # def load_dvm(self):
    #     try:
    #         self.dvm = DvmParser(self.name + ".dvm")
    #     except FileNotFoundError as e:
    #         if self.index != -1:
    #             if CONFIG.automatically_load_original_dvm is True:
    #                 self.load_original_dvm()
    #             else:
    #                 message_box = QMessageBox()
    #                 message_box.setIcon(QMessageBox.Icon.Question)
    #                 message_box.setText(f"{e}")
    #                 message_box.setInformativeText(f"Do you want to load the original level {self.index} dvm file instead?")
    #                 message_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    #                 message_box.setDefaultButton(QMessageBox.StandardButton.Ok)
    #                 response = message_box.exec()
    #                 if response == QMessageBox.StandardButton.Ok:
    #                     self.load_original_dvm()
    #                 else:
    #                     self.dvm = None
    #         else:
    #             QErrorBox(Exception("Unable to find correspondent map")).exec()
    #             self.dvm = None
    #
    # def load_original_dvm(self):
    #     filename = original_level_filename_we(self.index) + ".dvm"
    #     try:
    #         self.dvm = DvmParser(filename)
    #     except FileNotFoundError as e:
    #         self.dvm = None
    #         QErrorBox(e).exec()

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
                    self._dvm = DvmParser(os.path.join(CONFIG.backup_path, original_name(self.index) + ".dvm"))
                else:
                    raise e
        return self._dvm

    def is_original(self):
        hashes = ORIGINAL_LEVEL_HASH[self.index]
        if self.dvd.hash() == hashes[0]:
            return False
        if self.dvm.hash() == hashes[1]:
            return False
        # if self.scb.hash() == hashes[2]:
        #     return False
        # if self.stf.hash() == hashes[3]:
        #     return False
        return True

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
        # print(os.path.join(CONFIG.installation_path, original_name(self.index)))
        self.dvd.save_to_file(os.path.join(CONFIG.installation_path, original_name(self.index) + ".dvd"))

        # self.dvm.save_to_file(os.path.join(CONFIG.installation_path, original_name(self.index)))


class OriginalLevel(Level):
    def __init__(self, index):
        assert 0 <= index <= 25
        super().__init__(os.path.join(CONFIG.backup_path, original_name(index)), index)



