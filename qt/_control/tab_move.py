from PyQt6.QtGui import QColor, QPolygonF

from dvd.move import Layer, MainArea, Obstacle, Move
from qt._control.inspector_graphic import GeometrySubInspector
from qt._control.inspector_abstract import Inspector
from qt._control.tab__abstract import QTabControlGenericTree


class ObstacleInspector(Inspector):
    deletable = True
    draggable = True
    child_name = ""  # cannot add child

    def init_sub_inspector(self):
        self.sub_inspector_group["Polygon"] = [
            GeometrySubInspector(self, "poly", color=QColor(255, 90, 40)),
        ]


class MainAreaInspector(Inspector):
    # path color QColor(180, 110, 30)
    deletable = True
    child_name = "Obstacle"

    def init_sub_inspector(self):
        self.sub_inspector_group["Polygon"] = [
            GeometrySubInspector(self, "poly", color=QColor(160, 200, 40)),
        ]

    def new_odv_child(self):
        new_obstacle = Obstacle(self.odv_object)
        new_obstacle.poly = self._tab_control.scene.new_centered_polygon(scale=0.25)
        return new_obstacle


class LayerInspector(Inspector):
    deletable = True
    child_name = "Main Area"

    def new_odv_child(self):
        new_main_area = MainArea(self.odv_object)
        new_main_area.area = self._tab_control.scene.new_centered_polygon(scale=0.9)
        return new_main_area



class MoveInspector(Inspector):
    deletable = False
    child_name = "Layer"

    def new_odv_child(self):
        new_layer = Layer(self.odv_object)
        return new_layer

class QMoveTabControl(QTabControlGenericTree):
    inspector_types = {Move: MoveInspector,
                       Layer: LayerInspector,
                       MainArea: MainAreaInspector,
                       Obstacle: ObstacleInspector}
