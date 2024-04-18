from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QTabWidget, QLabel, QVBoxLayout, QCheckBox, QWidget, \
    QScrollArea, QTreeWidgetItemIterator


class PathLinkItem(QTreeWidgetItem):
    def __init__(self, parent, motion, i, j, k, l, m):
        super().__init__(parent)
        self.i = i
        self.j = j
        self.k = k
        self.l = l
        self.m = m
        self.path_link = motion.get_path_link(m)
        i_o, j_o, k_o, l_o = self.path_link.get_other((i, j, k, l,))
        self.setText(2, f"{motion[i_o][j_o][k_o][l_o].point} on {i_o} {j_o} {k_o}")
        self.setCheckState(2, Qt.CheckState.Unchecked)


class CrossingPointItem(QTreeWidgetItem):
    def __init__(self, parent, motion, i, j, k, l):
        super().__init__(parent)
        self.i = i
        self.j = j
        self.k = k
        self.l = l
        self.crossing_point = motion[i][j][k][l]
        self.setText(1, str(self.crossing_point.point))
        self.setCheckState(1, Qt.CheckState.Unchecked)
        if (nb_path_link := len(self.crossing_point)) > 0:
            self.setText(2, f"{nb_path_link} link{"s" if nb_path_link > 1 else ""}")
            self.setCheckState(2, Qt.CheckState.Unchecked)
        self.path_link_item = [PathLinkItem(self, motion, i, j, k, l, m) for m in self.crossing_point]


class AreaItem(QTreeWidgetItem):
    def __init__(self, parent, motion, i, j, k):
        super().__init__(parent)
        self.i = i
        self.j = j
        self.k = k
        self.area = motion[i][j][k]

        if self.k == 0:
            self.setText(0, f"main area")
        else:
            self.setText(0, f"exclude area {self.k}")
        self.setCheckState(0, Qt.CheckState.Unchecked)
        if (nb_crossing_point := len(self.area)) > 0:
            self.setText(1, f"{nb_crossing_point} CPoint{"s" if nb_crossing_point > 1 else ""}")
            self.setCheckState(1, Qt.CheckState.Unchecked)
        self.crossing_point_item = [CrossingPointItem(self, motion, i, j, k, l) for l, _ in enumerate(self.area)]


class CustomTreeWidget(QTreeWidget):
    def __init__(self, parent, scene):
        super().__init__(parent)
        self.scene = scene

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHeaderLabels(["Area", "CPoints", "Links"])

        self.itemClicked.connect(self.item_clicked)
        self.itemExpanded.connect(self.update_height)
        self.itemCollapsed.connect(self.update_height)

    def item_clicked(self, item, column):
        if column == 0:  # no tristate behavior
            pass

        elif (column == 1 and isinstance(item, AreaItem) or
              column == 2 and isinstance(item, CrossingPointItem)):  # parent
            for child_index in range(item.childCount()):
                child_item = item.child(child_index)
                child_item.setCheckState(column, item.checkState(column))

        else:  # child
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

        self.update_draw()

    def update_draw(self):
        iterator = QTreeWidgetItemIterator(self)
        while iterator.value():
            item = iterator.value()
            if isinstance(item, AreaItem):
                if item.checkState(0) == Qt.CheckState.Checked:
                    self.scene.move_scene.show_area(item.i, item.j, item.k)
                else:
                    self.scene.move_scene.hide_area(item.i, item.j, item.k)
            elif isinstance(item, CrossingPointItem):
                if item.checkState(1) == Qt.CheckState.Checked:
                    self.scene.move_scene.show_crossing_point(item.i, item.j, item.k, item.l)
                else:
                    self.scene.move_scene.hide_crossing_point(item.i, item.j, item.k, item.l)
            elif isinstance(item, PathLinkItem):
                if item.checkState(2) == Qt.CheckState.Checked:
                    self.scene.move_scene.show_path_link(item.m)
                else:
                    self.scene.move_scene.hide_path_link(item.m)
            else:
                raise Exception("oups")  # TODO
            iterator += 1


    def update_height(self):
        h = 18 * self.nb_expanded_item() + 2 + 22
        self.setMinimumHeight(h)
        self.setMaximumHeight(h)
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(2)

    def nb_expanded_item(self):
        # doesn't work with collapsed item which contain expanded item
        count = 0
        iterator = QTreeWidgetItemIterator(self)
        while iterator.value():
            item = iterator.value()
            if item.parent():
                if item.parent().isExpanded():
                    count += 1
            else:
                count += 1
            iterator += 1
        return count


class QSublayer(QWidget):
    def __init__(self, parent, scene, motion, i, j):
        super().__init__(parent)
        self.scene = scene
        self.i = i
        self.j = j
        self.sublayer = motion[i][j]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 0, 0, 30)

        self.checkbox = QCheckBox(f"Show sublayer {self.j} movable area")
        # myFont = QFont()
        # myFont.setBold(True)
        # myFont.setUnderline(True)
        # self.checkbox.setFont(myFont)
        self.checkbox.released.connect(parent.update_draw)
        layout.addWidget(self.checkbox)

        # self.collapsible_option = QCollapsible(self, f"area details")
        # collapse_layout = QVBoxLayout()

        self.tree = CustomTreeWidget(self, scene)
        self.area_item = [AreaItem(self.tree, motion, i, j, k) for k, _ in enumerate(self.sublayer)]
        self.tree.update_height()
        layout.addWidget(self.tree)

    def catch_click(self, item):
        print("Clicked", item.text(0))

    def catch_change(self, item):
        print("Changed", item.text(0))


class QLayer(QScrollArea):
    def __init__(self, parent, scene, motion, i):
        super().__init__(parent)
        self.scene = scene
        self.i = i
        self.layer = motion[i]

        content = QWidget()
        layout = QVBoxLayout(content)

        self.title = QLabel(f"Layer {self.i}")
        layout.addWidget(self.title)

        self.checkbox = QCheckBox("Show all movable areas")
        self.checkbox.setChecked(False)
        self.checkbox.released.connect(self.main_checkbox_clicked)

        layout.addWidget(self.checkbox)

        self.sublayer_widget = []
        for j, sublayer in enumerate(self.layer):
            sublayer_widget = QSublayer(self, scene, motion, i, j)
            self.sublayer_widget.append(sublayer_widget)
            layout.addWidget(sublayer_widget)

        layout.addStretch(255)
        self.setWidgetResizable(True)
        self.setWidget(content)

    def main_checkbox_clicked(self):
        for sublayer_widget in self.sublayer_widget:
            sublayer_widget.checkbox.setCheckState(self.checkbox.checkState())

        self.update_draw()

    def update_draw(self):
        active = 0
        for j, sublayer_widget in enumerate(self.sublayer_widget):
            if sublayer_widget.checkbox.checkState() == Qt.CheckState.Checked:
                active += 1
                self.scene.move_scene.show_sublayer(self.i, j)
            else:
                self.scene.move_scene.hide_sublayer(self.i, j)

        if active == 0:
            self.checkbox.setCheckState(Qt.CheckState.Unchecked)
            self.checkbox.setTristate(False)
        elif active == len(self.sublayer_widget):
            self.checkbox.setCheckState(Qt.CheckState.Checked)
            self.checkbox.setTristate(False)
        else:
            self.checkbox.setCheckState(Qt.CheckState.PartiallyChecked)


class QMoveControl(QTabWidget):
    def __init__(self, scene, motion):
        super().__init__()

        self.setTabPosition(QTabWidget.TabPosition.North)
        self.setMovable(False)

        ground_index = 0
        ladder_index = len(motion) - 1
        for i, layer in enumerate(motion):
            layer_widget = QLayer(self, scene, motion, i)
            if i == ground_index:
                self.addTab(layer_widget, f"Ground")
            elif i == ladder_index:
                self.addTab(layer_widget, f"Ladders")
            else:
                self.addTab(layer_widget, f"G+{i}")
