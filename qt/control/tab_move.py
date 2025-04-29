from PyQt6.QtGui import QColor, QPolygonF
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QStackedLayout

from dvd.move import Layer, MainArea, Obstacle, Move
from odv.odv_object import OdvRoot
from qt.control.generic_tree import QODVTreeItem, QGenericTree
from qt.control.inspector_graphic import GeometrySubInspector
from qt.control.inspector_abstract import Inspector
from qt.control.tab__abstract import QTabControlGenericTree, QTabControl


class ObstacleInspector(Inspector):
    deletable = True
    draggable = True
    child_name = ""  # cannot add child

    def init_sub_inspector(self):
        self.sub_inspector_group["Polygon"] = [
            GeometrySubInspector(self, "poly", color=QColor(255, 90, 40)),
        ]


class MainAreaInspector(Inspector):
    # path color QColor(180, 110, 30)
    deletable = True
    child_name = "Obstacle"

    def init_sub_inspector(self):
        self.sub_inspector_group["Polygon"] = [
            GeometrySubInspector(self, "poly", color=QColor(160, 200, 40)),
        ]

    def new_odv_child(self):
        new_obstacle = Obstacle(self.odv_object)
        new_obstacle.poly = self._tab_control.scene.new_centered_polygon(scale=0.25)
        return new_obstacle


class LayerInspector(Inspector):
    deletable = True
    child_name = "Main Area"

    def new_odv_child(self):
        new_main_area = MainArea(self.odv_object)
        new_main_area.poly = self._tab_control.scene.new_centered_polygon(scale=0.9)
        return new_main_area



class MoveInspector(Inspector):
    deletable = False
    child_name = "Layer"

    def new_odv_child(self):
        new_layer = Layer(self.odv_object)
        return new_layer





class QMoveTabControl(QTabControl):
    inspector_types = {Move: MoveInspector,
                       Layer: LayerInspector,
                       MainArea: MainAreaInspector,
                       Obstacle: ObstacleInspector}

    def __init__(self, parent, odv_root_list):
        super().__init__(parent)
        if isinstance(odv_root_list, (list, tuple)):
            self.odv_section_list = list(odv_root_list)
        else:
            self.odv_section_list = [odv_root_list]
        self.tree_items = dict()
        self.inspectors = dict()

        self.load()

    def load(self):
        def build_tree_structure(tree_parent_item, odv_root):
            if not isinstance(odv_root, OdvRoot):
                return
            for odv_object in odv_root:
                self.tree_items[odv_object] = QODVTreeItem(self, odv_object)
                tree_parent_item.addChild(self.tree_items[odv_object])
                self.inspectors[odv_object] = self.inspector_types.get(type(odv_object), Inspector)(self, odv_object)
                self.inspector_stack_layout.addWidget(self.inspectors[odv_object])

                build_tree_structure(self.tree_items[odv_object], odv_object)

        content = QWidget()
        layout = QVBoxLayout(content)
        self.tree = QGenericTree()
        self.tree.itemSelectionChanged.connect(self.item_selection_changed)
        self.tree.setMinimumHeight(300)

        self.inspector_stack_widget = QWidget(self)
        self.inspector_stack_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.inspector_stack_layout = QStackedLayout(self.inspector_stack_widget)

        for odv_section in self.odv_section_list:
            self.tree_items[odv_section] = QODVTreeItem(self, odv_section)
            self.tree.addTopLevelItem(self.tree_items[odv_section])
            self.inspectors[odv_section] = self.inspector_types.get(type(odv_section), Inspector)(self, odv_section)
            self.inspector_stack_layout.addWidget(self.inspectors[odv_section])
            if isinstance(odv_section, OdvRoot):
                build_tree_structure(self.tree_items[odv_section], odv_section)

        assert len(self.tree_items) == len(self.inspectors)

        # add inspector stack widget
        layout.addWidget(self.inspector_stack_widget)

        # add tree widget if multiple section or any itérable section
        if len(self.odv_section_list) > 1 or any([isinstance(odv_section, OdvRoot) for odv_section in self.odv_section_list]):
            layout.addWidget(self.tree)
        else:
            layout.addStretch()

        self.setWidget(content)

        self.tree.setCurrentItem(self.tree_items[self.odv_section_list[0]])
        self.tree.expandAll()

        self.update()

    def unload(self):
        for inspector in self.inspectors.values():
            for g in inspector.graphic_list:
                self.scene.removeItem(g)
        self.inspector_stack_widget.deleteLater()
        self.tree.deleteLater()
        self.tree_items = dict()
        self.inspectors = dict()


    def update(self):
        for inspector in self.inspectors.values():
            inspector.update()

    def item_selection_changed(self):
        active_odv_object = self.tree.selectedItems()[0].odv_object
        self.inspector_stack_layout.setCurrentWidget(self.inspectors[active_odv_object])
