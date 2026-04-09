from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QWidget


class SearchableMenu(QWidget):
    def __init__(self, actions, menu):
        super().__init__()

        self.menu = menu
        self.actions = actions

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        # Recherche
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search...")
        self.search.textChanged.connect(self.filter_items)
        self.search.setFocus()
        layout.addWidget(self.search)

        # Liste
        self.list_widget = QListWidget()
        self.list_widget.setMouseTracking(True)
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.list_widget.setSelectionBehavior(QListWidget.SelectionBehavior.SelectRows)
        self.list_widget.itemEntered.connect(self.on_item_hovered)
        self.list_widget.itemClicked.connect(self.trigger_action)
        layout.addWidget(self.list_widget)

        # Remplissage
        self.items = []
        for action in self.actions:
            item = QListWidgetItem(action.text())

            # Icône
            if not action.icon().isNull():
                item.setIcon(action.icon())

            # Stocker l'action
            item.setData(Qt.ItemDataRole.UserRole, action)

            # Respecter enabled/disabled
            item.setFlags(item.flags() if action.isEnabled() else Qt.ItemFlag.NoItemFlags)
            self.list_widget.addItem(item)
            self.items.append(item)
        # self.list_widget.sortItems(Qt.SortOrder.AscendingOrder)


    def on_item_hovered(self, item):
        self.list_widget.setCurrentItem(item)

    def filter_items(self, text):
        text = text.lower()
        for item in self.items:
            item.setHidden(text not in item.text().lower())

    def trigger_action(self, item):
        action = item.data(Qt.ItemDataRole.UserRole)
        if action and action.isEnabled():
            action.trigger()
        self.menu.close()