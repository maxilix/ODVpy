from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent, QCursor, QAction, QDropEvent
from PyQt6.QtWidgets import QTabWidget, QMenu, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTreeWidget, \
    QAbstractItemView, QSplitter, QLayout, QComboBox

from config import CONFIG

from qt._control.tab_bond import QBondTabControl
from qt._control.tab_buil import QBuilTabControl
from qt._control.tab_dvm import QMapTabControl
from qt._control.tab_jump import QJumpTabControl
from qt._control.tab_lift import QLiftTabControl
from qt._control.tab_mask import QMaskTabControl
from qt._control.tab_move import QMoveTabControl
from qt._control.tab_scb import QScbTabControl
from qt._control.tab_scrp import QScrpTabControl
from qt._control.tab_sght import QSghtTabControl


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


class QSectionControl(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        self.combo_box = QComboBox()
        self.combo_box.addItem("MISC - Miscellaneous")
        self.combo_box.addItem("BGND - Maps")
        self.combo_box.addItem("MOVE - Motions")
        self.combo_box.addItem("SGHT - Sights")
        self.combo_box.addItem("MASK - Masks")
        self.combo_box.addItem("WAYS - Ways")
        self.combo_box.addItem("ELEM - Elements")
        self.combo_box.addItem("FXBK - Sounds")
        self.combo_box.addItem("MSIC - Musics")
        self.combo_box.addItem("SND  - Sounds")
        self.combo_box.addItem("PAT  - Patches")
        self.combo_box.addItem("BOND - Bonds")
        self.combo_box.addItem("MAT  - Materials")
        self.combo_box.addItem("LIFT - Lifts")
        self.combo_box.addItem("AI   - Intelligences")
        self.combo_box.addItem("BUIL - Buildings")
        self.combo_box.addItem("SCRP - Scripts")
        self.combo_box.addItem("JUMP - Jumps")
        self.combo_box.addItem("CART - Mobiles")
        self.combo_box.addItem("DLGS - Dialogs")

        main_layout.addWidget(self.combo_box)



        self.setLayout(main_layout)


class QGenericTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.itemClicked.connect(self.item_clicked)
        self.itemDoubleClicked.connect(self.item_double_clicked)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.dragging_item = None

    # def update_height(self):
    #
    #     h = 18 * self.count() + 2
    #     self.setMinimumHeight(h)
    #     self.setMaximumHeight(h)

    # def count_visible_item(self):
    #     count = 0
    #     index = self.model().index(0, 0)
    #     while index.isValid():
    #         count += 1
    #         index = self.indexBelow(index)
    #     return count

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        self.dragging_item = item
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.dragging_item = None
        super().mouseReleaseEvent(event)

    @staticmethod
    def item_clicked(item, column):
        if column == 0:
            print("clicked")
            # item.clicked()

    @staticmethod
    def item_double_clicked(item, column):
        if column == 0:
            print("double clicked")

    # def contextMenuEvent(self, event: QContextMenuEvent):
    #     item = self.itemAt(event.pos())
    #     if item is not None:
    #         item.contextMenuEvent(event)

    def dropEvent(self, event: QDropEvent):
        # TODO implement move mechanic here
        super().dropEvent(event)
        # item_to_drop_in = self.itemAt(event.position().toPoint())
        # if self.dropIndicatorPosition() == QAbstractItemView.DropIndicatorPosition.OnItem:

    def startDrag(self, supportedActions):
        if self.dragging_item.draggable is True:
            super().startDrag(supportedActions)
            self.dragging_item = None


class QMainControl(QWidget):
    def __init__(self, parent, scene, level):
        super().__init__(parent)
        self.scene = scene
        self.level = level

        main_splitter = QSplitter(Qt.Orientation.Vertical)
        main_splitter.setChildrenCollapsible(False)
        # main_splitter.setStyleSheet("""
        #     QSplitter::handle {
        #         background-color: lightgray;}
        # """)

        top_splitter = QSplitter(Qt.Orientation.Horizontal)
        top_splitter.setChildrenCollapsible(False)

        self.section_zone = QSectionControl()
        self.section_zone.setMinimumWidth(400)
        # self.section_zone.setMaximumHeight(500)
        self.tree_zone = QGenericTree()
        self.tree_zone.setMinimumWidth(300)
        # self.tree_zone.setMaximumHeight(500)

        top_splitter.addWidget(self.section_zone)
        top_splitter.addWidget(self.tree_zone)


        self.object_zone = QLabel("object zone")
        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(self.object_zone)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(main_splitter)
        self.setLayout(main_layout)

    #     self.setTabPosition(QTabWidget.TabPosition.East)
    #     self.setMovable(True)
    #     self.setTabsClosable(True)
    #
    #     self.currentChanged.connect(self.current_changed)
    #     self.tabCloseRequested.connect(self.close_tab)
    #
    #     self.tab = dict()
    #     self.tab["DVM"] = QMapTabControl(self, level.dvm.level_map)
    #     self.tab["MISC"] = None
    #     self.tab["BGND"] = None
    #     self.tab["MOVE"] = QMoveTabControl(self, level.dvd.move)
    #     self.tab["SGHT"] = QSghtTabControl(self, level.dvd.sght)
    #     self.tab["MASK"] = QMaskTabControl(self, level.dvd.mask)
    #     self.tab["WAYS"] = None
    #     self.tab["ELEM"] = None
    #     self.tab["FXBK"] = None
    #     self.tab["MSIC"] = None
    #     self.tab["SND"] = None
    #     self.tab["PAT"] = None
    #     self.tab["BOND"] = QBondTabControl(self, level.dvd.bond)
    #     self.tab["MAT"] = None
    #     self.tab["LIFT"] = QLiftTabControl(self, level.dvd.lift)
    #     self.tab["AI"] = None
    #     self.tab["BUIL"] = QBuilTabControl(self, [level.dvd.buil.buildings, level.dvd.buil.special_doors])
    #     self.tab["SCRP"] = QScrpTabControl(self, level.dvd.scrp)
    #     self.tab["JUMP"] = QJumpTabControl(self, level.dvd.jump)
    #     self.tab["CART"] = None
    #     self.tab["DLGS"] = None
    #     self.tab["SCB"] = None # QScbTabControl(self, level.scb.classes)
    #
    #     initial_tabs = ["DVM"] + CONFIG.default_tabs
    #     for name in initial_tabs:
    #         self.add_tab(name)
    #
    #
    #
    #     # self.setCurrentWidget(self.bond_control)
    #
    #     # button = scene.addWidget(QPushButton("Button 1"))
    #     # button.setFlag(button.GraphicsItemFlag.ItemIgnoresTransformations)
    #     # button.setPos(20, 50)
    #     # button.setFlags(button.flags() | QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
    #
    #
    # def mousePressEvent(self, event: QMouseEvent):
    #     if event.button() == Qt.MouseButton.RightButton:
    #         tab_index = self.tabBar().tabAt(self.tabBar().mapFromParent(event.pos()))
    #         if tab_index == -1:
    #             menu = QMenu()
    #             add_submenu = menu.addMenu("Add tab")
    #             actions = []
    #             for k in self.tab:
    #                 if self.tab[k] is not None and k not in [self.tabText(i) for i in range(self.count())]:
    #                     actions.append(QAction(str(k)))
    #                     actions[-1].triggered.connect(lambda state, name=k: self.add_tab(name))
    #             add_submenu.addActions(actions)
    #             menu.exec(QCursor.pos())
    #         elif tab_index == self.tabBar().currentIndex():
    #             self.currentWidget().exec_tab_menu()
    #
    #
    #     super().mousePressEvent(event)
    #
    #
    # def current_changed(self, index):
    #     self.widget(index).update()
    #
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
    #
    #
    #
    #

