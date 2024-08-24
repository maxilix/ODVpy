from PyQt6.QtCore import Qt
from PyQt6.QtGui import QContextMenuEvent, QCursor, QColor, QAction
from PyQt6.QtWidgets import QAbstractItemView, QTreeWidget, QTreeWidgetItem, QMenu

class QODVTreeItem(QTreeWidgetItem):
    def __init__(self, tab_control, odv_object):
        super().__init__(None)
        self._tab_control = tab_control
        self.odv_object = odv_object
        self.current_state = None

    def setBold(self, value):
        f = self.font(0)
        f.setBold(value)
        self.setFont(0, f)

    def setColor(self, color = QColor('black')):
        self.setForeground(0, color)

    def global_update(self):
        self.inspector.update()

    def update(self):
        self.setBold(False)
        self.setColor()
        title = self.odv_object.name
        if any(self.inspector_edit_state_list()):
            title += " -Edit-"
            self.setBold(True)
        if self.inspector.valid_state is False:
            title += " -INVALID-"
            self.setBold(True)
            self.setColor(QColor('red'))

        if len((vl:=[v.isChecked() for v in self.inspector_visibility_checkbox_list()]))>0:
            self.setFlags(self.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            if all(vl):
                self.current_state = Qt.CheckState.Checked
            elif any(vl):
                self.current_state = Qt.CheckState.PartiallyChecked
            else:
                self.current_state = Qt.CheckState.Unchecked
            self.setCheckState(0, self.current_state)
        else:
            self.current_state = None
            # title = "      " + title
            # self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
            # self.current_state = Qt.CheckState.Unchecked
        self.setText(0, title)

    @property
    def inspector(self):
        return self._tab_control.inspectors[self.odv_object]

    def inspector_visibility_checkbox_list(self):
        rop = []
        for sub_inspector in self.inspector.sub_inspector_list:
            if hasattr(sub_inspector, "visibility_checkbox"):
                rop.append(sub_inspector.visibility_checkbox)
        return rop

    def inspector_edit_state_list(self):
        rop = []
        for sub_inspector in self.inspector.sub_inspector_list:
            if hasattr(sub_inspector, "edit"):
                rop.append(sub_inspector.edit)
        return rop

    def clicked(self):
        if self.current_state != self.checkState(0):
            # current state is obsolete, checkbox has changed
            # current state will be updated by the global update
            for checkbox in self.inspector_visibility_checkbox_list():
                checkbox.setCheckState(self.checkState(0))
            self.global_update()

    def contextMenuEvent(self, event):
        menu = QMenu()
        for e in self.inspector.tree_menu_common_actions():
            if isinstance(e, QAction):
                menu.addAction(e)
            else:
                submenu = menu.addMenu(e[0])
                submenu.addActions(e[1:])
        menu.exec(QCursor.pos())


class QGenericTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.itemClicked.connect(self.item_clicked)

        # self.setStyleSheet("""
        #     QTreeWidget::indicator[data="no_checkable"] {
        #         background-color: green;
        #         border: 1px solid darkgreen;
        #     }
        # """)
    # def update_height(self):
    #
    #     h = 18 * self.count() + 2
    #     self.setMinimumHeight(h)
    #     self.setMaximumHeight(h)
    #
    # def count_visible_item(self):
    #     count = 0
    #     index = self.model().index(0, 0)
    #     while index.isValid():
    #         count += 1
    #         index = self.indexBelow(index)
    #     return count

    @staticmethod
    def item_clicked(item, column):
        if column == 0:
            item.clicked()

    def contextMenuEvent(self, event: QContextMenuEvent):
        item = self.itemAt(event.pos())
        if item is not None:
            item.contextMenuEvent(event)
