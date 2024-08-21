from dvd.mask import Mask, MaskImage
from qt.control.inspector_abstract import Inspector
from qt.control.inspector_graphic import MaskImageSubInspector
from qt.control.tab_abstract import QTabControlGenericTree


class MaskImageInspector(Inspector):
    deletable = True
    child_name = ""  # cannot add child

    def init_sub_inspector(self):
        self.sub_inspector_group["Bitmap"] = [(msi:=MaskImageSubInspector(self, "image"))]
        msi.opacity_slider.setValue(40)
        msi.visibility_checkbox.setChecked(True)
        msi.graphic.setPos(self.odv_object.x, self.odv_object.y)



class MaskInspector(Inspector):
    deletable = False
    child_name = "Mask Image"

    # def new_odv_child(self):
    #     new_lift_area = LiftArea(self.odv_object)
    #     new_lift_area.move = self.odv_object.move
    #
    #     new_lift_area.lift_type = 1
    #     new_lift_area.main_area = None
    #     new_lift_area.main_area_below = None
    #     new_lift_area.main_area_above = None
    #     new_lift_area.gateway_below = self._tab_control.scene.new_centered_gateway(scale=0.2)
    #     new_lift_area.gateway_above = self._tab_control.scene.new_centered_gateway(scale=0.2)
    #     new_lift_area.perspective = 0
    #
    #     return new_lift_area


class QMaskTabControl(QTabControlGenericTree):
    inspector_types = {Mask: MaskInspector,
                       MaskImage: MaskImageInspector}
