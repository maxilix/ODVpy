from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem


class QMoveController(QTreeWidget):
    def __init__(self, motion):
        super().__init__()

        self.headerItem().setText(0, "Area")
        self.headerItem().setText(1, "col2")
        self.headerItem().setText(2, "Notes")

        for i, layer in enumerate(motion):
            layer_item = QTreeWidgetItem(self)
            layer_item.setText(0, f"Layer {i}")
            layer_item.setFlags(layer_item.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
            layer_item.setCheckState(0, Qt.CheckState.Unchecked)
            for j, sublayer in enumerate(layer):
                sublayer_item = QTreeWidgetItem(layer_item)
                sublayer_item.setText(0, f"SubLayer {j}")
                sublayer_item.setFlags(sublayer_item.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
                sublayer_item.setCheckState(0, Qt.CheckState.Unchecked)
                for k, area in enumerate(sublayer):
                    area_item = QTreeWidgetItem(sublayer_item)
                    if k == 0:
                        area_item.setText(0, f"Main Area")
                    else:
                        area_item.setText(0, f"Sub Area {k - 1}")
                    area_item.setFlags(sublayer_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    area_item.setCheckState(0, Qt.CheckState.Unchecked)

                # for i in range(1, 5):
                #     if i < 3:
                #         child.setText(i, "")
                #         child.setCheckState(i, Qt.CheckState.Unchecked)
                #     if i == 3:
                #         child.setText(i, "Any Notes?")
                #         child.setFlags(child.flags() | Qt.ItemFlag.ItemIsEditable)

