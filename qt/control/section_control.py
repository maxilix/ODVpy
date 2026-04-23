import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel, QStackedLayout, QSizePolicy, QPushButton, \
    QFileDialog, QComboBox

from app_context import AppContext as AC
from game_data import SECTION_FLAG, SECTION_FULLNAME, SECTION_DEPENDENCIES, NB_SECTION
from odv.data_section import Misc, Bgnd, Sght, section_types
from odv.data_section.move import Sector, Obstacle, Move, Layer
from odv.data_section.sght import SightObstacle
from odv.odv_object import OdvObjectIterable
from qt.common.separator_line import QHLine
from qt.control.generic_tree import QGenericTree
from qt.control.section_control_widgets import QHoverDetectionCheckboxesWidget
from qt.control.tab_bgnd import BgndItem, BgndInspector
from qt.control.tab_misc import MiscItem, MiscInspector
from qt.control.tab_move import MoveItem, MoveInspector, LayerItem, LayerInspector, SectorItem, SectorInspector, \
    ObstacleItem, ObstacleInspector
from qt.control.tab_sght import SghtItem, SghtInspector, SightObstacleItem, SightObstacleInspector

type_match = []
type_match.append([(Misc, MiscItem, MiscInspector)])
type_match.append([(Bgnd, BgndItem, BgndInspector)])
type_match.append([(Move, MoveItem, MoveInspector), (Layer, LayerItem, LayerInspector), (Sector, SectorItem, SectorInspector), (Obstacle, ObstacleItem, ObstacleInspector)])
type_match.append([(Sght, SghtItem, SghtInspector), (SightObstacle, SightObstacleItem, SightObstacleInspector)])



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
        tips = []
        if SECTION_DEPENDENCIES[self.section_id]:
            tips.append(f"{SECTION_FLAG[self.section_id]} depends on {", ".join([SECTION_FLAG[s] for s in SECTION_DEPENDENCIES[self.section_id]])}")
        transpose_dependencies = [i for i in range(NB_SECTION) if self.section_id in SECTION_DEPENDENCIES[i]]
        if transpose_dependencies:
            tips.append(f"{", ".join([SECTION_FLAG[s] for s in transpose_dependencies])} depend on {SECTION_FLAG[self.section_id]}")
        name_label.setToolTip("\n".join(tips))


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

        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Section status"))
        self.status_label = QLabel()
        status_layout.addWidget(self.status_label)
        section_layout.addLayout(status_layout)

        loading_layout = QHBoxLayout()
        loading_layout.addWidget(QLabel("Loading type"))
        self.load_combobox = QComboBox()
        self.load_combobox.addItem("Unload")
        self.load_combobox.addItem("Lazy")
        self.load_combobox.addItem("Complete")
        self.load_combobox.activated.connect(self.load_combobox_user_change)
        loading_layout.addWidget(self.load_combobox)
        section_layout.addLayout(loading_layout)

        hover_detection_layout = QHBoxLayout()
        hover_detection_layout.addWidget(QLabel("Hover detection"))
        self.hover_detection = QHoverDetectionCheckboxesWidget([t[0] for t in type_match[self.section_id]])
        hover_detection_layout.addWidget(self.hover_detection)
        hover_detection_layout.addStretch()
        section_layout.addLayout(hover_detection_layout)

        section_layout.addStretch()

        import_export_layout = QHBoxLayout()
        import_export_layout.addSpacing(120)
        self.import_button = QPushButton("Import")
        self.import_button.setStatusTip(f"Import the {SECTION_FLAG[self.section_id]} section form data or other DVD file.")
        self.import_button.clicked.connect(self.import_button_clicked)
        import_export_layout.addWidget(self.import_button)
        import_export_layout.addSpacing(10)
        self.export_button = QPushButton("Export")
        self.export_button.setStatusTip(f"Save the current {SECTION_FLAG[self.section_id]} section into a data file.")
        self.export_button.clicked.connect(self.export_button_clicked)
        import_export_layout.addWidget(self.export_button)
        # import_export_layout.addSpacing(20)
        section_layout.addLayout(import_export_layout)

        section_layout.addWidget(QHLine())

        top_layout.addWidget(self.section_widget)

        self.tree = QGenericTree()
        self.tree.itemSelectionChanged.connect(self.item_selection_changed)
        self.tree.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Minimum)
        self.tree.setFixedWidth(300)
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

    @property
    def status(self):
        if AC.level.data[self.section_id].loaded:
            return "Valid"  #TODO
        else:
            return "Unverified"

    def load_combobox_user_change(self, index):
        match index:
            case 0:
                self.unload()
            case 1:
                AC.level.data[self.section_id].load(AC.level)
                self.unload()
            case 2:
                self.load()

    def import_button_clicked(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dialog.setDirectory(os.curdir)
        s = SECTION_FLAG[self.section_id]
        filters = [f"Any {s.capitalize()} data file (*.dvd *.odv{s.lower()})",
                   f"DVD file (*.dvd)",
                   f"{s.capitalize()} file (*.odv{s.lower()})",
                   f"Any file (*)"]
        dialog.setNameFilters(filters)
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            self.unload()
            AC.level.data[self.section_id] = section_types[self.section_id].from_file(filename)
        self.update()

    def export_button_clicked(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setDirectory(os.curdir)
        flag = SECTION_FLAG[self.section_id]
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            if not os.path.isfile(filename):
                filename += f".odv{flag.lower()}"
            AC.level.data[self.section_id].to_file(filename)

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
        if not self.loaded:
            section = AC.level.data[self.section_id]
            if section is not None:
                section.load(AC.level)
                recursive_load(section, None)
                self.tree_items[section].setSelected(True)
                self.tree_items[section].setExpanded(True)
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
            self.load_combobox.setCurrentIndex(0)
            self.load_combobox.setEnabled(False)
            self.status_label.setText("No Data")
            self.hover_detection.setEnabled(False)
            self.export_button.setEnabled(False)
            self.inspector_stack_layout.setCurrentWidget(self.inspector_unload_section_widget)
            self.tree.setEnabled(False)
        else:
            self.load_combobox.setEnabled(True)
            self.status_label.setText(self.status)
            self.hover_detection.setEnabled(self.loaded)
            self.export_button.setEnabled(True)
            self.tree.setEnabled(self.loaded)
            if self.loaded:
                self.load_combobox.setCurrentIndex(2)
            else:
                self.inspector_stack_layout.setCurrentWidget(self.inspector_unload_section_widget)
                if section.loaded:
                    self.load_combobox.setCurrentIndex(1)
                else:
                    self.load_combobox.setCurrentIndex(0)
