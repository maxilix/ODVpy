from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout

from dvd.move import Layer, Sector, Obstacle, Move
from qt.control.tab_abstract import QMainTab
from qt.control.widget_inspector import QInspectorWidget
from qt.control.widget_sub_inspector import InfoQSIW


# class ObstacleInspector(Inspector):
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
# class MainAreaInspector(Inspector):
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
# class LayerInspector(Inspector):
#     deletable = True
#     child_name = "Main Area"
#
#     def new_odv_child(self):
#         new_main_area = Sector(self.odv_object)
#         new_main_area.poly = self._tab_control.scene.new_centered_polygon(scale=0.9)
#         return new_main_area
#


class MoveInspector(QInspectorWidget):
    deletable = False
    child_name = "Layer"

    # def new_odv_child(self):
    #     new_layer = Layer(self.odv_object)
    #     return new_layer

    def __init__(self, control, odv_object):
        super().__init__(control, odv_object)

        info_widget = InfoQSIW(self, self.get_info)
        self.add_sub_inspector(info_widget)






    def get_info(self):
        return "YOUHOU"





class QMoveTab(QMainTab):
    inspector_types = {Move: MoveInspector,
                       Layer: QInspectorWidget,
                       Sector: QInspectorWidget,
                       Obstacle: QInspectorWidget}

