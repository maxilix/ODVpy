from odv.data_section.mask import Mask, MaskLayer, MaskEntry
from qt.control.control_section import QSectionControl
from qt.control.generic_inspector import Inspector, QVisibilitySIW
from qt.control.generic_tree import QGenericTreeItem
from qt.graphics import GraphicMask


class MaskEntryInspector(Inspector):
    def __init__(self):
        super().__init__()

        self.visibility_siw = QVisibilitySIW(title="Binary mask", opacity_slider=True, edit_buttons=True)
        self.visibility_siw.update_required.connect(self.update)
        self.main_layout.addWidget(self.visibility_siw)

        self.main_layout.addStretch()

    def connect_to(self, new_items):
        super().connect_to(new_items)
        self.visibility_siw.connect_to([item.graphic_mask for item in self.items])


class MaskEntryItem(QGenericTreeItem):
    inspector_type = MaskEntryInspector
    draggable = True

    def __init__(self, section_control, mask_entry: MaskEntry):
        super().__init__(section_control, mask_entry)
        self.mask_entry = mask_entry

        self.graphic_mask = GraphicMask(self, self.mask_entry.mask_image, self.mask_entry.position)
        self.add_graphic(self.graphic_mask)

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
