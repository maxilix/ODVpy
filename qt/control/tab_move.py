from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QCheckBox, QPushButton

from odv.data_section.move import Layer, Sector, Obstacle, Move
from qt.common.utils import bounding_rect_of
from qt.control.control_section import QSectionControl
from qt.control.generic_inspector import Inspector
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

        ### Visibility Widget ###################################################
        geometry_visibility_layout = QHBoxLayout()
        geometry_visibility_layout.setContentsMargins(0, 0, 0, 0)

        geometry_visibility_layout.addWidget(QLabel("Visibility"))

        self.visibility_checkbox = QCheckBox()
        self.visibility_checkbox.setTristate(False)
        self.visibility_checkbox.clicked.connect(self.visibility_checkbox_clicked)
        geometry_visibility_layout.addWidget(self.visibility_checkbox)

        geometry_visibility_layout.addStretch()

        self.localise_button = QPushButton("Localise")
        self.localise_button.clicked.connect(self.localise_button_clicked)
        geometry_visibility_layout.addWidget(self.localise_button)

        self.main_layout.addLayout(geometry_visibility_layout)
        #########################################################################

        ### Geometry Edition Widget #############################################
        geometry_edit_layout = QHBoxLayout()
        geometry_edit_layout.setContentsMargins(0, 0, 0, 0)

        geometry_edit_layout.addWidget(QLabel("Polygon"))

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_button_clicked)
        geometry_edit_layout.addWidget(self.edit_button)

        geometry_edit_layout.addStretch()

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(lambda : self.save_cancel_button_clicked(save=True))
        geometry_edit_layout.addWidget(self.save_button)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(lambda : self.save_cancel_button_clicked(save=False))
        geometry_edit_layout.addWidget(self.cancel_button)

        self.main_layout.addLayout(geometry_edit_layout)
        #########################################################################

        ### Infos Widget ########################################################
        self.geometry_info_label = QLabel()

        self.main_layout.addWidget(self.geometry_info_label)
        #########################################################################

        self.main_layout.addStretch()

    def visibility_checkbox_clicked(self):
        self.visibility_checkbox.setTristate(False)
        self.visibility_checkbox.update()
        for item in self.items:
            item.graphic_obstacle.setVisible(self.visibility_checkbox.isChecked())
            item.update()

    def localise_button_clicked(self):
        if self.visibility_checkbox.checkState() != Qt.CheckState.Checked:
            self.visibility_checkbox.click()

        rect = bounding_rect_of([item.graphic_obstacle for item in self.items])
        self.items[0].graphic_obstacle.scene().move_to_rect(rect)

    def edit_button_clicked(self):
        if self.visibility_checkbox.checkState() != Qt.CheckState.Checked:
            self.visibility_checkbox.click()
        [item.graphic_obstacle.enter_edit_mode() for item in self.items]
        self.edit_button.setDisabled(True)
        self.save_button.setEnabled(True)
        self.cancel_button.setEnabled(True)

    def save_cancel_button_clicked(self, save):
        [item.graphic_obstacle.exit_edit_mode(save=save) for item in self.items]
        self.edit_button.setEnabled(True)
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        if save is True:
            for item in self.items:
                item.obstacle.poly = item.graphic_obstacle.polygon
        if len(self.items) == 1:
            n = len(self.items[0].obstacle.poly)
            self.geometry_info_label.setText(f"The polygon has {n} points.\n{"WARNING, polygons larger than 20 points cannot be dragged" if n > 20 else ""}")
        else:
            self.geometry_info_label.setText(f"")


    def connect_to(self, new_items):
        super().connect_to(new_items)
        if all([item.graphic_obstacle.isVisible() for item in self.items]):
            self.visibility_checkbox.setCheckState(Qt.CheckState.Checked)
        elif any([item.graphic_obstacle.isVisible() for item in self.items]):
            self.visibility_checkbox.setCheckState(Qt.CheckState.PartiallyChecked)
        else:
            self.visibility_checkbox.setCheckState(Qt.CheckState.Unchecked)

        if len(self.items) == 1:
            self.edit_button.setText("Edit")
            self.edit_button.setDisabled(self.items[0].graphic_obstacle.edit)
            self.save_button.setText("Save")
            self.save_button.setEnabled(self.items[0].graphic_obstacle.edit)
            self.cancel_button.setText("Cancel")
            self.cancel_button.setEnabled(self.items[0].graphic_obstacle.edit)

            n = len(self.items[0].obstacle.poly)
            self.geometry_info_label.setText(f"The polygon has {n} points.\n{"WARNING, polygons larger than 20 points cannot be dragged" if n > 20 else ""}")
        else:
            self.edit_button.setText("Edit All")
            self.edit_button.setDisabled(all([item.graphic_obstacle.edit for item in self.items]))
            self.save_button.setText("Save All")
            self.save_button.setEnabled(any([item.graphic_obstacle.edit for item in self.items]))
            self.cancel_button.setText("Cancel All")
            self.cancel_button.setEnabled(any([item.graphic_obstacle.edit for item in self.items]))

            self.geometry_info_label.setText(f"")



class GraphicObstacle(GraphicPolygon):
    thin_pen = OdvThinPen(QColor(255, 90, 40))
    light_brush = OdvLightBrush(QColor(255, 90, 40))
    high_brush = OdvHighBrush(QColor(255, 90, 40))



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
        self.main_layout.addStretch()

    def connect_to(self, new_items):
        super().connect_to(new_items)



class SectorItem(QGenericTreeItem):
    inspector_type = SectorInspector
    draggable = True

    def __init__(self, section_control, sector: Sector):
        super().__init__(section_control, sector)
        self.sector = sector

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
