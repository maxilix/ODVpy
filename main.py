from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, \
    QVBoxLayout, QHBoxLayout

from app_context import AppContext as AC
from odv.common import *
from config import Config
from game_data import *
from odv.level import Level, BackupedLevel, InstalledLevel
from qt.common.simple_messagebox import QErrorBox, QInfoBox
from qt.control.main_control import QControl
from qt.preferences import QPreferencesDialog
from qt.scene import QScene
from qt.scene_info_bar import QInfoBar
from qt.scene_tool_bar import QSceneToolBar
from qt.viewport import QViewport

# avoid recurrent warning like this
# qt.qpa.wayland.textinput: virtual void QtWaylandClient::QWaylandTextInputv3::zwp_text_input_v3_leave(wl_surface*) Got leave event for surface 0x0 with focusing surface 0x5611e36f3910
os.environ["QT_LOGGING_RULES"] = "qt.qpa.wayland.textinput=false"


class QWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('ODVpy Editor')
        self.showMaximized()
        self.setMinimumSize(1000, 800)
        self.status_bar = self.statusBar()

        menu = self.menuBar()
        # ============================== File menu ==============================
        file_menu = menu.addMenu("File")
        open_original_submenu = file_menu.addMenu("Open Original Level")

        for i in range(26):
            if i == 0:
                open_original_level_action = QAction(f"Demo level", self)
            else:
                open_original_level_action = QAction(f"Level {i}", self)
            open_original_level_action.triggered.connect(lambda state, index=i: self.open_original_level(index))
            open_original_level_action.setStatusTip(f'Open Mission {i} : {ORIGINAL_LEVEL_NAME[i]}')
            open_original_submenu.addAction(open_original_level_action)

        open_custom_level_action = QAction(f"Open Custom level", self)
        open_custom_level_action.triggered.connect(self.open_custom_level)
        file_menu.addAction(open_custom_level_action)

        close_level_action = QAction("Close level", self)
        close_level_action.triggered.connect(self.close_level)
        file_menu.addAction(close_level_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(app.quit)
        file_menu.addAction(quit_action)
        # =======================================================================

        # ============================== Edit menu ==============================
        edit_menu = menu.addMenu("Edit")
        open_preferences_dialog_action = QAction("Preferences", self)
        open_preferences_dialog_action.triggered.connect(self.open_preferences_dialog)
        edit_menu.addAction(open_preferences_dialog_action)
        # =======================================================================

        # ============================== Mod manager menu =======================
        mod_manager_menu = menu.addMenu("Mod")

        self.insert_current_level_action = QAction("Insert in game", self)
        # self.insert_current_level_action.triggered.connect(self.insert_current_level)
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
        # =======================================================================

        main_widget = QWidget(self)
        main_layout = QHBoxLayout(main_widget)

        # visualizer = QWidget(main_widget)
        visualizer_layout = QVBoxLayout()

        self.tool_bar = QSceneToolBar()
        self.scene = QScene()
        self.info_bar = QInfoBar()
        self.viewport = QViewport(self.scene, self.info_bar)

        visualizer_layout.addWidget(self.tool_bar)
        visualizer_layout.addWidget(self.viewport)
        visualizer_layout.addWidget(self.info_bar)

        main_layout.addLayout(visualizer_layout)

        self.control = QControl()
        self.control.sendStatus.connect(self.status_bar.showMessage)

        main_layout.addWidget(self.control)

        self.setCentralWidget(main_widget)

        AC.set_ui(scene=self.scene, tool_bar=self.tool_bar, control=self.control)

        AC.level = BackupedLevel(4)
        # AC.level = Level()

        self.status_bar.showMessage('Ready', 5000)


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

    # def insert_current_level(self):
    #     assert AC.level is not None
    #     AC.level.insert_in_game()

    def open_preferences_dialog(self):
        dialog = QPreferencesDialog(self)
        dialog.exec()

    def open_custom_level(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dialog.setDirectory(os.path.join(os.curdir,"dev","empty_level"))
        filters = ["Any Level file (*.dvd *.dvm *.scb *.stf)",
                   "DVD file (*.dvd)",
                   "DVM file (*.dvm)",
                   "SCB file (*.scb)",
                   "STF file (*.stf)",
                   "Any file (*)"]
        dialog.setNameFilters(filters)
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            filename_we = remove_extension(filename)
            AC.level = Level(filename_we)

    def open_original_level(self, index):
        AC.level = BackupedLevel(index)


    def close_level(self):
        AC.level = Level()

# def set_dark_mode(app):
#     dark_palette = QPalette()
#     dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
#     dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
#     dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
#     dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
#     dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
#     dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
#     dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
#     dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
#     dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
#     dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
#     dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(142, 45, 197))
#     dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
#
#     app.setPalette(dark_palette)
#     app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")


if __name__ == '__main__':
    Config.load()
    app = QApplication([])
    # print(QStyleFactory.keys())
    app.setStyle('Fusion')
    window = QWindow()
    window.show()
    app.exec()
    Config.save()
