from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene

from .abstract_view import View
from .move import QViewMotion


class QViewport(QGraphicsView):

    def __init__(self, scene):
        super().__init__(scene)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMouseTracking(True)

        self.max_zoom = 35
        self.min_zoom = 0.5
        self.zoom = 1
        self.zoom_factor = 1.2
        self.drag_position = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.setCursor(Qt.CursorShape.DragMoveCursor)
            self.drag_position = event.pos()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton and self.drag_position is not None:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.drag_position = None
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.drag_position is not None:
            delta = self.drag_position - event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + delta.y())
            self.drag_position = event.pos()
        super().mouseMoveEvent(event)


class QMainView(View, QGraphicsScene):
    def __init__(self, control, info_bar):
        super().__init__(control)
        self.info_bar = info_bar
        self.viewport = QViewport(self)
        pixmap = QPixmap(self.control.level.dvm.level_map)
        self.map = self.addPixmap(pixmap)

        self.view_motion = QViewMotion(self, self.control.control_motion)

    def mouseMoveEvent(self, event):
        pos = event.scenePos()
        self.info_bar.set_widget(x=pos.x(), y=pos.y())

        self.view_motion.refresh(pos)

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
        self.info_bar.set_widget(zoom=self.viewport.zoom)
