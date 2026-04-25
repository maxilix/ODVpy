from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QSizePolicy, \
    QStackedLayout

from odv.odv_object import OdvObjectIterable
from qt.control.widget_generic_tree import QGenericTreeItem, QGenericTreeWidget



class QMainTab(QScrollArea):
    inspector_types: dict

    def __init__(self, control, data_section):
        super().__init__()

        self.control = control
        self.setWidgetResizable(True)
        self.data_section = data_section
        self.tree_items = dict()
        self.inspectors = dict()

        content = QWidget()
        layout = QVBoxLayout(content)

        self.tree = QGenericTreeWidget()
        self.tree.itemSelectionChanged.connect(self.item_selection_changed)
        self.tree.setMinimumHeight(300)

        self.inspector_stack_widget = QWidget(self)
        self.inspector_stack_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.inspector_stack_layout = QStackedLayout(self.inspector_stack_widget)


        def build_tree_structure(odv_current_object, odv_parent_object=None):
            self.add_odv_object(odv_current_object, odv_parent_object)
            if isinstance(odv_current_object, OdvObjectIterable):
                for odv_child_object in odv_current_object:
                    build_tree_structure(odv_child_object, odv_current_object)
        build_tree_structure(self.data_section)
        assert len(self.tree_items) == len(self.inspectors)

        # add inspector stack widget
        layout.addWidget(self.inspector_stack_widget)

        # add tree widget section is iterable
        if isinstance(self.data_section, OdvObjectIterable):
            layout.addWidget(self.tree)
        else:
            layout.addStretch()

        self.setWidget(content)

        self.tree.setCurrentItem(self.tree_items[self.data_section])
        self.tree.expandAll()

        self.update()


    def item_selection_changed(self):
        active_odv_object = self.tree.selectedItems()[0].odv_object
        self.inspector_stack_layout.setCurrentWidget(self.inspectors[active_odv_object])
        self.inspectors[active_odv_object].update()

    def has_focus(self):
        return self.control.indexOf(self) == self.control.currentIndex()

    def take_focus(self):
        if not self.has_focus():
            self.control.setCurrentWidget(self)

    @property
    def scene(self):
        return self.control.scene

    @property
    def level(self):
        return self.control.level


    def add_odv_object(self, new_odv_object, odv_parent=None):
        # create inspector widget
        inspector_type = self.inspector_types[type(new_odv_object)]
        self.inspectors[new_odv_object] = inspector_type(self, new_odv_object)
        # add widget to layout
        self.inspector_stack_layout.addWidget(self.inspectors[new_odv_object])

        # create tree item
        self.tree_items[new_odv_object] = QGenericTreeItem(self, new_odv_object)
        # search corresponding parent and add the new item
        if odv_parent is None:
            self.tree.addTopLevelItem(self.tree_items[new_odv_object])
        else:
            tree_parent_item = self.tree_items[odv_parent]
            tree_parent_item.addChild(self.tree_items[new_odv_object])

        # update all tree
        # self.tree.update()

        # select corresponding tree item
        # self.tree.setCurrentItem(self.tree_items[new_odv_object])

