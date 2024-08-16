from PyQt6.QtCore import Qt, QPointF, QPropertyAnimation, pyqtProperty, QParallelAnimationGroup, QRectF, \
    QVariantAnimation, QSequentialAnimationGroup, QEasingCurve, QPoint, QSizeF, QRect, QSize, QEvent, pyqtSlot, \
    pyqtSignal
from PyQt6.QtGui import QPixmap, QBrush, QPen, QMouseEvent
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsRectItem, QGraphicsSceneMouseEvent, \
    QMenu


class QViewport(QGraphicsView):
    view_changed = pyqtSignal(QRectF)

    def __init__(self, scene, level_map, info_bar):
        super().__init__(scene)
        self.level_map = level_map
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

        # init a too large scene rectangle, to init position
        self.setSceneRect(QRectF(-self.level_map.width, -self.level_map.height, 3*self.level_map.width, 3*self.level_map.height))
        # init view position
        self.zoom = 1.5
        self.x = self.level_map.width // 2
        self.y = self.level_map.height // 2

    def adjust_margins(self):
        cr = self.current_visible_scene_rect()
        tr = self.scene().itemsBoundingRect()
        r = QRectF(-cr.width() / 2, -cr.height() / 2, cr.width() + tr.width(), cr.height() + tr.height())
        self.setSceneRect(r)

    def resizeEvent(self, event):
        self.adjust_margins()
        super().resizeEvent(event)

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

    def mouseMoveEvent(self, event: QMouseEvent):
        self.adjust_margins()
        mouse_scene_pos = self.mapToScene(event.pos())
        self.info_bar.set_info(x=mouse_scene_pos.x(), y=mouse_scene_pos.y())
        if self.drag_position is not None:
            delta = self.drag_position - event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + delta.y())
            self.drag_position = event.pos()
        super().mouseMoveEvent(event)

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

        self.adjust_margins()

        h = self.horizontalScrollBar()
        v = self.verticalScrollBar()
        self.x = mouse_scene_pos.x() + (h.pageStep() / 2 - mouse_view_pos.x()) / (self.zoom_shift_factor * self.zoom)
        self.y = mouse_scene_pos.y() + (v.pageStep() / 2 - mouse_view_pos.y()) / (self.zoom_shift_factor * self.zoom)

        # self.control.mousse_event(mouse_scene_pos, event)
        event.ignore()


    @pyqtProperty(float)
    def zoom(self):
        if self.level_map.height >= self.level_map.width:
            v = self.verticalScrollBar()
            vertical_zoom = (v.maximum() - v.minimum() + v.pageStep()) / self.sceneRect().height()
            return vertical_zoom
        else:
            h = self.horizontalScrollBar()
            horizontal_zoom = (h.maximum() - h.minimum() + h.pageStep()) / self.sceneRect().width()
            return horizontal_zoom


    @zoom.setter
    def zoom(self, new_zoom):
        if new_zoom < self.zoom_min:
            new_zoom = self.zoom_min
        if new_zoom > self.zoom_max:
            new_zoom = self.zoom_max
        current_zoom = self.zoom
        self.scale(new_zoom / current_zoom, new_zoom / current_zoom)
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

    def move_to_item(self, item: QGraphicsItem):
        self.move_to_rect(item.boundingRect())

    def move_to_rect(self, r: QRectF, marge_factor: float = 1.2):
        c = r.center()
        r_v = self.viewport().rect()
        zoom_w = r_v.width() / r.width()
        zoom_h = r_v.height() / r.height()
        self.move_to(c.x(), c.y(), min(zoom_w, zoom_h) / marge_factor)

    def move_to(self, x, y, zoom=None):
        duration = 600
        anims = []

        anim_x = QPropertyAnimation(self, b'x')
        anim_x.setDuration(duration)
        anim_x.setStartValue(self.x)
        # anim_x.setKeyValueAt(0.8, x)
        anim_x.setEndValue(x)
        anim_x.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anims.append(anim_x)

        anim_y = QPropertyAnimation(self, b'y')
        anim_y.setDuration(duration)
        anim_y.setStartValue(self.y)
        # anim_y.setKeyValueAt(0.8, y)
        anim_y.setEndValue(y)
        anim_y.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anims.append(anim_y)

        if zoom is not None:
            anim_zoom = QPropertyAnimation(self, b'zoom')
            anim_zoom.setDuration(int(1.5 * duration))
            anim_zoom.setStartValue(self.zoom)
            # anim_zoom.setKeyValueAt(0.25, self.zoom)
            anim_zoom.setEndValue(zoom)
            anim_zoom.setEasingCurve(QEasingCurve.Type.InOutCubic)
            anims.append(anim_zoom)

        group = QParallelAnimationGroup(self)
        for anim in anims:
            group.addAnimation(anim)
        group.start()

    def current_visible_scene_rect(self):
        return self.mapToScene(self.viewport().rect()).boundingRect()

