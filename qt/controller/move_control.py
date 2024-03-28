from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen, QBrush
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QTabWidget, QLabel, QVBoxLayout, QCheckBox, QWidget, \
    QListWidget, QListWidgetItem, QGroupBox, QSpacerItem, QSizePolicy, QScrollArea

import dvd.move
from qt.scene import QScene


class QSublayer(QWidget):
    def __init__(self, sublayer):
        super().__init__()
        layout = QVBoxLayout()

        self.checkbox = QCheckBox("Show sublayer movable area")
        layout.addWidget(self.checkbox)

        # self.checkbox = QCheckBox("Show main area")
        # layout.addWidget(self.checkbox)

        self.area_list = QListWidget()
        nb_area = len(sublayer)
        for k, area in enumerate(sublayer):
            if k == 0:
                area_item = QListWidgetItem(f"main area")
            else:
                area_item = QListWidgetItem(f"excluded area {k}")
            area_item.setFlags(area_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            area_item.setCheckState(Qt.CheckState.Unchecked)
            self.area_list.addItem(area_item)
        layout.addWidget(self.area_list)

        y = self.area_list.viewportSizeHint().height()
        self.area_list.setFixedHeight(y+2)

        # self.setCheckable(True)
        self.setLayout(layout)









class QLayer(QWidget):
    def __init__(self, layer):
        super().__init__()
        layout = QVBoxLayout()
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        layout.addItem(spacer)

        # layer_title = QLabel(f"Layer {i}")
        # layout.addWidget(layer_title)

        self.checkbox = QCheckBox("Show all movable areas")
        layout.addWidget(self.checkbox)

        self.sublayer_widget = [QSublayer(sublayer) for sublayer in layer]
        for w in self.sublayer_widget:
            layout.addWidget(w)

        content = QWidget()
        content.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Permet au widget interne de redimensionner le scroll area
        scroll_area.setWidget(content)
        # scroll_area.setAlignment(Qt.AlignmentFlag.AlignTop)  # Aligner le contenu en haut

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    # def __init__(self):
    #     super().__init__()
    #
    #     layout = QVBoxLayout()
    #     spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
    #     layout.addItem(spacer)
    #
    #     for i in range(5):  # Ajouter quelques boutons juste pour l'exemple
    #         button = QPushButton(f"Bouton {i+1}")
    #         l = QListWidget()
    #         nb_item = 10-i
    #         for _ in range(nb_item):
    #             item = QListWidgetItem(f"Item")
    #             # item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
    #             item.setCheckState(Qt.CheckState.Checked)
    #             l.addItem(item)
    #         l.setFixedHeight(nb_item*19)
    #         layout.addWidget(l)
    #         layout.setSpacing(10)  # Espacement entre les boutons
    #
    #     spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    #     layout.addItem(spacer)
    #
    #     content = QWidget()
    #     content.setLayout(layout)
    #
    #     scroll_area = QScrollArea()
    #     scroll_area.setWidgetResizable(True)  # Permet au widget interne de redimensionner le scroll area
    #     scroll_area.setWidget(content)
    #     # scroll_area.setAlignment(Qt.AlignmentFlag.AlignTop)  # Aligner le contenu en haut
    #
    #     main_layout = QVBoxLayout()
    #     main_layout.addWidget(scroll_area)
    #
    #     self.setLayout(main_layout)



















class QMoveController(QTabWidget):
    def __init__(self, scene, motion):
        super().__init__()
        # self.setFixedWidth(500)
        # self.setMinimumSize(200,1000)

        self.setTabPosition(QTabWidget.TabPosition.North)
        self.setMovable(False)

        ground_index = 0
        ladder_index = len(motion) - 1
        for i, layer in enumerate(motion):
            layer_widget = QLayer(layer)
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
