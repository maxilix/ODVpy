from PyQt6.QtGui import QColor

from dvd.scrp import Scrp, Script
from qt._control.inspector_abstract import Inspector
from qt._control.inspector_generic import InfoSubInspector
from qt._control.inspector_graphic import GeometrySubInspector
from qt._control.tab__abstract import QTabControlGenericTree


class ScriptInspector(Inspector):
    deletable = True
    child_name = ""  # cannot add child

    def init_sub_inspector(self):
        self.sub_inspector_group["P"] = [
            GeometrySubInspector(self, "p", color=QColor(180, 30, 220)),
        ]
        self.sub_inspector_group["Info"] = [
            InfoSubInspector(self, "classname", "classname"),
            # InfoSubInspector(self, "unk_short_1", "unk_short_1"),
            # InfoSubInspector(self, "unk_short_2", "unk_short_2"),
        ]


class ScrpInspector(Inspector):
    deletable = False
    child_name = "Script"

    # def new_odv_child(self):
    #     new_bond_line = BondLine(self.odv_object)
    #     new_bond_line.move = self.odv_object.move
    #     new_bond_line.line = self._tab_control.scene.new_centered_line(scale=0.25)
    #     new_bond_line.left_id = 0
    #     new_bond_line.right_id = 0
    #     new_bond_line.layer = None
    #     return new_bond_line


class QScrpTabControl(QTabControlGenericTree):
    inspector_types = {Scrp: ScrpInspector,
                       Script: ScriptInspector}
