from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QTabWidget, QLabel, QVBoxLayout, QCheckBox, QWidget, \
    QScrollArea, QTreeWidgetItemIterator

from .abstract_controller import Control, HierarchicalControl


class QControlPathLink(Control, QTreeWidgetItem):
    def __init__(self, parent, path_link, index):
        super().__init__(parent)
        self.path_link = path_link
        self.index = index

        i_o, j_o, k_o, l_o = self.path_link.indexes1
        self.setText(2, f"{self.path_link.point1.point} on {i_o} {j_o} {k_o}")
        self.setCheckState(2, Qt.CheckState.Unchecked)

    def update(self):
        self.view.setVisible(self.checkState(2) == Qt.CheckState.Checked)


class QControlCrossingPoint(HierarchicalControl, QTreeWidgetItem):
    def __init__(self, parent, crossing_point, index):
        super().__init__(parent)
        self.crossing_point = crossing_point
        self.index = index

        self.setText(1, str(self.crossing_point.point))
        self.setCheckState(1, Qt.CheckState.Unchecked)
        if (nb_path_link := len(self.crossing_point)) > 0:
            self.setText(2, f"{nb_path_link} link{"s" if nb_path_link > 1 else ""}")
            self.setCheckState(2, Qt.CheckState.Unchecked)

        # self.control_path_link_list = []
        for m, path_link in enumerate(self.crossing_point):
            control_path_link = QControlPathLink(self, path_link, m)
            self.control_list.append(control_path_link)

    def update(self):
        self.view.setVisible(self.checkState(1) == Qt.CheckState.Checked)


class QControlArea(QTreeWidgetItem, HierarchicalControl):
    def __init__(self, parent, area, index):
        super().__init__(parent)
        self.area = area
        self.index = index
        if area.is_main():
            self.setText(0, f"Main Area")
        else:
            self.setText(0, f"Obstacle {self.index}")

        self.setCheckState(0, Qt.CheckState.Unchecked)
        if (nb_crossing_point := len(self.area)) > 0:
            self.setText(1, f"{nb_crossing_point} CPoint{"s" if nb_crossing_point > 1 else ""}")
            self.setCheckState(1, Qt.CheckState.Unchecked)

        # self.control_crossing_point_list = []
        for l, crossing_point in enumerate(self.area):
            control_crossing_point = QControlCrossingPoint(self, crossing_point, l)
            self.control_list.append(control_crossing_point)

    def update(self):
        self.view.setVisible(self.checkState(0) == Qt.CheckState.Checked)


class CustomTreeWidget(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHeaderLabels(["Area", "CPoints", "Links"])

        self.itemClicked.connect(self.item_clicked)
        # self.currentItemChanged.connect(self.item_selection_changed)
        self.itemExpanded.connect(self.update_height)
        self.itemCollapsed.connect(self.update_height)

    def item_clicked(self, item, column):
        item.update()
        if column == 0 and isinstance(item, QControlArea):  # no tristate behavior
            pass

        elif (column == 1 and isinstance(item, QControlArea) or
              column == 2 and isinstance(item, QControlCrossingPoint)):  # parent
            for child_index in range(item.childCount()):
                child_item = item.child(child_index)
                child_item.setCheckState(column, item.checkState(column))
                child_item.update()

        elif (column == 1 and isinstance(item, QControlCrossingPoint) or
              column == 2 and isinstance(item, QControlPathLink)):  # child
            parent_item = item.parent()
            active_child = 0
            for child_index in range(parent_item.childCount()):
                child_item = parent_item.child(child_index)
                active_child += (child_item.checkState(column) == Qt.CheckState.Checked)
            if active_child == 0:
                parent_item.setCheckState(column, Qt.CheckState.Unchecked)
                # item.setTristate(False)
            elif active_child == parent_item.childCount():
                parent_item.setCheckState(column, Qt.CheckState.Checked)
                # item.setTristate(False)
            else:
                parent_item.setCheckState(column, Qt.CheckState.PartiallyChecked)

        else:
            pass


    #     self.update()
    #
    # def update(self):
    #     pass
        # iterator = QTreeWidgetItemIterator(self)
        # while iterator.value():
        #     item = iterator.value()
        #     if isinstance(item, QControlArea):
        #         if item.checkState(0) == Qt.CheckState.Checked:
        #             # self.scene.move_scene.show_area(item.i, item.j, item.k)
        #             pass
        #         else:
        #             # self.scene.move_scene.hide_area(item.i, item.j, item.k)
        #             pass
        #     elif isinstance(item, QControlCrossingPoint):
        #         if item.checkState(1) == Qt.CheckState.Checked:
        #             # self.scene.move_scene.show_crossing_point(item.i, item.j, item.k, item.l)
        #             pass
        #         else:
        #             # self.scene.move_scene.hide_crossing_point(item.i, item.j, item.k, item.l)
        #             pass
        #     elif isinstance(item, QControlPathLink):
        #         if item.checkState(2) == Qt.CheckState.Checked:
        #             # self.scene.move_scene.show_path_link(item.m)
        #             pass
        #         else:
        #             # self.scene.move_scene.hide_path_link(item.m)
        #             pass
        #     else:
        #         raise Exception("oups")  # TODO
        #     iterator += 1

    def update_height(self):
        h = 18 * self.count_visible_item() + 2 + 22
        self.setMinimumHeight(h)
        self.setMaximumHeight(h)
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(2)

    def count_visible_item(self):
        count = 0
        index = self.model().index(0, 0)
        while index.isValid():
            count += 1
            index = self.indexBelow(index)
        return count

class QControlSublayer(HierarchicalControl, QWidget):
    def __init__(self, parent, sublayer, index):
        super().__init__(parent)
        self.sublayer = sublayer
        self.index = index

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 0, 0, 30)

        self.checkbox = QCheckBox(f"Show sublayer {self.index} movable area")
        # myFont = QFont()
        # myFont.setBold(True)
        # myFont.setUnderline(True)
        # self.checkbox.setFont(myFont)
        self.checkbox.released.connect(parent.update)
        layout.addWidget(self.checkbox)

        self.tree = CustomTreeWidget(self)

        # self.control_area_list = []
        for k, area in enumerate(self.sublayer):
            control_area = QControlArea(self.tree, area, k)
            self.control_list.append(control_area)

        self.tree.update_height()
        # print(f"{self.tree} updated at init")
        layout.addWidget(self.tree)

    # def catch_click(self, item):
    #     print("Clicked", item.text(0))
    #
    # def catch_change(self, item):
    #     print("Changed", item.text(0))


class QControlLayer(HierarchicalControl, QScrollArea):
    def __init__(self, parent, layer, index):
        super().__init__(parent)
        self.layer = layer
        self.index = index

        content = QWidget()
        layout = QVBoxLayout(content)

        self.title = QLabel(f"Layer {self.index}")
        layout.addWidget(self.title)

        self.checkbox = QCheckBox("Show all movable areas")
        self.checkbox.setChecked(False)
        self.checkbox.released.connect(self.main_checkbox_clicked)
        layout.addWidget(self.checkbox)

        for j, sublayer in enumerate(self.layer):
            control_sublayer = QControlSublayer(self, sublayer, j)
            self.control_list.append(control_sublayer)
            layout.addWidget(control_sublayer)

        layout.addStretch(255)
        self.setWidgetResizable(True)
        self.setWidget(content)

    def main_checkbox_clicked(self):
        for control_sublayer in self.control_list:
            control_sublayer.checkbox.setCheckState(self.checkbox.checkState())

        self.update()

    def update(self):
        active = 0
        for j, control_sublayer in enumerate(self.control_list):
            if control_sublayer.checkbox.checkState() == Qt.CheckState.Checked:
                active += 1
                control_sublayer.view.setVisible(True)
                print("visible")
            else:
                control_sublayer.view.setVisible(False)

        if active == 0:
            self.checkbox.setCheckState(Qt.CheckState.Unchecked)
            self.checkbox.setTristate(False)
        elif active == len(self):
            self.checkbox.setCheckState(Qt.CheckState.Checked)
            self.checkbox.setTristate(False)
        else:
            self.checkbox.setCheckState(Qt.CheckState.PartiallyChecked)


class QControlMotion(HierarchicalControl, QTabWidget):
    def __init__(self, parent, motion):
        super().__init__(parent)
        self.motion = motion

        self.setTabPosition(QTabWidget.TabPosition.North)
        self.setMovable(False)

        ground_index = 0
        ladders_index = len(self.motion) - 1
        # self.control_layer_list = []
        for i, layer in enumerate(motion):
            control_layer = QControlLayer(self, layer, i)
            if i == ground_index:
                self.addTab(control_layer, f"Ground")
            elif i == ladders_index:
                self.addTab(control_layer, f"Ladders")
            else:
                self.addTab(control_layer, f"G+{i}")
            self.control_list.append(control_layer)
