import shutil

from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QFileDialog, \
    QMessageBox

from settings import *
from backup import check_installation, InvalidHashError


class QPreferencesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Preferences')
        self.setMinimumSize(1000, 400)
        self.setStyleSheet("QDialog {border: 1px solid gray;}")

        main_layout = QVBoxLayout(self)

        # installation path
        installation_path_widget = QWidget()
        installation_path_layout = QHBoxLayout(installation_path_widget)
        label = QLabel(f'Installation path : ')
        installation_path_layout.addWidget(label)
        line_edit = QLineEdit()
        line_edit.setText(CONFIG.installation_path)
        line_edit.setReadOnly(True)
        installation_path_layout.addWidget(line_edit)
        change_button = QPushButton('Change')
        installation_path_layout.addWidget(change_button)
        change_button.clicked.connect(lambda x: self.change_installation_path(line_edit))
        check_button = QPushButton('Check')
        installation_path_layout.addWidget(check_button)
        check_button.clicked.connect(lambda x: self.check_installation_path(line_edit))

        # backup original files
        backup_widget = QWidget()
        backup_layout = QHBoxLayout(backup_widget)
        label = QLabel(f'Manage original data files')
        backup_layout.addWidget(label)
        backup_layout.addStretch()
        restore_button = QPushButton('Restore')
        backup_layout.addWidget(restore_button)
        restore_button.clicked.connect(self.restore_original_files)
        backup_button = QPushButton('Backup')
        backup_layout.addWidget(backup_button)
        backup_button.clicked.connect(self.backup_original_files)

        # close buttons
        close_buttons_widget = QWidget()
        close_buttons_layout = QHBoxLayout(close_buttons_widget)
        close_buttons_layout.addStretch()
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(lambda x: self.save_and_close(save=False))
        close_buttons_layout.addWidget(cancel_button)
        save_button = QPushButton('Save')
        save_button.clicked.connect(lambda x: self.save_and_close(save=True))
        close_buttons_layout.addWidget(save_button)

        main_layout.addWidget(installation_path_widget)
        main_layout.addWidget(backup_widget)
        main_layout.addStretch()
        main_layout.addWidget(close_buttons_widget)

    def change_installation_path(self, line_edit):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)

        if dialog.exec():
            dirname = dialog.selectedFiles()
            if len(dirname) == 1:
                CONFIG.installation_path = dirname[0]
                line_edit.setText(CONFIG.installation_path)

    def check_installation_path(self, line_edit):
        try:
            check_installation(CONFIG.installation_path)
        except (InvalidHashError, FileNotFoundError) as e:
            message_box = QMessageBox()
            message_box.setText(f"{e}")
            CONFIG.installation_path = ""
            line_edit.setText(CONFIG.installation_path)
            message_box.exec()
            return False
        message_box = QMessageBox()
        message_box.setText(f"Check Completed")
        message_box.exec()
        return True

    def backup_original_files(self):
        try:
            check_installation(CONFIG.installation_path)
        except (InvalidHashError, FileNotFoundError) as e:
            message_box = QMessageBox()
            message_box.setText(f"{e}")
            message_box.exec()

        for filename in ORIGINAL_HASH:
            source_filename = os.path.join(CONFIG.installation_path, filename)
            destination_filename = os.path.join("backup", filename)
            os.makedirs(os.path.dirname(destination_filename), exist_ok=True)
            shutil.copy2(source_filename, destination_filename)
        message_box = QMessageBox()
        message_box.setText(f"Backup Completed")
        message_box.exec()

    def restore_original_files(self):
        try:
            check_installation("backup")
        except (InvalidHashError, FileNotFoundError) as e:
            message_box = QMessageBox()
            message_box.setText(f"{e}")
            message_box.exec()

        for filename in ORIGINAL_HASH:
            source_filename = os.path.join("backup", filename)
            destination_filename = os.path.join(CONFIG.installation_path, filename)
            shutil.copy2(source_filename, destination_filename)
        message_box = QMessageBox()
        message_box.setText(f"Restore Completed")
        message_box.exec()




    def save_and_close(self, save):
        if save is True:
            CONFIG.save()
        else:
            CONFIG.load()
        self.close()
