from PyQt6.QtGui import QColor

from dvd.mask import Mask, MaskEntry
from qt.common.utils import maskimage_to_qimage
from qt.control.inspector_abstract import Inspector
from qt.control.inspector_generic import InfoSubInspector
from qt.control.inspector_graphic import MaskImageSubInspector, GeometrySubInspector
from qt.control.tab__abstract import QTabControlGenericTree
from qt.graphics import GraphicMultiLine


class MaskEntryInspector(Inspector):
    odv_object: MaskEntry
    deletable = True
    child_name = ""  # cannot add child

    def init_sub_inspector(self):
        self.sub_inspector_group["Bitmap"] = [(msi:=MaskImageSubInspector(self, "qimage"))]
        msi.opacity_slider.setValue(40)
        msi.graphic.setPos(self.odv_object.position)

        self.sub_inspector_group["Info"] = [
            InfoSubInspector(self, "layer_id", "layer_id"),
            InfoSubInspector(self, "flag", "flag"),
            InfoSubInspector(self, "u4", "u4"),

        ]



        self.sub_inspector_group["Multiline"] = []
        if self.odv_object.multiline_1 != []:
            self.sub_inspector_group["Multiline"] += [GeometrySubInspector(self, "point_list_1", "L1", graphic_type=GraphicMultiLine, color=QColor(0, 255, 0))]
        if self.odv_object.multiline_2 != []:
            self.sub_inspector_group["Multiline"] += [GeometrySubInspector(self, "point_list_2", "L2", graphic_type=GraphicMultiLine, color=QColor(0, 0, 255))]
        if self.sub_inspector_group["Multiline"] == []:
            self.sub_inspector_group.pop("Multiline")

    @property
    def qimage(self):
        # getter return a QImage
        return maskimage_to_qimage(self.odv_object.maskimage, (0,0,255))

class MaskInspector(Inspector):
    deletable = False
    child_name = "Mask Image"

    # def new_odv_child(self):



class QMaskTabControl(QTabControlGenericTree):
    inspector_types = {Mask: MaskInspector,
                       MaskEntry: MaskEntryInspector}
