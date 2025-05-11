from math import floor

from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout


class QInfoBar(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._x = 0
        self._y = 0
        self._zoom = 0

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.position_label = QLabel()
        main_layout.addWidget(self.position_label)

        main_layout.addStretch()

        self.tree_items_label = QLabel()
        main_layout.addWidget(self.tree_items_label)

    def set_xy(self,x,y):
        self._x = x
        self._y = y
        self.position_label.setText(f"({floor(self._x)} , {floor(self._y)})   {round(self._zoom*100)}%")

    def set_zoom(self,zoom):
        self._zoom = zoom
        self.position_label.setText(f"({floor(self._x)} , {floor(self._y)})   {round(self._zoom*100)}%")

    def set_tree_items(self, items):
        self.tree_items_label.setText(" - ".join([i.name for i in items]))
