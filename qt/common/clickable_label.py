from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel


class QClickableLabel(QLabel):
    clicked = pyqtSignal()
    double_clicked = pyqtSignal()

    def mousePressEvent(self, ev):
        self.clicked.emit()

    def mouseDoubleClickEvent(self, a0):
        self.double_clicked.emit()


