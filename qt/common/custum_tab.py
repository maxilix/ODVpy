from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QTabBar, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QFont, QColor
import sys


class HorizontalTextTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        # super().paintEvent(event)

        for index in range(self.count()):
            rect = self.tabRect(index)
            text = self.tabText(index)
            painter.save()

            # Positionner le texte à l'horizontale
            painter.translate(rect.center())  # Déplacer à la position du centre de l'onglet
            painter.rotate(0)  # Pas de rotation, texte horizontal
            painter.translate(-rect.center())  # Retourner à la position initiale

            font = QFont("Arial", 12, QFont.Weight.Normal)
            painter.setFont(font)
            painter.setPen(QColor(0, 0, 0))  # Couleur du texte

            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)

            painter.restore()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Onglets à gauche avec texte horizontal")

        tab_widget = QTabWidget()

        # Utiliser notre sous-classe de QTabBar
        tab_widget.setTabBar(HorizontalTextTabBar())
        tab_widget.setTabPosition(QTabWidget.TabPosition.West)

        tab_widget.addTab(QLabel("Contenu de l'onglet 1"), "Onglet 1")
        tab_widget.addTab(QLabel("Contenu de l'onglet 2"), "Onglet 2")
        tab_widget.addTab(QLabel("Contenu de l'onglet 3"), "Onglet 3")

        layout = QVBoxLayout()
        layout.addWidget(tab_widget)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())
