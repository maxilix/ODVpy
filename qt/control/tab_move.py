from PyQt6.QtGui import QColor, QPolygonF

from dvd.move import Layer, Sector, Obstacle, Move
from qt.control.inspector_graphic import GeometrySubInspector
from qt.control.widget_inspector import QInspectorWidget
from qt.control.main_tab import QMainTab
from qt.control.widget_sub_inspector import GeometryQSIW


# class ObstacleQInspectorWidget(QInspectorWidget):
#     deletable = True
#     draggable = True
#     child_name = ""  # cannot add child
#
#     def init_sub_inspector(self):
#         self.sub_inspector_group["Polygon"] = [
#             GeometrySubInspector(self, "poly", color=QColor(255, 90, 40)),
#         ]
#
#
# class MainAreaQInspectorWidget(QInspectorWidget):
#     # path color QColor(180, 110, 30)
#     deletable = True
#     child_name = "Obstacle"
#
#     def init_sub_inspector(self):
#         self.sub_inspector_group["Polygon"] = [
#             GeometrySubInspector(self, "poly", color=QColor(160, 200, 40)),
#         ]
#
#     def new_odv_child(self):
#         new_obstacle = Obstacle(self.odv_object)
#         new_obstacle.poly = self._tab_control.scene.new_centered_polygon(scale=0.25)
#         return new_obstacle
#
#
# class LayerQInspectorWidget(QInspectorWidget):
#     deletable = True
#     child_name = "Main Area"
#
#     def new_odv_child(self):
#         new_main_area = Sector(self.odv_object)
#         new_main_area.poly = self._tab_control.scene.new_centered_polygon(scale=0.9)
#         return new_main_area
#
#
#
# class MoveQInspectorWidget(QInspectorWidget):
#     deletable = False
#     child_name = "Layer"
#
#     def new_odv_child(self):
#         new_layer = Layer(self.odv_object)
#         return new_layer


class MoveQIW(QInspectorWidget):
    deletable = False
    child_name = "Layer"


    def __init__(self, tab, odv_object):
        super().__init__(tab, odv_object)

        self.move = odv_object

        self.mapQSIW = GeometryQSIW(self, self.get, self.set)
        self.add_sub_inspector(self.mapQSIW)

        self.update()


    def get_info(self):
        return f"size: {self.level_map.width} x {self.level_map.height}"

    def get(self):
        return None

    def set(self, new_map_filename):
        return None


class QMoveTab(QMainTab):
    inspector_types = {Move: MoveQIW,
                       Layer: QInspectorWidget,
                       Sector: QInspectorWidget,
                       Obstacle: QInspectorWidget}
