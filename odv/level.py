import re

from PyQt6.QtWidgets import QMessageBox

from qt.common.simple_messagebox import QErrorBox
from settings import *
from config import CONFIG

from dvd import DvdParser
from dvm import DvmParser


class Level(object):
    def __init__(self, filename_we):
        self.filename_we = filename_we  # filename without extension
        try:
            m = re.findall(r"level_(\d\d)", self.filename_we)
            self.index = int(m[-1])
        except IndexError:
            self.index = -1

        self.dvd = None
        # self.scb = None
        self.dvm = None

        self.load_dvd()
        if self.dvd is not None:
            self.load_dvm()


    def load_dvm(self):
        try:
            self.dvm = DvmParser(self.filename_we + ".dvm")
        except FileNotFoundError as e:
            if self.index != -1:
                if CONFIG.automatically_load_original_dvm is True:
                    self.load_original_dvm()
                else:
                    message_box = QMessageBox()
                    message_box.setIcon(QMessageBox.Icon.Question)
                    message_box.setText(f"{e}")
                    message_box.setInformativeText(f"Do you want to load the original level {self.index} dvm file instead?")
                    message_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                    message_box.setDefaultButton(QMessageBox.StandardButton.Ok)
                    response = message_box.exec()
                    if response == QMessageBox.StandardButton.Ok:
                        self.load_original_dvm()
                    else:
                        self.dvm = None
            else:
                QErrorBox(Exception("Unable to find correspondent map")).exec()
                self.dvm = None

    def load_original_dvm(self):
        filename = original_level_filename_we(self.index) + ".dvm"
        try:
            self.dvm = DvmParser(filename)
        except FileNotFoundError as e:
            self.dvm = None
            QErrorBox(e).exec()

    def load_dvd(self):
        try:
            self.dvd = DvdParser(self.filename_we + ".dvd")
        except FileNotFoundError as e:
            self.dvd = None
            QErrorBox(e).exec()

    @property
    def loaded(self):
        return self.dvd is not None and self.dvm is not None  # and self.scb is not None
