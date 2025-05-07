# from PyQt6.QtGui import QAction, QCursor
# from PyQt6.QtWidgets import QScrollArea, QMenu, QWidget, QVBoxLayout, QSizePolicy, \
#     QStackedLayout
#
# from odv.odv_object import OdvObjectIterable
# from qt.control.generic_tree import QGenericTree, QODVTreeItem
# from qt.control.inspector_abstract import Inspector
#
#
# class QTabControl(QScrollArea):
#     def __init__(self, main_control):
#         super().__init__()
#         self.main_control = main_control
#         self.setWidgetResizable(True)
#         self._scene_menu_priority = 2  # Nornal
#         self._scene_menu_exclusive = False
#
#     @property
#     def scene(self):
#         return self.main_control.scene
#
#     @property
#     def level(self):
#         return self.main_control.level
#
#     def scene_menu_priority(self):
#         return self._scene_menu_priority + 0.5 * self.has_focus()
#
#     def scene_menu_enabled(self):
#         return self._scene_menu_priority > 0
#
#     def _set_scene_menu_priority(self, priority: 0 | 1 | 2 | 3):
#         assert priority in [0, 1, 2, 3]
#         self._scene_menu_priority = priority
#
#     def scene_menu_exclusive(self):
#         return self._scene_menu_exclusive
#
#     def _set_scene_menu_exclusive(self, value: bool):
#         self._scene_menu_exclusive = value
#
#     def exec_tab_menu(self):
#         menu = QMenu()
#         menu.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
#
#         priority_submenu = menu.addMenu("Priority")
#         a_priority = [QAction("Disable"), QAction("Low"), QAction("Normal"), QAction("High")]
#         for p, a in enumerate(a_priority):
#             a.setCheckable(True)
#             a.setChecked(self._scene_menu_priority == p)
#             a.triggered.connect(lambda state, priority=p: self._set_scene_menu_priority(priority))
#             priority_submenu.addAction(a)
#         a_exclusive = QAction("Exclusive")
#         a_exclusive.setCheckable(True)
#         a_exclusive.setChecked(self._scene_menu_exclusive)
#         a_exclusive.triggered.connect(self._set_scene_menu_exclusive)
#         priority_submenu.addSeparator()
#         priority_submenu.addAction(a_exclusive)
#
#         menu.exec(QCursor.pos())
#
#     def has_focus(self):
#         return self.main_control.indexOf(self) == self.main_control.currentIndex()
#
#     def take_focus(self):
#         if not self.has_focus():
#             self.main_control.setCurrentWidget(self)
#
#
# class QTabControlGenericTree(QTabControl):
#     inspector_types: dict
#
#     def __init__(self, parent, odv_root_list):
#         super().__init__(parent)
#         if isinstance(odv_root_list, (list, tuple)):
#             self.odv_section_list = list(odv_root_list)
#         else:
#             self.odv_section_list = [odv_root_list]
#         self.tree_items = dict()
#         self.inspectors = dict()
#
#     def load(self):
#         def build_tree_structure(tree_parent_item, odv_root):
#             if not isinstance(odv_root, OdvObjectIterable):
#                 return
#             for odv_object in odv_root:
#                 self.tree_items[odv_object] = QODVTreeItem(self, odv_object)
#                 tree_parent_item.addChild(self.tree_items[odv_object])
#                 self.inspectors[odv_object] = self.inspector_types.get(type(odv_object), Inspector)(self, odv_object)
#                 self.inspector_stack_layout.addWidget(self.inspectors[odv_object])
#
#                 build_tree_structure(self.tree_items[odv_object], odv_object)
#
#         content = QWidget()
#         layout = QVBoxLayout(content)
#         self.tree = QGenericTree()
#         self.tree.itemSelectionChanged.connect(self.item_selection_changed)
#         self.tree.setMinimumHeight(300)
#
#         self.inspector_stack_widget = QWidget(self)
#         self.inspector_stack_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
#         self.inspector_stack_layout = QStackedLayout(self.inspector_stack_widget)
#
#         for odv_section in self.odv_section_list:
#             self.tree_items[odv_section] = QODVTreeItem(self, odv_section)
#             self.tree.addTopLevelItem(self.tree_items[odv_section])
#             self.inspectors[odv_section] = self.inspector_types.get(type(odv_section), Inspector)(self, odv_section)
#             self.inspector_stack_layout.addWidget(self.inspectors[odv_section])
#             if isinstance(odv_section, OdvObjectIterable):
#                 build_tree_structure(self.tree_items[odv_section], odv_section)
#
#         assert len(self.tree_items) == len(self.inspectors)
#
#         # add inspector stack widget
#         layout.addWidget(self.inspector_stack_widget)
#
#         # add tree widget if multiple section or any itérable section
#         if len(self.odv_section_list) > 1 or any([isinstance(odv_section, OdvObjectIterable) for odv_section in self.odv_section_list]):
#             layout.addWidget(self.tree)
#         else:
#             layout.addStretch()
#
#         self.setWidget(content)
#
#         self.tree.setCurrentItem(self.tree_items[self.odv_section_list[0]])
#         self.tree.expandAll()
#
#         self.update()
#
#     def unload(self):
#         for inspector in self.inspectors.values():
#             for g in inspector.graphic_list:
#                 self.scene.removeItem(g)
#         self.inspector_stack_widget.deleteLater()
#         self.tree.deleteLater()
#         self.tree_items = dict()
#         self.inspectors = dict()
#
#
#     def update(self):
#         for inspector in self.inspectors.values():
#             inspector.update()
#
#     def item_selection_changed(self):
#         active_odv_object = self.tree.selectedItems()[0].odv_object
#         self.inspector_stack_layout.setCurrentWidget(self.inspectors[active_odv_object])
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel, QStackedLayout

from odv.data_section import Misc, Move
from odv.data_section.move import Layer, Sector, Obstacle
from odv.odv_object import OdvObjectIterable
from qt.control.generic_tree import QGenericTree, QGenericTreeItem
from qt.control.generic_inspector import Inspector


class QSectionControl(QWidget):
    item_types = dict()
    # d:dict
    # inspector_types:dict


    def __init__(self, control, section):
        super().__init__()
        self.control = control
        self.section = section
        self.d = dict()
        self.inspectors = dict()
        # self.inspectors = {Misc: Inspector(),
        #                    Move: Inspector(),
        #                    Layer: Inspector(),
        #                    Sector: Inspector(),
        #                    Obstacle: Inspector()}


        main_layout = QVBoxLayout(self)

        top_widget = QWidget()
        top_widget.setMinimumHeight(300)
        top_widget.setMaximumHeight(500)

        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)

        self.section_widget = QWidget()
        self.section_widget.setFixedWidth(300)
        section_layout = QVBoxLayout(self.section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)

        section_title = QLabel(self.section.fullname)
        font = section_title.font()
        font.setPointSize(22)
        section_title.setFont(font)
        # section_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        section_layout.addWidget(section_title)
        section_layout.addStretch()

        top_layout.addWidget(self.section_widget)

        self.tree = QGenericTree()
        self.tree.itemSelectionChanged.connect(self.item_selection_changed)
        self.tree.setMinimumWidth(200)
        # self.tree.resize(300,400)
        top_layout.addWidget(self.tree)

        main_layout.addWidget(top_widget)


        inspector_stack_widget = QWidget()
        self.inspector_stack_layout = QStackedLayout(inspector_stack_widget)
        self.inspector_wrong_selection_widget = QLabel("Wrong selection\nSelect one or more elements of the same type to inspect them")
        self.inspector_wrong_selection_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inspector_stack_layout.addWidget(self.inspector_wrong_selection_widget)
        # for inspector_widget in self.inspectors.values():
        #     self.inspector_stack_layout.addWidget(inspector_widget)

        main_layout.addWidget(inspector_stack_widget)


    def load(self):
        def recursive_load(odv_current_object, odv_parent_object=None):
            item_type = self.item_types.get(type(odv_current_object), QGenericTreeItem)

            new_tree_item = item_type(self, odv_current_object)
            if item_type not in self.inspectors:
                self.inspectors[item_type] = item_type.inspector_type()
                self.inspector_stack_layout.addWidget(self.inspectors[item_type])
            # new_tree_item.setText(0, odv_current_object.name)
            if odv_parent_object is None:
                self.tree.addTopLevelItem(new_tree_item)
            else:
                self.d[odv_parent_object].addChild(new_tree_item)
            self.d[odv_current_object] = new_tree_item
            new_tree_item.update()
            if isinstance(odv_current_object, OdvObjectIterable):
                for odv_child_object in odv_current_object:
                    recursive_load(odv_child_object, odv_current_object)

        recursive_load(self.section, None)
        self.d[self.section].setSelected(True)
        self.d[self.section].setExpanded(True)
        if not isinstance(self.section, OdvObjectIterable):
            self.tree.setEnabled(False)

    def item_selection_changed(self):
        selected = self.tree.selectedItems()
        if selected == [] or any([type(selected[0]) != type(e) for e in selected[1:]]):
            self.inspector_stack_layout.setCurrentWidget(self.inspector_wrong_selection_widget)
        else:
            inspector = self.inspectors[type(selected[0])]
            inspector.item_list = selected
            self.inspector_stack_layout.setCurrentWidget(inspector)

    @property
    def scene(self):
        return self.control.scene




