from typing import List

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel, QStackedLayout, QSizePolicy, QPushButton, \
    QWidgetAction, QCheckBox, QMenu, QToolButton

from odv.odv_object import OdvObjectIterable, OdvObject
from qt.common.separator_line import QHLine
from qt.control.generic_inspector import Inspector
from qt.control.generic_tree import QGenericTree, QGenericTreeItem



class QHoverDetectionCheckboxesWidget(QWidget):
    def __init__(self, odv_types):
        super().__init__()
        self.odv_types = odv_types

        layout = QHBoxLayout(self)

        self.button = QToolButton()
        self.button.setFixedHeight(20)
        self.button.setFixedWidth(20)
        self.button.setArrowType(Qt.ArrowType.DownArrow)
        self.button.setEnabled(True)  # ------------------- #
        self.button.clicked.connect(self.show_menu)         #
        if len(odv_types) > 1:                              #
            layout.addWidget(self.button)                   #
        else:                                               #
            layout.addSpacing(26)                           #
                                                            #
        self.checkboxes = [QCheckBox()]                     #
                                                            #
        self.checkboxes[0].setChecked(True)  # ------------ #
        self.checkboxes[0].stateChanged.connect(lambda: self.button.setEnabled(self.checkboxes[0].isChecked()))
        layout.addWidget(self.checkboxes[0])

        layout.addWidget(QLabel(odv_types[0].__name__))

        if len(odv_types) > 1:
            self.menu = QMenu()

            # for label, state in zip(labels[1:], init_states[1:]):
            for item_type in odv_types[1:]:
                cb = QCheckBox(item_type.__name__)
                cb.setChecked(True)
                cb.setStyleSheet("""
                    QCheckBox {
                        padding: 6px 8px 6px 8px;  /* réduit vertical, garde espace gauche */
                        margin: 0px;
                    }
                """)
                action = QWidgetAction(self.menu)
                action.setDefaultWidget(cb)
                self.menu.addAction(action)
                self.checkboxes.append(cb)

    def show_menu(self):
        self.menu.exec(self.button.mapToGlobal(self.checkboxes[0].rect().bottomLeft() + QPoint(18,12)))

    def isChecked(self, t):
        i = self.odv_types.index(t)
        return self.checkboxes[0].isChecked() and self.checkboxes[i].isChecked()



class QSectionControl(QWidget):
    item_types = dict()
    type_match = list()
    odv_types: List[OdvObject]
    tree_item_types: List[QGenericTreeItem]
    inspector_types: List[Inspector]

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
        self.section_widget.setFixedWidth(300)
        section_layout = QVBoxLayout(self.section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)

        name_label = QLabel(self.section.name)
        font = name_label.font()
        font.setPointSize(22)
        name_label.setFont(font)
        section_layout.addWidget(name_label)

        fullname_label = QLabel(f"{self.section.fullname}")
        font = fullname_label.font()
        font.setPointSize(14)
        fullname_label.setFont(font)
        section_layout.addWidget(fullname_label)

        section_layout.addWidget(QHLine())


        hover_detection_layout = QHBoxLayout()
        hover_detection_layout.addWidget(QLabel("Hover detection"))
        self.hover_detection = QHoverDetectionCheckboxesWidget(self.odv_types)
        hover_detection_layout.addWidget(self.hover_detection)
        hover_detection_layout.addStretch()

        section_layout.addLayout(hover_detection_layout)


        section_layout.addStretch()

        import_export_layout = QHBoxLayout()
        import_export_layout.addSpacing(120)
        import_button = QPushButton("Import")
        import_button.setStatusTip(f"Import the {self.section.name} form data or other DVD file.")
        import_export_layout.addWidget(import_button)
        import_export_layout.addSpacing(10)
        export_button = QPushButton("Export")
        export_button.setStatusTip(f"Save the current {self.section.name} into a data file.")
        import_export_layout.addWidget(export_button)
        # import_export_layout.addSpacing(20)
        section_layout.addLayout(import_export_layout)

        section_layout.addWidget(QHLine())




        # section_layout.addStretch()

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
            type_index = self.odv_types.index(type(odv_current_object))
            # item_type = self.item_types.get(type(odv_current_object), QGenericTreeItem)
            odv_type = self.odv_types[type_index]
            tree_item_type = self.tree_item_types[type_index]
            inspector_type = self.inspector_types[type_index]


            new_tree_item = tree_item_type(self, odv_current_object)
            if tree_item_type not in self.inspectors:
                self.inspectors[tree_item_type] = inspector_type()
                self.inspector_stack_layout.addWidget(self.inspectors[tree_item_type])
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

    # def hover_detection(self, tree_item):
    #     assert self is tree_item.section_control
    #     return self.hover_detection_widget.isChecked()[list(self.item_types.keys()).index(type(tree_item._odv_object))]

    @property
    def scene(self):
        return self.control.scene
