from odv.data_section.mask import Mask, MaskLayer, MaskEntry
from qt.control.control_section import QSectionControl
from qt.control.generic_inspector import Inspector, QGeometrySIW
from qt.control.generic_tree import QGenericTreeItem
from qt.graphics import GraphicMask, GraphicMultiLine


class MaskEntryInspector(Inspector):
    def __init__(self):
        super().__init__()

        self.mask_vsiw = QGeometrySIW(title="Binary mask", opacity_slider=True, edit_buttons=True)
        self.mask_vsiw.update_required.connect(self.update)
        self.main_layout.addWidget(self.mask_vsiw)

        self.l1_vsiw = QGeometrySIW(title="L1", edit_buttons=True)
        self.l1_vsiw.update_required.connect(self.update)
        self.main_layout.addWidget(self.l1_vsiw)

        # self.l2_vsiw = QVisibilitySIW(title="L2", edit_buttons=True)
        # self.l2_vsiw.update_required.connect(self.update)
        # self.main_layout.addWidget(self.l2_vsiw)

        self.main_layout.addStretch()

    def connect_to(self, new_items):
        super().connect_to(new_items)
        self.mask_vsiw.connect_to([item.graphic_mask for item in self.items])
        self.l1_vsiw.connect_to([item.graphic_l1 for item in self.items])
        # self.l2_vsiw.connect_to([item.graphic_l2 for item in self.items])


class MaskEntryItem(QGenericTreeItem):
    inspector_type = MaskEntryInspector
    draggable = True

    def __init__(self, section_control, mask_entry: MaskEntry):
        super().__init__(section_control, mask_entry)
        self.mask_entry = mask_entry

        self.graphic_mask = GraphicMask(self, self.mask_entry.mask_image, self.mask_entry.position)
        self.add_graphic(self.graphic_mask)

        self.graphic_l1 = None
        if self.mask_entry.point_list_1:
            self.graphic_l1 = GraphicMultiLine(self, self.mask_entry.point_list_1)
            self.add_graphic(self.graphic_l1)


#########################################################################

class LayerInspector(Inspector):
    def __init__(self):
        super().__init__()
        self.main_layout.addStretch()

    def connect_to(self, new_items):
        super().connect_to(new_items)



class LayerItem(QGenericTreeItem):
    inspector_type = LayerInspector
    draggable = True

    def __init__(self, section_control, layer: MaskLayer):
        super().__init__(section_control, layer)
        self.layer = layer

#########################################################################

class MaskInspector(Inspector):
    def __init__(self):
        super().__init__()
        self.main_layout.addStretch()

    def connect_to(self, new_items):
        super().connect_to(new_items)


class MaskItem(QGenericTreeItem):
    inspector_type = MaskInspector
    draggable = False

    def __init__(self, section_control, mask:Mask):
        super().__init__(section_control, mask)
        self.mask = mask

#########################################################################

class QMaskControl(QSectionControl):
    item_types = {Mask: MaskItem,
                  MaskLayer: LayerItem,
                  MaskEntry: MaskEntryItem}
