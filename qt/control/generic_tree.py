from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QDropEvent
from PyQt6.QtWidgets import QTreeWidgetItem, QAbstractItemView, QTreeWidget

from qt.control.generic_inspector import Inspector


class QGenericTreeItem(QTreeWidgetItem):
    inspector_type = Inspector

    def __init__(self, odv_object):
        super().__init__()
        self.odv_object = odv_object
        self.sub_inspector_list = []
        # self.current_state = None

    def setBold(self, value):
        f = self.font(0)
        f.setBold(value)
        self.setFont(0, f)

    def setColor(self, color = QColor('black')):
        self.setForeground(0, color)

    def update(self):
        self.setBold(False)
        self.setColor()
        title = self.name
        # if any(self.inspector_edit_state_list()):
        #     title += " -Edit-"
        #     self.setBold(True)
        # if self.inspector.valid_state is False:
        #     title += " -INVALID-"
        #     self.setBold(True)
        #     self.setColor(QColor('red'))

        # if len((vl:=[v.isChecked() for v in self.inspector_visibility_checkbox_list()]))>0:
        #     self.setFlags(self.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        #     if all(vl):
        #         self.current_state = Qt.CheckState.Checked
        #     elif any(vl):
        #         self.current_state = Qt.CheckState.PartiallyChecked
        #     else:
        #         self.current_state = Qt.CheckState.Unchecked
        #     self.setCheckState(0, self.current_state)
        # else:
        #     self.current_state = None
        #     title = "      " + title
        #     self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
        #     self.current_state = Qt.CheckState.Unchecked
        self.setText(0, title)


    # def clicked(self):
    #     if self.current_state != self.checkState(0):
    #         # current state is obsolete, checkbox has changed
    #         # current state will be updated by the global update
    #         for checkbox in self.inspector_visibility_checkbox_list():
    #             checkbox.setCheckState(self.checkState(0))
    #         self.global_update()

    @property
    def name(self):
        return self.odv_object.name



class QGenericTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setExpandsOnDoubleClick(False)
        self.itemClicked.connect(self.item_clicked)
        self.itemDoubleClicked.connect(self.item_double_clicked)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        # self.dragging_item = None

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

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        # self.dragging_item = item
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.dragging_item = None
        super().mouseReleaseEvent(event)

    @staticmethod
    def item_clicked(item, column):
        if column == 0:
            print("clicked")
            # item.clicked()

    @staticmethod
    def item_double_clicked(item, column):
        if column == 0:
            print("double clicked")

    # def contextMenuEvent(self, event: QContextMenuEvent):
    #     item = self.itemAt(event.pos())
    #     if item is not None:
    #         item.contextMenuEvent(event)

    def dropEvent(self, event: QDropEvent):
        # TODO implement move mechanic here
        super().dropEvent(event)
        # item_to_drop_in = self.itemAt(event.position().toPoint())
        # if self.dropIndicatorPosition() == QAbstractItemView.DropIndicatorPosition.OnItem:

    def startDrag(self, supportedActions: Qt.DropAction):
        # if self.dragging_item.draggable is True:
        super().startDrag(supportedActions)
        # self.dragging_item = None

