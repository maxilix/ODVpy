from odv.data_section.sght import Sght, SightObstacle
from qt.control.generic_inspector import Inspector

from qt.control.generic_tree import QGenericTreeItem


class SightObstacleInspector(Inspector):
    def __init__(self):
        super().__init__()
        self.main_layout.addStretch()

    def connect_to(self, new_items):
        super().connect_to(new_items)


class SightObstacleItem(QGenericTreeItem):

    def __init__(self, section_control, sight_obstacle: SightObstacle):
        super().__init__(section_control, sight_obstacle)
        self.sight_obstacle = sight_obstacle

        # self.graphic_sight_obstacle = GraphicSightObstacle(...)
        # self.add_graphic(self.graphic_sight_obstacle)

#########################################################################

class SghtInspector(Inspector):
    def __init__(self):
        super().__init__()
        self.main_layout.addStretch()

    def connect_to(self, new_items):
        super().connect_to(new_items)


class SghtItem(QGenericTreeItem):

    def __init__(self, section_control, sght:Sght):
        super().__init__(section_control, sght)
        self.sght = sght