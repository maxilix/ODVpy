from PyQt6.QtGui import QColor, QPolygonF
from PyQt6.QtWidgets import QLabel

from odv.data_section.move import Layer, Sector, Obstacle, Move
from qt.common.separator_line import QHLine
from qt.control.control_section import QSectionControl
from qt.control.generic_inspector import Inspector, QGeometrySIW
from qt.control.generic_tree import QGenericTreeItem
from qt.graphics import GraphicPolygon, OdvThinPen, OdvLightBrush, OdvHighBrush


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



#########################################################################

class ObstacleInspector(Inspector):
    def __init__(self):
        super().__init__()

        self.obstacle_siw = QGeometrySIW(geometry_name="Polygon")
        self.obstacle_siw.update_required.connect(self.update_both)
        self.obstacle_siw.value_changed.connect(self.update_model)
        self.main_layout.addWidget(self.obstacle_siw)

        self.main_layout.addWidget(QHLine())

        self.geometry_info_label = QLabel()
        self.main_layout.addWidget(self.geometry_info_label)

        self.main_layout.addStretch()

    def update_model(self):
        for item in self.items:
            item.obstacle.poly = QPolygonF(item.graphic_obstacle.polygon)


    def connect_to(self, new_items):
        super().connect_to(new_items)
        self.obstacle_siw.connect_to([item.graphic_obstacle for item in self.items])

        if len(self.items) == 1:
            n = len(self.items[0].obstacle.poly)
            # TODO enable drag of large polynom
            self.geometry_info_label.setText(f"The current saved polygon has {n} points.\n{"WARNING, polygons larger than 20 points cannot be dragged du to performance issues." if n > 20 else ""}")
        else:
            self.geometry_info_label.setText(f"")


class GraphicObstacle(GraphicPolygon):
    thin_pen = OdvThinPen(QColor(255, 90, 40))
    light_brush = OdvLightBrush(QColor(255, 90, 40))
    high_brush = OdvHighBrush(QColor(255, 90, 40))
    initial_opacity = 1


class ObstacleItem(QGenericTreeItem):
    inspector_type = ObstacleInspector
    draggable = True

    def __init__(self, section_control, obstacle: Obstacle):
        super().__init__(section_control, obstacle)
        self.obstacle = obstacle

        self.graphic_obstacle = GraphicObstacle(self, self.obstacle.poly)
        self.add_graphic(self.graphic_obstacle)

#########################################################################

class SectorInspector(Inspector):
    def __init__(self):
        super().__init__()

        self.sector_siw = QGeometrySIW(geometry_name="Polygon")
        self.sector_siw.update_required.connect(self.update_both)
        self.sector_siw.value_changed.connect(self.update_model)
        self.main_layout.addWidget(self.sector_siw)

        self.main_layout.addWidget(QHLine())

        self.obstacle_list_label = QLabel()
        self.main_layout.addWidget(self.obstacle_list_label)

        self.main_layout.addWidget(QHLine())

        self.geometry_info_label = QLabel()
        self.main_layout.addWidget(self.geometry_info_label)



        self.main_layout.addStretch()

    def update_model(self):
        for item in self.items:
            item.sector.poly = QPolygonF(item.graphic_sector.polygon)


    def connect_to(self, new_items):
        super().connect_to(new_items)
        self.sector_siw.connect_to([item.graphic_sector for item in self.items])


        if len(self.items) == 1:
            n = len(self.items[0].sector.poly)
            # TODO enable drag of large polynom
            self.geometry_info_label.setText(f"The current saved polygon has {n} points.{"\nWARNING, polygons larger than 20 points cannot be dragged\nPerformance issues" if n > 20 else ""}")
            self.obstacle_list_label.setText(f"The {self.items[0].name} has {len(self.items[0].sector.obstacle_list)} obstacles.")
        else:
            self.geometry_info_label.setText(f"")
            self.obstacle_list_label.setText(f"")


class SectorGraphic(GraphicPolygon):
    thin_pen = OdvThinPen(QColor(160, 200, 40))
    light_brush = OdvLightBrush(QColor(160, 200, 40))
    high_brush = OdvHighBrush(QColor(160, 200, 40))
    initial_opacity = 1

class SectorItem(QGenericTreeItem):
    inspector_type = SectorInspector
    draggable = True

    def __init__(self, section_control, sector: Sector):
        super().__init__(section_control, sector)
        self.sector = sector

        self.graphic_sector = SectorGraphic(self, self.sector.poly)
        self.add_graphic(self.graphic_sector)

#########################################################################

class LayerInspector(Inspector):
    def __init__(self):
        super().__init__()
        self.main_layout.addStretch()

    def connect_to(self, new_items):
        super().connect_to(new_items)

class LayerItem(QGenericTreeItem):
    inspector_type = LayerInspector
    draggable = True

    def __init__(self, section_control, layer: Layer):
        super().__init__(section_control, layer)
        self.layer = layer

#########################################################################

class MoveInspector(Inspector):
    def __init__(self):
        super().__init__()
        self.main_layout.addStretch()

    def connect_to(self, new_items):
        super().connect_to(new_items)



class MoveItem(QGenericTreeItem):
    inspector_type = MoveInspector
    draggable = False

    def __init__(self, section_control, move:Move):
        super().__init__(section_control, move)
        self.move = move

#########################################################################

class QMoveControl(QSectionControl):
    item_types = {Move: MoveItem,
                  Layer: LayerItem,
                  Sector: SectorItem,
                  Obstacle: ObstacleItem}
