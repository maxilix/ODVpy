from PyQt6.QtGui import QColor

from odv.data_section.jump import Jump, JumpArea
from qt.control.generic_inspector import Inspector
from qt.control._sub_inspector import OdvObjectListSubInspector, LongTextSubInspector
from qt.control.inspector_graphic import GeometrySubInspector
from qt.control.control_section import QTabControlGenericTree
from qt.graphics import GraphicMultiLine


class JumpAreaInspector(Inspector):
    deletable = True
    child_name = ""  # cannot add child

    def init_sub_inspector(self):

        self.sub_inspector_group["Infos"] = [
            LongTextSubInspector(self, "text"),
        ]
        self.sub_inspector_group["Properties"] = [
            OdvObjectListSubInspector(self, "roof_sector", "Roof Sector", iterable=self.odv_object.move.sector_iterator(include_None=False)),
            OdvObjectListSubInspector(self, "ground_sector", "Ground Sector",
                                      iterable=self.odv_object.move.sector_iterator(include_None=False)),
        ]
        self.sub_inspector_group["Graphics"] = [
            GeometrySubInspector(self, "landing_polygon", "Landing", color=QColor(255, 255, 255)),
            GeometrySubInspector(self, "first_point", "First point", color=QColor(255, 0, 0)),
            GeometrySubInspector(self, "jump_start_line", "Line", graphic_type=GraphicMultiLine, color=QColor(0, 255, 0)),
        ]

    @property
    def jump_start_line(self):
        return [e.p for e in self.odv_object.jump_start_list]

    @property
    def first_point(self):
        return self.odv_object.jump_start_list[0].p

    @property
    def text(self):
        rop = ""
        for e in self.odv_object.jump_start_list:
            rop += f"{e.u1} {e.u2} {e.u3}\n"
        return rop[:-1]


class JumpInspector(Inspector):
    deletable = False
    child_name = "Jump Area"

    # def new_odv_child(self):
    #     new_jump_area = JumpArea(self.odv_object)
    #     new_jump_area.move = self.odv_object.move
    #
    #     return new_Jump_area


class QJumpTabControl(QTabControlGenericTree):
    inspector_types = {Jump: JumpInspector,
                       JumpArea: JumpAreaInspector}
