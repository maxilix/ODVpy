from PyQt6.QtCore import Qt, QPointF, QPropertyAnimation, pyqtProperty, QParallelAnimationGroup, QRectF, \
    QVariantAnimation, QSequentialAnimationGroup, QEasingCurve, QPoint, QSizeF, QRect, QSize, QEvent
from PyQt6.QtGui import QPixmap, QBrush, QPen, QMouseEvent
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsRectItem, QGraphicsSceneMouseEvent

from .abstract_view import View
from .motion import QViewMotion
from ..controller.motion import QGraphicsArea


class QViewport(QGraphicsView):

    def __init__(self, scene, dvm_size, info_bar, control):
        super().__init__(scene)
        self.dvm_size = dvm_size
        self.info_bar = info_bar
        self.control = control

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setMouseTracking(True)
        self.drag_position = None

        self.zoom_factor = 1.1
        self.zoom_shift_factor = 1.0
        self.zoom_max = 25
        self.zoom_min = 0.5

        self.setSceneRect(QRectF(-dvm_size.width()/2,
                                 -dvm_size.height()/2,
                                 2*self.dvm_size.width(),
                                 2*self.dvm_size.height()))

        # initial view position
        self.zoom = 0.7  # set zoom first, as it defines the margins around the dvm
        self.x = dvm_size.width() // 2
        self.y = dvm_size.height() // 2

        # self.zoom = 3.4
        # self.x = 700
        # self.y = 1700

    def mousePressEvent(self, event):
        mouse_scene_pos = self.mapToScene(event.pos())
        if event.button() == Qt.MouseButton.MiddleButton:
            self.setCursor(Qt.CursorShape.DragMoveCursor)
            self.drag_position = event.pos()
        # elif event.button() == Qt.MouseButton.LeftButton:
        #     # self.move_to(QRectF(334, 162, 100, 100))
        #     # self.move_to(649, 727)
        #     # self.zoom = 10
        #     pass
        # elif event.button() == Qt.MouseButton.RightButton:
        #     # self.move_to(QRectF(100, 300, 50, 50))
        #     self.move_to(100, 100)
        #     # self.zoom = 1
        #     pass
        # self.control.mousse_event(mouse_scene_pos, event)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        mouse_scene_pos = self.mapToScene(event.pos())
        if event.button() == Qt.MouseButton.MiddleButton and self.drag_position is not None:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.drag_position = None
        # self.control.mousse_event(mouse_scene_pos, event)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        mouse_scene_pos = self.mapToScene(event.pos())
        self.info_bar.set_info(x=mouse_scene_pos.x(), y=mouse_scene_pos.y())
        if self.drag_position is not None:
            delta = self.drag_position - event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + delta.y())
            self.drag_position = event.pos()

        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event):
        event.ignore()
        super().mouseDoubleClickEvent(event)

    def leaveEvent(self, event: QEvent):
        super().leaveEvent(event)
        # self.control.mousse_event(None, event)

    def wheelEvent(self, event):
        mouse_view_pos = event.position().toPoint()
        mouse_scene_pos = self.mapToScene(mouse_view_pos)

        delta = event.angleDelta().y()
        if delta > 0 and self.zoom < self.zoom_max:
            self.zoom *= self.zoom_factor
        elif delta < 0 and self.zoom > self.zoom_min:
            self.zoom /= self.zoom_factor
        else:
            pass

        h = self.horizontalScrollBar()
        v = self.verticalScrollBar()
        self.x = mouse_scene_pos.x() + (h.pageStep()/2 - mouse_view_pos.x()) / (self.zoom_shift_factor * self.zoom)
        self.y = mouse_scene_pos.y() + (v.pageStep()/2 - mouse_view_pos.y()) / (self.zoom_shift_factor * self.zoom)

        # self.control.mousse_event(mouse_scene_pos, event)
        event.ignore()

    @pyqtProperty(float)
    def zoom(self):
        v = self.verticalScrollBar()
        vertical_zoom = (v.maximum() - v.minimum() + v.pageStep()) / self.sceneRect().height()
        return vertical_zoom

    @zoom.setter
    def zoom(self, new_zoom):
        current_zoom = self.zoom
        self.scale(new_zoom/current_zoom, new_zoom/current_zoom)
        x_margin = self.horizontalScrollBar().pageStep()/new_zoom / 2# + 10
        y_margin = self.verticalScrollBar().pageStep()/new_zoom / 2# + 10
        self.setSceneRect(QRectF(-x_margin, -y_margin, self.dvm_size.width() + 2*x_margin, self.dvm_size.height() + 2*y_margin))
        self.info_bar.set_info(zoom=self.zoom)

    @pyqtProperty(float)
    def x(self):
        h = self.horizontalScrollBar()
        return (h.value() + h.pageStep() / 2) / self.zoom

    @x.setter
    def x(self, value):
        h = self.horizontalScrollBar()
        h.setValue(int(self.zoom * value - h.pageStep() / 2))

    @pyqtProperty(float)
    def y(self):
        v = self.verticalScrollBar()
        return (v.value() + v.pageStep() / 2) / self.zoom

    @y.setter
    def y(self, value):
        v = self.verticalScrollBar()
        v.setValue(int(self.zoom * value - v.pageStep() / 2))

    def set_rect_view(self, new_rect_view):
        self.fitInView(new_rect_view, Qt.AspectRatioMode.KeepAspectRatio)
        r_v = self.viewport().rect()
        r_s = self.mapToScene(r_v).boundingRect()
        self._zoom = r_v.width()/r_s.width()
        # self.centerOn(self._rect_view.center())

    def move_to(self, x, y, zoom=None):
        duration = 1500
        anims = []

        anim_x = QPropertyAnimation(self, b'x')
        anim_x.setDuration(duration)
        anim_x.setStartValue(self.x)
        anim_x.setKeyValueAt(0.8, x)
        anim_x.setEndValue(x)
        # anim_x.setEasingCurve(QEasingCurve.Type.InOutQuad)
        anims.append(anim_x)

        anim_y = QPropertyAnimation(self, b'y')
        anim_y.setDuration(duration)
        anim_y.setStartValue(self.y)
        anim_y.setKeyValueAt(0.8, y)
        anim_y.setEndValue(y)
        # anim_y.setEasingCurve(QEasingCurve.Type.InOutQuad)
        anims.append(anim_y)

        if zoom is not None:
            anim_zoom = QPropertyAnimation(self, b'zoom')
            anim_zoom.setDuration(duration)
            anim_zoom.setStartValue(self.zoom)
            anim_zoom.setKeyValueAt(0.2, self.zoom)
            anim_zoom.setEndValue(zoom)
            # anim_zoom.setEasingCurve(QEasingCurve.Type.InQuad)
            anims.append(anim_zoom)

        group = QParallelAnimationGroup(self)
        for anim in anims:
            group.addAnimation(anim)
        group.start()


class QScene(QGraphicsScene):
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        for i in self.items(event.scenePos()):
            i.mouseMoveEvent(event)
        super().mouseMoveEvent(event)





