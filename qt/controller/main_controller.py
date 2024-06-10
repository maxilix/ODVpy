import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QLabel
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtGui import QPalette, QColor

from dvd import section_list
from .abstract_controller import Control
from .motion import QControlMotion


class QMainControl(Control, QTabWidget):
    def __init__(self, level):
        super().__init__()
        self.level = level

        self.setMinimumWidth(550)

        self.setTabPosition(QTabWidget.TabPosition.East)
        self.setMovable(False)

        # ["MISC", "BGND", "MOVE", "SGHT", "MASK", "WAYS", "ELEM", "FXBK", "MSIC", "SND_", "PAT_", "BOND", "MAT_", "LIFT", "AI__", "BUIL", "SCRP", "JUMP", "CART", "DLGS"]:

        # Miscellaneous
        # self.addTab(QLabel(section_list[0]), section_list[0])

        # Background
        # self.addTab(QLabel(section_list[1]), section_list[1])

        # Motion
        self.control_motion = QControlMotion(self, level.dvd.move)
        self.addTab(self.control_motion, section_list[2])
        self.sub_control.append(self.control_motion)

        # Sight
        # self.addTab(QLabel(section_list[3]), section_list[3])

        # Mask
        # self.addTab(QLabel(section_list[4]), section_list[4])

        # Ways
        # self.addTab(QLabel(section_list[5]), section_list[5])

        # Elements
        # self.addTab(QLabel(section_list[6]), section_list[6])

        # FXBK
        # self.addTab(QLabel(section_list[7]), section_list[7])

        # Music
        # self.addTab(QLabel(section_list[8]), section_list[8])

        # ...

    # def update(self):
    #     pass
    #
    # def add_view(self, view):
    #     self.control_motion.add_view(view.view_motion)

