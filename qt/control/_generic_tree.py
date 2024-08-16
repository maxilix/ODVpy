from PyQt6.QtCore import Qt
from PyQt6.QtGui import QContextMenuEvent, QCursor
from PyQt6.QtWidgets import QAbstractItemView, QTreeWidget, QTreeWidgetItem, QMenu


class QODVTreeItem(QTreeWidgetItem):
    def __init__(self, tab_control, odv_object):
        super().__init__(None)
        self._tab_control = tab_control
        self.odv_object = odv_object
        # if self.odv_item.q_graphic_item is not None:
        #     if self.odv_item.visible:
        #         self.setCheckState(0, Qt.CheckState.Checked)
        #     else:
        #         self.setCheckState(0, Qt.CheckState.Unchecked)
        self.update()


    def setBold(self, value):
        f = self.font(0)
        f.setBold(value)
        self.setFont(0, f)

    def update(self):
        self.setText(0, self.odv_object.name)

    @property
    def inspector(self):
        return self._tab_control.inspectors[self.odv_object]



    # @property
    # def visible(self):
    #     if self.odv_item.q_graphic_item is not None:
    #         return self.checkState(0) == Qt.CheckState.Checked
    #     else:
    #         return False
    #
    # @visible.setter
    # def visible(self, state):
    #     if self.odv_item.q_graphic_item is not None:
    #         if state:
    #             self.setCheckState(0, Qt.CheckState.Checked)
    #         else:
    #             self.setCheckState(0, Qt.CheckState.Unchecked)

    # def contextMenuEvent(self, event):
    #     menu = QMenu()
    #     menu.addAction(self.odv_item.a_localise)
    #     menu.addActions(self.odv_item.scene_menu_common_actions())
    #     menu.exec(QCursor.pos())


class QGenericTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # self.itemClicked.connect(self.tree_item_clicked)

    # def addChild(self, child):
    #     self.addTopLevelItem(child)

    # def update_height(self):
    #
    #     h = 18 * self.count() + 2
    #     self.setMinimumHeight(h)
    #     self.setMaximumHeight(h)

    # def count_visible_item(self):
    #     count = 0
    #     index = self.model().index(0, 0)
    #     while index.isValid():
    #         count += 1
    #         index = self.indexBelow(index)
    #     return count

    # @staticmethod
    # def tree_item_clicked(tree_item, column):
    #     if column == 0:
    #         tree_item.odv_item.visible = tree_item.visible
    #
    # def contextMenuEvent(self, event: QContextMenuEvent):
    #     item = self.itemAt(event.pos())
    #     item.contextMenuEvent(event)
