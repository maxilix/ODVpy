from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QFileDialog

from settings import CONFIG


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
        change_button = QPushButton('Set')
        installation_path_layout.addWidget(change_button)
        change_button.clicked.connect(lambda x: self.change_installation_path(line_edit))

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


    def save_and_close(self, save):
        if save is True:
            CONFIG.save()
        else:
            CONFIG.load()
        self.close()
