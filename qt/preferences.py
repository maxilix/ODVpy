from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QFileDialog

from config import Config
from odv.common import *
from odv.level import InstalledLevel
from qt.common.simple_messagebox import QErrorBox, QInfoBox


class QPreferencesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Preferences')
        self.setMinimumSize(1000, 400)
        # self.setGeometry(50, 30, 1000, 400)

        # self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("QDialog {border: 1px solid gray;}")

        main_layout = QVBoxLayout(self)

        # installation path
        installation_path_widget = QWidget()
        installation_path_layout = QHBoxLayout(installation_path_widget)
        label = QLabel(f'Installation path : ')
        installation_path_layout.addWidget(label)
        self.installation_path_label = QLineEdit()
        self.installation_path_label.setText(str(Config.installation_path))
        self.installation_path_label.setReadOnly(True)
        installation_path_layout.addWidget(self.installation_path_label)
        change_button = QPushButton('Change')
        installation_path_layout.addWidget(change_button)
        change_button.clicked.connect(self.change_installation_path)
        check_button = QPushButton('Check')
        installation_path_layout.addWidget(check_button)
        check_button.clicked.connect(self.check_installation_path)

        # close buttons
        close_buttons_widget = QWidget()
        close_buttons_layout = QHBoxLayout(close_buttons_widget)
        close_buttons_layout.addStretch()
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(lambda x: self.close(save=False))
        close_buttons_layout.addWidget(cancel_button)
        save_button = QPushButton('Save')
        save_button.clicked.connect(lambda x: self.close(save=True))
        close_buttons_layout.addWidget(save_button)

        main_layout.addWidget(installation_path_widget)
        main_layout.addStretch()
        main_layout.addWidget(close_buttons_widget)

    def change_installation_path(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)

        if dialog.exec():
            dirname = dialog.selectedFiles()
            if len(dirname) == 1:
                Config.installation_path = Path(dirname[0])
                self.installation_path_label.setText(str(Config.installation_path))

    def check_installation_path(self):
        if self.installation_path_label.text() == "":
            return False
        for index in range(26):
            try:
                level = InstalledLevel(index)
                if level.is_original() is False:
                    raise InvalidHashError(f"Invalid hash for level {index}.")
            except (InvalidHashError, FileNotFoundError) as e:
                # Config.installation_path = ""
                # self.installation_path_label.setText(Config.installation_path)
                QErrorBox(e).exec()
                return False
        QInfoBox("Check Completed").exec()
        return True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            event.accept()
            self.close(save=False)

    def close(self, save=False):
        if save is True:
            Config.save()
        else:
            Config.load()
        super().close()

