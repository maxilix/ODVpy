from PyQt6.QtGui import QColor, QPolygonF

from common import UShort, UChar
from dvd.buil import Buil, Door, Building, SpecialDoors, Buildings
from qt.control.inspector_abstract import Inspector
from qt.control.inspector_generic import IntegerBoxInspector, InfoSubInspector, ConstantEnumListInspector, \
    MultiCheckBoxInspector, CheckBoxInspector, IntegerTwinBoxInspector, OdvObjectListSubInspector
from qt.control.inspector_graphic import GeometrySubInspector
from qt.control.tab_abstract import QTabControlGenericTree

DOOR_TYPE = {0: "Invisible Door",
             1: "Normal Door",
             2: "Trapdoor",
             3: "Special Door"}


class DoorInspector(Inspector):
    deletable = True
    child_name = ""

    def init_odv_prop(self):
        if self.odv_object.shape != QPolygonF():
            self.sub_inspector_group["Door Shape"] = [GeometrySubInspector(self, "shape", color=QColor(30, 30, 255))]
        self.sub_inspector_group["Properties"] = [ConstantEnumListInspector(self, "door_type", "Type", enum=DOOR_TYPE),
                                                  # MultiCheckBoxInspector(self, "lock_state", "Lock", label_list=["locked", "unlockable"], column=2, conditional=[None, 0]),
                                                  CheckBoxInspector(self, "unk_bool_0", "unk_bool_0"),
                                                  CheckBoxInspector(self, "locked", "locked"),
                                                  CheckBoxInspector(self, "unlockable", "unlockable"),
                                                  CheckBoxInspector(self, "unk_bool_3", "unk_bool_3"),
                                                  CheckBoxInspector(self, "unk_bool_4", "unk_bool_4"),
                                                  CheckBoxInspector(self, "unk_bool_5", "unk_bool_5"),
                                                  CheckBoxInspector(self, "unk_bool_6", "unk_bool_6"),
                                                  CheckBoxInspector(self, "unk_bool_7", "unk_bool_7"),
                                                  CheckBoxInspector(self, "unk_bool_8", "unk_bool_8"),

                                                  IntegerBoxInspector(self, "anim_id", "anim_id", int_type=UShort),
                                                  IntegerTwinBoxInspector(self, "allowed_sens", "allowed_sens", int_type=UChar),]
        self.sub_inspector_group["Main Ares"] = [OdvObjectListSubInspector(self, "main_area_1", "From", iterable=self.odv_object.move.main_area_iterator()),
                                                 OdvObjectListSubInspector(self, "main_area_3", "To", iterable=self.odv_object.move.main_area_iterator())]
        self.sub_inspector_group["Gateway"] = [GeometrySubInspector(self, "gateway", color=QColor(200, 120, 40))]



    @property
    def lock_state(self):
        return [self.odv_object.locked, self.odv_object.unlockable]

    @lock_state.setter
    def lock_state(self, state):
        self.odv_object.locked = state[0]
        self.odv_object.unlockable = state[1]


    #
    # def new_odv_child(self):
    #     new_obstacle = Obstacle(self.odv_object)
    #     new_obstacle.poly = self._tab_control.scene.new_centered_polygon()
    #     return new_obstacle


class BuildingInspector(Inspector):
    deletable = True
    child_name = "Door"

    def init_odv_prop(self):
        self.sub_inspector_group["Properties"] = [IntegerBoxInspector(self, "unk1", "unk1", int_type=UShort),
                                                  InfoSubInspector(self, "character_id_list", "char id")]

    # def new_odv_child(self):
    #     new_main_area = MainArea(self.odv_object)
    #     new_main_area.poly = self._tab_control.scene.new_centered_polygon()
    #     return new_main_area



class BuildingsInspector(Inspector):
    deletable = False
    child_name = "Building"

    # def new_odv_child(self):
    #     new_layer = Layer(self.odv_object)
    #     return new_layer

class SpecialDoorsInspector(Inspector):
    deletable = False
    child_name = "Special Door"

class QBuilTabControl(QTabControlGenericTree):
    inspector_types = {Buildings: BuildingsInspector,
                       SpecialDoors: SpecialDoorsInspector,
                       Building: BuildingInspector,
                       Door: DoorInspector}

