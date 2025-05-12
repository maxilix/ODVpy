from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QDropEvent
from PyQt6.QtWidgets import QTreeWidgetItem, QAbstractItemView, QTreeWidget

from qt.common.utils import bounding_rect_of, same_type
from qt.control.generic_inspector import Inspector


class QGenericTreeItem(QTreeWidgetItem):
    inspector_type = Inspector
    draggable = False

    def __init__(self, section_control, odv_object):
        super().__init__()
        self.section_control = section_control
        self._odv_object = odv_object
        self._graphics = []

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

        if len(self._graphics) > 0:
            self.setFlags(self.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            self.setCheckState(0, self.graphics_visibility_state())
        else:
            self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
            title = "      " + title
        self.setText(0, title)

    def clicked(self):
        if Qt.ItemFlag.ItemIsUserCheckable in self.flags() and self.graphics_visibility_state() != self.checkState(0):
            # current state is obsolete, checkbox has changed
            if self.checkState(0) == Qt.CheckState.Checked:
                self.show_graphics()
            else:
                self.hide_graphics()
            self.section_control.update_current_inspector()

    def double_clicked(self):
        self.localise_graphics()

    @property
    def name(self):
        return self._odv_object.name

    # @property
    # def scene(self):
    #     return self.section_control.scene

    def add_graphic(self, graphic_item):
        self._graphics.append(graphic_item)
        self.section_control.scene.addItem(graphic_item)

    def remove_graphic(self, graphic_item):
        self._graphics.remove(graphic_item)
        self.section_control.scene.removeItem(graphic_item)

    def graphics_visibility_state(self):
        l = [g.isVisible() for g in self._graphics]
        if all(l):
            return Qt.CheckState.Checked
        elif any(l):
            return Qt.CheckState.PartiallyChecked
        else:
            return Qt.CheckState.Unchecked

    def show_graphics(self):
        for g in self._graphics:
            g.setVisible(True)
        self.setCheckState(0, Qt.CheckState.Checked)

    def hide_graphics(self):
        for g in self._graphics:
            g.setVisible(False)
        self.setCheckState(0, Qt.CheckState.Unchecked)

    def localise_graphics(self):
        if self._graphics:
            self.show_graphics()
            rect = bounding_rect_of(self._graphics)
            self.section_control.scene.move_to_rect(rect)
            self.section_control.update_current_inspector()

    def focus(self):
        self.treeWidget().clearSelection()
        parent = self.parent()
        while parent:
            parent.setExpanded(True)
            parent = parent.parent()
        self.setSelected(True)
        self.treeWidget().scrollToItem(self)
        self.section_control.control.setCurrentWidget(self.section_control)



class QGenericTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setStyleSheet("""QTreeWidget:disabled{ background-color: #b0b0b0; }""")

        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setExpandsOnDoubleClick(False)
        self.itemClicked.connect(self.item_clicked)
        self.itemDoubleClicked.connect(self.item_double_clicked)

        # self.setDragEnabled(True)
        # self.setAcceptDrops(True)
        # self.setDropIndicatorShown(True)
        # self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.dragging_items = []

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
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging_items = self.selectedItems()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.dragging_items = []
        super().mouseReleaseEvent(event)

    @staticmethod
    def item_clicked(item, column):
        if column == 0:
            item.clicked()

    @staticmethod
    def item_double_clicked(item, column):
        if column == 0:
            item.double_clicked()

    # def contextMenuEvent(self, event: QContextMenuEvent):
    #     item = self.itemAt(event.pos())
    #     if item is not None:
    #         item.contextMenuEvent(event)

    def dropEvent(self, event: QDropEvent):
        assert len(self.dragging_items) > 0 and same_type(self.dragging_items)
        dragging_type = type(self.dragging_items[0])
        dragging_parent_type = type(self.dragging_items[0].parent())
        target_item = self.itemAt(event.position().toPoint())
        indicator = self.dropIndicatorPosition()

        # print(self.dragging_item.parent().text(0))
        #
        # if ((indicator == QAbstractItemView.DropIndicatorPosition.OnItem
        #     and type(target_item) == type(self.dragging_item.parent()))
        #     or ((indicator == QAbstractItemView.DropIndicatorPosition.AboveItem or indicator == QAbstractItemView.DropIndicatorPosition.BelowItem)
        #     and type(target_item) == type(self.dragging_item))):
        #     super().dropEvent(event)
        # else:
        #     event.ignore()
        #
        # print(self.dragging_item.parent().text(0))
        # print(self.dragging_item.setSelected(True))


        # print(self.dragging_item.parent())
        # print(target_item, indicator)

        # event.accept()

        # TODO implement move mechanic here
        # print(event.dropAction())
        # event.ignore()
        # item_to_drop_in = self.itemAt(event.position().toPoint())
        # if self.dropIndicatorPosition() == QAbstractItemView.DropIndicatorPosition.OnItem:

    def startDrag(self, supportedActions: Qt.DropAction):

        if len(self.dragging_items) > 0 and same_type(self.dragging_items) and self.dragging_items[0].draggable:
            super().startDrag(supportedActions)
        # self.dragging_item = None
