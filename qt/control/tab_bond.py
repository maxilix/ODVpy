from PyQt6.QtGui import QColor

from odv.data_section.bond import BondLine, Bond
from qt.control.inspector_abstract import Inspector
from qt.control.inspector_generic import OdvObjectListSubInspector
from qt.control.inspector_graphic import GeometrySubInspector
from qt.control.tab__abstract import QTabControlGenericTree


# class GraphicBondLine(QCGFixedLine):
#     def __init__(self, odv_object):
#         super().__init__(odv_object)
#         self.setPen(QCGPen(QColor(0, 180, 255)))
#
#     def paint(self, painter: QPainter, option, widget=None):
#         super().paint(painter, option, widget)
#         if self.visible:
#             painter.setRenderHints(QPainter.RenderHint.Antialiasing)
#             line = self.line()
#             length = line.length()
#             rot90 = QTransform(0, 1, -1, 0, 0, 0)
#             font_size = 6
#             left_point = rot90.map(line.p2() - line.p1()) / length * font_size + (line.p1() + line.p2()) / 2
#             right_point = rot90.map(line.p1() - line.p2()) / length * font_size + (line.p1() + line.p2()) / 2
#             font = painter.font()
#             font.setPixelSize(font_size)
#             painter.setFont(font)
#
#             painter.drawText(
#                 QRectF(left_point.x() - 2*font_size, left_point.y() - 2*font_size, 4 * font_size, 4 * font_size),
#                 Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter, self.text_l)
#             painter.drawText(
#                 QRectF(right_point.x() - 2*font_size, right_point.y() - 2*font_size, 4 * font_size, 4 * font_size),
#                 Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter, self.text_r)
#
#     def update(self, rect: QRectF = QRectF()):
#         super().update(rect)
#         self.setLine(QLineF(self.odv_object.p1, self.odv_object.p2))
#         self.text_r = str(self.odv_object.right_id)
#         self.text_l = str(self.odv_object.left_id)


class BondLineInspector(Inspector):
    deletable = True
    child_name = ""  # cannot add child

    def init_sub_inspector(self):
        self.sub_inspector_group["Properties"] = [
            OdvObjectListSubInspector(self, "layer", "Layer", iterable=self.odv_object.move),
            OdvObjectListSubInspector(self, "sight_obstacle_1", "Sight",
                                      iterable=self.odv_object.sght.walkable_sight_iterator()),
            OdvObjectListSubInspector(self, "sight_obstacle_2", "Sight",
                                      iterable=self.odv_object.sght.walkable_sight_iterator()),
        ]
        self.sub_inspector_group["Line"] = [
            GeometrySubInspector(self, "line", color=QColor(0, 180, 255)),
        ]




class BondInspector(Inspector):
    deletable = False
    child_name = "Bond Line"

    def new_odv_child(self):
        new_bond_line = BondLine(self.odv_object)
        new_bond_line.move = self.odv_object.move
        new_bond_line.sght = self.odv_object.sght
        new_bond_line.line = self._tab_control.scene.new_centered_line(scale=0.25)
        new_bond_line.sight_obstacle_1 = None
        new_bond_line.sight_obstacle_2 = None
        new_bond_line.layer = None
        return new_bond_line


class QBondTabControl(QTabControlGenericTree):
    inspector_types = {Bond: BondInspector,
                       BondLine: BondLineInspector}
