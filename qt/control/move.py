from math import floor
from typing import Self, Iterator

from PyQt6.QtCore import Qt, QRectF, QLineF, QPointF, pyqtSignal, QObject
from PyQt6.QtGui import QColor, QPen, QBrush, QPainter, QPainterPath, QAction, QCursor, QContextMenuEvent, QMouseEvent, \
    QPolygonF
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QTabWidget, QLabel, QVBoxLayout, QCheckBox, QWidget, \
    QScrollArea, QPushButton, QHBoxLayout, QSpinBox, QGraphicsScene, \
    QGraphicsItem, QMenu, QGraphicsPolygonItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsItemGroup, \
    QGraphicsObject, QGraphicsPathItem

from dvd.move import Obstacle, MovePolygon
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

    def __init__(self, pos: QPointF, parent):
        super().__init__(-self.size / 2, -self.size / 2, self.size, self.size)
        self.parent = parent
        self.setPen(parent.pen)
        self.setBrush(parent.low_brush)

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
        self.parent.point_deleted(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_moving = True
            self.setBrush(self.parent.high_brush)
        elif event.button() == Qt.MouseButton.RightButton:
            menu = QMenu()
            menu.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
            action_delete = QAction("Delete Point")
            action_delete.setEnabled(self.parent.is_point_deletable)
            action_delete.triggered.connect(self.delete)
            menu.addAction(action_delete)

            a = self.parent.common_actions()  # temp variable needed
            menu.addActions(a)

            menu.exec(QCursor.pos())

    def mouseReleaseEvent(self, event):
        # self.setPos(self.mapToScene(event.pos()))
        self._is_moving = False
        self.setBrush(self.parent.low_brush)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._is_moving is True:
            self.setPos(self.mapToScene(event.pos()))
            self.parent.point_moved(self)


class QGraphicsMovableLine(QGraphicsLineItem):
    _mp1: QGraphicsMovablePoint
    _mp2: QGraphicsMovablePoint

    def __init__(self, mp1: QGraphicsMovablePoint, mp2: QGraphicsMovablePoint, parent):
        super().__init__()
        self.parent = parent
        self.setPen(parent.pen)

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
        new_point = QGraphicsMovablePoint(pos, self.parent)
        self.scene().addItem(new_point)
        old_mp2 = self.mp2
        self.mp2 = new_point
        new_line = QGraphicsMovableLine(new_point, old_mp2, self.parent)
        self.scene().addItem(new_line)
        self.parent.point_added(self.mp1, new_point, new_line)

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

            a = self.parent.common_actions()  # temp variable needed
            menu.addActions(a)
            menu.exec(QCursor.pos())
        else:
            super().mousePressEvent(event)


class QGraphicsMovablePolygon(QGraphicsPathItem):

    def __init__(self, mp_list: list[QGraphicsMovablePoint], parent):
        super().__init__()
        self.parent = parent
        self.mp_list = mp_list
        self.setBrush(parent.low_brush)
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

            a = self.parent.common_actions()  # temp variable needed
            menu.addActions(a)

            menu.exec(QCursor.pos())
        else:
            super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.leftButton:
            self._drag_position = self.mapToScene(event.pos()).truncated()
            self.setBrush(self.parent.high_brush)
        else:
            super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        # self.setPos(self.mapToScene(event.pos()))
        self._drag_position = None
        self.setBrush(self.parent.low_brush)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._drag_position is not None:
            delta = self.mapToScene(event.pos()).truncated() - self._drag_position
            for mp in self.mp_list:
                mp.move(delta)
                self.parent.point_moved(mp)
            self._drag_position = self.mapToScene(event.pos()).truncated()


class QGraphicsFixedPolygon(QGraphicsPolygonItem):

    def __init__(self, poly: QPolygonF, parent):
        super().__init__(poly.translated(0.5, 0.5))
        self.parent = parent
        self.setBrush(parent.low_brush)
        self.setPen(parent.pen)
        self.setAcceptHoverEvents(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            menu = QMenu()
            menu.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
            # action_delete = QAction("Delete Point")
            # action_delete.setEnabled(self.parent.is_point_deletable)
            # action_delete.triggered.connect(self.delete)
            # menu.addAction(action_delete)

            a = self.parent.common_actions()  # temp variable needed
            menu.addActions(a)

            menu.exec(QCursor.pos())
        else:
            super().mousePressEvent(event)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        super().paint(painter, option, widget)

    def hoverEnterEvent(self, event):
        self.setBrush(self.parent.high_brush)
        self.parent.control.setSelected(True)
        self.update()

    def hoverLeaveEvent(self, event):
        self.setBrush(self.parent.low_brush)
        self.parent.control.setSelected(False)
        self.update()


class QGraphicsArea(QGraphicsItem):

    def __init__(self, area: MovePolygon, scene: QGraphicsScene, control):
        super().__init__()
        self.area = area
        self.control = control
        self.scene = scene
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemHasNoContents)

        main_color = QColor(160, 200, 40) if area.main else QColor(255, 90, 40)

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

    def boundingRect(self):
        return self.area.qpf.boundingRect()

    def point_moved(self, point_item: QGraphicsMovablePoint):
        n = len(self.point_item)
        index = self.point_item.index(point_item)
        self.line_item[(index - 1) % n].mp2 = point_item
        self.line_item[index].mp1 = point_item
        self.movable_poly.mp_list = self.point_item

    def point_added(self, previous_point_item: QGraphicsMovablePoint, new_point_item: QGraphicsMovablePoint,
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
            action_edit = QAction("Enter edit mode")
            action_edit.triggered.connect(self.enter_edit_mode)
            return [action_edit]
        else:
            separator = QAction()
            separator.setSeparator(True)
            action_save = QAction("Exit edit mode && Save")
            action_save.triggered.connect(lambda: self.exit_edit_mode(save=True))
            action_cancel = QAction("Exit edit mode && Cancel")
            action_cancel.triggered.connect(lambda: self.exit_edit_mode(save=False))
            return [separator, action_save, action_cancel]

    def setVisible(self, visible: bool):
        if self._edit is True:
            self.movable_poly.setVisible(visible)
            [p.setVisible(visible) for p in self.point_item]
            [l.setVisible(visible) for l in self.line_item]
        else:
            self.fixed_poly.setVisible(visible)
        super().setVisible(visible)


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

    def exit_edit_mode(self, save: bool):
        if self._edit is True:
            self._edit = False
            if save is True:
                self.area.qpf = QPolygonF([p.pos().truncated() for p in self.point_item])

            # remove old graphics
            if self.movable_poly is not None:
                self.scene.removeItem(self.movable_poly)
                self.movable_poly = None
            [self.scene.removeItem(p) for p in self.point_item]
            self.point_item = []
            [self.scene.removeItem(l) for l in self.line_item]
            self.line_item = []

            # build new graphics
            self.fixed_poly = QGraphicsFixedPolygon(self.area.qpf, self)

            # add new graphics to the scene
            self.scene.addItem(self.fixed_poly)


class QControlArea(QTreeWidgetItem):

    def __init__(self, parent, scene: QGraphicsScene, area):
        super().__init__(parent)
        self.scene = scene
        self.area = area

        self.graphic_item = QGraphicsArea(area, scene, self)
        if area.main:
            self.setText(0, f"Main Area")
        else:
            self.setText(0, f"Obstacle {area.k}")

        self.setCheckState(0, Qt.CheckState.Unchecked)
        # self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate)

    def update(self):
        self.graphic_item.setVisible(self.checkState(0) == Qt.CheckState.Checked)


class QControlSublayer(QTreeWidgetItem):
    def __init__(self, parent, scene, sublayer):
        super().__init__(parent)
        self.scene = scene
        self.sublayer = sublayer
        self.setText(0, f"Sublayer {sublayer.j}")
        self.setCheckState(0, Qt.CheckState.Unchecked)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate)

        # self.main_area_item = QControlArea(self, self.scene, sublayer.main, -1)
        self.area_item = [QControlArea(self, self.scene, area) for area in sublayer]

    def __iter__(self):
        return iter(self.area_item)

    def __len__(self):
        return len(self.area_item)

    def __getitem__(self, index):
        return self.area_item[index]


class QControlLayer(QTreeWidgetItem):
    def __init__(self, parent, scene, layer):
        super().__init__(parent)
        self.scene = scene
        self.layer = layer
        self.setText(0, f"Layer {layer.i}")
        self.setCheckState(0, Qt.CheckState.Unchecked)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate)

        self.sublayer_item = [QControlSublayer(self, self.scene, sublayer) for sublayer in layer]

    def __iter__(self):
        return iter(self.sublayer_item)

    def __len__(self):
        return len(self.sublayer_item)

    def __getitem__(self, index):
        return self.sublayer_item[index]


class QAreaTreeWidget(QTreeWidget):
    def __init__(self, parent, scene: QScene):
        super().__init__(parent)
        self.scene = scene

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # self.setHeaderLabels(["Layer", "Sublayer", "Area"])
        self.setHeaderHidden(True)

        # self.itemDoubleClicked.connect(self.item_double_clicked)
        self.itemChanged.connect(self.item_changed)
        self.itemExpanded.connect(self.update_height)
        self.itemCollapsed.connect(self.update_height)

    def item_changed(self, item, column):
        if column == 0 and isinstance(item, QControlArea):
            item.update()

    # def item_double_clicked(self, item, column):
    #     pass

    def update_height(self):
        # h = 18 * self.count_visible_item() + 24  # with header
        h = 18 * self.count_visible_item() + 2  # without header

        self.setMinimumHeight(h)
        self.setMaximumHeight(h)
        self.resizeColumnToContents(0)

    def count_visible_item(self):
        count = 0
        index = self.model().index(0, 0)
        while index.isValid():
            count += 1
            index = self.indexBelow(index)
        return count

    def contextMenuEvent(self, event: QContextMenuEvent):
        item = self.itemAt(event.pos())
        if isinstance(item, QControlArea):
            menu = QMenu(self)
            action_localise = QAction("Localise", self)
            action_edit = QAction("Edit", self)
            action_delete = QAction("Delete", self)

            menu.addAction(action_localise)
            menu.addAction(action_edit)
            menu.addAction(action_delete)

            action = menu.exec(event.globalPos())

            if action == action_localise:
                self.scene.move_to_item(item.graphic_item)
                item.setCheckState(0, Qt.CheckState.Checked)
            elif action == action_edit:
                item.graphic_item.enter_edit_mode()
                item.setCheckState(0, Qt.CheckState.Checked)
            elif action == action_delete:
                print("Delete action triggered")
                # Implement your delete action here


class QMotionControl(QScrollArea):
    def __init__(self, parent, scene, move):
        super().__init__(parent)
        self.highlight_widget = None
        self.scene = scene
        self.move = move
        self.layer_item = []
        self.init_ui()

    def init_ui(self):
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

        tree_widget = QAreaTreeWidget(self, self.scene)
        self.layer_item = [QControlLayer(tree_widget, self.scene, layer) for layer in self.move]
        tree_widget.update_height()
        layout.addWidget(tree_widget)

        layout.addStretch(255)

        # self.set_highlight_mode()
        self.setWidgetResizable(True)
        self.setWidget(content)

    # def set_highlight_mode(self):
    #     state = self.check_box.isChecked()
    #     self.label.setEnabled(state)
    #     self.spin.setEnabled(state)
    #     for i, layer_item in enumerate(self):
    #         for sublayer_item in layer_item:
    #             for area_item in sublayer_item[1:]:
    #                 area_item.graphic_item.setHighlight(state and self.spin.value() == i)
    #             sublayer_item[0].graphic_item.setHighlight(False)

    def __iter__(self):
        return iter(self.layer_item)

    def __len__(self):
        return len(self.layer_item)

    def __getitem__(self, index):
        return self.layer_item[index]
