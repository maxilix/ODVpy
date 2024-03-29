
from PyQt6.QtCore import Qt, QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation, pyqtSlot
from PyQt6.QtWidgets import QWidget, QToolButton, QScrollArea, QSizePolicy, QVBoxLayout, QFrame


class QCollapsible(QWidget):
    def __init__(self, parent, title):
        super().__init__(parent)

        self.toggle_button = QToolButton()
        self.toggle_button.setText(title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.ArrowType.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QParallelAnimationGroup(self)

        self.content_area = QScrollArea()
        self.content_area.setMinimumHeight(0)
        self.content_area.setMaximumHeight(0)

        self.content_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.content_area.setFrameShape(QFrame.Shape.NoFrame)
        # self.content_area.setFrameShape(Qt.FramelessWindowHint) QFrame.NoFrame)

        lay = QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self.content_area, b"maximumHeight"))

    @pyqtSlot()
    def on_pressed(self):
        if self.toggle_button.isChecked():
            self.toggle_button.setArrowType(Qt.ArrowType.RightArrow)
            self.toggle_animation.setDirection(QAbstractAnimation.Direction.Backward)
        else:
            self.toggle_button.setArrowType(Qt.ArrowType.DownArrow)
            self.toggle_animation.setDirection(QAbstractAnimation.Direction.Forward)
        self.toggle_animation.start()

    def set_content_layout(self, layout:QVBoxLayout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = (self.sizeHint().height() - self.content_area.maximumHeight())
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(150)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(150)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)