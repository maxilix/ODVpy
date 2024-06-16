from math import ceil

from PyQt6.QtCore import QRectF, Qt, QPointF
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter, QPainterPath, QFont
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsPathItem, QGraphicsPolygonItem, QGraphicsLineItem, \
    QGraphicsSimpleTextItem

from .abstract_view import View, HierarchicalView


# class QViewPathLink(View, QGraphicsLineItem):
#     def __init__(self, scene, control):
#         super().__init__(control, control.path_link.QLineF())
#         self.main_color = QColor(0, 255, 255)
#
#         pen_color = self.main_color
#         pen_color.setAlpha(128)
#         pen = QPen(pen_color)
#         pen.setWidth(1)
#         pen.setStyle(Qt.PenStyle.DotLine)
#
#         self.setPen(pen)
#         scene.addItem(self)
#         font = QFont()
#         font.setPixelSize(10)
#
#         p1 = QPointF(control.path_link.point1.point.x, control.path_link.point1.point.y)
#         p2 = QPointF(control.path_link.point2.point.x, control.path_link.point2.point.y)
#
#         t1_text = f"{control.path_link.unk_obj_list[0].t1}"
#         self.t1_text_item = QGraphicsSimpleTextItem(t1_text)
#         self.t1_text_item.setFont(font)
#         self.t1_text_item.setPos(0.1*p1 + 0.9*p2)
#         scene.addItem(self.t1_text_item)
#
#         t2_text = f"{control.path_link.unk_obj_list[0].t2}"
#         self.t2_text_item = QGraphicsSimpleTextItem(t2_text)
#         self.t2_text_item.setFont(font)
#         self.t2_text_item.setPos(0.9*p1+0.1*p2)
#         scene.addItem(self.t2_text_item)
#
#
#
#
#         self.setVisible(False)
#
#     def setVisible(self, visible):
#         self.t1_text_item.setVisible(visible)
#         self.t2_text_item.setVisible(visible)
#         super().setVisible(visible)


class QViewPathLink(View, QGraphicsItem):
    def __init__(self, scene, control):
        super().__init__(control)

        self.main_color = QColor(0, 255, 255)
        pen_color = self.main_color
        pen_color.setAlpha(127)
        self.pen = QPen(pen_color)
        self.pen.setWidth(1)
        self.pen.setStyle(Qt.PenStyle.DotLine)
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        self.setVisible(False)
        scene.addItem(self)

    def boundingRect(self) -> QRectF:
        l = self.control.path_link.QLineF()
        x = min(l.x1(), l.x2())
        y = min(l.y1(), l.y2())
        w = max(l.x1(), l.x2()) - min(l.x1(), l.x2())
        h = max(l.y1(), l.y2()) - min(l.y1(), l.y2())
        return QRectF(x, y, w, h)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(self.pen)
        painter.drawLine(self.control.path_link.QLineF())

        font_size = 6
        font = painter.font()
        font.setPixelSize(font_size)
        painter.setFont(font)
        pen_color = self.main_color
        pen_color.setAlpha(255)
        painter.setPen(pen_color)

        pl = self.control.path_link
        t1 = " ".join([str(e) for e in pl.link_viability[0].start_viabilities])
        t2 = " ".join([str(e) for e in pl.link_viability[0].end_viabilities])

        p1 = QPointF(pl.start_position.position.x, pl.start_position.position.y)
        p2 = QPointF(pl.end_position.position.x, pl.end_position.position.y)
        p2, p1 = 0.9*p1 + 0.1*p2, 0.1*p1 + 0.9*p2  # swap p1 and p2

        painter.drawText(QRectF(p1.x() - font_size, p1.y() - font_size, 2*font_size, 2*font_size),
                         Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter, t1)
        painter.drawText(QRectF(p2.x() - font_size, p2.y() - font_size, 2*font_size, 2*font_size),
                         Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter, t2)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path


class QViewCrossingPoint(HierarchicalView, QGraphicsItem):
    def __init__(self, scene, control):
        super().__init__(control)
        for m, _ in enumerate(self.control):
            self.view_list.append(QViewPathLink(scene, self.control[m]))

        self.size = 3
        self.nb_pathfinder = len(self.control.crossing_point.accesses)

        self.setVisible(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.setPos(self.control.crossing_point.QPointF())  # - QPointF(self.size / 2, self.size / 2))
        scene.addItem(self)

    def boundingRect(self) -> QRectF:
        return QRectF(1 - 1.5*self.nb_pathfinder - self.size/2,
                      -2 - self.size/2,
                      self.size + 3*self.nb_pathfinder - 2,
                      self.size + 4)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # draw cross
        cross_pen = QPen(QColor(0, 180, 255, 255))
        cross_pen.setWidth(1)
        cross_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(cross_pen)

        painter.drawLine(QPointF(-self.size/2, -self.size/2), QPointF(self.size/2, self.size/2))
        painter.drawLine(QPointF(-self.size/2, self.size/2), QPointF(self.size/2, -self.size/2))

        # draw accesses
        allow_pen = QPen(QColor(0, 255, 0, 255))
        allow_pen.setWidth(1)
        allow_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        disallow_pen = QPen(QColor(255, 0, 0, 255))
        disallow_pen.setWidth(1)
        disallow_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        access_pens = (disallow_pen, allow_pen)

        for path_index in range(self.nb_pathfinder):
            accesses = self.control.crossing_point.accesses[path_index]
            access_NE = bool(accesses & 0b0001)
            access_NW = bool(accesses & 0b0010)
            access_SW = bool(accesses & 0b0100)
            access_SE = bool(accesses & 0b1000)

            painter.setPen(access_pens[access_NE])
            painter.drawPoint(QPointF(1.5 + 1.5*path_index - 1.5*self.nb_pathfinder - self.size/2, -1.5 - self.size/2))

            painter.setPen(access_pens[access_NW])
            painter.drawPoint(QPointF(self.size/2 + 1.5*path_index, -1.5 - self.size/2))

            painter.setPen(access_pens[access_SW])
            painter.drawPoint(QPointF(self.size/2 + 1.5*path_index, 1.5 + self.size/2))

            painter.setPen(access_pens[access_SE])
            painter.drawPoint(QPointF(1.5 + 1.5*path_index - 1.5*self.nb_pathfinder - self.size/2, 1.5 + self.size/2))

        # # draw W rect:
        # w_rect_pen = QPen(QColor(255, 255, 255, 255))
        # w_rect_pen.setWidthF(0.1)
        # w_rect_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        # w_rect_brush = QBrush(QColor(255, 255, 255, 64))
        # painter.setPen(w_rect_pen)
        # painter.setBrush(w_rect_brush)
        # w = ([6.0, 3.0], [11.0, 6.0], [19.0, 11.0])
        # for e in w:
        #     painter.drawRect(QRectF(-2*e[0], -2*e[1], 4*e[0], 4*e[1]))

    def shape(self):
        path = QPainterPath()
        path.addRect(QRectF(-self.size/2, -self.size/2, self.size, self.size))
        # path.addRect(self.boundingRect())
        return path

    def refresh(self, mousse_position):
        pass

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.size *= 1.5
        self.update(self.boundingRect())

class QViewArea(HierarchicalView, QGraphicsPolygonItem):
    def __init__(self, scene, control):
        super().__init__(control, control.area.QPolygonF())
        for l, _ in enumerate(self.control):
            self.view_list.append(QViewCrossingPoint(scene, self.control[l]))

        if self.control.area.main:
            self.main_color = QColor(160, 200, 40)
        else:
            self.main_color = QColor(255, 90, 40)

        pen_color = self.main_color
        pen_color.setAlpha(128)
        pen = QPen(pen_color)
        pen.setWidth(1)

        brush_color = self.main_color
        brush_color.setAlpha(32)
        brush = QBrush(brush_color)

        self.setVisible(False)
        self.setPen(pen)
        self.setBrush(brush)

        scene.addItem(self)

    def refresh(self, mousse_position):
        if self.control.area.main:
            pass
        else:
            brush_color = self.main_color
            if self.polygon().containsPoint(mousse_position, Qt.FillRule.OddEvenFill):
                self.control.setSelected(True)
                brush_color.setAlpha(64)
                self.setBrush(QBrush(brush_color))
                self.setVisible(True)
            else:
                self.control.setSelected(False)
                brush_color.setAlpha(32)
                self.setBrush(QBrush(brush_color))
                if self.control.checkState(0) == Qt.CheckState.Checked:
                    self.setVisible(True)
                else:
                    self.setVisible(False)

        for view in self.view_list:
            view.refresh(mousse_position)


class QViewSublayer(HierarchicalView, QGraphicsPathItem):
    def __init__(self, scene, control):
        super().__init__(control, control.sublayer.allow_QPainterPath())
        # super(QGraphicsPathItem, self).__init__(control)
        for k, _ in enumerate(self.control):
            self.view_list.append(QViewArea(scene, self.control[k]))

        # self.graphic_area_list = []
        # for k, _ in enumerate(self.control_sublayer.sublayer):
        #     graphic_area = QViewArea(self.control_sublayer.control_area_list[k])
        #     self.graphic_area_list.append(graphic_area)

        # self.main_color = QColor(64, 128, 64)
        self.main_color = QColor(180, 110, 30)

        pen_color = self.main_color
        pen_color.setAlpha(128)
        pen = QPen(pen_color)
        pen.setWidth(1)

        # brush_color = self.main_color
        # brush_color.setAlpha(16)
        # brush = QBrush(brush_color)

        self.setVisible(False)
        self.setPen(pen)
        # self.setBrush(brush)
        scene.addItem(self)

    def refresh(self, mousse_position):
        # if self.isVisible():
        #     brush_color = self.main_color
        #     if self.path().contains(mousse_position):
        #         brush_color.setAlpha(32)
        #     else:
        #         brush_color.setAlpha(16)
        #     self.setBrush(QBrush(brush_color))
        for view in self.view_list:
            view.refresh(mousse_position)


class QViewLayer(HierarchicalView):
    def __init__(self, scene, control):
        super().__init__(control)

        for j, _ in enumerate(self.control):
            self.view_list.append(QViewSublayer(scene, self.control[j]))

    def refresh(self, mousse_position):
        for view in self.view_list:
            view.refresh(mousse_position)


class QViewMotion(HierarchicalView):
    def __init__(self, scene, control):
        super().__init__(control)

        for i, _ in enumerate(self.control):
            self.view_list.append(QViewLayer(scene, self.control[i]))


    def refresh(self, mousse_position):
        for view in self.view_list:
            view.refresh(mousse_position)
