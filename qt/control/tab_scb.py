from qt.control.widget_inspector import QInspectorWidget
from qt.control.inspector_generic import InfoSubInspector, LongTextSubInspector
from qt.control.main_tab import QMainTab
from scb.scb_parser import ScbClassGroup, ScbClass, ScbFunction


class ScbFunctionQInspectorWidget(QInspectorWidget):
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


class ScbClassQInspectorWidget(QInspectorWidget):
    deletable = True
    child_name = "Function"

    def init_sub_inspector(self):
        pass



class ScbClassGroupQInspectorWidget(QInspectorWidget):
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


class QScbTabControl(QMainTab):
    inspector_types = {ScbClassGroup: ScbClassGroupQInspectorWidget,
                       ScbClass: ScbClassQInspectorWidget,
                       ScbFunction: ScbFunctionQInspectorWidget}
