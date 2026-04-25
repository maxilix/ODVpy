from PyQt6.QtWidgets import QMessageBox


class QInfoBox(QMessageBox):
    def __init__(self, info):
        super().__init__()
        # self.setWindowFlags(self.windowFlags() | Qt.WindowType.SubWindow)  # Deprecated Warning
        self.setStyleSheet("""
            QMessageBox {
                border: 2px solid black;
                border-radius: 3px;
                }
            """)
        self.setIcon(QMessageBox.Icon.Information)
        self.setText(f"{info}")
        self.setStandardButtons(QMessageBox.StandardButton.Ok)


class QErrorBox(QMessageBox):
    def __init__(self, error):
        super().__init__()
        # self.setWindowFlags(self.windowFlags() | Qt.WindowType.SubWindow)  # Deprecated Warning
        self.setStyleSheet("""
            QMessageBox {
                border: 2px solid black;
                border-radius: 3px;
                }
            """)
        self.setIcon(QMessageBox.Icon.Warning)
        self.setText(f"{error}")
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
