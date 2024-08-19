from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QTabWidget

from qt.control.tab_bond import QBondTabControl
from qt.control.tab_buil import QBuilTabControl
from qt.control.tab_dvm import QMapTabControl
from qt.control.tab_lift import QLiftTabControl
from qt.control.tab_move import QMoveTabControl
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

        self.setMinimumWidth(400)

        self.currentChanged.connect(self.current_changed)
        self.setTabPosition(QTabWidget.TabPosition.East)
        self.setMovable(False)

        # Map
        self.dvm_tab = QMapTabControl(self, level.dvm.level_map)
        self.addTab(self.dvm_tab, "DVM")

        # Miscellaneous

        # Background

        # Motion
        self.move_tab = QMoveTabControl(self, level.dvd.move)
        self.addTab(self.move_tab, "MOVE")

        # Sights

        # Masks

        # Ways

        # Elements

        # FX Bank

        # Music

        # Sounds

        # Patches

        # Bonds
        self.bond_tab = QBondTabControl(self, level.dvd.bond)
        self.addTab(self.bond_tab, "BOND")

        # Materials

        # Lifts
        self.lift_tab = QLiftTabControl(self, level.dvd.lift)
        self.addTab(self.lift_tab, "LIFT")

        # AI

        # Buildings
        self.buil_tab = QBuilTabControl(self, [level.dvd.buil.buildings, level.dvd.buil.special_doors])
        self.addTab(self.buil_tab, "BUIL")

        # Scripts

        # Jumps

        # Carts

        # Dialogues

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


    def current_changed(self, index):
        self.widget(index).update()


