from PyQt6.QtGui import QColor

from dvd.scrp import Scrp, Script
from qt.control.widget_inspector import QInspectorWidget
from qt.control.inspector_generic import InfoSubInspector
from qt.control.inspector_graphic import GeometrySubInspector
from qt.control.main_tab import QMainTab


class ScriptQInspectorWidget(QInspectorWidget):
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


class ScrpQInspectorWidget(QInspectorWidget):
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


class QScrpTabControl(QMainTab):
    inspector_types = {Scrp: ScrpQInspectorWidget,
                       Script: ScriptQInspectorWidget}
