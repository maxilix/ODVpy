
from math import floor

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QLabel


class QInfoBar(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._x = 0
        self._y = 0
        self._zoom = 1
        self._level_index = -1
        self._level_size = QSize(0, 0)
        self.refresh()

    def set_widget(self, **kwargs):
        if "x" in kwargs:
            self._x = kwargs["x"]
        if "y" in kwargs:
            self._y = kwargs["y"]
        if "zoom" in kwargs:
            self._zoom = kwargs["zoom"]
        if "level_index" in kwargs:
            self._level_index = kwargs["level_index"]
        if "level_size" in kwargs:
            self._level_size = kwargs["level_size"]
        self.refresh()

    def refresh(self):
        self.setText(f"x:{floor(self._x)}\t"
                     f"y:{floor(self._y)}\t"
                     f"zoom:{round(self._zoom*100)}%\t"
                     f"level:{self._level_index:02}\t"
                     f"size:{self._level_size.width()}x{self._level_size.height()}")

