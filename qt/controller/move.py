from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem


class QMoveController(QTreeWidget):
    def __init__(self):
        super().__init__()

        self.headerItem().setText(0, "Area")
        self.headerItem().setText(1, "col2")
        self.headerItem().setText(2, "Notes")

        for ii in range(3):
            parent = QTreeWidgetItem(self)
            parent.setText(0, "Parent {}".format(ii))
            parent.setFlags(parent.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
            parent.setCheckState(0, Qt.CheckState.PartiallyChecked)
            for x in range(4):
                child = QTreeWidgetItem(parent)
                child.setText(0, "Child {}".format(x))
                child.setFlags(child.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                child.setCheckState(0, Qt.CheckState.Unchecked)

                #create the checkbox
                for i in range(1, 5):
                    if i < 3:
                        child.setText(i, "")
                        child.setCheckState(i, Qt.CheckState.Unchecked)
                    if i == 3:
                        child.setText(i, "Any Notes?")
                        child.setFlags(child.flags() | Qt.ItemFlag.ItemIsEditable)

