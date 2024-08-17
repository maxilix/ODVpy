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
                                                  MultiCheckBoxInspector(self, "lock_state", "Lock", label_list=["locked", "unlockable"], column=2, conditional=[None, 0]),
                                                  CheckBoxInspector(self, "unk0", "unk0"),
                                                  CheckBoxInspector(self, "unk1", "unk1"),
                                                  CheckBoxInspector(self, "unk2", "unk2"),
                                                  CheckBoxInspector(self, "unk3", "unk3"),
                                                  CheckBoxInspector(self, "unk4", "unk4"),
                                                  CheckBoxInspector(self, "unk5", "unk5"),
                                                  CheckBoxInspector(self, "unk6", "unk6"),
                                                  IntegerBoxInspector(self, "unk7", "unk7", int_type=UShort),
                                                  IntegerTwinBoxInspector(self, "unk8", "unk8", int_type=UChar),]
        self.sub_inspector_group["Main Ares"] = [OdvObjectListSubInspector(self, "main_area_in", "From", iterable=self.odv_object.move.main_area_iterator()),
                                                 OdvObjectListSubInspector(self, "main_area_out", "To", iterable=self.odv_object.move.main_area_iterator())]


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

