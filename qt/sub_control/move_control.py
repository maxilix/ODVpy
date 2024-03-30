from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen, QBrush
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QTabWidget, QLabel, QVBoxLayout, QCheckBox, QWidget, \
    QListWidget, QListWidgetItem, QGroupBox, QSpacerItem, QSizePolicy, QScrollArea
from qt.common import QCollapsible

import dvd.move
from qt.scene import QScene


class QTreeWidgetAreaItem(QTreeWidgetItem):
    def __init__(self, parent, area_index, area):
        super().__init__(parent)
        if area_index == 0:
            self.setText(0, f"main area")
        else:
            self.setText(0, f"exclude area {area_index}")
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        self.setCheckState(0, Qt.CheckState.Unchecked)


class QSublayer(QWidget):
    def __init__(self, parent, sublayer_index, sublayer):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 0, 0, 30)

        self.checkbox = QCheckBox(f"Show sublayer {sublayer_index} movable area")
        self.checkbox.clicked.connect(parent.update_draw)
        layout.addWidget(self.checkbox)

        self.collapsible_option = QCollapsible(self, f"area details")
        collapse_layout = QVBoxLayout()

        # label = QCheckBox("Show main area")
        # collapse_layout.addWidget(label)

        self.area_tree = QTreeWidget()
        self.area_tree.setColumnCount(2)
        self.area_tree.setHeaderLabels(["Area", "CPoints", "Links"])
        collapse_layout.addWidget(self.area_tree)
        # self.area_header_item = QTreeWidgetItem(self.area_tree)
        # self.area_header_item.setText(0, "Check All")
        # self.area_header_item.setFlags(self.area_header_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        # self.area_header_item.setCheckState(0, Qt.CheckState.Unchecked)
        self.area_item = []
        for k, area in enumerate(sublayer):
            area_item = QTreeWidgetAreaItem(None, k, area)
            self.area_item.append(area_item)
            self.area_tree.addTopLevelItem(area_item)
        self.area_tree.resizeColumnToContents(0)
        y = self.area_tree.viewportSizeHint().height()
        self.area_tree.setFixedHeight(y+2)
        self.collapsible_option.set_content_layout(collapse_layout)
        layout.addWidget(self.collapsible_option)



class QLayer(QScrollArea):
    def __init__(self, parent, scene, layer_index, layer):
        super().__init__(parent)
        self.scene = scene
        self.layer_index = layer_index
        self.layer = layer

        content = QWidget()
        layout = QVBoxLayout(content)

        self.title = QLabel(f"Layer {self.layer_index}")
        layout.addWidget(self.title)

        self.checkbox = QCheckBox("Show all movable areas")
        self.checkbox.setChecked(False)
        self.checkbox.clicked.connect(self.clicked)
        layout.addWidget(self.checkbox)

        self.sublayer_widget = []
        for j, sublayer in enumerate(layer):
            sublayer_widget = QSublayer(self, j, sublayer)
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
                self.scene.move_scene.show_sublayer(self.layer_index, j)
            else:
                self.scene.move_scene.hide_sublayer(self.layer_index, j)

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
            layer_widget = QLayer(self, scene, i, layer)
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
