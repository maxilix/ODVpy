from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeWidgetItem

from qt.control.widget_generic_tree import QGenericTreeItem
from qt.control.widget_inspector import QInspectorWidget


class QOdvObject(object):

    def __init__(self, odv_object):
        self.odv_object = odv_object
        self.inspectorWidget = QInspectorWidget(self)
        self.tree_item = QTreeWidgetItem()
