from PyQt6.QtGui import QColor

from common import *
from dvd.lift import LiftArea, Lift
from qt.control.inspector_abstract import Inspector
from qt.control.inspector_generic import OdvObjectListSubInspector, IntegerBoxInspector, \
    ConstantEnumListInspector
from qt.control.inspector_graphic import GeometrySubInspector
from qt.control.tab_abstract import QTabControlGenericTree

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
            OdvObjectListSubInspector(self, "main_area_under", "Under", iterable=self.odv_object.move.main_area_iterator()),
            OdvObjectListSubInspector(self, "main_area", "", iterable=self.odv_object.move.main_area_iterator()),
            OdvObjectListSubInspector(self, "main_area_over", "Over", iterable=self.odv_object.move.main_area_iterator()),
        ]
        self.sub_inspector_group["Gateways"] = [
            GeometrySubInspector(self, "gateway_under","Under", color=QColor(200, 120, 40)),
            GeometrySubInspector(self, "gateway_over", "Over", color=QColor(200, 120, 40)),
        ]


class LiftInspector(Inspector):
    deletable = False
    child_name = "Lift Area"

    def new_odv_child(self):
        new_lift_area = LiftArea(self.odv_object)
        new_lift_area.move = self.odv_object.move

        new_lift_area.lift_type = 1
        new_lift_area.main_area = None
        new_lift_area.main_area_under = None
        new_lift_area.main_area_over = None
        new_lift_area.gateway_under = self._tab_control.scene.new_centered_gateway(scale=0.2)
        new_lift_area.gateway_over = self._tab_control.scene.new_centered_gateway(scale=0.2)
        new_lift_area.perspective = 0

        return new_lift_area


class QLiftTabControl(QTabControlGenericTree):
    inspector_types = {Lift: LiftInspector,
                       LiftArea: LiftAreaInspector}
