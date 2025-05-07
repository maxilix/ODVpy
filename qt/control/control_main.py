from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QCursor, QAction
from PyQt6.QtWidgets import QTabWidget, QMenu

from qt.control.control_section import QSectionControl
from qt.control.tab_misc import QMiscControl
from qt.control.tab_move import QMoveControl


class QControl(QTabWidget):

    sendStatus = pyqtSignal(str, int)


    def __init__(self, parent, scene, level):
        super().__init__(parent)
        self.scene = scene
        self.level = level
        # self.setMinimumWidth(500)

        # class QControlBar(QTabBar):
        #     def __init__(self, parent=None):
        #         super().__init__(parent)
        #         self.addTab("+")
        #         self.setStyleSheet("""
        #         QTabBar::tab {
        #             padding-top: 8px;
        #             padding-bottom: 8px;
        #             padding-left: 6px;
        #             padding-right: 6px;
        #         }
        #         """)
        #
        #     def mousePressEvent(self, event):
        #         if event.button() == Qt.MouseButton.LeftButton and self.tabAt(event.pos()) == (self.count() - 1):
        #             print("ADD")
        #         else:
        #             if event.button() == Qt.MouseButton.RightButton:
        #                 tab_index = self.tabAt(event.pos())
        #                 self.parent().tab_clicked(tab_index)
        #             super().mousePressEvent(event)
        # self.setTabBar(QControlBar(self))

        self.setTabPosition(QTabWidget.TabPosition.East)
        self.setMovable(True)

        # self.currentChanged.connect(self.current_changed)

        self.tab = dict()
        # self.tab["DVM"] = QMapTabControl(self, level.dvm.level_map)
        self.tab["MISC"] = QMiscControl(self, level.dvd.misc)
        # self.tab["BGND"] = QSectionControl(self, level.dvd.bgnd)
        self.tab["MOVE"] = QMoveControl(self, level.dvd.move)
        # self.tab["SGHT"] = QSectionControl(self, level.dvd.sght)
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
        initial_tabs = ["MISC", "MOVE"]
        for name in initial_tabs:
            self.add_tab(name)
        self.setCurrentWidget(self.tab["MISC"])

        # button = scene.addWidget(QPushButton("Button 1"))
        # button.setFlag(button.GraphicsItemFlag.ItemIgnoresTransformations)
        # button.setPos(20, 50)
        # button.setFlags(button.flags() | QGraphicsItem.GraphicsItemFlag.ItemIsMovable)


    def mousePressEvent(self, event: QMouseEvent):
        # TODO make the click detectable only on the TabBar rect
        if event.button() == Qt.MouseButton.RightButton:
            tab_index = self.tabBar().tabAt(self.tabBar().mapFromParent(event.pos()))
            menu = QMenu()
            if tab_index != -1:
                section_name = self.tabText(tab_index)
                close_action = QAction(f"Close {section_name}")
                close_action.triggered.connect(lambda state, name=section_name: self.close_tab(name))
                menu.addAction(close_action)
                menu.addSeparator()

            add_actions = []
            for section_name in self.tab:
                if self.tab[section_name] is not None and section_name not in [self.tabText(i) for i in range(self.count())]:
                    add_actions.append(QAction(f"Add {section_name}"))
                    add_actions[-1].triggered.connect(lambda state, name=section_name: self.add_tab(name))
            menu.addActions(add_actions)
            menu.exec(QCursor.pos())

        super().mousePressEvent(event)

    # def current_changed(self, index):
    #     self.widget(index).update()

    def close_tab(self, name):
        if name == "DVM":
            print("DVM is not closable")
        else:
            print(f"close {name}")

    def add_tab(self, name):
        self.addTab(self.tab[name], name)
        self.setCurrentWidget(self.tab[name])
