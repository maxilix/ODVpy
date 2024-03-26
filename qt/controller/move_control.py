from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen, QBrush
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem

import dvd.move
from qt.map_scene import QMapScene


# from dvd.move import Layer, Sublayer, MoveArea


class QMotionItem(QTreeWidgetItem):
    def __init__(self, parent, indexes, motion_object):
        super().__init__(parent)
        self._parent = parent
        self.motion_object = motion_object
        self.indexes = indexes

        match type(self.motion_object):
            case dvd.move.Layer:
                self.setText(0, f"Layer {self.indexes[-1]}")
                self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
            case dvd.move.Sublayer:
                self.setText(0, f"Sublayer {self.indexes[-1]}")
                self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
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

        for i, layer in enumerate(self.motion):
            layer_item = QMotionItem(self, (i,), layer)
            for j, sublayer in enumerate(layer):
                sublayer_item = QMotionItem(layer_item, (i, j), sublayer)
                for k, move_area in enumerate(sublayer):
                    area_item = QMotionItem(sublayer_item, (i, j, k), move_area)

        self.currentItemChanged.connect(self.catch_current_changed)
        self.itemChanged.connect(self.catch_changed)

        # for i in range(1, 5):
        #     if i < 3:
        #         child.setText(i, "")
        #         child.setCheckState(i, Qt.CheckState.Unchecked)
        #     if i == 3:
        #         child.setText(i, "Any Notes?")
        #         child.setFlags(child.flags() | Qt.ItemFlag.ItemIsEditable)

    def catch_changed(self, item: QMotionItem, col):
        print(item.indexes)
        if isinstance(item.motion_object, dvd.move.MoveArea):
            if item.checkState(0) == Qt.CheckState.Checked:
                self.scene.add_move_area(item.indexes, item.motion_object)
            else:
                self.scene.remove_move_area(item.indexes, item.motion_object)


    def catch_current_changed(self, curent, previous):
        print(curent, previous)

    # def show_sub_area(self, area):
    #     color = QColor(255, 0, 0, 128)
    #     pen = QPen(color)  # outline color
    #     color.setAlpha(16)
    #     brush = QBrush(color)  # fill color
    #     poly = area.QPolygonF()
    #     self.scene.addPolygon(area.QPolygonF(), pen, brush)
    #     self.scene.
