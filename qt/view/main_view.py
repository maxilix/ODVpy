from PyQt6.QtCore import Qt, QPointF, QPropertyAnimation, pyqtProperty, QParallelAnimationGroup, QRectF, \
    QVariantAnimation, QSequentialAnimationGroup, QEasingCurve, QPoint
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

        self.drag_position = None
        self.zoom_factor = 1.1
        self.zoom = 1
        self.max_zoom = 25
        self.min_zoom = 0.5

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.setCursor(Qt.CursorShape.DragMoveCursor)
            self.drag_position = event.pos()
        elif event.button() == Qt.MouseButton.LeftButton:
            self.move_to(QRectF(334, 162, 100, 100))
        elif event.button() == Qt.MouseButton.RightButton:
            self.move_to(QRectF(100, 300, 50, 50))

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton and self.drag_position is not None:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.drag_position = None
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.drag_position is not None:
            delta = self.drag_position - event.pos()
            # new_rect_view = QRectF(self.rect_view.x() + delta.x(),
            #                        self.rect_view.y() + delta.y(),
            #                        self.rect_view.width(),
            #                        self.rect_view.height())
            # self.rect_view = new_rect_view
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + delta.y())
            self.drag_position = event.pos()

        # r_v = self.viewport().rect()
        # r_s = self.mapToScene(r_v).boundingRect()
        #
        # print(f"{r_v.width()/r_s.width()}")
        super().mouseMoveEvent(event)

    # def wheelEvent(self, event):
    #     event.accept()
    #     # scene_position = self.mapToScene(event.position().toPoint())
    #     # x = scene_position.x()
    #     # y = scene_position.y()
    #     #
    #     # current_rect_view = self.mapToScene(self.viewport().rect()).boundingRect()
    #     f = 1.0
    #     # dl = x - current_rect_view.left()
    #     # dr = current_rect_view.right() - x
    #     # dt = y - current_rect_view.top()
    #     # db = current_rect_view.bottom() - y
    #     #
    #     # new_rect_view = QRectF()
    #     # new_rect_view.setLeft(x-f*dl)
    #     # new_rect_view.setRight(x+f*dr)
    #     # new_rect_view.setTop(y-f*dt)
    #     # new_rect_view.setBottom(y-f*db)
    #     #
    #     # self.set_rect_view(new_rect_view)
    #
    #     event.accept()
    #
    #     scene_position = self.mapToScene(event.position().toPoint())
    #     # print(f"{scene_position=}")
    #     viewport_position = self.mapFromGlobal(event.globalPosition())
    #     # print(f"{viewport_position=}")
    #
    #     current_rect_view = self.mapToScene(self.viewport().rect()).boundingRect()
    #     # current_rect_view = QRectF(current_rect_view.x() + 2.28592814371257/2,
    #     #                            current_rect_view.y() + 1,
    #     #                            current_rect_view.width() - 2,
    #     #                            current_rect_view.height() - 2)
    #     print(f"{current_rect_view=}")
    #     # size = self.size()
    #     # print(f"{size=}")
    #
    #
    #     delta = event.angleDelta().y()
    #     if delta > 0:  # and self.zoom < self.max_zoom:
    #         self.scale(f, f)
    #         # self.zoom *= self.zoom_factor
    #     elif delta < 0: # and self.zoom > self.min_zoom:
    #         self.scale(1.0 / f, 1.0 / f)
    #         # self.zoom /= self.zoom_factor
    #     else:
    #         pass
    #
    #     self.set_rect_view(current_rect_view)

    def set_rect_view(self, new_rect_view):
        self.fitInView(new_rect_view, Qt.AspectRatioMode.KeepAspectRatio)
        r_v = self.viewport().rect()
        r_s = self.mapToScene(r_v).boundingRect()
        self.zoom = r_v.width()/r_s.width()
        # self.centerOn(self._rect_view.center())

    def move_to(self, new_rect_view):
        current_rect_view = self.mapToScene(self.viewport().rect()).boundingRect()
        transition_rect_view = current_rect_view.united(new_rect_view)
        # w_r = 0.1*transition_rect_view.width()
        # h_r = 0.1*transition_rect_view.height()
        # transition_rect_view.setLeft(transition_rect_view.left() + w_r)
        # transition_rect_view.setRight(transition_rect_view.right() - w_r)
        # transition_rect_view.setTop(transition_rect_view.top() + h_r)
        # transition_rect_view.setBottom(transition_rect_view.bottom() - h_r)

        anim_out = QVariantAnimation()
        anim_out.setDuration(350)
        anim_out.setStartValue(current_rect_view)
        anim_out.setEndValue(transition_rect_view)
        anim_out.setEasingCurve(QEasingCurve.Type.OutSine)
        anim_out.valueChanged.connect(self.set_rect_view)

        anim_in = QVariantAnimation()
        anim_in.setDuration(350)
        anim_in.setStartValue(transition_rect_view)
        anim_in.setEndValue(new_rect_view)
        anim_out.setEasingCurve(QEasingCurve.Type.InSine)
        anim_in.valueChanged.connect(self.set_rect_view)

        anim = QSequentialAnimationGroup(self)
        anim.addAnimation(anim_out)
        anim.addAnimation(anim_in)
        anim.start()


class QMainView(View, QGraphicsScene):
    def __init__(self, control, info_bar):
        super().__init__(control)
        self.info_bar = info_bar
        pixmap = QPixmap(self.control.level.dvm.level_map)
        self.map = self.addPixmap(pixmap)
        rect = QRectF(-pixmap.width()/2, -pixmap.height()/2, 2*pixmap.width(), 2*pixmap.height())
        self.setSceneRect(rect)

        self.viewport = QViewport(self)
        self.view_motion = QViewMotion(self, self.control.control_motion)
        # self.viewport.set_rect_view(QRectF(334, 162, 46, 96))

    def mouseMoveEvent(self, event):
        pos = event.scenePos()
        self.info_bar.set_widget(x=pos.x(), y=pos.y())

        self.view_motion.refresh(pos)

    def wheelEvent(self, event):
        # scenePos retourne la coordonné du dvm indépendament du zoom
        event.accept()
        # # print(f"{event.pos()=}")
        # scene_position = event.scenePos()
        # # print(f"{scene_position=}")
        # global_position = event.screenPos()
        # # print(f"{global_position=}")
        # mapped_position = self.viewport.mapFromGlobal(global_position)
        # # print(f"{mapped_position=}")

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
        new_position = QPointF(scene_position.x() + (size.width() /2-relative_position.x()) / (1 * self.viewport.zoom),
                               scene_position.y() + (size.height()/2-relative_position.y()) / (1 * self.viewport.zoom))
        self.viewport.centerOn(new_position)

        self.info_bar.set_widget(zoom=self.viewport.zoom)

