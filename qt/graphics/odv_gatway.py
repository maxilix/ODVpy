from PyQt6.QtCore import QLineF

from common import Gateway
from qt.graphics.common import OdvGraphic
from qt.graphics.odv_line import OdvArrowElement, OdvEditLineElement, OdvFixLineElement
from qt.graphics.odv_point import OdvEditPointElement


class OdvGraphicGateway(OdvGraphic):

    def __init__(self, sub_inspector):
        super().__init__(sub_inspector)

        p1,p2,p3 = self.gateway

        self.arrow1 = OdvArrowElement(self.sub_inspector, QLineF(p1, p2))
        self.arrow2 = OdvArrowElement(self.sub_inspector, QLineF(p2, p3))
        self.add_child(self.arrow1)
        self.add_child(self.arrow2)

        self.line1_fix = None
        self.line2_fix = None
        self.p1_edit = None
        self.p2_edit = None
        self.p3_edit = None
        self.line1_edit = None
        self.line2_edit = None

        self.exit_edit_mode(save=False)

    @property
    def gateway(self):
        return self.sub_inspector.current

    @gateway.setter
    def gateway(self, gateway):
        self.sub_inspector.current = gateway.truncated()

    def enter_edit_mode(self):
        self.remove_child(self.line1_fix)
        self.remove_child(self.line2_fix)
        self.line1_fix = None
        self.line2_fix = None

        p1,p2,p3 = self.gateway
        self.p1_edit = OdvEditPointElement(self.sub_inspector, p1, movable=True, deletable=False)
        self.p2_edit = OdvEditPointElement(self.sub_inspector, p2, movable=True, deletable=False)
        self.p3_edit = OdvEditPointElement(self.sub_inspector, p3, movable=True, deletable=False)
        self.add_child(self.p1_edit)
        self.add_child(self.p2_edit)
        self.add_child(self.p3_edit)

        self.line1_edit = OdvEditLineElement(self.sub_inspector, self.p1_edit, self.p2_edit, secable=False, deletable=False)
        self.line2_edit = OdvEditLineElement(self.sub_inspector, self.p2_edit, self.p3_edit, secable=False, deletable=False)
        self.add_child(self.line1_edit)
        self.add_child(self.line2_edit)

        self.update()

    def exit_edit_mode(self, save):
        if save is True:
            self.gateway = Gateway(self.p1_edit.pos(), self.p2_edit.pos(), self.p3_edit.pos())

        self.remove_child(self.p1_edit)
        self.remove_child(self.p2_edit)
        self.remove_child(self.p3_edit)
        self.remove_child(self.line1_edit)
        self.remove_child(self.line2_edit)
        self.p1_edit = None
        self.p2_edit = None
        self.p3_edit = None
        self.line1_edit = None
        self.line2_edit = None

        p1, p2, p3 = self.gateway
        l1, l2 = QLineF(p1, p2), QLineF(p2, p3)
        self.line1_fix = OdvFixLineElement(self.sub_inspector, l1)
        self.line2_fix = OdvFixLineElement(self.sub_inspector, l2)
        self.add_child(self.line1_fix)
        self.add_child(self.line2_fix)

        self.arrow1.base_line = l1
        self.arrow2.base_line = l2

        self.update()

    def point_moved(self, point_item: OdvEditPointElement):
        if point_item == self.p1_edit or point_item == self.p2_edit:
            self.line1_edit.update()
            self.arrow1.base_line = QLineF(self.p1_edit.pos(), self.p2_edit.pos())
        if point_item == self.p2_edit or point_item == self.p3_edit:
            self.line2_edit.update()
            self.arrow2.base_line = QLineF(self.p2_edit.pos(), self.p3_edit.pos())


    def point_added(self,
                    previous_point_item: OdvEditPointElement,
                    new_point_item: OdvEditPointElement,
                    new_line_item: OdvEditLineElement):
        raise

    def point_deleted(self, point_item: OdvEditPointElement):
        raise

    def line_deleted(self, line_item: OdvEditLineElement):
        raise

