from PyQt6.QtGui import QColor

from common import *
from dvd.lift import LiftArea, Lift
from qt.control.inspector_abstract import Inspector
from qt.control.inspector_generic import OdvObjectListSubInspector, IntegerBoxInspector, \
    ConstantEnumListInspector
from qt.control.inspector_graphic import GeometrySubInspector
from qt.control.tab__abstract import QTabControlGenericTree

LIFT_TYPE = {0: "???",
             1: "Stair",
             2: "Ladders",
             3: "Wall"}


class LiftAreaInspector(Inspector):
    deletable = True
    child_name = ""  # cannot add child

    def init_sub_inspector(self):
        self.sub_inspector_group["Properties"] = [
            ConstantEnumListInspector(self, "lift_type", "Type", enum=LIFT_TYPE),
            IntegerBoxInspector(self, "perspective", "Perspective", int_type=UChar),
        ]
        self.sub_inspector_group["Main Areas"] = [
            OdvObjectListSubInspector(self, "main_area_below", "Below", iterable=self.odv_object.move.main_area_iterator(include_None=False)),
            OdvObjectListSubInspector(self, "main_area", "", iterable=self.odv_object.move.main_area_iterator(include_None=False)),
            OdvObjectListSubInspector(self, "main_area_above", "Above", iterable=self.odv_object.move.main_area_iterator(include_None=False)),
        ]
        self.sub_inspector_group["Gateways"] = [
            GeometrySubInspector(self, "gateway_below","Below", color=QColor(200, 120, 40)),
            GeometrySubInspector(self, "gateway_above", "Above", color=QColor(200, 120, 40)),
        ]


class LiftInspector(Inspector):
    deletable = False
    child_name = "Lift Area"

    def new_odv_child(self):
        new_lift_area = LiftArea(self.odv_object)
        new_lift_area.move = self.odv_object.move

        new_lift_area.lift_type = 1
        new_lift_area.main_area = None
        new_lift_area.main_area_below = None
        new_lift_area.main_area_above = None
        new_lift_area.gateway_below = self._tab_control.scene.new_centered_gateway(scale=0.2)
        new_lift_area.gateway_above = self._tab_control.scene.new_centered_gateway(scale=0.2)
        new_lift_area.perspective = 0

        return new_lift_area


class QLiftTabControl(QTabControlGenericTree):
    inspector_types = {Lift: LiftInspector,
                       LiftArea: LiftAreaInspector}
