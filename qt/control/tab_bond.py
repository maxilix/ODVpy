from PyQt6.QtCore import QLineF
from PyQt6.QtGui import QColor

from dvd.bond import BondLine
from qt.control.inspector_graphic import GeometrySubInspector
from qt.control.inspector_abstract import Inspector
from qt.control.tab_abstract import QTabControlGenericTree
from qt.control.inspector_generic import OdvObjectListSubInspector, UShortTwinBoxInspector


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
    def init_odv_prop(self):
        self.prop["Line"] = GeometrySubInspector(self, "line", QColor(0, 180, 255))
        self.prop["Layer"] = OdvObjectListSubInspector(self, "layer")
        self.prop["Trigger"] = UShortTwinBoxInspector(self, "trigger_id")

    @property
    def line(self):
        return QLineF(self.odv_object.p1, self.odv_object.p2)

    @line.setter
    def line(self, line):
        self.odv_object.p1 = line.p1()
        self.odv_object.p2 = line.p2()



    # @property
    # def layer(self):
    #     return self.odv_object.layer
    #
    # @layer.setter
    # def layer(self, layer):
    #     self.odv_object.layer = layer

    # def __getattr__(self, attr_name):
    #     print("getattr", attr_name)
    #     if hasattr(self.odv_object, attr_name):
    #         return getattr(self.odv_object, attr_name)
    #     else:
    #         print(f"{self.odv_object} has no attribute {attr_name}")
    #         raise AttributeError
    #
    # def __setattr__(self, attr_name, value):
    #     print("setattr", attr_name)
    #     if hasattr(self.odv_object, attr_name):
    #         setattr(self.odv_object, attr_name, value)
    #     else:
    #         print(f"{self.odv_object} has no attribute {attr_name}")
    #         raise AttributeError


    @property
    def trigger_id(self):
        return (self.odv_object.right_id, self.odv_object.left_id)

    @trigger_id.setter
    def trigger_id(self, trigger_id):
        self.odv_object.right_id = trigger_id[0]
        self.odv_object.left_id = trigger_id[1]


class QBondTabControl(QTabControlGenericTree):
    inspector_types = {BondLine: BondLineInspector}