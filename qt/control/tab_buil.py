from PyQt6.QtGui import QColor, QPolygonF

from common import *
from dvd.buil import Door, Building, SpecialDoors, Buildings
from qt.control.inspector_abstract import Inspector
from qt.control.inspector_generic import IntegerBoxInspector, InfoSubInspector, ConstantEnumListInspector, \
    MultiCheckBoxInspector, CheckBoxInspector, IntegerTwinBoxInspector, OdvObjectListSubInspector
from qt.control.inspector_graphic import GeometrySubInspector
from qt.control.tab__abstract import QTabControlGenericTree

DOOR_TYPE = {0: "Invisible Door",
             1: "Normal Door",
             2: "Trapdoor"}


class DoorInspector(Inspector):
    deletable = True
    child_name = ""

    def init_sub_inspector(self):
        if self.odv_object.door_type == 3:  # special door
            self.sub_inspector_group["Properties"] = [
                CheckBoxInspector(self, "enable", "Enable?"),
                MultiCheckBoxInspector(self, "lock_state", "Lock", label_list=["locked", "unlockable"], column=2, conditional=[None, 0]),
                CheckBoxInspector(self, "unk_bool_3", "unk_bool_3"),
                CheckBoxInspector(self, "unk_bool_4", "unk_bool_4"),
                CheckBoxInspector(self, "unk_bool_5", "unk_bool_5"),
                CheckBoxInspector(self, "unk_bool_6", "unk_bool_6"),
                CheckBoxInspector(self, "unk_bool_7", "unk_bool_7"),
                CheckBoxInspector(self, "unk_bool_8", "unk_bool_8"),
                IntegerBoxInspector(self, "anim_id", "anim_id", int_type=UShort),
                IntegerTwinBoxInspector(self, "allowed_sens", "allowed_sens", int_type=UChar),
            ]
        else:
            self.sub_inspector_group["Properties"] = [
                ConstantEnumListInspector(self, "door_type", "Type", enum=DOOR_TYPE),
                CheckBoxInspector(self, "enable", "Enable?"),
                MultiCheckBoxInspector(self, "lock_state", "Lock", label_list=["locked", "unlockable"], column=2, conditional=[None, 0]),
                CheckBoxInspector(self, "unk_bool_3", "unk_bool_3"),
                CheckBoxInspector(self, "unk_bool_4", "unk_bool_4"),
                CheckBoxInspector(self, "unk_bool_5", "unk_bool_5"),
                CheckBoxInspector(self, "unk_bool_6", "unk_bool_6"),
                CheckBoxInspector(self, "unk_bool_7", "unk_bool_7"),
                CheckBoxInspector(self, "unk_bool_8", "unk_bool_8"),
                IntegerBoxInspector(self, "anim_id", "anim_id", int_type=UShort),
                IntegerTwinBoxInspector(self, "allowed_sens", "allowed_sens", int_type=UChar), ]
            self.sub_inspector_group["Door Frame"] = [
                GeometrySubInspector(self, "shape", color=QColor(0, 140, 255)),
            ]

        self.sub_inspector_group["Main Areas"] = [
            OdvObjectListSubInspector(self, "main_area_1", "From", iterable=self.odv_object.move.main_area_iterator()),
            OdvObjectListSubInspector(self, "main_area_3", "To", iterable=self.odv_object.move.main_area_iterator()),
        ]
        self.sub_inspector_group["Gateway"] = [
            GeometrySubInspector(self, "gateway", color=QColor(220, 200, 80)),
        ]


    @property
    def lock_state(self):
        return [self.odv_object.locked, self.odv_object.unlockable]

    @lock_state.setter
    def lock_state(self, state):
        self.odv_object.locked = state[0]
        self.odv_object.unlockable = state[1]



class BuildingInspector(Inspector):
    deletable = True
    child_name = "Door"

    def init_sub_inspector(self):
        self.sub_inspector_group["Properties"] = [IntegerBoxInspector(self, "unk1", "unk1", int_type=UShort),
                                                  InfoSubInspector(self, "character_id_list", "char id")]

    def new_odv_child(self):
        new_door = Door(self.odv_object)
        new_door.move = self.odv_object.move
        new_door.door_type = 1  # normal door
        new_door.enable = 1
        new_door.locked = 0
        new_door.unlockable = 0
        new_door.unk_bool_3 = 0
        new_door.unk_bool_4 = 0
        new_door.unk_bool_5 = 0
        new_door.unk_bool_6 = 0
        new_door.unk_bool_7 = 0
        new_door.unk_bool_8 = 0
        new_door.shape = self._tab_control.scene.new_centered_polygon(scale=0.1)
        new_door.gateway = self._tab_control.scene.new_centered_gateway(scale=0.2)
        new_door.main_area_1 = None
        new_door.main_area_3 = None
        new_door.anim_id = UShort.max()
        new_door.allowed_sens = (0,0)
        return new_door



class BuildingsInspector(Inspector):
    deletable = False
    child_name = "Building"

    def new_odv_child(self):
        new_building = Building(self.odv_object)
        new_building.move = self.odv_object.move
        new_building.unk1 = 0
        new_building.character_id_list = []
        return new_building

class SpecialDoorsInspector(Inspector):
    deletable = False
    child_name = "Special Door"

    def new_odv_child(self):
        new_door = Door(self.odv_object)
        new_door.move = self.odv_object.move
        new_door.door_type = 3  # special door
        new_door.enable = 1
        new_door.locked = 0
        new_door.unlockable = 0
        new_door.unk_bool_3 = 0
        new_door.unk_bool_4 = 0
        new_door.unk_bool_5 = 0
        new_door.unk_bool_6 = 0
        new_door.unk_bool_7 = 0
        new_door.unk_bool_8 = 0
        new_door.shape = QPolygonF()
        new_door.gateway = self._tab_control.scene.new_centered_gateway(scale=0.2)
        new_door.main_area_1 = None
        new_door.main_area_3 = None
        new_door.anim_id = UShort.max()
        new_door.allowed_sens = (0,0)
        return new_door


class QBuilTabControl(QTabControlGenericTree):
    inspector_types = {Buildings: BuildingsInspector,
                       SpecialDoors: SpecialDoorsInspector,
                       Building: BuildingInspector,
                       Door: DoorInspector}

