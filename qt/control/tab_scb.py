from qt.control.generic_inspector import Inspector
from qt.control._sub_inspector import InfoSubInspector, LongTextSubInspector
from qt.control.control_section import QTabControlGenericTree
from odv.parser.scb_parser import ScbClassGroup, ScbClass, ScbFunction


class ScbFunctionInspector(Inspector):
    deletable = True
    child_name = ""  # cannot add child

    def init_sub_inspector(self):
        self.sub_inspector_group["Info"] = [
            InfoSubInspector(self, "info"),
            LongTextSubInspector(self, "text"),
        ]



    @property
    def info(self):
        return f"{len(self.odv_object.quad)} quads"

    @property
    def text(self):
        rop = ""
        for q in self.odv_object.quad:
            rop+= f"{str(q)}\n"
        return rop[:-1]


class ScbClassInspector(Inspector):
    deletable = True
    child_name = "Function"

    def init_sub_inspector(self):
        pass



class ScbClassGroupInspector(Inspector):
    deletable = False
    child_name = "Class"

    # def new_odv_child(self):
    #     new_bond_line = BondLine(self.odv_object)
    #     new_bond_line.move = self.odv_object.move
    #     new_bond_line.line = self._tab_control.scene.new_centered_line(scale=0.25)
    #     new_bond_line.left_id = 0
    #     new_bond_line.right_id = 0
    #     new_bond_line.layer = None
    #     return new_bond_line


class QScbTabControl(QTabControlGenericTree):
    inspector_types = {ScbClassGroup: ScbClassGroupInspector,
                       ScbClass: ScbClassInspector,
                       ScbFunction: ScbFunctionInspector}
