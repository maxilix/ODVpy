
import sys
import re
from math import floor, ceil

from PyQt6.QtCore import Qt, QSize, QPoint, QLineF, QRectF, QPointF
from PyQt6.QtGui import QImage, QPixmap, QPolygonF, QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, \
    QGraphicsLineItem, QVBoxLayout, QHBoxLayout, QLabel, QToolBar, QSplitter, QFileDialog, QMessageBox
from PyQt6.QtGui import QPen, QBrush, QColor

from qt.viewer import QViewer
from qt.control import QControl

from settings import original_level_filename
from debug import *

from common import *
from dvd import DvdParser
from dvm import DvmParser


class ODVLevel(object):
    def __init__(self, filename):
        self.dvd = None
        self.dvm = None
        # self._fully_loaded = False

        self.load_dvd(filename)
        if self.dvd is not None:
            self.load_dvm(filename)

    def load_dvd(self, filename):
        filename += ".dvd"
        try:
            self.dvd = DvdParser(filename)
        except FileNotFoundError:
            message_box = QMessageBox()
            message_box.setText(f"Unable to open {filename}")
            message_box.exec()
            self.dvd = None

    def load_dvm(self, filename):
        filename += ".dvm"
        try:
            self.dvm = DvmParser(filename)
        except FileNotFoundError:
            m = re.findall(r"level_(\d\d)", filename)
            guess_level_index = int(m[-1])
            message_box = QMessageBox()
            message_box.setText(f"Unable to open {filename}")
            message_box.setInformativeText(f"Do you want to load the original level {guess_level_index} dvm file instead?")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            message_box.setDefaultButton(QMessageBox.StandardButton.Ok)
            response = message_box.exec()
            if response == QMessageBox.StandardButton.Ok:
                self.load_dvm(original_level_filename(guess_level_index))
            else:
                self.dvm = None

    def __bool__(self):
        return self.dvd is not None and self.dvm is not None


class QWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Open Death Valley py')
        # self.setMinimumSize(QSize(800, 600))
        self.showMaximized()
        # self.setGeometry(0, 0, 500, 500)
        self.current_level = None
        # self.current_level = ODVLevel(original_level_filename(0))

        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        open_original_submenu = file_menu.addMenu("Open Original Level")

        for i in range (26):
            if i == 0:
                open_original_level_action = QAction(f"Demo level", self)
            else:
                open_original_level_action = QAction(f"Level {i}", self)
            open_original_level_action.triggered.connect(lambda state, index=i: self.load_level(original_level_filename(index)))
            open_original_submenu.addAction(open_original_level_action)

        open_custom_level_action = QAction(f"Open Custom level", self)
        open_custom_level_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_custom_level_action)

        close_level_action = QAction("Close level", self)
        close_level_action.triggered.connect(self.unload_level)
        file_menu.addAction(close_level_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(exit)
        file_menu.addAction(quit_action)

        self.set_widget()

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        # dialog.setDirectory(r'C:\images')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        filters = ["Any Level file (*.dvd *.dvm *.scb *.stf)",
                   "DVD file (*.dvd)",
                   "DVM file (*.dvm)",
                   "SCB file (*.scb)",
                   "STF file (*.stf)",
                   "Any file (*)"]
        dialog.setNameFilters(filters)
        # dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if len(filenames) == 1:
                filename = filenames[0].rsplit(".",1)[0]
                self.load_level(filename)

    def load_level(self, filename):
        self.current_level = ODVLevel(filename)
        if self.current_level:
            self.set_widget()
        else:
            self.current_level = None

    def unload_level(self):
        self.current_level = None
        self.set_widget()

    def set_widget(self):
        # layout = QHBoxLayout()
        if self.current_level is None:
            main_widget = QLabel("Select level")
            main_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # layout.addWidget(q_label)
        else:
            main_widget = QSplitter(self)
            viewer = QViewer(self.current_level)
            control = QControl(viewer.scene, self.current_level)
            viewer.scene.set_control_pointer(control)

            main_widget.addWidget(viewer)
            main_widget.addWidget(control)
            main_widget.setChildrenCollapsible(False)

        # w = QWidget()
        # w.setLayout(layout)
        self.setCentralWidget(main_widget)


if __name__ == '__main__':
    app = QApplication([])
    window = QWindow()
    window.show()
    app.exec()
