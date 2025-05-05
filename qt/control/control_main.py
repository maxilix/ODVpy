from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QCursor, QAction, QDropEvent
from PyQt6.QtWidgets import QTabWidget, QMenu, QWidget, QSplitter, QVBoxLayout, QComboBox, QLabel, QTreeWidgetItem, \
    QHBoxLayout, QTreeWidget, QAbstractItemView, QPushButton, QStackedLayout

from config import CONFIG
from odv.data_section import Move, Misc, Bgnd
from odv.data_section.move import Layer, Sector, Obstacle
from odv.odv_object import OdvObjectIterable, OdvObject
from odv.section import odv_section_list, Section
from qt.control.inspector_abstract import Inspector
# from qt.control.generic_tree import QGenericTree

from qt.control.tab_bond import QBondTabControl
from qt.control.tab_buil import QBuilTabControl
from qt.control.tab_dvm import QMapTabControl
from qt.control.tab_jump import QJumpTabControl
from qt.control.tab_lift import QLiftTabControl
from qt.control.tab_mask import QMaskTabControl
from qt.control.tab_move import QMoveTabControl, MoveInspector, LayerInspector, SectorInspector, ObstacleInspector
from qt.control.tab_scb import QScbTabControl
from qt.control.tab_scrp import QScrpTabControl
from qt.control.tab_sght import QSghtTabControl


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
        # self.dragging_item = None

        # item1 = QTreeWidgetItem(self)
        # item1.setText(0, "object 1")
        # item11 = QTreeWidgetItem(item1)
        # item11.setText(0, "object 1.1")
        # item2 = QTreeWidgetItem(self)
        # item2.setText(0, "object 2")
        # self.setEnabled(False)

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
        # self.dragging_item = item
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

    def startDrag(self, supportedActions: Qt.DropAction):
        # if self.dragging_item.draggable is True:
        super().startDrag(supportedActions)
        # self.dragging_item = None



class QODVObject(object):
    def __init__(self, odv_object):
        assert isinstance(odv_object, OdvObject)
        self.odv_object = odv_object

    def load(self):
        pass





class QSection(object):


    def __init__(self, main_control, odv_section:Section):
        self.main_control = main_control
        self.section = odv_section
        self.tree = QGenericTree()
        self.inspectors = dict()
        self._d = dict()

        ### ICI

        self.inspectors = {Section: Inspector(self),
                       Move: Inspector(self),
                       Misc: Inspector(self),
                       Bgnd: Inspector(self),
                       Layer: Inspector(self),
                       Sector: Inspector(self),
                       Obstacle: Inspector(self)}

        def recursive_load(odv_current_object, odv_parent_object=None):
            new_tree_item = QTreeWidgetItem()
            new_tree_item.setText(0, odv_current_object.name)
            if odv_parent_object is None:
                pass
                self.tree.addTopLevelItem(new_tree_item)
            else:
                self._d[odv_parent_object][0].addChild(new_tree_item)
            self._d[odv_current_object] = (new_tree_item, self.inspectors[type(odv_current_object)])

            if isinstance(odv_current_object, OdvObjectIterable):
                for odv_child_object in odv_current_object:
                    recursive_load(odv_child_object, odv_current_object)

        recursive_load(self.section, None)

















class QControl(QWidget):

    sendStatus = pyqtSignal(str, int)

    def __init__(self, parent, scene, level):
        super().__init__(parent)
        self.scene = scene
        self.level = level
        # self.setMinimumWidth(800)


        self.q_section = dict()
        self.q_section["MISC"] = QSection(self, level.dvd.misc)
        self.q_section["BGND"] = QSection(self, level.dvd.bgnd)
        self.q_section["MOVE"] = QSection(self, level.dvd.move)

        main_layout = QVBoxLayout(self)
        # main_splitter.setChildrenCollapsible(False)
        # main_splitter.setStyleSheet("""
        #     QSplitter::handle {
        #         background-color: lightgray;}
        # """)

        top_widget = QWidget()
        top_widget.setMaximumHeight(400)

        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)

        section_widget = QWidget()
        section_widget.setMinimumWidth(250)
        sections_layout = QVBoxLayout(section_widget)
        sections_layout.setContentsMargins(0, 0, 0, 0)

        self.sections_combo_box = QComboBox()
        sections_layout.addWidget(self.sections_combo_box)
        line_layout = QHBoxLayout()
        self.section_full_name_label = QLabel()
        line_layout.addWidget(self.section_full_name_label)
        line_layout.addStretch()
        # self.load_unload_button = QPushButton()
        # self.load_unload_button.setText("Load")
        # self.load_unload_button.clicked.connect(self.load_unload_button_clicked)
        # line_layout.addWidget(self.load_unload_button)
        sections_layout.addLayout(line_layout)
        sections_layout.addStretch()

        top_layout.addWidget(section_widget)
        self.tree_stack_layout = QStackedLayout()
        # self.tree_stack.setMinimumWidth(250)
        # self.tree_stack.setMaximumWidth(400)
        # self.tree.setMaximumHeight(400)
        for q_section in self.q_section.values():
            self.tree_stack_layout.addWidget(q_section.tree)
        top_layout.addLayout(self.tree_stack_layout)
        self.tree_stack_layout.setCurrentWidget(self.q_section["MISC"].tree)

        main_layout.addWidget(top_widget)

        object_zone = QLabel("object zone")
        main_layout.addWidget(object_zone)

        self.sections_combo_box.currentIndexChanged.connect(self.current_section_changed)
        for section_name in self.q_section.keys():
            self.sections_combo_box.addItem(section_name)
        self.sections_combo_box.setCurrentIndex(0)

    def current_section_changed(self, section_index):
        section_name = odv_section_list[section_index]
        self.section_full_name_label.setText(section_name)
        self.tree_stack_layout.setCurrentWidget(self.q_section[section_name].tree)

        # if section_index == 2:
        #     build_tree_structure(self.tree, self.level.dvd.move.tree_structure)
        # self.tree.setEnabled(self.tree.topLevelItemCount() > 0)

    # def load_unload_button_clicked(self):
    #     qs = self.current_q_section
    #     if qs.loaded is True:
    #         self.load_unload_button.setText("Load")
    #         self.tree_stack.takeTopLevelItem(0)  # remove top level item without clear memory
    #         qs.unload()
    #     else:
    #         qs.load()
    #         self.load_unload_button.setText("Unload")
    #         self.tree_stack.takeTopLevelItem(0)  # remove top level item without clear memory
    #         self.tree_stack.addTopLevelItem(qs.section_tree_item())




        # section_name = odv_section_list[self.sections_combo_box.currentIndex()]
        # self.q_section[section_name].load()

    # def rebuild_tree_structure(self):
    #     def recursive_built(odv_current_object, parent_item=None):
    #         # self.add_odv_object(odv_current_object, odv_parent_object)
    #         new_item = QTreeWidgetItem()
    #         new_item.setText(0, odv_current_object.name)
    #         if parent_item is None:
    #             self.tree.addTopLevelItem(new_item)
    #             new_item.setSelected(True)  # todo
    #         else:
    #             parent_item.addChild(new_item)
    #         if isinstance(odv_current_object, OdvObjectIterable):
    #             for odv_child_object in odv_current_object:
    #                 recursive_built(odv_child_object, new_item)
    #
    #     self.tree.clear()
    #     recursive_built(self.active_section())
    #     self.tree.expandAll()

    @property
    def current_q_section(self):
        section_name = odv_section_list[self.sections_combo_box.currentIndex()]
        return self.q_section[section_name]

        # self.tab = dict()
        # self.tab["DVM"] = QMapTabControl(self, level.dvm.level_map)
        # self.tab["MISC"] = None
        # self.tab["BGND"] = None
        # self.tab["MOVE"] = QMoveTabControl(self, level.dvd.move)
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
        # self.tab["SCB"] = None QScbTabControl(self, level.scb.classes)
        #
        # initial_tabs = ["DVM"] + CONFIG.default_tabs
        # for name in initial_tabs:
        #     self.add_tab(name)



        # self.setCurrentWidget(self.bond_control)

        # button = scene.addWidget(QPushButton("Button 1"))
        # button.setFlag(button.GraphicsItemFlag.ItemIgnoresTransformations)
        # button.setPos(20, 50)
        # button.setFlags(button.flags() | QGraphicsItem.GraphicsItemFlag.ItemIsMovable)


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





