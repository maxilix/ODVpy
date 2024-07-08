import sys

from PyQt6.QtCore import QPointF, QEvent, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QLabel, QMenu, QScrollArea, QGraphicsScene
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtGui import QPalette, QColor, QPixmap, QWheelEvent, QMouseEvent, QAction, QCursor

from qt.control.common import QControl
from qt.control.map import QMapControl
from qt.control.move import QMotionControl


# MISC - Miscellaneous
# BGND - Map
# MOVE - Motion
# SGHT - Sights
# MASK - Masks
# WAYS - Ways
# ELEM - Elements
# FXBK - Sounds
# MSIC - Sounds
# SND  - Sounds
# PAT  - Patches
# BOND - Motion
# MAT  -
# LIFT - Motion
# AI   -
# BUIL -
# SCRP -
# JUMP -
# CART - Elements
# DLGS -


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
        self.miscellaneous_control = QControl(self, scene)
        self.addTab(self.miscellaneous_control, "Miscellaneous")

        # Motion
        self.motion_control = QMotionControl(self, scene, level.dvd.move)
        self.addTab(self.motion_control, "Motion")

        # Sights
        self.sights_control = QControl(self, scene)
        self.addTab(self.sights_control, "Sights")

        # Masks
        self.masks_control = QControl(self, scene)
        self.addTab(self.masks_control, "Masks")

        # Ways
        self.ways_control = QControl(self, scene)
        self.addTab(self.ways_control, "Ways")

        # Elements
        self.elements_control = QControl(self, scene)
        self.addTab(self.elements_control, "Elements")

        # Sounds
        self.sounds_control = QControl(self, scene)
        self.addTab(self.sounds_control, "Sounds")

        # Music
        # self.addTab(QLabel(section_list[8]), section_list[8])

        # ...


    def mousePressEvent(self, event: QMouseEvent):
        if (event.button() == Qt.MouseButton.RightButton and
                self.tabBar().tabAt(self.tabBar().mapFromParent(event.pos())) == self.tabBar().currentIndex()):
            self.currentWidget().exec_context_menu()

        super().mousePressEvent(event)


