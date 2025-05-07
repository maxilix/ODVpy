from odv.data_section import Misc
from qt.control.control_section import QSectionControl
from qt.control.generic_inspector import Inspector
from qt.control.generic_tree import QGenericTreeItem
from qt.control.sub_inspector import InfoQSIW


class MiscInspector(Inspector):
    def __init__(self):
        super().__init__()

        self.add_sub_inspector(InfoQSIW(self, "info"))



class MiscItem(QGenericTreeItem):
    inspector_type = MiscInspector

    def __init__(self,section_control, misc:Misc):
        super().__init__(section_control, misc)
        self.misc = misc

    @property
    def info(self):
        return (f"b0:\t{int.from_bytes(self.misc.b0)}\n"
                f"f:\t{self.misc.f}\n"
                f"b1:\t{int.from_bytes(self.misc.b1)}\n"
                f"radius:\t{self.misc.muwStandardViewPolygonRadius}\n"
                f"hearing:\t{self.misc.hearing_factor}\n"
                f"night :\t{self.misc.night}\n"
                f"b2:\t{int.from_bytes(self.misc.b2)}\n"
                f"tail:\t{self.misc.tail}\n")




class QMiscControl(QSectionControl):
    item_types = {Misc: MiscItem}

