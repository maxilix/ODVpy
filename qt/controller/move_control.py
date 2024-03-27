from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen, QBrush
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem

import dvd.move
from qt.map_scene import QMapScene


# from dvd.move import Layer, Sublayer, MoveArea


class QMotionItem(QTreeWidgetItem):
    def __init__(self, parent, indexes, motion_object):
        super().__init__(parent)
        self.parent = parent
        self.motion_object = motion_object
        self.indexes = indexes

        match type(self.motion_object):
            case dvd.move.Layer:
                self.setText(0, f"Layer {self.indexes[-1]}")
                self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
            case dvd.move.Sublayer:
                self.setText(0, f"Sublayer {self.indexes[-1]}")
                self.setFlags(self.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            case dvd.move.MoveArea:
                if self.indexes[-1] == 0:
                    self.setText(0, f"Main Area")
                else:
                    self.setText(0, f"Sub Area {self.indexes[-1] - 1}")
                self.setFlags(self.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            case _:
                raise Exception("Motion depth error")

        self.setCheckState(0, Qt.CheckState.Unchecked)

    # def _depth(self):
    #     if isinstance(self._parent, QTreeWidget):
    #         return 0
    #     else:
    #         return self._parent._depth() + 1


class QMoveController(QTreeWidget):
    def __init__(self, scene: QMapScene, motion):
        super().__init__()
        self.scene = scene
        self.motion = motion
        self.setColumnCount(2)
        self.setHeaderLabels(["Area", "other"])
        self.setColumnWidth(0, 180)
        self.layer_item = []
        self.sublayer_item = []
        self.move_area_item = []

        for i, layer in enumerate(self.motion):
            self.layer_item.append(QMotionItem(self, (i,), layer))
            self.sublayer_item.append([])
            self.move_area_item.append([])
            for j, sublayer in enumerate(layer):
                self.sublayer_item[i].append(QMotionItem(self.layer_item[-1], (i, j,), sublayer))
                self.move_area_item[i].append([])
                for k, move_area in enumerate(sublayer):
                    self.move_area_item[i][j].append(QMotionItem(self.sublayer_item[-1][-1], (i, j, k,), move_area))

        # self.currentItemChanged.connect(self.catch_current_changed)
        # self.itemChanged.connect(self.catch_changed)
        self.itemClicked.connect(self.catch_click)

        # for i in range(1, 5):
        #     if i < 3:
        #         child.setText(i, "")
        #         child.setCheckState(i, Qt.CheckState.Unchecked)
        #     if i == 3:
        #         child.setText(i, "Any Notes?")
        #         child.setFlags(child.flags() | Qt.ItemFlag.ItemIsEditable)

    def catch_click(self, item: QMotionItem, col):
        for i, layer_item in enumerate(self.layer_item):
            match layer_item.checkState(0):
                case Qt.CheckState.Checked:
                    pass
                case Qt.CheckState.Unchecked:
                    pass
                case Qt.CheckState.PartiallyChecked:
                    for j, sublayer_item in self.sublayer_item[i]:
                        match sublayer_item.checkState(0):
                            case Qt.CheckState.Checked:
                                pass
                            case Qt.CheckState.Unchecked:
                                pass
                            case Qt.CheckState.PartiallyChecked:
                                for k, move_area_item in self.move_area_item[i][j]:
                                    match sublayer_item.checkState(0):
                                        case Qt.CheckState.Checked:
                                            self.scene.add_move_area((i, j, k,), move_area_item.motion_object)
                                        case Qt.CheckState.Unchecked:
                                            self.scene.remove_move_area((i, j, k,))




        if isinstance(item.motion_object, dvd.move.MoveArea) and item.parent.checkState(0) != Qt.CheckState.Checked:
            self.scene.remove_sublayer(item.parent.indexes)
            for k, move_area in enumerate(item.parent.motion_object):
                pass
            if item.checkState(0) == Qt.CheckState.Checked:
                self.scene.add_move_area(item.indexes, item.motion_object)
            else:
                self.scene.remove_move_area(item.indexes)

        elif isinstance(item.motion_object, dvd.move.MoveArea) and item.parent.checkState(0) == Qt.CheckState.Checked:
            for k, _ in enumerate(item.parent.motion_object):
                self.scene.remove_move_area(item.parent.indexes + (k,))
            self.scene.add_sublayer(item.parent.indexes, item.parent.motion_object)

        elif isinstance(item.motion_object, dvd.move.Sublayer) and item.checkState(0) == Qt.CheckState.Checked:
            for k, _ in enumerate(item.motion_object):
                self.scene.remove_move_area(item.parent.indexes + (k,))
            self.scene.add_sublayer(item.indexes, item.motion_object)

        elif isinstance(item.motion_object, dvd.move.Sublayer) and item.checkState(0) == Qt.CheckState.Unchecked:
            # it was checked and user uncheck it, so they are no move_area to add or remove
            self.scene.remove_sublayer(item.indexes)

        elif isinstance(item.motion_object, dvd.move.Layer) and item.checkState(0) == Qt.CheckState.Checked:
            for j, sublayer in enumerate(item.motion_object):
                self.scene.add_sublayer(item.indexes + (j,), sublayer)

        elif isinstance(item.motion_object, dvd.move.Layer) and item.checkState(0) == Qt.CheckState.Unchecked:
            for j, _ in enumerate(item.motion_object):
                self.scene.remove_sublayer(item.indexes + (j,))



    def catch_changed(self, item: QMotionItem, col):
        if isinstance(item.motion_object, dvd.move.MoveArea):
            # if item.parent.checkState(0) == Qt.CheckState.Checked :
            #     for k, move_area in enumerate(item.parent.motion_object):
            #         self.scene.remove_move_area(item.parent.indexes + (k,), move_area)
            #     # self.scene.add_sublayer(item.parent.indexes, item.parent.motion_object)
            # else:
            #     # self.scene.remove_sublayer(item.parent.indexes, item.parent.motion_object)
            if item.checkState(0) == Qt.CheckState.Checked:
                self.scene.add_move_area(item.indexes, item.motion_object)
            else:
                self.scene.remove_move_area(item.indexes, item.motion_object)

    def catch_current_changed(self, curent, previous):
        pass
        # print(curent, previous)

    # def show_sub_area(self, area):
    #     color = QColor(255, 0, 0, 128)
    #     pen = QPen(color)  # outline color
    #     color.setAlpha(16)
    #     brush = QBrush(color)  # fill color
    #     poly = area.QPolygonF()
    #     self.scene.addPolygon(area.QPolygonF(), pen, brush)
    #     self.scene.
