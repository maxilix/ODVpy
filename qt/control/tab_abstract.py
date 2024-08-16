from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import QScrollArea, QTabWidget, QMenu, QWidget, QVBoxLayout, QSizePolicy, \
    QStackedLayout

from odv.odv_object import OdvRoot
from qt.control._generic_tree import QGenericTree, QODVTreeItem
from qt.control.inspector_abstract import Inspector


class QTabControl(QScrollArea):
    def __init__(self, parent: QTabWidget):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self._scene_menu_priority = 2  # Nornal
        self._scene_menu_exclusive = False

    @property
    def scene(self):
        return self.parent().scene

    @property
    def level(self):
        return self.parent().level

    def scene_menu_priority(self):
        return self._scene_menu_priority + 0.5 * self.has_focus()

    def scene_menu_enabled(self):
        return self._scene_menu_priority > 0

    def _set_scene_menu_priority(self, priority: 0 | 1 | 2 | 3):
        assert priority in [0, 1, 2, 3]
        self._scene_menu_priority = priority

    def scene_menu_exclusive(self):
        return self._scene_menu_exclusive

    def _set_scene_menu_exclusive(self, value: bool):
        self._scene_menu_exclusive = value

    def exec_scene_menu(self):
        menu = QMenu()
        menu.setStyleSheet(":enabled {color: black} :disabled {color: gray}")

        priority_submenu = menu.addMenu("Priority")
        a_priority = [QAction("Disable"), QAction("Low"), QAction("Normal"), QAction("High")]
        for p, a in enumerate(a_priority):
            a.setCheckable(True)
            a.setChecked(self._scene_menu_priority == p)
            a.triggered.connect(lambda state, priority=p: self._set_scene_menu_priority(priority))
            priority_submenu.addAction(a)
        a_exclusive = QAction("Exclusive")
        a_exclusive.setCheckable(True)
        a_exclusive.setChecked(self._scene_menu_exclusive)
        a_exclusive.triggered.connect(self._set_scene_menu_exclusive)
        priority_submenu.addSeparator()
        priority_submenu.addAction(a_exclusive)

        menu.exec(QCursor.pos())

    def has_focus(self):
        return self.parent().indexOf(self) == self.parent().currentIndex()

    def take_focus(self):
        if not self.has_focus():
            self.parent().parent().setCurrentWidget(self)


class QTabControlGenericTree(QTabControl):
    inspector_types: dict

    def __init__(self, parent, odv_section_list):
        super().__init__(parent)
        if isinstance(odv_section_list, (list, tuple)):
            self.odv_section_list = list(odv_section_list)
        else:
            self.odv_section_list = [odv_section_list]
        self.tree_items = dict()
        self.inspectors = dict()

        def build_tree_structure(tree_parent_item, odv_root):
            if not isinstance(odv_root, OdvRoot):
                return
            for odv_object in odv_root:
                # q_odv_item = self.q_odv_item_types[-depth](self, self.scene, odv_item)
                self.tree_items[odv_object] = QODVTreeItem(self, odv_object)
                tree_parent_item.addChild(self.tree_items[odv_object])
                self.inspectors[odv_object] = self.inspector_types.get(type(odv_object), Inspector)(self, odv_object)
                self.inspector_stack_layout.addWidget(self.inspectors[odv_object])


                build_tree_structure(self.tree_items[odv_object], odv_object)

        content = QWidget()
        layout = QVBoxLayout(content)
        self.tree = QGenericTree()

        self.tree.itemSelectionChanged.connect(self.item_selection_changed)
        inspector_stack_widget = QWidget(self)
        inspector_stack_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.inspector_stack_layout = QStackedLayout(inspector_stack_widget)

        for odv_section in self.odv_section_list:
            self.tree_items[odv_section] = QODVTreeItem(self, odv_section)
            self.tree.addTopLevelItem(self.tree_items[odv_section])
            self.inspectors[odv_section] = self.inspector_types.get(type(odv_section), Inspector)(self, odv_section)
            self.inspector_stack_layout.addWidget(self.inspectors[odv_section])
            if isinstance(odv_section, OdvRoot):
                build_tree_structure(self.tree_items[odv_section], odv_section)

        assert len(self.tree_items) == len(self.inspectors)
        # add inspector stack widget
        layout.addWidget(inspector_stack_widget)

        # add tree widget if multiple section or any itérable section
        if len(self.odv_section_list) > 1 or any([isinstance(odv_section, OdvRoot) for odv_section in self.odv_section_list]):
            layout.addSpacing(50)
            layout.addWidget(self.tree)
        else:
            layout.addStretch()

        self.setWidget(content)
        self.tree.setCurrentItem(self.tree_items[self.odv_section_list[0]])

        # for odv_section in self.odv_section_list:
        #     self.tree_items[odv_section].setExpanded(True)
        self.tree.expandAll()

        for inspector in self.inspectors.values():
            inspector.update()



    def item_selection_changed(self):
        active_odv_object = self.tree.selectedItems()[0].odv_object
        self.inspector_stack_layout.setCurrentWidget(self.inspectors[active_odv_object])

    # def set_current_item(self, item=None):
    #     if isinstance(item, QODVItem):
    #         q_odv_item = item
    #     elif isinstance(item, QODVInspectorItem) or isinstance(item, QODVTreeItem):
    #         q_odv_item = item.odv_item
    #     else:
    #         raise ValueError("item must be QDVDObject, QDVDInspectorItem or QDVDTreeItem")
    #     self.tree.setCurrentItem(q_odv_item.q_tree_item)
    #
    # def is_current_item(self, item):
    #     if isinstance(item, QODVItem):
    #         q_odv_item = item
    #     elif isinstance(item, QODVInspectorItem) or isinstance(item, QODVTreeItem):
    #         q_odv_item = item.odv_item
    #     else:
    #         raise ValueError("item must be QDVDObject, QDVDInspectorItem or QDVDTreeItem")
    #     return q_odv_item == self.tree.selectedItems()[0].q_odv_item



