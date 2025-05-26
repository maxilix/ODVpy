from math import floor

from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout


class QInfoBar(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.position_label = QLabel()
        self.position_label.setFixedWidth(100)
        main_layout.addWidget(self.position_label)

        self.zoom_label = QLabel()
        self.zoom_label.setFixedWidth(80)
        main_layout.addWidget(self.zoom_label)

        main_layout.addStretch()

        self.tree_items_label = QLabel()
        main_layout.addWidget(self.tree_items_label)

    def set_xy(self, x, y = None):
        if x is None and y is None:
            self.position_label.setText(f"(   ,   )")
        else:
            self.position_label.setText(f"({floor(x)} , {floor(y)})")


    def set_zoom(self, zoom):
        self.zoom_label.setText(f"{round(zoom*100)}%")

    def set_tree_items(self, items):
        self.tree_items_label.setText(" - ".join([i.name for i in items]))
