from PyQt6.QtCore import QLineF, QRectF, QPointF
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QGraphicsLineItem

from qt.graphics.common import OdvGraphicElement, OdvGraphic
from qt.graphics.odv_point import OdvEditPointElement


class OdvFixLineElement(OdvGraphicElement, QGraphicsLineItem):
    def __init__(self, sub_inspector, line: QLineF):
        super().__init__(sub_inspector, line.truncated().translated(0.5, 0.5))
        self.setPen(self.sub_inspector.pen)

    def shape(self):
        # virtually extends the line width for click detection
        temp_line = QGraphicsLineItem(self.line())
        pen = self.pen()
        pen.setWidthF(pen.widthF() * 5)
        temp_line.setPen(pen)
        return temp_line.shape()


class OdvEditLineElement(OdvGraphicElement, QGraphicsLineItem):
    def __init__(self, sub_inspector, p1: OdvEditPointElement, p2: OdvEditPointElement, secable: bool = False, deletable: bool = False):
        super().__init__(sub_inspector)
        self.setPen(self.sub_inspector.pen)
        self._p1 = p1
        self._p2 = p2
        self.secable = secable
        self.deletable = deletable

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

    def delete(self):
        if self.parentItem() is not None:
            self.parentItem().line_deleted(self)
        self.scene().removeItem(self)

    def add_point(self, pos: QPointF):
        deletable = self.p1.deletable or self.p2.deletable
        new_point = OdvEditPointElement(self.sub_inspector, pos, movable=True, deletable=deletable)
        self.scene().addItem(new_point)
        old_p2 = self.p2
        self.p2 = new_point
        new_line = OdvEditLineElement(self.sub_inspector, new_point, old_p2, secable=True)
        self.scene().addItem(new_line)
        if self.parentItem() is not None:
            self.parentItem().point_added(self.p1, new_point, new_line)

    def shape(self):
        # virtually extends the line width for click detection
        temp_line = QGraphicsLineItem(self.line())
        pen = self.pen()
        pen.setWidthF(pen.widthF() * 5)
        temp_line.setPen(pen)
        return temp_line.shape()

    def scene_menu_local_actions(self, scene_position):
        rop = []
        if self.secable is True:
            a_add_point = QAction("Add Point")
            a_add_point.triggered.connect(lambda: self.add_point(scene_position))
            rop.append(a_add_point)

        if self.deletable and self.p1.deletable and self.p2.deletable:
            a_delete = QAction("Delete Line")
            a_delete.triggered.connect(self.delete)
            rop.append(a_delete)

        if self.p1.movable or self.p2.movable:
            a_lock = QAction("Lock Points")
            a_lock.triggered.connect(self.lock)
            rop.append(a_lock)

        if self.p1.movable is False or self.p2.movable is False:
            a_unlock = QAction("Unlock Points")
            a_unlock.triggered.connect(self.unlock)
            rop.append(a_unlock)

        return rop

    def lock(self):
        self.p1.lock()
        self.p2.lock()

    def unlock(self):
        self.p1.unlock()
        self.p2.unlock()


class OdvLine(OdvGraphic):
    def __init__(self, sub_inspector):
        super().__init__(sub_inspector)

        self.line_fix = None
        self.p1_item = None
        self.p2_item = None
        self.line_item = None

        self.exit_edit_mode(save=False)

    @property
    def line(self):
        return self.sub_inspector.current

    @line.setter
    def line(self, line):
        self.sub_inspector.current = line.truncated()

    def enter_edit_mode(self):
        self.remove_child(self.line_fix)
        self.line_fix = None

        self.p1_item = OdvEditPointElement(self.sub_inspector, self.line.p1(), movable=True, deletable=False)
        self.p2_item = OdvEditPointElement(self.sub_inspector, self.line.p2(), movable=True, deletable=False)
        self.line_item = OdvEditLineElement(self.sub_inspector, self.p1_item, self.p2_item, secable=False, deletable=True)
        self.add_child(self.p1_item)
        self.add_child(self.p2_item)
        self.add_child(self.line_item)

        self.update()

    def exit_edit_mode(self, save):
        if save is True:
            self.line = QLineF(self.p1_item.pos(), self.p2_item.pos())

        self.remove_child(self.p1_item)
        self.remove_child(self.p2_item)
        self.remove_child(self.line_item)
        self.p1_item = None
        self.p2_item = None
        self.line_item = None

        self.line_fix = OdvFixLineElement(self.sub_inspector, self.line)
        self.add_child(self.line_fix)

        self.update()

    def point_moved(self, point_item: OdvEditPointElement):
        self.line_item.update()

    def point_deleted(self, point_item: OdvEditPointElement):
        pass

    def line_deleted(self, line_item: OdvEditLineElement):
        # self.p1_item.delete()
        # self.p2_item.delete()
        self.delete()
