import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush
from PyQt6.QtCore import Qt, QPointF
import math


class QPerspective(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 300)
        self.perspective = 0  # Initial angle (0 - 15, representing 16 positions)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw the clock face
        rect = self.rect().adjusted(10, 10, -10, -10)
        center = rect.center()
        radius = min(rect.width(), rect.height()) / 2

        # Draw the outer circle of the clock
        painter.setPen(QPen(QColor(0, 0, 0, 180), 3))
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawEllipse(rect)

        # Draw the inner circle (to make it look more like a standard clock)
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.drawEllipse(center, 5, 5)

        # Draw the hour marks
        num_marks = 16
        mark_length = radius * 0.1
        for i in range(num_marks):
            angle = 360.0 / num_marks * i
            x1 = center.x() + (radius - mark_length) * math.cos(math.radians(angle - 90))
            y1 = center.y() + (radius - mark_length) * math.sin(math.radians(angle - 90))
            x2 = center.x() + radius * math.cos(math.radians(angle - 90))
            y2 = center.y() + radius * math.sin(math.radians(angle - 90))
            painter.setPen(QPen(QColor(0, 0, 0, 150), 2))
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        # Draw the hand
        hand_length = radius * 0.7
        hand_angle = (360.0 / 16) * self.perspective
        hand_x = center.x() + hand_length * math.cos(math.radians(hand_angle - 90))
        hand_y = center.y() + hand_length * math.sin(math.radians(hand_angle - 90))
        painter.setPen(QPen(QColor(255, 0, 0), 3))
        painter.drawLine(center.toPointF(), QPointF(hand_x, hand_y))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.set_angle_from_position(event.pos())
            self.update()  # Repaint the widget

    def mouseMoveEvent(self, event):
        self.set_angle_from_position(event.pos())
        self.update()  # Repaint the widget

    def set_angle_from_position(self, pos):
        center = self.rect().center()
        dx = pos.x() - center.x()
        dy = pos.y() - center.y()
        angle = math.degrees(math.atan2(dy, dx))
        # angle = (angle + 90) % 360  # Convert to standard angle
        self.perspective = round((angle + 90) / (360.0 / 16)) % 16


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    window = QMainWindow()
    widget = QPerspective()
    window.setCentralWidget(widget)
    window.show()
    sys.exit(app.exec())
