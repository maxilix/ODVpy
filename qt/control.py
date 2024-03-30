import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QLabel
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtGui import QPalette, QColor

from dvd import section_list
from .sub_control import QMoveControl


class QControl(QTabWidget):
    def __init__(self, scene, level):
        super().__init__()
        self.setFixedWidth(500)
        #self.setMinimumSize(200,1000)

        self.setTabPosition(QTabWidget.TabPosition.East)
        self.setMovable(False)

        # ["MISC", "BGND", "MOVE", "SGHT", "MASK", "WAYS", "ELEM", "FXBK", "MSIC", "SND_", "PAT_", "BOND", "MAT_", "LIFT", "AI__", "BUIL", "SCRP", "JUMP", "CART", "DLGS"]:

        # Miscellaneous
        self.addTab(QLabel(section_list[0]), section_list[0])

        # Background
        self.addTab(QLabel(section_list[1]), section_list[1])

        # Motion
        self.addTab(QMoveControl(scene, level.dvd.move), section_list[2])

        # Sight
        self.addTab(QLabel(section_list[3]), section_list[3])

        # Mask
        self.addTab(QLabel(section_list[4]), section_list[4])

        # Ways
        self.addTab(QLabel(section_list[5]), section_list[5])

        # Elements
        self.addTab(QLabel(section_list[6]), section_list[6])

        # FXBK
        self.addTab(QLabel(section_list[7]), section_list[7])

        # Music
        self.addTab(QLabel(section_list[8]), section_list[8])

        # ...

