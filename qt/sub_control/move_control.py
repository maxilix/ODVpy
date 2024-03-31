from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen, QBrush, QFont
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QTabWidget, QLabel, QVBoxLayout, QCheckBox, QWidget, \
    QListWidget, QListWidgetItem, QGroupBox, QSpacerItem, QSizePolicy, QScrollArea, QAbstractScrollArea, \
    QTreeWidgetItemIterator
from qt.common import QCollapsible

import dvd.move
from qt.scene import QScene


class QTreeWidgetAreaItem(QTreeWidgetItem):
    def __init__(self, parent, motion, i, j, k):
        super().__init__(parent)
        self.i = i
        self.j = j
        self.k = k
        self.area = motion[i][j][k]

        if self.k == 0:
            self.setText(1, f"main area")
        else:
            self.setText(1, f"exclude area {self.k}")
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsUserTristate | Qt.ItemFlag.ItemIsUserCheckable)
        self.setCheckState(0, Qt.CheckState.Unchecked)
        self.setCheckState(1, Qt.CheckState.Unchecked)
        self.crossing_point_item = []
        for l, crossing_point in enumerate(self.area):
            crossing_point_item = QTreeWidgetItem(self)
            crossing_point_item.setFlags(crossing_point_item.flags() | Qt.ItemFlag.ItemIsUserTristate | Qt.ItemFlag.ItemIsUserCheckable)
            crossing_point_item.setText(1, str(crossing_point.point))
            crossing_point_item.setCheckState(1, Qt.CheckState.Unchecked)
            if (nb_links := len(crossing_point)) > 0:
                crossing_point_item.setText(2, f"{nb_links} link{"s" if nb_links > 1 else ""}")
                crossing_point_item.setCheckState(2, Qt.CheckState.Unchecked)
            # self.crossing_point_item.append(crossing_point_item)
            for link_index in crossing_point:
                link_path_item = QTreeWidgetItem(crossing_point_item)
                link_path_item.setFlags(link_path_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                indexes_self = (self.i, self.j, self.k, l,)
                link = motion.get_link(link_index)
                i_o, j_o, k_o, l_o = link.get_other(indexes_self)
                link_path_item.setCheckState(2, Qt.CheckState.Unchecked)
                link_path_item.setText(2, f"{motion[i_o][j_o][k_o][l_o].point} on {i_o} {j_o} {k_o}")







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
        self.checkbox.clicked.connect(parent.update_draw)
        layout.addWidget(self.checkbox)

        self.collapsible_option = QCollapsible(self, f"area details")
        collapse_layout = QVBoxLayout()

        self.area_tree = QTreeWidget()
        self.area_tree.setColumnCount(2)
        self.area_tree.setHeaderLabels(["Area", "CPoints", "Links"])
        collapse_layout.addWidget(self.area_tree)

        self.area_item = []
        for k, area in enumerate(self.sublayer):
            area_item = QTreeWidgetAreaItem(None, motion, i, j, k)
            self.area_item.append(area_item)
            self.area_tree.addTopLevelItem(area_item)

        self.area_tree.resizeColumnToContents(0)
        self.area_tree.resizeColumnToContents(1)
        self.area_tree.resizeColumnToContents(2)
        # self.area_tree.itemClicked.connect(self.catch_click)
        self.area_tree.itemChanged.connect(self.catch_change)
        self.area_tree.itemExpanded.connect(self.update_height)
        self.area_tree.itemCollapsed.connect(self.update_height)
        # self.area_tree.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        # self.area_tree.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.update_height()

        self.collapsible_option.set_content_layout(collapse_layout)
        layout.addWidget(self.collapsible_option)

    def update_height(self):

        w = self.area_tree.size().width()
        # h = self.area_tree.viewportSizeHint().height()
        print(self.count_items())
        h = 19*self.count_items()+2

        self.area_tree.resize(w, h)
        # self.area_tree.setMinimumHeight(new_h)
        # self.area_tree.viewport().setMinimumHeight(new_h)

    def count_items(self):
        count = 0
        iterator = QTreeWidgetItemIterator(self.area_tree)  # pass your treewidget as arg
        while iterator.value():
            item = iterator.value()

            if item.parent():
                if item.parent().isExpanded():
                    count += 1
            else:
                # root item
                count += 1
            iterator += 1

        return count

        # self.area_tree.setBaseSize(w, h+2)
        # self.area_tree.adjustSize()
        # y = self.area_tree.size().height()
        # print(y)
        # self.area_tree.viewport().size   .setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        # print(len(self.area_tree.children()))
        # self.area_tree.setSizeAdjustPolicy() (QAbstractScrollArea. .AdjustToContents)
        # self.area_tree.viewport().setMinimumHeight(y+2)

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
        self.checkbox.clicked.connect(self.clicked)
        layout.addWidget(self.checkbox)

        self.sublayer_widget = []
        for j, sublayer in enumerate(self.layer):
            sublayer_widget = QSublayer(self, scene, motion, i, j)
            self.sublayer_widget.append(sublayer_widget)
            layout.addWidget(sublayer_widget)

        layout.addStretch()
        self.setWidgetResizable(True)
        self.setWidget(content)

    def clicked(self):
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
        elif active == len(self.sublayer_widget):
            self.checkbox.setCheckState(Qt.CheckState.Checked)
        else:
            self.checkbox.setCheckState(Qt.CheckState.PartiallyChecked)




class QMoveControl(QTabWidget):
    def __init__(self, scene, motion):
        super().__init__()
        # self.setFixedWidth(500)
        # self.setMinimumSize(200,1000)

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




#
# # from dvd.move import Layer, Sublayer, MoveArea
#
#
# class QMotionItem(QTreeWidgetItem):
#     def __init__(self, parent, indexes, motion_object):
#         super().__init__(parent)
#         self.parent = parent
#         self.motion_object = motion_object
#         self.indexes = indexes
#
#         match type(self.motion_object):
#             case dvd.move.Layer:
#                 self.setText(0, f"Layer {self.indexes[-1]}")
#                 self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
#             case dvd.move.Sublayer:
#                 self.setText(0, f"Sublayer {self.indexes[-1]}")
#                 self.setFlags(self.flags() | Qt.ItemFlag.ItemIsUserCheckable)
#             case dvd.move.MoveArea:
#                 if self.indexes[-1] == 0:
#                     self.setText(0, f"Main Area")
#                 else:
#                     self.setText(0, f"Sub Area {self.indexes[-1] - 1}")
#                 self.setFlags(self.flags() | Qt.ItemFlag.ItemIsUserCheckable)
#             case _:
#                 raise Exception("Motion depth error")
#
#         self.setCheckState(0, Qt.CheckState.Unchecked)
#
#     # def _depth(self):
#     #     if isinstance(self._parent, QTreeWidget):
#     #         return 0
#     #     else:
#     #         return self._parent._depth() + 1
#
#
# class QMoveController(QTreeWidget):
#     def __init__(self, scene: QScene, motion):
#         super().__init__()
#         self.scene = scene
#         self.motion = motion
#         self.setColumnCount(2)
#         self.setHeaderLabels(["Area", "other"])
#         self.setColumnWidth(0, 180)
#         self.layer_item = []
#         self.sublayer_item = []
#         self.move_area_item = []
#         # self.setSelectionMode()
#
#         for i, layer in enumerate(self.motion):
#             self.layer_item.append(QMotionItem(self, (i,), layer))
#             self.sublayer_item.append([])
#             self.move_area_item.append([])
#             for j, sublayer in enumerate(layer):
#                 self.sublayer_item[i].append(QMotionItem(self.layer_item[-1], (i, j,), sublayer))
#                 self.move_area_item[i].append([])
#                 for k, move_area in enumerate(sublayer):
#                     self.move_area_item[i][j].append(QMotionItem(self.sublayer_item[-1][-1], (i, j, k,), move_area))
#
#         # self.currentItemChanged.connect(self.catch_current_changed)
#         # self.itemChanged.connect(self.catch_changed)
#         self.itemClicked.connect(self.catch_click)
#
#         # for i in range(1, 5):
#         #     if i < 3:
#         #         child.setText(i, "")
#         #         child.setCheckState(i, Qt.CheckState.Unchecked)
#         #     if i == 3:
#         #         child.setText(i, "Any Notes?")
#         #         child.setFlags(child.flags() | Qt.ItemFlag.ItemIsEditable)
#
#     def catch_click(self, item: QMotionItem, col):
#         for i, layer_item in enumerate(self.layer_item):
#             match layer_item.checkState(0):
#                 case Qt.CheckState.Checked:
#                     pass
#                 case Qt.CheckState.Unchecked:
#                     pass
#                 case Qt.CheckState.PartiallyChecked:
#                     for j, sublayer_item in self.sublayer_item[i]:
#                         match sublayer_item.checkState(0):
#                             case Qt.CheckState.Checked:
#                                 pass
#                             case Qt.CheckState.Unchecked:
#                                 pass
#                             case Qt.CheckState.PartiallyChecked:
#                                 for k, move_area_item in self.move_area_item[i][j]:
#                                     match sublayer_item.checkState(0):
#                                         case Qt.CheckState.Checked:
#                                             self.scene.add_move_area((i, j, k,), move_area_item.motion_object)
#                                         case Qt.CheckState.Unchecked:
#                                             self.scene.remove_move_area((i, j, k,))
#
#
#
#
#         if isinstance(item.motion_object, dvd.move.MoveArea) and item.parent.checkState(0) != Qt.CheckState.Checked:
#             self.scene.remove_sublayer(item.parent.indexes)
#             for k, move_area in enumerate(item.parent.motion_object):
#                 pass
#             if item.checkState(0) == Qt.CheckState.Checked:
#                 self.scene.add_move_area(item.indexes, item.motion_object)
#             else:
#                 self.scene.remove_move_area(item.indexes)
#
#         elif isinstance(item.motion_object, dvd.move.MoveArea) and item.parent.checkState(0) == Qt.CheckState.Checked:
#             for k, _ in enumerate(item.parent.motion_object):
#                 self.scene.remove_move_area(item.parent.indexes + (k,))
#             self.scene.add_sublayer(item.parent.indexes, item.parent.motion_object)
#
#         elif isinstance(item.motion_object, dvd.move.Sublayer) and item.checkState(0) == Qt.CheckState.Checked:
#             for k, _ in enumerate(item.motion_object):
#                 self.scene.remove_move_area(item.parent.indexes + (k,))
#             self.scene.add_sublayer(item.indexes, item.motion_object)
#
#         elif isinstance(item.motion_object, dvd.move.Sublayer) and item.checkState(0) == Qt.CheckState.Unchecked:
#             # it was checked and user uncheck it, so they are no move_area to add or remove
#             self.scene.remove_sublayer(item.indexes)
#
#         elif isinstance(item.motion_object, dvd.move.Layer) and item.checkState(0) == Qt.CheckState.Checked:
#             for j, sublayer in enumerate(item.motion_object):
#                 self.scene.add_sublayer(item.indexes + (j,), sublayer)
#
#         elif isinstance(item.motion_object, dvd.move.Layer) and item.checkState(0) == Qt.CheckState.Unchecked:
#             for j, _ in enumerate(item.motion_object):
#                 self.scene.remove_sublayer(item.indexes + (j,))
#
#
#
#     def catch_changed(self, item: QMotionItem, col):
#         if isinstance(item.motion_object, dvd.move.MoveArea):
#             # if item.parent.checkState(0) == Qt.CheckState.Checked :
#             #     for k, move_area in enumerate(item.parent.motion_object):
#             #         self.scene.remove_move_area(item.parent.indexes + (k,), move_area)
#             #     # self.scene.add_sublayer(item.parent.indexes, item.parent.motion_object)
#             # else:
#             #     # self.scene.remove_sublayer(item.parent.indexes, item.parent.motion_object)
#             if item.checkState(0) == Qt.CheckState.Checked:
#                 self.scene.add_move_area(item.indexes, item.motion_object)
#             else:
#                 self.scene.remove_move_area(item.indexes, item.motion_object)
#
#     def catch_current_changed(self, curent, previous):
#         pass
#         # print(curent, previous)
#
#     # def show_sub_area(self, area):
#     #     color = QColor(255, 0, 0, 128)
#     #     pen = QPen(color)  # outline color
#     #     color.setAlpha(16)
#     #     brush = QBrush(color)  # fill color
#     #     poly = area.QPolygonF()
#     #     self.scene.addPolygon(area.QPolygonF(), pen, brush)
#     #     self.scene.
