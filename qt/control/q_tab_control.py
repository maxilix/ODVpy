from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import QScrollArea, QTabWidget, QMenu, QWidget, QVBoxLayout, QSizePolicy, \
    QStackedLayout

from qt.control.q_odv_item import QODVItem
from qt.control.q_generic_tree import QGenericTree, QODVTreeItem
from qt.control.q_inspector import QDVDInspectorItem


class QTabControl(QScrollArea):
    def __init__(self, parent: QTabWidget, scene):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self._scene_menu_priority = 2  # Nornal
        self._scene_menu_exclusive = False
        self.scene = scene

    def scene_menu_priority(self):
        return self._scene_menu_priority

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
    q_odv_item_types = [QODVItem]

    def __init__(self, parent, scene, dvd_section):
        super().__init__(parent, scene)
        self.dvd_section = dvd_section
        self.q_odv_items = []

        def build_tree_structure(q_tree_parent_item, dvd_root, depth):
            if depth == 0:
                return
            for odv_item in dvd_root:
                q_odv_item = self.q_odv_item_types[-depth](self, self.scene, odv_item)
                q_tree_parent_item.addChild(q_odv_item.q_tree_item)
                self.inspector_stack_layout.addWidget(q_odv_item.q_inspector_item)

                self.q_odv_items.append(q_odv_item)
                build_tree_structure(q_odv_item.q_tree_item, odv_item, depth - 1)

        content = QWidget()
        layout = QVBoxLayout(content)
        self.tree = QGenericTree(self)
        self.tree.itemSelectionChanged.connect(self.item_selection_changed)
        inspector_stack_widget = QWidget(self)
        inspector_stack_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.inspector_stack_layout = QStackedLayout(inspector_stack_widget)

        build_tree_structure(self.tree, self.dvd_section, len(self.q_odv_item_types))
        layout.addWidget(inspector_stack_widget)
        layout.addSpacing(50)
        layout.addWidget(self.tree)

        self.setWidget(content)

        self.tree.topLevelItem(0).setSelected(True)

    def item_selection_changed(self):
        q_odv_item = self.tree.selectedItems()[0].q_odv_item
        self.inspector_stack_layout.setCurrentWidget(q_odv_item.q_inspector_item)

    def set_current_item(self, item=None):
        if isinstance(item, QODVItem):
            q_odv_item = item
        elif isinstance(item, QDVDInspectorItem) or isinstance(item, QODVTreeItem):
            q_odv_item = item.q_odv_item
        else:
            raise ValueError("item must be QDVDObject, QDVDInspectorItem or QDVDTreeItem")
        self.tree.setCurrentItem(q_odv_item.q_tree_item)

    def is_current_item(self, item):
        if isinstance(item, QODVItem):
            q_odv_item = item
        elif isinstance(item, QDVDInspectorItem) or isinstance(item, QODVTreeItem):
            q_odv_item = item.q_odv_item
        else:
            raise ValueError("item must be QDVDObject, QDVDInspectorItem or QDVDTreeItem")
        return q_odv_item == self.tree.selectedItems()[0].q_odv_item
