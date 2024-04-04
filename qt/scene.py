from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene

from .sub_scene import MoveScene


class QViewport(QGraphicsView):

    def __init__(self, scene):
        super().__init__(scene)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMouseTracking(True)

        self.max_zoom = 35
        self.min_zoom = 0.5
        self.zoom = 1
        self.zoom_factor = 1.2


class QScene(QGraphicsScene):
    def __init__(self, parent, info_bar, level):
        super().__init__(parent)
        self.info_bar = info_bar
        self.control = None
        self.viewport = QViewport(self)

        pixmap = QPixmap(level.dvm.level_map)
        self.map = self.addPixmap(pixmap)

        self.move_scene = MoveScene(self, level.dvd.move)

    def mouseMoveEvent(self, event):
        pos = event.scenePos()
        self.info_bar.update(x=pos.x(), y=pos.y())

        self.move_scene.refresh(pos)

    def wheelEvent(self, event):
        event.accept()

        if event.delta() > 0 and self.viewport.zoom < self.viewport.max_zoom:
            self.viewport.scale(self.viewport.zoom_factor, self.viewport.zoom_factor)
            self.viewport.zoom *= self.viewport.zoom_factor
        elif event.delta() < 0 and self.viewport.zoom > self.viewport.min_zoom:
            self.viewport.scale(1.0 / self.viewport.zoom_factor, 1.0 / self.viewport.zoom_factor)
            self.viewport.zoom /= self.viewport.zoom_factor
        else:
            pass

        scene_position = event.scenePos()
        global_position = event.screenPos()
        relative_position = self.viewport.mapFromGlobal(global_position)
        size = self.viewport.size()
        new_position = QPointF(scene_position.x() + (size.width() /2-relative_position.x()) / (1.1 * self.viewport.zoom),
                               scene_position.y() + (size.height()/2-relative_position.y()) / (1.1 * self.viewport.zoom))
        self.viewport.centerOn(new_position)
        self.info_bar.update(zoom=self.viewport.zoom)

    def set_control_pointer(self, control):
        self.control = control
