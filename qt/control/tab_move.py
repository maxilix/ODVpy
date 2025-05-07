from PyQt6.QtGui import QColor

from odv.data_section.move import Layer, Sector, Obstacle, Move
from qt.control.control_section import QSectionControl
from qt.control.generic_inspector import Inspector
from qt.control.generic_tree import QGenericTreeItem
from qt.control.sub_inspector import InfoQSIW


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
# class SectorInspector(Inspector):
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
#         new_sector = Sector(self.odv_object)
#         new_sector.poly = self._tab_control.scene.new_centered_polygon(scale=0.9)
#         return new_sector
#
#
#
# class MoveInspector(Inspector):
#     deletable = False
#     child_name = "Layer"
#
#     def new_odv_child(self):
#         new_layer = Layer(self.odv_object)
#         return new_layer


class LayerInspector(Inspector):
    def __init__(self):
        super().__init__()

        self.add_sub_inspector(InfoQSIW(self, "info"))



class LayerItem(QGenericTreeItem):
    inspector_type = LayerInspector

    def __init__(self, layer:Layer):
        super().__init__(layer)
        self.layer = layer

    @property
    def info(self):
        return f"polygon : {self.layer.total_polygon()}"









class QMoveControl(QSectionControl):
    item_types = {Move: QGenericTreeItem,
                  Layer: LayerItem,
                  Sector: QGenericTreeItem,
                  Obstacle: QGenericTreeItem}
