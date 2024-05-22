from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QPropertyAnimation, QPoint, QSize


from PyQt6.QtCore import QAbstractAnimation, QVariant, QVariantAnimation, pyqtSlot
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class SampleWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout.setSpacing(0)

        self.button = QPushButton(self)
        self.button.setText("Start animation")
        self.button.clicked.connect(lambda: self.start_animation(180))
        horizontal_layout.addWidget(self.button)

        self.setLayout(horizontal_layout)

    def start_animation(self, value: int) -> None:
        self._animation = QVariantAnimation(self)
        self._animation.setStartValue(0)
        self._animation.setEndValue(value)
        self._animation.setDuration(400)
        self._animation.valueChanged.connect(self._on_animation_value_changed)
        self._animation.finished.connect(self._on_animation_finished)
        self._animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    @pyqtSlot()
    def _on_animation_finished(self) -> None:
        print("Animation finished")

    @pyqtSlot(QVariant)
    def _on_animation_value_changed(self, value: int) -> None:
        print("Animation value changed to", value)


if __name__ == "__main__":
    a = QApplication([])
    buttonAnimWidget = SampleWidget(None)
    buttonAnimWidget.resize(QSize(800, 600))
    buttonAnimWidget.show()
    a.exec()
