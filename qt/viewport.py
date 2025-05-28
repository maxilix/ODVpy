from PyQt6.QtCore import Qt, QPropertyAnimation, pyqtProperty, QParallelAnimationGroup, QRectF, QEasingCurve, pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QGraphicsView, QGraphicsItem


class QViewport(QGraphicsView):
    view_changed = pyqtSignal(QRectF)

    def __init__(self, scene, info_bar):
        super().__init__(scene)
        self.info_bar = info_bar

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.horizontalScrollBar().valueChanged.connect(
            lambda: self.view_changed.emit(self.current_visible_scene_rect()))
        self.verticalScrollBar().valueChanged.connect(
            lambda: self.view_changed.emit(self.current_visible_scene_rect()))

        self.setMouseTracking(True)
        self.drag_position = None

        self.zoom_factor = 1.1
        self.zoom_shift_factor = 1.0
        self.zoom_max = 50
        self.zoom_min = 0.5

        self.info_bar.set_xy(None)
        self.info_bar.set_zoom(self.zoom)

    def adjust_margins(self):
        cr = self.current_visible_scene_rect()
        margin_x = cr.width() / 2
        margin_y = cr.height() / 2
        self.setSceneRect(self.scene().itemsBoundingRect().adjusted(-margin_x, -margin_y, margin_x, margin_y))

    # def resizeEvent(self, event):
    #     self.adjust_margins()
    #     super().resizeEvent(event)

    def leaveEvent(self, a0):
        # unpleasant behavior with context menus
        # self.info_bar.set_xy(None)
        super().leaveEvent(a0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.setCursor(Qt.CursorShape.DragMoveCursor)
            self.drag_position = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            if self.drag_position is not None:
                self.setCursor(Qt.CursorShape.ArrowCursor)
                self.drag_position = None
        else:
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        # Not necessary for every mouse movement, but useful when an item is drawn outside the DVM.
        self.adjust_margins()

        mouse_scene_pos = self.mapToScene(event.pos())
        self.info_bar.set_xy(mouse_scene_pos.x(), mouse_scene_pos.y())
        if self.drag_position is not None:
            delta = self.drag_position - event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + delta.y())
            self.drag_position = event.pos()
        super().mouseMoveEvent(event)

    def wheelEvent(self, event):
        # save mousse positions before zooming
        mouse_view_pos = event.position().toPoint()
        mouse_scene_pos = self.mapToScene(mouse_view_pos)

        # apply the correct zoom
        delta = event.angleDelta().y()
        if delta > 0 and self.zoom < self.zoom_max:
            self.zoom *= self.zoom_factor
        elif delta < 0 and self.zoom > self.zoom_min:
            self.zoom /= self.zoom_factor
        else:
            pass  # do not change the zoom

        # Refocus the view according to the mouse position
        h = self.horizontalScrollBar()
        v = self.verticalScrollBar()
        self.x = mouse_scene_pos.x() + (h.pageStep() / 2 - mouse_view_pos.x()) / (self.zoom_shift_factor * self.zoom)
        self.y = mouse_scene_pos.y() + (v.pageStep() / 2 - mouse_view_pos.y()) / (self.zoom_shift_factor * self.zoom)

        # Todo is it useful ?
        # event.ignore()

    @pyqtProperty(float)
    def zoom(self):
        transform = self.transform()
        scale_x = transform.m11()  # get horizontal zoom
        scale_y = transform.m22()  # get vertical zoom
        return (scale_x+scale_y)/2

    @zoom.setter
    def zoom(self, new_zoom):
        if new_zoom < self.zoom_min:
            new_zoom = self.zoom_min
        if new_zoom > self.zoom_max:
            new_zoom = self.zoom_max
        current_zoom = self.zoom
        self.scale(new_zoom / current_zoom, new_zoom / current_zoom)
        self.adjust_margins()
        self.info_bar.set_zoom(self.zoom)

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

    def move_to_rect(self, r: QRectF, max_zoom:float = 10):
        c = r.center()
        r_v = self.viewport().rect()
        zoom_x = r_v.width() / r.width()
        zoom_y = r_v.height() / r.height()
        self.move_to(c.x(), c.y(), min(zoom_x, zoom_y, max_zoom))

    def move_to(self, x, y, zoom=None):
        duration = 600  # millisecond
        group = QParallelAnimationGroup(self)

        anim_x = QPropertyAnimation(self, b'x')
        anim_x.setDuration(duration)
        anim_x.setStartValue(self.x)
        anim_x.setEndValue(x)
        anim_x.setEasingCurve(QEasingCurve.Type.InOutCubic)
        group.addAnimation(anim_x)

        anim_y = QPropertyAnimation(self, b'y')
        anim_y.setDuration(duration)
        anim_y.setStartValue(self.y)
        anim_y.setEndValue(y)
        anim_y.setEasingCurve(QEasingCurve.Type.InOutCubic)
        group.addAnimation(anim_y)

        if zoom is not None:
            if zoom < self.zoom_min:
                zoom = self.zoom_min
            if zoom > self.zoom_max:
                zoom = self.zoom_max
            anim_zoom = QPropertyAnimation(self, b'zoom')
            anim_zoom.setDuration(int(1.2 * duration))
            anim_zoom.setStartValue(self.zoom)
            anim_zoom.setEndValue(zoom)
            anim_zoom.setEasingCurve(QEasingCurve.Type.InOutCubic)
            group.addAnimation(anim_zoom)

        group.start()

    def current_visible_scene_rect(self):
        return self.mapToScene(self.viewport().rect()).boundingRect()
