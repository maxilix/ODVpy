from PyQt6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent


class QScene(QGraphicsScene):
    # def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
    #     print("lkjhf")


    # def __init__(self, parent):
    #     super().__init__(parent)
    #     self.

    def _main_viewport(self):
        return self.views()[0]

    def move_to_item(self, item):
        self._main_viewport().move_to_item(item)

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.MouseButton.RightButton:
    #         print("Scene BUTTON")


