from PyQt6.QtCore import QLineF, QRectF, Qt
from PyQt6.QtGui import QPainter, QTransform, QPen, QColor
from PyQt6.QtWidgets import QFormLayout, QPushButton

from qt.control.q_inspector import Inspector, GraphicInspectorWidget, IntegerLineEditInspectorWidget
from qt.control.q_tab_control import QTabControlGenericTree
from qt.graphics.common import QThinPen
from qt.graphics.line import QCGFixedLine


class QBondLinkLineItem(QCGFixedLine):
    def __init__(self, odv_object):
        super().__init__(odv_object)

        self.setPen(QThinPen(QColor(0, 180, 255)))


    def paint(self, painter: QPainter, option, widget=None):
        super().paint(painter, option, widget)
        if self.visible:
            painter.setRenderHints(QPainter.RenderHint.Antialiasing)
            l = self.line()
            length = l.length()
            rotate = QTransform(0, 1, -1, 0, 0, 0)
            font_size = 6
            left_point = rotate.map(l.p2() - l.p1()) / length * font_size + (l.p1() + l.p2()) / 2
            right_point = rotate.map(l.p1() - l.p2()) / length * font_size + (l.p1() + l.p2()) / 2
            font = painter.font()
            font.setPixelSize(font_size)
            painter.setFont(font)

            painter.drawText(
                QRectF(left_point.x() - font_size, left_point.y() - font_size, 2 * font_size, 2 * font_size),
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter, self.text_l)
            painter.drawText(
                QRectF(right_point.x() - font_size, right_point.y() - font_size, 2 * font_size, 2 * font_size),
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter, self.text_r)

    def update(self, rect: QRectF = QRectF()):
        super().update(rect)
        self.setLine(QLineF(self.odv_object.p1, self.odv_object.p2))
        self.text_r = str(self.odv_object.right_id)
        self.text_l = str(self.odv_object.left_id)




class BondLinkInspector(Inspector):
    def init_sections(self):
        sub_layout = QFormLayout()
        sub_layout.setHorizontalSpacing(15)

        graphic = QBondLinkLineItem(self.odv_object)
        self.scene.addItem(graphic)
        sub_layout.addRow("Line", GraphicInspectorWidget(graphic))

        sub_layout.addRow("Layer index", IntegerLineEditInspectorWidget(self.odv_object, "layer_id"))

        b = QPushButton("Button")
        b.clicked.connect(self.bc)
        sub_layout.addRow("Test", b)


        self.main_layout.addLayout(sub_layout)

    def bc(self):
        print(self)
        print(self.tree_item().inspector())

class QBondTabControl(QTabControlGenericTree):
    inspector_types = [BondLinkInspector]
