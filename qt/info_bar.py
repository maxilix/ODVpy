
from math import floor

from PyQt6.QtWidgets import QLabel


class QInfoBar(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._x = 0
        self._y = 0
        self._zoom = 1
        self.refresh()

    def set_widget(self, **kwargs):
        if "x" in kwargs:
            self._x = kwargs["x"]
        if "y" in kwargs:
            self._y = kwargs["y"]
        if "zoom" in kwargs:
            self._zoom = kwargs["zoom"]
        self.refresh()

    def refresh(self):
        self.setText(f"x:{floor(self._x)}\ty:{floor(self._y)}\tzoom:{round(self._zoom*100)}%")

