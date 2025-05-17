import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QStyle, QToolButton, \
    QStyleFactory


class IconViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Standard icons of PyQt6")
        self.resize(400, 800)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container = QWidget()
        layout = QVBoxLayout(container)

        for attr in dir(QStyle.StandardPixmap):
            if attr.startswith("SP_"):
                try:
                    row = QHBoxLayout()
                    icon_button = QToolButton()
                    icon = self.style().standardIcon(getattr(QStyle.StandardPixmap, attr))
                    icon_button.setIcon(icon)
                    row.addWidget(icon_button)

                    row.addSpacing(30)

                    text_label = QLabel(attr)
                    text_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
                    row.addWidget(text_label)

                    row.addStretch()

                    layout.addLayout(row)
                except Exception as e:
                    print(f"Error with {attr}: {e}")

        scroll_area.setWidget(container)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print(QStyleFactory.keys())
    app.setStyle('Fusion')
    viewer = IconViewer()
    viewer.show()
    sys.exit(app.exec())
