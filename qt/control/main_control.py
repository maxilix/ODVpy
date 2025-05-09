from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QCursor, QAction
from PyQt6.QtWidgets import QTabWidget, QMenu

from qt.control.tab_dvm import QDvmTab
from qt.control.tab_move import QMoveTab


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


class QControl(QTabWidget):

    sendStatus = pyqtSignal(str, int)

    def __init__(self, parent, scene, level):
        super().__init__(parent)
        self.scene = scene
        self.level = level
        self.setMinimumWidth(800)
        self.setTabPosition(QTabWidget.TabPosition.East)
        self.setMovable(True)
        self.setTabsClosable(False)

        self.currentChanged.connect(self.current_changed)
        # self.tabCloseRequested.connect(self.close_tab)

        self.tab = dict()
        self.tab["DVM"] = QDvmTab(self, level.dvm.level_map)
        # self.tab["MISC"] = None
        # self.tab["BGND"] = None
        self.tab["MOVE"] = QMoveTab(self, level.dvd.move)
        # self.tab["SGHT"] = QSghtTabControl(self, level.dvd.sght)
        # self.tab["MASK"] = QMaskTabControl(self, level.dvd.mask)
        # self.tab["WAYS"] = None
        # self.tab["ELEM"] = None
        # self.tab["FXBK"] = None
        # self.tab["MSIC"] = None
        # self.tab["SND"] = None
        # self.tab["PAT"] = None
        # self.tab["BOND"] = QBondTabControl(self, level.dvd.bond)
        # self.tab["MAT"] = None
        # self.tab["LIFT"] = QLiftTabControl(self, level.dvd.lift)
        # self.tab["AI"] = None
        # self.tab["BUIL"] = QBuilTabControl(self, [level.dvd.buil.buildings, level.dvd.buil.special_doors])
        # self.tab["SCRP"] = QScrpTabControl(self, level.dvd.scrp)
        # self.tab["JUMP"] = QJumpTabControl(self, level.dvd.jump)
        # self.tab["CART"] = None
        # self.tab["DLGS"] = None
        # self.tab["SCB"] = None # QScbTabControl(self, level.scb.classes)

        # initial_tabs = ["DVM"] + CONFIG.default_tabs
        # for name in initial_tabs:
        #     self.add_tab(name)
        for name in ["DVM", "MOVE"]:
            self.addTab(self.tab[name], name)

        # button = scene.addWidget(QPushButton("Button 1"))
        # button.setFlag(button.GraphicsItemFlag.ItemIgnoresTransformations)
        # button.setPos(20, 50)
        # button.setFlags(button.flags() | QGraphicsItem.GraphicsItemFlag.ItemIsMovable)


    def mousePressEvent(self, event: QMouseEvent):
        return
        if event.button() == Qt.MouseButton.RightButton:
            tab_index = self.tabBar().tabAt(self.tabBar().mapFromParent(event.pos()))
            if tab_index == -1:
                menu = QMenu()
                add_submenu = menu.addMenu("Add tab")
                actions = []
                for k in self.tab:
                    if self.tab[k] is not None and k not in [self.tabText(i) for i in range(self.count())]:
                        actions.append(QAction(str(k)))
                        actions[-1].triggered.connect(lambda state, name=k: self.add_tab(name))
                add_submenu.addActions(actions)
                menu.exec(QCursor.pos())
            elif tab_index == self.tabBar().currentIndex():
                self.currentWidget().exec_tab_menu()


        super().mousePressEvent(event)


    def current_changed(self, index):
        self.widget(index).update()

    # def close_tab(self, index):
    #     if self.tabText(index) == "DVM":
    #         print("DVM is not closable")
    #     else:
    #         self.widget(index).unload()
    #         self.removeTab(index)
    #
    # def add_tab(self, name):
    #     self.addTab(self.tab[name], name)
    #     self.tab[name].load()
    #     self.setCurrentWidget(self.tab[name])





