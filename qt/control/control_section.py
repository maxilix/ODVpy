from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel, QStackedLayout, QSizePolicy

from odv.odv_object import OdvObjectIterable
from qt.control.generic_tree import QGenericTree, QGenericTreeItem


class QSectionControl(QWidget):
    item_types = dict()

    def __init__(self, control, section):
        super().__init__()
        self.control = control
        self.section = section
        self.tree_items = dict()
        self.inspectors = dict()

        main_layout = QVBoxLayout(self)

        top_widget = QWidget()
        top_widget.setFixedHeight(400)
        # top_widget.setMinimumHeight(300)
        # top_widget.setMaximumHeight(500)

        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)

        self.section_widget = QWidget()
        self.section_widget.setFixedWidth(250)
        section_layout = QVBoxLayout(self.section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)

        section_title = QLabel(self.section.fullname)
        font = section_title.font()
        font.setPointSize(22)
        section_title.setFont(font)
        # section_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        section_layout.addWidget(section_title)
        section_layout.addStretch()

        top_layout.addWidget(self.section_widget)

        self.tree = QGenericTree()
        self.tree.itemSelectionChanged.connect(self.item_selection_changed)
        self.tree.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Minimum)
        self.tree.setMinimumWidth(350)
        self.tree.setFixedHeight(400)
        # self.tree.setBaseSize(250, 400)
        # self.tree.resize(800,400)
        top_layout.addWidget(self.tree)

        main_layout.addWidget(top_widget)

        inspector_stack_widget = QWidget()
        self.inspector_stack_layout = QStackedLayout(inspector_stack_widget)
        self.inspector_wrong_selection_widget = QLabel("Wrong selection\nSelect one or more elements of the same type to inspect them")
        self.inspector_wrong_selection_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inspector_stack_layout.addWidget(self.inspector_wrong_selection_widget)

        main_layout.addWidget(inspector_stack_widget)

    def load(self):
        def recursive_load(odv_current_object, odv_parent_object=None):
            item_type = self.item_types.get(type(odv_current_object), QGenericTreeItem)

            new_tree_item = item_type(self, odv_current_object)
            if item_type not in self.inspectors:
                self.inspectors[item_type] = item_type.inspector_type()
                self.inspector_stack_layout.addWidget(self.inspectors[item_type])
            if odv_parent_object is None:
                self.tree.addTopLevelItem(new_tree_item)
            else:
                self.tree_items[odv_parent_object].addChild(new_tree_item)
            self.tree_items[odv_current_object] = new_tree_item
            new_tree_item.update()
            if isinstance(odv_current_object, OdvObjectIterable):
                for odv_child_object in odv_current_object:
                    recursive_load(odv_child_object, odv_current_object)

        recursive_load(self.section, None)
        self.tree_items[self.section].setSelected(True)
        self.tree_items[self.section].setExpanded(True)
        if not isinstance(self.section, OdvObjectIterable):
            self.tree.setEnabled(False)

    def item_selection_changed(self):
        selected = self.tree.selectedItems()
        if selected == [] or any([type(selected[0]) != type(e) for e in selected[1:]]):
            self.inspector_stack_layout.setCurrentWidget(self.inspector_wrong_selection_widget)
        else:
            inspector = self.inspectors[type(selected[0])]
            inspector.connect_to(selected)
            self.inspector_stack_layout.setCurrentWidget(inspector)

    def update_current_inspector(self):
        self.inspector_stack_layout.currentWidget().update()

    @property
    def scene(self):
        return self.control.scene
