from PyQt6.QtCore import QLineF, QRectF
from PyQt6.QtGui import QAction, QTransform, QPainter
from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsItem

from qt.graphics_old import QGraphicsLargeLineItem
from qt.graphics_old.base_elem import OdvGraphicElement
from qt.graphics_old.point_elem import OdvEditPointElement


class OdvArrowElement(OdvGraphicElement, QGraphicsItem):
    def __init__(self, parent_item):
        super().__init__(parent_item)
        self.r_branch = QLineF()
        self.l_branch = QLineF()
        self._base_line = QLineF()
        # wait to have base_line before update

    @property
    def base_line(self):
        return self._base_line

    @base_line.setter
    def base_line(self, base_line: QLineF):
        self._base_line = base_line
        self.update()

    def update(self, rect: QRectF = QRectF()):
        length = self.base_line.length()
        size = 1.3
        vector = (self.base_line.p2() - self.base_line.p1()) / length * size
        center = (self.base_line.p1() + self.base_line.p2()) / 2
        rot90 = QTransform(0, 1, -1, 0, 0, 0)
        rp = center + rot90.map(vector) - 0.8 * vector
        lp = center - rot90.map(vector) - 0.8 * vector
        cp = center + 0.8 * vector
        self.r_branch = QLineF(rp, cp)
        self.l_branch = QLineF(lp, cp)
        super().update(rect)

    def paint(self, painter: QPainter, option, widget=None):
        if self.visible:
            painter.setRenderHints(QPainter.RenderHint.Antialiasing)
            painter.setPen(self.sub_inspector.pen)
            painter.drawLine(self.r_branch)
            painter.drawLine(self.l_branch)

    def shape(self):
        temp_r_branch = QGraphicsLineItem(self.r_branch)
        temp_r_branch.setPen(self.sub_inspector.pen)
        temp_l_branch = QGraphicsLineItem(self.l_branch)
        temp_l_branch.setPen(self.sub_inspector.pen)
        return temp_r_branch.shape() + temp_l_branch.shape()

    def boundingRect(self):
        return self.shape().boundingRect()


class OdvFixLineElement(OdvGraphicElement, QGraphicsLargeLineItem):
    def __init__(self, parent_item, line: QLineF):
        super().__init__(parent_item)
        if (ga := self.parentItem().grid_alignment) is not None:
            line = line.truncated().translated(ga)
        self.setLine(line)
        self.setPen(self.sub_inspector.pen)
        self.update()


class OdvEditLineElement(OdvGraphicElement, QGraphicsLargeLineItem):
    def __init__(self, parent_item, p1: OdvEditPointElement, p2: OdvEditPointElement, secable: bool = False):  # , deletable: bool = False):
        super().__init__(parent_item)
        self.setPen(self.sub_inspector.pen)
        self.secable = secable
        # set the private attribute directly to perform a single update
        self._p1 = p1
        self._p2 = p2
        self.update()

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, value):
        self._p1 = value
        self.update()

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, value):
        self._p2 = value
        self.update()

    def update(self, rect: QRectF = QRectF()):
        temp_line = QLineF(self.p1.pos(), self.p2.pos())
        length = temp_line.length()
        if length > OdvEditPointElement.size:
            p1 = self.p1.pos()
            p2 = self.p2.pos()
            f = (OdvEditPointElement.size / 2) / length
            p1, p2 = (1 - f) * p1 + f * p2, (1 - f) * p2 + f * p1
            self.setLine(QLineF(p1, p2))
        else:
            self.setLine(QLineF())
        super().update(rect)

    def scene_menu_local_actions(self, scene_position):
        rop = []
        if self.secable is True:
            a_add_point = QAction("Add Point")
            a_add_point.triggered.connect(lambda: self.parentItem().add_point(scene_position, self))
            rop.append(a_add_point)
        return rop
