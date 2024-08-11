from PyQt6.QtCore import QLineF, QRectF, Qt
from PyQt6.QtGui import QPainter, QTransform, QPen, QColor
from PyQt6.QtWidgets import QFormLayout, QPushButton

from dvd.bond import BondLine
from dvd.move import Layer
from qt.control.q_inspector import Inspector, PolygonInspectorWidget, OdvObjectComboBoxInspector, UShortSpinBoxInspector
from qt.control.q_tab_control import QTabControlGenericTree
from qt.graphics.common import QCGPen
from qt.graphics.line import QCGFixedLine


class GraphicBondLine(QCGFixedLine):
    def __init__(self, odv_object):
        super().__init__(odv_object)
        self.setPen(QCGPen(QColor(0, 180, 255)))

    def paint(self, painter: QPainter, option, widget=None):
        super().paint(painter, option, widget)
        if self.visible:
            painter.setRenderHints(QPainter.RenderHint.Antialiasing)
            line = self.line()
            length = line.length()
            rot90 = QTransform(0, 1, -1, 0, 0, 0)
            font_size = 6
            left_point = rot90.map(line.p2() - line.p1()) / length * font_size + (line.p1() + line.p2()) / 2
            right_point = rot90.map(line.p1() - line.p2()) / length * font_size + (line.p1() + line.p2()) / 2
            font = painter.font()
            font.setPixelSize(font_size)
            painter.setFont(font)

            painter.drawText(
                QRectF(left_point.x() - 2*font_size, left_point.y() - 2*font_size, 4 * font_size, 4 * font_size),
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter, self.text_l)
            painter.drawText(
                QRectF(right_point.x() - 2*font_size, right_point.y() - 2*font_size, 4 * font_size, 4 * font_size),
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter, self.text_r)

    def update(self, rect: QRectF = QRectF()):
        super().update(rect)
        self.setLine(QLineF(self.odv_object.p1, self.odv_object.p2))
        self.text_r = str(self.odv_object.right_id)
        self.text_l = str(self.odv_object.left_id)


class BondLineInspector(Inspector):
    def init_prop_section(self):
        graphic = GraphicBondLine(self.odv_object)
        self.scene.addItem(graphic)
        self.prop["Line"] = PolygonInspectorWidget(graphic)
        self.prop["Line"].changed.connect(self.set_line)

        self.prop["Layer"] = OdvObjectComboBoxInspector(self.odv_object.layer)
        self.prop["Layer"].changed.connect(self.set_layer)

        self.prop["Right id"] = UShortSpinBoxInspector(self.odv_object.right_id)
        self.prop["Right id"].changed.connect(self.set_right_id)

        self.prop["Left id"] = UShortSpinBoxInspector(self.odv_object.left_id)
        self.prop["Left id"].changed.connect(self.set_left_id)

    def set_line(self, line):
        self.odv_object.p1 = line.p1()
        self.odv_object.p2 = line.p2()

    def set_layer(self, layer):
        self.odv_object.layer = layer

    def set_right_id(self, right_id):
        self.odv_object.right_id = right_id
        self.prop["Line"].graphic.update()

    def set_left_id(self, left_id):
        self.odv_object.left_id = left_id
        self.prop["Line"].graphic.update()


class QBondTabControl(QTabControlGenericTree):
    graphic_types = {BondLine: [GraphicBondLine]}
    inspector_types = {BondLine: BondLineInspector}
