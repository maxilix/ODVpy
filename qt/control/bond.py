from PyQt6.QtCore import Qt, QLineF
from PyQt6.QtGui import QContextMenuEvent, QAction, QCursor
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QGraphicsLineItem, QMenu

from qt.control.common import QTabControl


class QBondItem(QListWidgetItem):
    def __init__(self, parent, scene, b):
        super().__init__(parent)
        self.scene = scene
        self.b = b
        self.setCheckState(Qt.CheckState.Checked)

        self.line = QGraphicsLineItem(QLineF(b.p1, b.p2))
        self.scene.addItem(self.line)

        self.update()

    @property
    def i(self):
        return self.listWidget().indexFromItem(self).row()

    def update(self):
        self.setText(f"Bond {self.i} - {self.b.left_id} {self.b.right_id} - {self.b.layer_id}")
        self.line.setVisible(self.checkState() == Qt.CheckState.Checked)

    def contextMenuEvent(self, event):
        menu = QMenu()
        a_localise = QAction("Localise")
        a_localise.triggered.connect(self.localise)
        menu.addAction(a_localise)

        # menu.addActions(self.common_actions())
        menu.exec(QCursor.pos())

    def localise(self):
        self.setCheckState(Qt.CheckState.Checked)
        self.scene.move_to_item(self.line)


class QBondListWidget(QListWidget):
    def __init__(self, parent, scene, bond):
        super().__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scene = scene
        self.bond = bond

        for b in bond.bond_list:
            QBondItem(self, self.scene, b)

        self.itemChanged.connect(self.item_changed)

    def update_height(self):
        pass
        h = 18 * self._count_visible_item() + 2
        self.setMinimumHeight(h)
        self.setMaximumHeight(h)

    def update(self):
        self.update_height()
        super().update()

    def _count_visible_item(self):
        count = 0
        index = self.model().index(0, 0)
        while index.isValid():
            count += 1
            index = self.indexBelow(index)
        return count

    def item_changed(self, item):
        item.update()

    def contextMenuEvent(self, event: QContextMenuEvent):
        item = self.itemAt(event.pos())
        item.contextMenuEvent(event)


class QBondControl(QTabControl):
    def __init__(self, parent, scene, bond):
        super().__init__(parent, scene)
        self.bond = bond

        content = QWidget()
        layout = QVBoxLayout(content)

        self.list_widget_label = QLabel("Bonds Definition")
        layout.addWidget(self.list_widget_label)

        self.list_widget = QBondListWidget(self, scene, bond)
        layout.addWidget(self.list_widget)

        layout.addStretch(255)

        self.setWidget(content)
