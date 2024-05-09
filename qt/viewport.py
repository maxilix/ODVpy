# class QViewport(QGraphicsView):
#
#     def __init__(self, scene: QScene):
#         super().__init__(scene)
#         self.scene = scene
#         self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
#         self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#         self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#         self.setMouseTracking(True)
#
#         self.scene = scene
#
#         self.max_zoom = 35
#         self.min_zoom = 0.5
#         self.zoom = 1
#         self.zoom_factor = 1.2
#
#     def wheelEvent(self, event: QWheelEvent):
#         # event.accept()
#         angle = event.angleDelta().y()
#         if angle > 0 and self.zoom < self.max_zoom:
#             self.scale(self.zoom_factor, self.zoom_factor)
#             self.zoom *= self.zoom_factor
#         elif angle < 0 and self.zoom > self.min_zoom:
#             self.scale(1.0 / self.zoom_factor, 1.0 / self.zoom_factor)
#             self.zoom /= self.zoom_factor
#         else:
#             pass
#
#         scene_position = event.scenePosition()
#         scene_position = self.mapToScene(event.position().toPoint())
#         print(scene_position)
#         global_position = event.globalPosition()
#         relative_position = self.mapFromGlobal(global_position)
#         size = self.size()
#         new_position = QPointF(scene_position.x() + (size.width() /2-relative_position.x())/(1.1 * self.zoom),
#                                scene_position.y() + (size.height()/2-relative_position.y())/(1.1 * self.zoom))
#         self.centerOn(new_position)
