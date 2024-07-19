from math import floor
from typing import Self, Iterator

from PyQt6.QtCore import Qt, QRectF, QLineF, QPointF, pyqtSignal, QObject
from PyQt6.QtGui import QColor, QPen, QBrush, QPainter, QPainterPath, QAction, QCursor, QContextMenuEvent, QMouseEvent, \
    QPolygonF, QPolygon
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QTabWidget, QLabel, QVBoxLayout, QCheckBox, QWidget, \
    QScrollArea, QPushButton, QHBoxLayout, QSpinBox, QGraphicsScene, \
    QGraphicsItem, QMenu, QGraphicsPolygonItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsItemGroup, \
    QGraphicsObject, QGraphicsPathItem

from dvd.move import Obstacle, MovePolygon
from qt.control.common import QControl
from qt.scene import QScene


# class QGraphicsArea(QGraphicsItem):
#
#     def __init__(self, main_color: QColor,  area: Obstacle, scene: QGraphicsScene, control):
#         super().__init__()
#         self.area = area
#         self.control = control
#         self.main_color = main_color
#
#         self.poly_pen_color = self.main_color
#         self.poly_pen_color.setAlpha(255)
#         self.poly_pen = QPen(self.poly_pen_color)
#         self.poly_pen.setWidthF(0.4)
#         self.poly_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
#
#         self.poly_brush_color = self.main_color
#         self.poly_brush_color.setAlpha(32)
#         self.poly_brush = QBrush(self.poly_brush_color)
#
#         self._highlightable = True
#         self._highlight = False
#         self._visible = True
#
#         scene.addItem(self)
#         # self.setAcceptHoverEvents(True)
#         self.setAcceptTouchEvents(True)
#
#     def setVisible(self, visible: bool) -> None:
#         self._visible = visible
#         super().setVisible(self._visible or self._highlightable)
#         self.update()
#
#     def setHighlight(self, highlightable: bool) -> None:
#         self._highlightable = highlightable
#         super().setVisible(self._visible or self._highlightable)
#         self.update()
#
#     def boundingRect(self) -> QRectF:
#         r = self.area.qpf.boundingRect()
#         r.setX(r.x() - self.poly_pen.widthF() / 2)
#         r.setY(r.y() - self.poly_pen.widthF() / 2)
#         r.setWidth(r.width() + self.poly_pen.widthF())
#         r.setHeight(r.height() + self.poly_pen.widthF())
#         return r
#
#     def paint(self, painter: QPainter, option, widget=None):
#         if self._highlight and self._highlightable:
#             self.poly_brush_color.setAlpha(64)
#         else:
#             if self._visible is True:
#                 self.poly_brush_color.setAlpha(32)
#             else:
#                 # no drawing
#                 return
#
#         self.poly_brush = QBrush(self.poly_brush_color)
#
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#
#         painter.setPen(self.poly_pen)
#         painter.setBrush(self.poly_brush)
#
#         painter.drawPolygon(self.area.qpf.translated(0.5, 0.5), Qt.FillRule.OddEvenFill)
#
#     def shape(self):
#         path = QPainterPath()
#         path.addPolygon(self.area.qpf)
#         return path
#
#     def hoverEnterEvent(self, event):
#         # print("enter")
#         self._highlight = True
#         self.control.setSelected(True)
#         self.update()
#
#     def hoverLeaveEvent(self, event):
#         # print("leave")
#         self._highlight = False
#         self.control.setSelected(False)
#         self.update()
#
#     def mouseMoveEvent(self, event):
#         print("mouse move")
#
#     def mousePressEvent(self, event):
#         if event.button() == Qt.MouseButton.RightButton:
#             self._highlight = True
#             self.control.setSelected(True)
#             menu = QMenu()
#             # header = QAction(f"{self.control.text(0)}")
#             # f = header.font()
#             # f.setBold(True)
#             # header.setFont(f)
#             # header.setEnabled(False)
#             action_show = QAction("Show")
#             action_hide = QAction("Hide")
#             action_edit = QAction("Edit")
#             action_delete = QAction("Delete")
#
#             # menu.addAction(header)
#             menu.addSection(f"{self.control.text(0)}")
#             menu.addAction(action_show)
#             menu.addAction(action_hide)
#             menu.addSeparator()
#             menu.addAction(action_edit)
#             menu.addAction(action_delete)
#
#             action = menu.exec(QCursor.pos())
#
#             if action == action_show:
#                 self.control.setCheckState(0, Qt.CheckState.Checked)
#             elif action == action_hide:
#                 self.control.setCheckState(0, Qt.CheckState.Unchecked)
#             elif action == action_edit:
#                 print("EDIT")
#             elif action == action_delete:
#                 print("DELETE")

# class QGraphicsFixedArea(QGraphicsPolygonItem):
#     def mousePressEvent(self, event):
#         if event.button() == Qt.MouseButton.RightButton:
#             menu = QMenu()
#             action_show = QAction("Show")
#             action_hide = QAction("Hide")
#             action_edit = QAction("Edit")
#             action_delete = QAction("Delete")
#
#             menu.addSection(f"text")
#             menu.addAction(action_show)
#             menu.addAction(action_hide)
#             menu.addSeparator()
#             menu.addAction(action_edit)
#             menu.addAction(action_delete)
#
#             action = menu.exec(QCursor.pos())
#
#             if action == action_show:
#                 print("SHOW")
#             elif action == action_hide:
#                 print("HIDE")
#             elif action == action_edit:
#                 print("EDIT")
#             elif action == action_delete:
#                 print("DELETE")


class QGraphicsMovablePoint(QGraphicsEllipseItem):
    size: float = 2.2

    def __init__(self, pos: QPointF, control):
        super().__init__(-self.size / 2, -self.size / 2, self.size, self.size)
        self.control = control
        self.setPen(control.pen)
        self.setBrush(control.low_brush)

        self.setPos(pos)
        self._is_moving = False

    def setPos(self, pos: QPointF):
        super().setPos(floor(pos.x()) + 0.5, floor(pos.y()) + 0.5)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        super().paint(painter, option, widget)

    def move(self, vector: QPointF):
        self.setPos(self.pos() + vector)

    def delete(self):
        self.scene().removeItem(self)
        self.control.point_deleted(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_moving = True
            self.setBrush(self.control.high_brush)
        elif event.button() == Qt.MouseButton.RightButton:
            menu = QMenu()
            menu.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
            action_delete = QAction("Delete Point")
            action_delete.setEnabled(self.control.is_point_deletable)
            action_delete.triggered.connect(self.delete)
            menu.addAction(action_delete)

            a = self.control.common_actions()  # temp variable needed
            menu.addActions(a)

            menu.exec(QCursor.pos())

    def mouseReleaseEvent(self, event):
        # self.setPos(self.mapToScene(event.pos()))
        self._is_moving = False
        self.setBrush(self.control.low_brush)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._is_moving is True:
            self.setPos(self.mapToScene(event.pos()))
            self.control.point_moved(self)


class QGraphicsMovableLine(QGraphicsLineItem):
    _mp1: QGraphicsMovablePoint
    _mp2: QGraphicsMovablePoint

    def __init__(self, mp1: QGraphicsMovablePoint, mp2: QGraphicsMovablePoint, control):
        super().__init__()
        self.control = control
        self.setPen(control.pen)

        self._mp2 = mp2  # set _mp2 first because, mp1 property use mp2
        self.mp1 = mp1
        self.mp2 = mp2

    @property
    def mp1(self):
        return self._mp1

    @mp1.setter
    def mp1(self, value):
        self._mp1 = value
        self.update()

    @property
    def mp2(self):
        return self._mp2

    @mp2.setter
    def mp2(self, value):
        self._mp2 = value
        self.update()

    def update(self, rect: QRectF = QRectF()):
        temp_line = QLineF(self.mp1.pos(), self.mp2.pos())
        length = temp_line.length()
        if length > QGraphicsMovablePoint.size:
            p1 = self.mp1.pos()
            p2 = self.mp2.pos()
            f = (QGraphicsMovablePoint.size / 2) / length
            p1, p2 = (1 - f) * p1 + f * p2, (1 - f) * p2 + f * p1
            self.setLine(QLineF(p1, p2))
        else:
            self.setLine(QLineF())
        super().update(rect)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        super().paint(painter, option, widget)

    def delete(self):
        self.scene().removeItem(self)

    def add_point(self, pos: QPointF):
        new_point = QGraphicsMovablePoint(pos, self.control)
        self.scene().addItem(new_point)
        old_mp2 = self.mp2
        self.mp2 = new_point
        new_line = QGraphicsMovableLine(new_point, old_mp2, self.control)
        self.scene().addItem(new_line)
        self.control.point_added(self.mp1, new_point, new_line)

    def shape(self):
        # virtually extends the line width for click detection
        temp_line = QGraphicsLineItem(self.line())
        pen = self.pen()
        pen.setWidthF(pen.widthF() * 5)
        temp_line.setPen(pen)
        return temp_line.shape()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            menu = QMenu()
            action_add_point = QAction("Add Point")
            action_add_point.triggered.connect(lambda: self.add_point(self.mapToScene(event.pos())))
            menu.addAction(action_add_point)

            a = self.control.common_actions()  # temp variable needed
            menu.addActions(a)
            menu.exec(QCursor.pos())
        else:
            super().mousePressEvent(event)


class QGraphicsMovablePolygon(QGraphicsPathItem):

    def __init__(self, mp_list: list[QGraphicsMovablePoint], control):
        super().__init__()
        self.control = control
        self.mp_list = mp_list
        self.setBrush(control.low_brush)
        self.setPen(QPen(Qt.GlobalColor.transparent))
        self._drag_position = None

    @property
    def mp_list(self):
        return self._mp_list

    @mp_list.setter
    def mp_list(self, value):
        self._mp_list = value
        path = QPainterPath()
        path.addPolygon(QPolygonF([mp.pos() for mp in self._mp_list]))
        negative = QPainterPath()
        for mp in self._mp_list:
            negative.addEllipse(mp.boundingRect().translated(mp.pos()))
        self.setPath(path - negative)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            menu = QMenu()
            menu.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
            # action_delete = QAction("Delete Point")
            # action_delete.setEnabled(self.parent.is_point_deletable)
            # action_delete.triggered.connect(self.delete)
            # menu.addAction(action_delete)

            a = self.control.common_actions()  # temp variable needed
            menu.addActions(a)

            menu.exec(QCursor.pos())
        else:
            super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = self.mapToScene(event.pos()).truncated()
            self.setBrush(self.control.high_brush)
        else:
            super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        # self.setPos(self.mapToScene(event.pos()))
        self._drag_position = None
        self.setBrush(self.control.low_brush)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._drag_position is not None:
            delta = self.mapToScene(event.pos()).truncated() - self._drag_position
            for mp in self.mp_list:
                mp.move(delta)
                self.control.point_moved(mp)
            self._drag_position = self.mapToScene(event.pos()).truncated()


class QGraphicsFixedPolygon(QGraphicsPolygonItem):

    def __init__(self, poly: QPolygonF, control):
        super().__init__(poly.translated(0.5, 0.5))
        self.control = control
        self.setBrush(control.low_brush)
        self.setPen(control.pen)
        self.setAcceptHoverEvents(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            menu = QMenu()
            menu.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
            # action_delete = QAction("Delete Point")
            # action_delete.setEnabled(self.parent.is_point_deletable)
            # action_delete.triggered.connect(self.delete)
            # menu.addAction(action_delete)

            a = self.control.common_actions()  # temp variable needed
            menu.addActions(self.control.common_actions())

            menu.exec(QCursor.pos())
        else:
            super().mousePressEvent(event)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        super().paint(painter, option, widget)

    def hoverEnterEvent(self, event):
        self.setBrush(self.control.high_brush)
        self.control.setSelected(True)
        self.update()
        # super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(self.control.low_brush)
        self.control.setSelected(False)
        self.update()
        # super().hoverLeaveEvent(event)


class QControlArea(QTreeWidgetItem):

    def __init__(self, parent, scene: QGraphicsScene,  area: MovePolygon):
        super().__init__(parent)
        self.scene = scene
        self.area = area

        self.setCheckState(0, Qt.CheckState.Unchecked)

        if area.main:
            main_color = QColor(160, 200, 40)
        else:
            main_color = QColor(255, 90, 40)

        # self._visible = True
        self._edit = False
        # self._enable = True

        self.pen_color = main_color
        self.pen_color.setAlpha(255)
        self.pen = QPen(self.pen_color)
        self.pen.setWidthF(0.3)
        self.pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        self.pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

        self.brush_color = main_color
        self.brush_color.setAlpha(32)
        self.low_brush = QBrush(self.brush_color)
        self.brush_color.setAlpha(96)
        self.high_brush = QBrush(self.brush_color)

        self.a_enter_edit = QAction("Enter edit mode")
        self.a_enter_edit.triggered.connect(self.enter_edit_mode)
        self.a_exit_edit_save = QAction("Exit edit mode && Save")
        self.a_exit_edit_save.triggered.connect(lambda: self.exit_edit_mode(save=True))
        self.a_exit_edit_cancel = QAction("Exit edit mode && Cancel")
        self.a_exit_edit_cancel.triggered.connect(lambda: self.exit_edit_mode(save=False))
        self.a_add_obstacle = QAction("Add obstacle")
        self.a_add_obstacle.triggered.connect(lambda: self.parent().add_obstacle(self.k))
        self.a_remove_obstacle = QAction("Remove obstacle")
        self.a_remove_obstacle.triggered.connect(lambda: self.parent().remove_obstacle(self.k))

        # Define editable objects
        self.point_item = []
        self.is_point_deletable = 0
        self.line_item = []
        self.movable_poly = None

        # Define fixed objects
        self.fixed_poly = None

        # simulation of exiting edit mode to create fixed objects
        self._edit = True
        self.exit_edit_mode(save=False)
        self.update()

    @property
    def i(self):
        if self.parent() is None:
            return -1
        return self.parent().i

    @property
    def j(self):
        if self.parent() is None:
            return -1
        return self.parent().j

    @property
    def k(self):
        if self.parent() is None:
            return -1
        return self.parent().indexOfChild(self)

    @property
    def short_name(self):
        if self.area.main:
            return "Main Area"
        else:
            return f"Obstacle {self.k}"

    @property
    def abs_name(self):
        if self.area.main:
            return f"Main Area {self.i} {self.j}"
        else:
            return f"Obstacle {self.i} {self.j} {self.k}"

    def setBold(self, value):
        f = self.font(0)
        f.setBold(value)
        self.setFont(0, f)

    def update(self):
        name = self.short_name
        if self._edit is True:
            self.setBold(True)
            name += " ... editing ..."
        else:
            self.setBold(False)
        self.setText(0, name)
        self.setText(1, f"{self.area.global_id}")

        self.setVisible(self.checkState(0) == Qt.CheckState.Checked)

    def point_moved(self, point_item: QGraphicsMovablePoint):
        n = len(self.point_item)
        index = self.point_item.index(point_item)
        self.line_item[(index - 1) % n].mp2 = point_item
        self.line_item[index].mp1 = point_item
        self.movable_poly.mp_list = self.point_item

    def point_added(self,
                    previous_point_item: QGraphicsMovablePoint,
                    new_point_item: QGraphicsMovablePoint,
                    new_line_item: QGraphicsMovableLine):
        index = self.point_item.index(previous_point_item)
        self.point_item.insert(index + 1, new_point_item)
        self.line_item.insert(index + 1, new_line_item)
        self.is_point_deletable = True
        self.movable_poly.mp_list = self.point_item

    def point_deleted(self, point_item):
        n = len(self.point_item)
        index = self.point_item.index(point_item)
        self.line_item[(index - 1) % n].mp2 = self.point_item[(index + 1) % n]
        self.line_item[index].delete()
        self.line_item.remove(self.line_item[index])
        self.point_item.remove(point_item)
        if len(self.point_item) <= 3:
            self.is_point_deletable = False
        self.movable_poly.mp_list = self.point_item



    def common_actions(self) -> list[QAction]:
        if self._edit is False:
            return [self.a_enter_edit, self.a_add_obstacle, self.a_remove_obstacle]
        else:
            return [self.a_add_obstacle, self.a_remove_obstacle, self.a_exit_edit_save, self.a_exit_edit_cancel]

    def setVisible(self, visible: bool):
        if self._edit is True:
            self.movable_poly.setVisible(visible)
            [p.setVisible(visible) for p in self.point_item]
            [l.setVisible(visible) for l in self.line_item]
        else:
            self.fixed_poly.setVisible(visible)

    def remove_graphics(self):
        if self.movable_poly is not None:
            self.scene.removeItem(self.movable_poly)
            self.movable_poly = None
        if self.fixed_poly is not None:
            self.scene.removeItem(self.fixed_poly)
            self.fixed_poly = None
        [self.scene.removeItem(p) for p in self.point_item]
        self.point_item = []
        [self.scene.removeItem(l) for l in self.line_item]
        self.line_item = []

    def enter_edit_mode(self):
        if self._edit is False:
            self._edit = True

            # remove old graphics
            if self.fixed_poly is not None:
                self.scene.removeItem(self.fixed_poly)
                self.fixed_poly = None

            # build new graphics
            self.point_item = [QGraphicsMovablePoint(p, self) for p in self.area]
            self.is_point_deletable = len(self.area) > 3
            self.line_item = [QGraphicsMovableLine(mp1, mp2, self) for mp1, mp2 in
                              zip(self.point_item, self.point_item[1:] + [self.point_item[0]])]
            self.movable_poly = QGraphicsMovablePolygon(self.point_item, self)

            # add new graphics to the scene
            self.scene.addItem(self.movable_poly)
            [self.scene.addItem(p) for p in self.point_item]
            [self.scene.addItem(l) for l in self.line_item]

            self.setCheckState(0, Qt.CheckState.Checked)
            self.update()

    def exit_edit_mode(self, save: bool):
        if self._edit is True:
            self._edit = False
            if save is True:
                self.area.poly = QPolygonF([p.pos().truncated() for p in self.point_item])

            # remove old graphics
            if self.movable_poly is not None:
                self.scene.removeItem(self.movable_poly)
                self.movable_poly = None
            [self.scene.removeItem(p) for p in self.point_item]
            self.point_item = []
            [self.scene.removeItem(l) for l in self.line_item]
            self.line_item = []

            # build new graphics
            self.fixed_poly = QGraphicsFixedPolygon(self.area.poly, self)

            # add new graphics to the scene
            self.scene.addItem(self.fixed_poly)

            self.update()

    def contextMenuEvent(self, event):
        menu = QMenu()
        a_localise = QAction("Localise")
        a_localise.triggered.connect(self.localise)
        menu.addAction(a_localise)

        menu.addActions(self.common_actions())
        menu.exec(QCursor.pos())

    def localise(self):
        self.setCheckState(0, Qt.CheckState.Checked)
        if self._edit is True:
            self.scene.move_to_item(self.movable_poly)
        else:
            self.scene.move_to_item(self.fixed_poly)



class QControlSublayer(QTreeWidgetItem):
    def __init__(self, parent, scene, sublayer):
        super().__init__(parent)
        self.scene = scene
        self.sublayer = sublayer
        self.setCheckState(0, Qt.CheckState.Unchecked)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate)

        for area in sublayer:
            QControlArea(self, self.scene, area)

        self.update()

    @property
    def i(self):
        if self.parent() is None:
            return -1
        return self.parent().i


    @property
    def j(self):
        if self.parent() is None:
            return -1
        return self.parent().indexOfChild(self)

    def add_obstacle(self, k):
        r: QRectF = self.scene.viewport().current_visible_scene_rect()
        p1 = (0.7*r.topLeft() + 0.3*r.bottomRight()).truncated()
        p2 = (0.7*r.topRight() + 0.3*r.bottomLeft()).truncated()
        p3 = (0.7*r.bottomRight() + 0.3*r.topLeft()).truncated()
        p4 = (0.7*r.bottomLeft() + 0.3*r.topRight()).truncated()
        new_poly = QPolygonF([p1, p2, p3, p4])
        new_obstacle = self.sublayer.add_obstacle(new_poly, k + 1)
        new_child_item = QControlArea(None, self.scene, new_obstacle)
        self.insertChild(k + 1, new_child_item)
        new_child_item.setCheckState(0, Qt.CheckState.Checked)
        new_child_item.enter_edit_mode()
        for index in range(k+1, self.childCount()):
            self.child(index).update()
        self.treeWidget().update_height()

    def remove_obstacle(self, k):
        self.sublayer.remove_obstacle(k)
        item = self.child(k)
        item.remove_graphics()
        self.removeChild(item)
        for index in range(k, self.childCount()):
            self.child(index).update()
        self.treeWidget().update_height()


    def update(self):
        self.setText(0, f"Sublayer {self.j}")


class QControlLayer(QTreeWidgetItem):
    def __init__(self, parent, scene, layer):
        super().__init__(parent)
        self.scene = scene
        self.layer = layer
        self.setCheckState(0, Qt.CheckState.Unchecked)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate)
        self.setExpanded(True)

        for sublayer in layer:
            QControlSublayer(self, self.scene, sublayer)

        self.update()


    @property
    def i(self):
        return self.treeWidget().indexOfTopLevelItem(self)

    def update(self):
        self.setText(0, f"Layer {self.i}")


class QAreaTreeWidget(QTreeWidget):
    def __init__(self, parent, scene, move):
        super().__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setColumnCount(2)
        # self.setHeaderHidden(False)

        self.scene = scene
        self.move = move

        for layer in move:
            QControlLayer(self, self.scene, layer)

        self.itemChanged.connect(self.item_changed)
        self.itemExpanded.connect(self.update_height)
        self.itemCollapsed.connect(self.update_height)


    def update_height(self):
        h = self.header().height() + 18 * self._count_visible_item() + 2
        self.setMinimumHeight(h)
        self.setMaximumHeight(h)
        self.setColumnWidth(0, 200)
        # self.resizeColumnToContents(0)
        # self.resizeColumnToContents(1)

    def update(self):
        super().update()
        self.update_height()

    def _count_visible_item(self):
        count = 0
        index = self.model().index(0, 0)
        while index.isValid():
            count += 1
            index = self.indexBelow(index)
        return count

    def item_changed(self, item, column):
        item.update()

    def contextMenuEvent(self, event: QContextMenuEvent):
        item = self.itemAt(event.pos())
        if isinstance(item, QControlArea):
            item.contextMenuEvent(event)


class QMotionControl(QControl):
    def __init__(self, parent, scene, move):
        super().__init__(parent, scene)
        self.highlight_widget = None
        self.move = move
        self.layer_item = []

        content = QWidget()
        layout = QVBoxLayout(content)

        # sub_content = QWidget()
        # sub_layout = QHBoxLayout(sub_content)
        # self.check_box = QCheckBox()
        # self.check_box.setCheckState(Qt.CheckState.Checked)
        # self.check_box.clicked.connect(self.set_highlight_mode)
        # sub_layout.addWidget(self.check_box)
        # self.label = QLabel("Highlight on layer")
        # self.label.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
        # sub_layout.addWidget(self.label)
        # self.spin = QSpinBox()
        # self.spin.setMinimum(0)
        # self.spin.setMaximum(len(self.motion) - 1)
        # self.spin.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
        # self.spin.valueChanged.connect(self.set_highlight_mode)
        # sub_layout.addWidget(self.spin)
        # sub_layout.addStretch(255)
        # layout.addWidget(sub_content)

        self.tree_widget_label = QLabel("Areas Definition")
        layout.addWidget(self.tree_widget_label)

        self.tree_widget = QAreaTreeWidget(self, scene, move)
        layout.addWidget(self.tree_widget)

        layout.addStretch(255)
        self.setWidget(content)

    def update(self):
        super().update()
        self.tree_widget.update()



    # def set_highlight_mode(self):
    #     state = self.check_box.isChecked()
    #     self.label.setEnabled(state)
    #     self.spin.setEnabled(state)
    #     for i, layer_item in enumerate(self):
    #         for sublayer_item in layer_item:
    #             for area_item in sublayer_item[1:]:
    #                 area_item.graphic_item.setHighlight(state and self.spin.value() == i)
    #             sublayer_item[0].graphic_item.setHighlight(False)


    # def __iter__(self):
    #     return iter(self.layer_item)
    #
    # def __len__(self):
    #     return len(self.layer_item)
    #
    # def __getitem__(self, index):
    #     return self.layer_item[index]
