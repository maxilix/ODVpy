from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QTabWidget

from qt.control.bond import QBondTabControl
from qt.control.map import QMapTabControl
from qt.control.move import QMoveTabControl
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
    def __init__(self, parent, scene, level):
        super().__init__(parent)
        self.scene = scene
        self.level = level

        self.setMinimumWidth(500)

        self.setTabPosition(QTabWidget.TabPosition.East)
        self.setMovable(False)

        # Map
        # self.map_control = QMapTabControl(self, level.dvm, level.dvd.bgnd)
        # self.addTab(self.map_control, "Map")

        # Miscellaneous
        # self.miscellaneous_control = QTabControl(self, scene)
        # self.addTab(self.miscellaneous_control, "MISC")

        # Motion
        self.motion_control = QMoveTabControl(self, level.dvd.move)
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
        self.bond_control = QBondTabControl(self, level.dvd.bond)
        self.addTab(self.bond_control, "BOND")

        # self.update()

        # self.setCurrentWidget(self.bond_control)

        # button = scene.addWidget(QPushButton("Button 1"))
        # button.setFlag(button.GraphicsItemFlag.ItemIgnoresTransformations)
        # button.setPos(20, 50)
        # button.setFlags(button.flags() | QGraphicsItem.GraphicsItemFlag.ItemIsMovable)


    def mousePressEvent(self, event: QMouseEvent):
        if (event.button() == Qt.MouseButton.RightButton and
                self.tabBar().tabAt(self.tabBar().mapFromParent(event.pos())) == self.tabBar().currentIndex()):
            self.currentWidget().exec_scene_menu()

        super().mousePressEvent(event)
