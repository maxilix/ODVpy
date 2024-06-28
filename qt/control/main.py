import sys

from PyQt6.QtCore import QPointF, QEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QLabel
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtGui import QPalette, QColor, QPixmap, QWheelEvent, QMouseEvent

from .map import QMapControl
from .move import QMotionControl


class QMainControl(QTabWidget):
    def __init__(self, parent, scene, level):
        super().__init__(parent)
        # self.scene = scene
        # self.level = level

        self.setMinimumWidth(800)

        self.setTabPosition(QTabWidget.TabPosition.East)
        self.setMovable(False)

        # Map
        self.map_control = QMapControl(self, scene, level.dvm, level.dvd.bgnd)
        self.addTab(self.map_control, "Map")

        # Miscellaneous
        # self.addTab(QLabel(section_list[0]), section_list[0])

        # Motion
        self.control_motion = QMotionControl(self, scene, level.dvd.move)
        self.addTab(self.control_motion, "Motion")

        # Sight
        # self.addTab(QLabel(section_list[3]), section_list[3])

        # Masks
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


    def update(self):
        pass


