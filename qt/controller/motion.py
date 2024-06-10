from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QTabWidget, QLabel, QVBoxLayout, QCheckBox, QWidget, \
    QScrollArea, QTreeWidgetItemIterator, QPushButton, QHBoxLayout, QSpinBox

from .abstract_controller import Control, HierarchicalControl


class QControlArea(Control, QTreeWidgetItem):
    def __init__(self, parent, area, index):
        super().__init__(parent)
        self.area = area
        self.index = index
        if area.main:
            self.setText(0, f"Main Area")
        else:
            self.setText(0, f"Obstacle {self.index}")

        self.setCheckState(0, Qt.CheckState.Unchecked)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate)
    #
    # def update(self):
    #     self.view.setVisible(self.checkState(0) == Qt.CheckState.Checked)


class QControlSublayer(HierarchicalControl, QTreeWidgetItem):
    def __init__(self, parent, sublayer, index):
        super().__init__(parent)
        self.sublayer = sublayer
        self.index = index
        self.setText(0, f"Sublayer {self.index}")
        self.setCheckState(0, Qt.CheckState.Unchecked)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate)

        self.control_list = [QControlArea(self, area, k) for k, area in enumerate(self.sublayer)]


class QControlLayer(HierarchicalControl, QTreeWidgetItem):
    def __init__(self, parent, layer, index):
        super().__init__(parent)
        self.layer = layer
        self.index = index
        self.setText(0, f"Layer {self.index}")
        self.setCheckState(0, Qt.CheckState.Unchecked)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate)

        self.control_list = [QControlSublayer(self, sublayer, j) for j, sublayer in enumerate(self.layer)]


class QHighlightWidget(QWidget):
    def __init__(self, parent, nb_layer):
        super().__init__(parent)
        layout = QHBoxLayout(self)

        self.check_box = QCheckBox()
        self.check_box.setCheckState(Qt.CheckState.Checked)
        self.check_box.clicked.connect(self.update)
        layout.addWidget(self.check_box)

        self.label = QLabel("Highlight on layer")
        self.label.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
        layout.addWidget(self.label)

        layout.addStretch(255)

        self.spin = QSpinBox()
        self.spin.setMinimum(0)
        self.spin.setMaximum(nb_layer)
        self.spin.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
        layout.addWidget(self.spin)
        self.update()

    def update(self):
        if self.check_box.isChecked() is True:
            self.label.setEnabled(True)
            self.spin.setEnabled(True)
        else:
            self.label.setEnabled(False)
            self.spin.setEnabled(False)

    def value(self):
        if self.check_box.isChecked() is False:
            return -1
        else:
            return self.spin.value()


class QAreaTreeWidget(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setHeaderLabels(["Layer", "Sublayer", "Area"])
        self.setHeaderHidden(True)

        self.itemDoubleClicked.connect(self.item_double_clicked)
        self.itemExpanded.connect(self.update_height)
        self.itemCollapsed.connect(self.update_height)

    def item_double_clicked(self, item, column):
        pass

    def update_height(self):
        h = 18 * self.count_visible_item() + 2 + 22
        self.setMinimumHeight(h)
        self.setMaximumHeight(h)
        self.resizeColumnToContents(0)

    def count_visible_item(self):
        count = 0
        index = self.model().index(0, 0)
        while index.isValid():
            count += 1
            index = self.indexBelow(index)
        return count


class QControlAreas(HierarchicalControl, QScrollArea):
    def __init__(self, parent, motion):
        super().__init__(parent)
        self.motion = motion
        self.set_widget()

    def set_widget(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        if self.motion.loaded_areas is False:
            load_areas_button = QPushButton("Load areas")
            load_areas_button.clicked.connect(self.load_areas)
            layout.addWidget(load_areas_button)
        else:
            reload_area_button = QPushButton("Reload from data")
            reload_area_button.clicked.connect(self.load_areas)
            layout.addWidget(reload_area_button)
            highlight_widget = QHighlightWidget(self, len(self.motion))
            layout.addWidget(highlight_widget)
            tree_widget = QAreaTreeWidget(self)
            layout.addWidget(tree_widget)

            self.control_list = [QControlLayer(tree_widget, layer, i) for i, layer in enumerate(self.motion)]
            self.view.__init__(self.view.scene, self)

            tree_widget.update_height()

        layout.addStretch(255)
        self.setWidgetResizable(True)
        self.setWidget(content)

    def load_areas(self):
        self.motion.load(only_areas=True)
        self.set_widget()


class QControlMotion(Control, QTabWidget):
    def __init__(self, parent, motion):
        super().__init__(parent)
        self.motion = motion

        self.setTabPosition(QTabWidget.TabPosition.North)
        self.setMovable(False)

        self.control_areas = QControlAreas(self, self.motion)
        self.addTab(self.control_areas, f"Areas")

        self.control_pathfinder = QWidget(self)
        self.addTab(self.control_pathfinder, f"PathFinder")


    def add_view(self, view):
        super().add_view(view)
        self.control_areas.add_view(view.view_areas)
        # self.control_pathfinder.add_view(view.view_pathfinder)




