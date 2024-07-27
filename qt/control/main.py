import sys

from PyQt6.QtCore import QPointF, QEvent, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QLabel, QMenu, QScrollArea, QGraphicsScene, \
    QPushButton, QGraphicsItem
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtGui import QPalette, QColor, QPixmap, QWheelEvent, QMouseEvent, QAction, QCursor

from qt.control.bond import QBondControl
from qt.control.common import QTabControl
from qt.control.map import QMapControl
from qt.control.move import QMotionControl
from qt.scene import QScene


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
    def __init__(self, parent, scene: QScene, level):
        super().__init__(parent)
        # self.scene = scene
        # self.level = level

        self.setMinimumWidth(400)

        self.setTabPosition(QTabWidget.TabPosition.East)
        self.setMovable(False)

        # Map
        self.map_control = QMapControl(self, scene, level.dvm, level.dvd.bgnd)
        self.addTab(self.map_control, "DVM")

        # Miscellaneous
        # self.miscellaneous_control = QTabControl(self, scene)
        # self.addTab(self.miscellaneous_control, "MISC")

        # Motion
        self.motion_control = QMotionControl(self, scene, level.dvd.move)
        self.addTab(self.motion_control, "MOVE")

        # Sights
        # self.sights_control = QTabControl(self, scene)
        # self.addTab(self.sights_control, "Sights")

        # Masks
        # self.masks_control = QTabControl(self, scene)
        # self.addTab(self.masks_control, "Masks")

        # Ways
        # self.ways_control = QTabControl(self, scene)
        # self.addTab(self.ways_control, "Ways")

        # Elements
        # self.elements_control = QTabControl(self, scene)
        # self.addTab(self.elements_control, "Elements")

        # Sounds
        # self.sounds_control = QTabControl(self, scene)
        # self.addTab(self.sounds_control, "Sounds")

        # Music
        # self.addTab(QLabel(section_list[8]), section_list[8])

        # ...

        # Bonds
        self.bond_control = QBondControl(self, scene, level.dvd.bond)
        self.addTab(self.bond_control, "BOND")

        # self.update()

        # self.setCurrentWidget(self.motion_control)

        button = scene.addWidget(QPushButton("Button 1"))
        button.setFlag(button.GraphicsItemFlag.ItemIgnoresTransformations)
        button.setPos(20, 50)
        button.setFlags(button.flags() | QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

    # def update(self):
    #     super().update()
    #     self.motion_control.update()

    def mousePressEvent(self, event: QMouseEvent):
        if (event.button() == Qt.MouseButton.RightButton and
                self.tabBar().tabAt(self.tabBar().mapFromParent(event.pos())) == self.tabBar().currentIndex()):
            self.currentWidget().exec_context_menu()

        super().mousePressEvent(event)
