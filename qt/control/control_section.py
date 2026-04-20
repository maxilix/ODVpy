from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel, QStackedLayout, QSizePolicy, QPushButton, \
    QWidgetAction, QCheckBox, QMenu, QToolButton

from config import Config
from game_data import SECTION_FLAG, SECTION_FULLNAME
from odv.data_section import Misc, Bgnd
from odv.data_section.move import Sector, Obstacle, Move, Layer
from odv.odv_object import OdvObjectIterable
from qt.common.separator_line import QHLine
from qt.control.generic_tree import QGenericTree
from qt.control.tab_bgnd import BgndItem, BgndInspector
from qt.control.tab_misc import MiscItem, MiscInspector
from qt.control.tab_move import MoveItem, MoveInspector, LayerItem, LayerInspector, SectorItem, SectorInspector, \
    ObstacleItem, ObstacleInspector

from app_context import AppContext as AC

type_match = []
type_match.append([(Misc, MiscItem, MiscInspector)])
type_match.append([(Bgnd, BgndItem, BgndInspector)])
type_match.append([(Move, MoveItem,MoveInspector), (Layer, LayerItem, LayerInspector), (Sector, SectorItem, SectorInspector), (Obstacle, ObstacleItem, ObstacleInspector)])

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
    section_id: int

    def __init__(self, section_id):

        super().__init__()
        self.section_id = section_id
        self.tree_items = dict()
        self.inspectors = dict()

        main_layout = QVBoxLayout(self)

        top_widget = QWidget()
        top_widget.setFixedHeight(400)

        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)

        self.section_widget = QWidget()
        self.section_widget.setFixedWidth(250)
        section_layout = QVBoxLayout(self.section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)

        name_label = QLabel(f"{SECTION_FLAG[self.section_id]} Section")
        font = name_label.font()
        font.setPointSize(22)
        name_label.setFont(font)
        section_layout.addWidget(name_label)

        fullname_label = QLabel(SECTION_FULLNAME[self.section_id])
        font = fullname_label.font()
        font.setPointSize(14)
        fullname_label.setFont(font)
        section_layout.addWidget(fullname_label)

        section_layout.addWidget(QHLine())

        self.load_button = QPushButton()
        self.load_button.clicked.connect(self.load_button_clicked)
        section_layout.addWidget(self.load_button)

        hover_detection_layout = QHBoxLayout()
        hover_detection_layout.addWidget(QLabel("Hover detection"))
        self.hover_detection = QHoverDetectionCheckboxesWidget([t[0] for t in type_match[self.section_id]])
        hover_detection_layout.addWidget(self.hover_detection)
        hover_detection_layout.addStretch()
        section_layout.addLayout(hover_detection_layout)

        section_layout.addStretch()

        import_export_layout = QHBoxLayout()
        import_export_layout.addSpacing(120)
        import_button = QPushButton("Import")
        import_button.setStatusTip(f"Import the {SECTION_FLAG[self.section_id]} section form data or other DVD file.")
        import_export_layout.addWidget(import_button)
        import_export_layout.addSpacing(10)
        export_button = QPushButton("Export")
        export_button.setStatusTip(f"Save the current {SECTION_FLAG[self.section_id]} section into a data file.")
        import_export_layout.addWidget(export_button)
        # import_export_layout.addSpacing(20)
        section_layout.addLayout(import_export_layout)

        section_layout.addWidget(QHLine())

        # section_layout.addStretch()

        top_layout.addWidget(self.section_widget)

        self.tree = QGenericTree()
        self.tree.itemSelectionChanged.connect(self.item_selection_changed)
        self.tree.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Minimum)
        self.tree.setFixedWidth(300)
        self.tree.setFixedHeight(400)
        top_layout.addWidget(self.tree)

        main_layout.addWidget(top_widget)

        inspector_stack_widget = QWidget()
        self.inspector_stack_layout = QStackedLayout(inspector_stack_widget)
        self.inspector_wrong_selection_widget = QLabel("Select one or more elements of the same type to inspect them")
        self.inspector_wrong_selection_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inspector_stack_layout.addWidget(self.inspector_wrong_selection_widget)
        self.inspector_unload_section_widget = QLabel(f"The {SECTION_FLAG[self.section_id]} section is currently unloaded")
        self.inspector_unload_section_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inspector_stack_layout.addWidget(self.inspector_unload_section_widget)

        main_layout.addWidget(inspector_stack_widget)


    @property
    def loaded(self):
        if self.tree_items == dict():
            assert self.inspectors == dict()
            return False
        else:
            assert self.tree_items != dict()
            return True

    def load_button_clicked(self):
        if self.loaded:
            self.unload()
        else:
            self.load()

    def load(self):
        def recursive_load(odv_current_object, odv_parent_object=None):
            types_tuple = [t for t in type_match[self.section_id] if type(odv_current_object) == t[0]][0]
            tree_item_type = types_tuple[1]
            inspector_type = types_tuple[2]

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

        section = AC.level.data[self.section_id]
        if section is not None:
            section.load(AC.level)
            recursive_load(section, None)
            self.tree_items[section].setSelected(True)
            self.tree_items[section].setExpanded(True)
            if not isinstance(section, OdvObjectIterable):
                self.tree.setEnabled(False)
            self.update()

    def unload(self):
        if self.loaded:
            for k in self.tree_items:
                self.tree_items[k].remove_graphic()
            self.tree.clear()
            self.tree_items.clear()
            for k in self.inspectors:
                self.inspector_stack_layout.removeWidget(self.inspectors[k])
            self.inspectors.clear()
            self.update()


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

    def update(self):
        super().update()
        section = AC.level.data[self.section_id]
        if section is None:
            self.load_button.setText("No data to load")
            self.load_button.setEnabled(False)
            self.inspector_stack_layout.setCurrentWidget(self.inspector_unload_section_widget)
        else:
            self.load_button.setEnabled(True)
            if self.loaded:
                self.load_button.setText("Unload data")
            else:
                self.load_button.setText("Load data")
                self.inspector_stack_layout.setCurrentWidget(self.inspector_unload_section_widget)



