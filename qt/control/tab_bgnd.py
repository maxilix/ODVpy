from odv.data_section import Bgnd
from qt.common.utils import image_to_qimage
from qt.control.control_section import QSectionControl
from qt.control.generic_inspector import Inspector
from qt.control.generic_tree import QGenericTreeItem
from qt.control.sub_inspector import MapPropertyWidget
from qt.graphics import GraphicMap


class BgndInspector(Inspector):
    def __init__(self):
        super().__init__()
        self.item = self.item_list[0]

        self.add_sub_inspector(MapPropertyWidget(self.item.map_gitem))

    def update(self):
        super().update()




class BgndItem(QGenericTreeItem):
    inspector_type = BgndInspector

    def __init__(self, section_control, bgnd:Bgnd):
        super().__init__(section_control, bgnd)
        self.bgnd = bgnd

        self.map_gitem = GraphicMap(image_to_qimage(self.bgnd.map_image))
        self.scene.addItem(self.map_gitem)








class QBgndControl(QSectionControl):
    item_types = {Bgnd: BgndItem}

