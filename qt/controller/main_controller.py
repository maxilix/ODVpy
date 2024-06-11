import sys

from PyQt6.QtCore import QPointF, QEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QLabel
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtGui import QPalette, QColor, QPixmap, QWheelEvent, QMouseEvent

from dvd import section_list
from .abstract_controller import Control
from .dvm import QControlDVM
from .motion import QControlMotion


class QControl(QTabWidget):
    def __init__(self, parent, scene, level):
        super().__init__(parent)
        # self.scene = scene
        # self.level = level

        self.setMinimumWidth(550)

        self.setTabPosition(QTabWidget.TabPosition.East)
        self.setMovable(False)

        # DVM
        self.control_dvm = QControlDVM(self, scene, level.dvm)
        self.addTab(self.control_dvm, "DVM")


        # ["MISC", "BGND", "MOVE", "SGHT", "MASK", "WAYS", "ELEM", "FXBK", "MSIC", "SND_", "PAT_", "BOND", "MAT_", "LIFT", "AI__", "BUIL", "SCRP", "JUMP", "CART", "DLGS"]:

        # Miscellaneous
        # self.addTab(QLabel(section_list[0]), section_list[0])

        # Background
        # self.addTab(QLabel(section_list[1]), section_list[1])

        # Motion
        self.control_motion = QControlMotion(self, scene, level.dvd.move)
        self.addTab(self.control_motion, section_list[2])

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

    def mousse_event(self, scene_position: QPointF, event: QEvent):
        self.control_motion.mousse_event(scene_position, event)


    def update(self):
        pass


