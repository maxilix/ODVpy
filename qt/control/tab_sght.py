from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColor

from common import *
from dvd.sght import Sght, SightObstacle
from qt.control.widget_inspector import QInspectorWidget
from qt.control.inspector_generic import InfoSubInspector, OdvObjectListSubInspector
from qt.control.inspector_graphic import GeometrySubInspector
from qt.control.main_tab import QMainTab
from qt.graphics.sight import GraphicSightObstacle


class SightObstacleQInspectorWidget(QInspectorWidget):
    deletable = True
    child_name = ""  # cannot add child

    def init_sub_inspector(self):
        self.sub_inspector_group["Info"] = [
            InfoSubInspector(self, "unk_char_1", "unk_char_1"),
            InfoSubInspector(self, "unk_char_2", "unk_char_2"),
            InfoSubInspector(self, "unk_char_3", "unk_char_3"),
            InfoSubInspector(self, "unk_char_4", "unk_char_4"),
            InfoSubInspector(self, "nb_sight_vline", "nb_sight_vline"),

        ]

        self.sub_inspector_group["Main Areas"] = [
            OdvObjectListSubInspector(self, "main_area", iterable=self.odv_object.move.main_area_iterator(include_None=True)),
        ]

        self.sub_inspector_group["Geometry"] = [
            GeometrySubInspector(self, "vline_list", color=QColor(255,255,255), graphic_type=GraphicSightObstacle)
        ]

    @property
    def nb_sight_vline(self):
        return len(self.odv_object.vline_list)


class SghtQInspectorWidget(QInspectorWidget):
    deletable = False
    child_name = "Sight Obstacle"

    # def new_odv_child(self):
    #     new_lift_area = LiftArea(self.odv_object)
    #     new_lift_area.move = self.odv_object.move
    #
    #     new_lift_area.lift_type = 1
    #     new_lift_area.main_area = None
    #     new_lift_area.main_area_below = None
    #     new_lift_area.main_area_above = None
    #     new_lift_area.gateway_below = self._tab_control.scene.new_centered_gateway(scale=0.2)
    #     new_lift_area.gateway_above = self._tab_control.scene.new_centered_gateway(scale=0.2)
    #     new_lift_area.perspective = 0
    #
    #     return new_lift_area


class QSghtTabControl(QMainTab):
    inspector_types = {Sght: SghtQInspectorWidget,
                       SightObstacle: SightObstacleQInspectorWidget}
