from PyQt6.QtGui import QColor

from dvd.mask import Mask, MaskImage
from qt.control.inspector_abstract import Inspector
from qt.control.inspector_generic import InfoSubInspector
from qt.control.inspector_graphic import MaskImageSubInspector, GeometrySubInspector
from qt.control.tab__abstract import QTabControlGenericTree
from qt.graphics import GraphicMultiLine


class MaskImageInspector(Inspector):
    odv_object: MaskImage
    deletable = True
    child_name = ""  # cannot add child

    def init_sub_inspector(self):
        self.sub_inspector_group["Bitmap"] = [(msi:=MaskImageSubInspector(self, "image"))]
        msi.opacity_slider.setValue(40)
        msi.graphic.setPos(self.odv_object.position)

        self.sub_inspector_group["Info"] = [
            InfoSubInspector(self, "layer_id", "layer_id"),
            InfoSubInspector(self, "flag", "flag"),
            InfoSubInspector(self, "u4", "u4"),

        ]



        self.sub_inspector_group["Multiline"] = []
        if self.odv_object.point_list_1 != []:
            self.sub_inspector_group["Multiline"] += [GeometrySubInspector(self, "point_list_1", "L1", graphic_type=GraphicMultiLine, color=QColor(0, 255, 0))]
        if self.odv_object.point_list_2 != []:
            self.sub_inspector_group["Multiline"] += [GeometrySubInspector(self, "point_list_2", "L2", graphic_type=GraphicMultiLine, color=QColor(0, 0, 255))]
        if self.sub_inspector_group["Multiline"] == []:
            self.sub_inspector_group.pop("Multiline")



class MaskInspector(Inspector):
    deletable = False
    child_name = "Mask Image"

    # def new_odv_child(self):



class QMaskTabControl(QTabControlGenericTree):
    inspector_types = {Mask: MaskInspector,
                       MaskImage: MaskImageInspector}
