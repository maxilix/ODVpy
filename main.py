from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QSplitter, QFileDialog, QPushButton

from odv.level import Level, BackupedLevel, InstalledLevel
from qt.common.simple_messagebox import QErrorBox, QInfoBox
from qt.preferences import QPreferencesDialog
from qt.viewer import QViewer
from qt.controller.main_controller import QMainControl

from config import CONFIG
from common import *

# from debug import *


class QWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Open Death Valley py')
        self.showMaximized()
        # self.setMinimumSize(800, 600)
        # self.setGeometry(0, 0, 500, 500)

        self.current_level = None
        # self.current_level = Level("./dev/empty_level/empty_level_19")
        # self.current_level = InstalledLevel(19)

        menu = self.menuBar()
        # ============================== File menu ==============================
        file_menu = menu.addMenu("File")
        open_original_submenu = file_menu.addMenu("Open Original Level")

        for i in range(26):
            if i == 0:
                open_original_level_action = QAction(f"Demo level", self)
            else:
                open_original_level_action = QAction(f"Level {i}", self)
            open_original_level_action.triggered.connect(lambda state, index=i: self.load_original_level(index))
            open_original_submenu.addAction(open_original_level_action)

        open_custom_level_action = QAction(f"Open Custom level", self)
        open_custom_level_action.triggered.connect(self.load_custom_level)
        file_menu.addAction(open_custom_level_action)

        close_level_action = QAction("Close level", self)
        close_level_action.triggered.connect(self.unload_level)
        file_menu.addAction(close_level_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(exit)
        file_menu.addAction(quit_action)
        # ============================== File menu ==============================

        # ============================== Edit menu ==============================
        edit_menu = menu.addMenu("Edit")
        open_preferences_dialog_action = QAction("Preferences", self)
        open_preferences_dialog_action.triggered.connect(self.open_preferences_dialog)
        edit_menu.addAction(open_preferences_dialog_action)
        # ============================== Edit menu ==============================

        # ============================== Mod manager menu =======================
        mod_manager_menu = menu.addMenu("Mod")

        self.insert_current_level_action = QAction("Insert in game", self)
        self.insert_current_level_action.triggered.connect(self.insert_current_level)
        mod_manager_menu.addAction(self.insert_current_level_action)

        backup_submenu = mod_manager_menu.addMenu("Backup")
        backup_all_action = QAction("Backup all", self)
        backup_all_action.triggered.connect(lambda state: self.backup_level(range(26)))
        backup_submenu.addAction(backup_all_action)
        backup_submenu.addSeparator()
        for i in range(26):
            if i == 0:
                backup_action = QAction(f"Demo level", self)
            else:
                backup_action = QAction(f"Level {i}", self)
            backup_action.triggered.connect(lambda state, index=i: self.backup_level([index]))
            backup_submenu.addAction(backup_action)

        restore_submenu = mod_manager_menu.addMenu("Restore")
        restore_all_action = QAction("Restore all", self)
        restore_all_action.triggered.connect(lambda state: self.restore_level(range(26)))
        restore_submenu.addAction(restore_all_action)
        restore_submenu.addSeparator()
        for i in range(26):
            if i == 0:
                restore_action = QAction(f"Demo level", self)
            else:
                restore_action = QAction(f"Level {i}", self)
            restore_action.triggered.connect(lambda state, index=i: self.restore_level([index]))
            restore_submenu.addAction(restore_action)
        # ============================== Mod manager menu =======================

        self.setStyleSheet("""
            QMenu::item:!enabled {
                color: gray;
            }
        """)
        self.set_widget()

    @staticmethod
    def backup_level(selected):
        for index in selected:
            try:
                level = InstalledLevel(index)
                level.backup()
            except (InvalidHashError, FileNotFoundError) as e:
                QErrorBox(e).exec()

        if len(selected) > 1:
            QInfoBox("Backup Completed").exec()

    @staticmethod
    def restore_level(selected):
        for index in selected:
            try:
                level = BackupedLevel(index)
                level.restore()
            except (InvalidHashError, FileNotFoundError) as e:
                QErrorBox(e).exec()

        if len(selected) > 1:
            QInfoBox("Restore Completed").exec()

    def insert_current_level(self):
        assert self.current_level is not None
        self.current_level.insert_in_game()

    def open_preferences_dialog(self):
        dialog = QPreferencesDialog(self)
        dialog.exec()

    def load_custom_level(self):
        dialog = QFileDialog(self)
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
                filename_we = remove_extension(filenames[0])
                self.current_level = Level(filename_we)
                self.set_widget()

    def load_original_level(self, index):
        self.current_level = BackupedLevel(index)
        self.set_widget()

    def unload_level(self):
        self.current_level = None
        self.set_widget()

    def set_widget(self):
        if self.current_level is None:
            self.insert_current_level_action.setEnabled(False)
            main_widget = QLabel("Select level")
            main_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.insert_current_level_action.setEnabled(True)
            main_widget = QSplitter(self)

            # bi-directional pointer:
            # main_control has pointer on main_view
            # main_view has pointer on main_control

            main_control = QMainControl(self.current_level)
            viewer = QViewer(self, main_control)
            main_control.add_view(viewer.main_view)

            viewer.info_bar.set_widget(level_index=self.current_level.index)

            main_widget.addWidget(viewer)
            main_widget.addWidget(main_control)
            main_widget.setChildrenCollapsible(False)

        self.setCentralWidget(main_widget)


if __name__ == '__main__':
    CONFIG.load()
    app = QApplication([])
    window = QWindow()
    window.show()
    app.exec()
