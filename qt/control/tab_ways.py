from PyQt6.QtGui import QColor

from odv.data_section.ways import Patrol, Waypoint, Ways
from qt.control.control_section import QSectionControl
from qt.control.generic_inspector import Inspector, QVisibilitySIW
from qt.control.generic_tree import QGenericTreeItem
from qt.graphics import GraphicMultiLine, OdvThinPen, OdvLightBrush, OdvHighBrush


class WaypointInspector(Inspector):
    def __init__(self):
        super().__init__()
        self.main_layout.addStretch()

    def connect_to(self, new_items):
        super().connect_to(new_items)



class WaypointItem(QGenericTreeItem):
    inspector_type = WaypointInspector
    draggable = True

    def __init__(self, section_control, waypoint: Waypoint):
        super().__init__(section_control, waypoint)
        self.waypoint = waypoint


#########################################################################

class PatrolInspector(Inspector):
    def __init__(self):
        super().__init__()

        self.patrol_vsiw = QVisibilitySIW(title="Patrol", edit_buttons=True)
        self.patrol_vsiw.update_required.connect(self.update)
        self.main_layout.addWidget(self.patrol_vsiw)

        self.main_layout.addStretch()

    def connect_to(self, new_items):
        super().connect_to(new_items)
        self.patrol_vsiw.connect_to([item.graphic_patrol for item in self.items])



class GraphicPatrol(GraphicMultiLine):
    thin_pen = OdvThinPen(QColor(255, 50, 255))
    light_brush = OdvLightBrush(QColor(255, 50, 255))
    high_brush = OdvHighBrush(QColor(255, 50, 255))


class PatrolItem(QGenericTreeItem):
    inspector_type = PatrolInspector
    draggable = True

    def __init__(self, section_control, patrol: Patrol):
        super().__init__(section_control, patrol)
        self.patrol = patrol

        self.graphic_patrol = GraphicPatrol(self, [w.point for w in self.patrol])
        self.add_graphic(self.graphic_patrol)

#########################################################################

class WaysInspector(Inspector):
    def __init__(self):
        super().__init__()
        self.main_layout.addStretch()

    def connect_to(self, new_items):
        super().connect_to(new_items)


class WaysItem(QGenericTreeItem):
    inspector_type = WaysInspector

    def __init__(self, section_control, ways:Ways):
        super().__init__(section_control, ways)
        self.ways = ways

#########################################################################

class QWaysControl(QSectionControl):
    item_types = {Ways: WaysItem,
                  Patrol: PatrolItem,
                  Waypoint: WaypointItem}
