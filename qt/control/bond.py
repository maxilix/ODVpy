from PyQt6.QtCore import QLineF, QRectF, Qt
from PyQt6.QtGui import QColor, QPainter, QTransform
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGridLayout, QLabel, QLineEdit

from qt.control.q_generic_tree import QODVTreeItem
from qt.control.q_odv_item import QODVItem
from qt.control.q_inspector import QDVDInspectorItem
from qt.control.q_tab_control import QTabControlGenericTree
from qt.graphics.line import QCGFixedLine


class QBondLinkGraphicItem(QCGFixedLine):
    def __init__(self, q_dvd_item):
        line = QLineF(q_dvd_item.odv_item.p1, q_dvd_item.odv_item.p2)
        super().__init__(q_dvd_item, line)

    def paint(self, painter: QPainter, option, widget=None):
        if self.visible:
            painter.setRenderHints(QPainter.RenderHint.Antialiasing)
            super().paint(painter, option, widget)
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
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter, str(self.q_dvd_item.odv_item.left_id))
            painter.drawText(
                QRectF(right_point.x() - font_size, right_point.y() - font_size, 2 * font_size, 2 * font_size),
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter, str(self.q_dvd_item.odv_item.right_id))


class QBondLinkInspectorItem(QDVDInspectorItem):
    def __init__(self, q_dvd_item):
        self.properties_layout = QGridLayout()

        label = QLabel("Layer Id")
        self.properties_layout.addWidget(label, 0, 0)
        self.layer_id = QLineEdit()
        self.properties_layout.addWidget(self.layer_id, 0, 1)

        label = QLabel("Left Area Id")
        self.properties_layout.addWidget(label, 1, 0)
        self.left_id = QLineEdit()
        self.properties_layout.addWidget(self.left_id, 1, 1)

        label = QLabel("Right Area Id")
        self.properties_layout.addWidget(label, 2, 0)
        self.right_id = QLineEdit()
        self.properties_layout.addWidget(self.right_id, 2, 1)

        super().__init__(q_dvd_item)


class QBondLinkItem(QODVItem):
    colors = [QColor(0, 180, 255)]
    q_graphic_item_type = QBondLinkGraphicItem
    q_inspector_item_type = QBondLinkInspectorItem
    q_tree_item_type = QODVTreeItem


class QBondTabControl(QTabControlGenericTree):
    q_odv_item_types = [QBondLinkItem]
