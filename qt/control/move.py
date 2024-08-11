from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColor, QPolygonF

from dvd.move import Layer, MainArea, Obstacle
from qt.control.q_inspector import Inspector, PolygonInspectorWidget
from qt.control.q_tab_control import QTabControlGenericTree


# class GraphicObstacle(QCGPolygonGroup):
#     def __init__(self, obstacle):
#         super().__init__(obstacle, obstacle.poly)
#         c = QColor(255, 90, 40)
#         # self.setPen(QThinPen(c))
#         # self.setBrush(QLightBrush(c))
#
#     # def update(self, rect: QRectF = QRectF()):
#     #     super().update(rect)
#     #     self.setPolygon(self.odv_object.poly)


class ObstacleInspector(Inspector):
    # path color QColor(180, 110, 30)
    def init_prop_section(self):
        # graphic = GraphicObstacle(self.odv_object)
        # self.scene.addItem(graphic)
        self.prop["Polygon"] = PolygonInspectorWidget(self, self.odv_object.poly, QColor(255, 90, 40))
        self.prop["Polygon"].changed.connect(self.set_poly)

    def set_poly(self, poly):
        self.odv_object.poly = poly


# class GraphicMainArea(QCGPolygonGroup):
#     def __init__(self, main_area):
#         super().__init__(main_area, main_area.poly)
#         c = QColor(160, 200, 40)
#         # self.setPen(QThinPen(c))
#         # self.setBrush(QLightBrush(c))
#
#     # def update(self, rect: QRectF = QRectF()):
#     #     super().update(rect)
#     #     self.setPolygon(self.odv_object.poly)


class MainAreaInspector(Inspector):
    # path color QColor(180, 110, 30)
    def init_prop_section(self):
        # graphic = GraphicMainArea(self.odv_object)
        # self.scene.addItem(graphic)
        self.prop["Polygon"] = PolygonInspectorWidget(self, self.odv_object.poly, QColor(160, 200, 40))
        # self.prop["Polygon"].changed.connect(self.set_poly)

    # def set_poly(self, poly):
    #     self.odv_object.poly = poly


class QMoveTabControl(QTabControlGenericTree):
    inspector_types = {Layer: Inspector,
                       MainArea: MainAreaInspector,
                       Obstacle: ObstacleInspector}



# class QControlArea(QTreeWidgetItem):
#
#     def __init__(self, parent, scene: QGraphicsScene, area: MovePolygon):
#         super().__init__(parent)
#         self.scene = scene
#         self.area = area
#
#         self.setCheckState(0, Qt.CheckState.Unchecked)
#         if area.main:
#             main_color = QColor(160, 200, 40)
#         else:
#             main_color = QColor(255, 90, 40)
#
#         self.pen_color = main_color
#         self.pen_color.setAlpha(255)
#         self.pen = QPen(self.pen_color)
#         self.pen.setWidthF(0.3)
#         self.pen.setCapStyle(Qt.PenCapStyle.FlatCap)
#         self.pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
#
#         self.brush_color = main_color
#         self.brush_color.setAlpha(32)
#         self.brush = QBrush(self.brush_color)
#         self.low_brush = QBrush(self.brush_color)
#         self.brush_color.setAlpha(96)
#         self.high_brush = QBrush(self.brush_color)
#
#         self._edit = False
#         self.fixed_polygon = QCGHighlightablePolygon(self, self.area.poly)
#         self.scene.addItem(self.fixed_polygon)
#         self.editable_polygon = None
#
#         self.init_actions()
#
#         self.update()
#
#     @property
#     def context_menu_local_exclusive(self):
#         return self._edit
#
#     @property
#     def context_menu_name(self):
#         if self.area.main:
#             return f"Main area {self.area.global_id}"
#         else:
#             return f"Obstacle {self.area.global_id}"
#
#     def init_actions(self):
#         self.a_localise = QAction("Localise")
#         self.a_localise.triggered.connect(self.localise)
#
#         self.a_enter_edit = QAction("Enter edit mode")
#         self.a_enter_edit.triggered.connect(self.enter_edit_mode)
#
#         self.a_exit_edit_save = QAction("Exit edit mode && Save")
#         self.a_exit_edit_save.triggered.connect(lambda: self.exit_edit_mode(save=True))
#
#         self.a_exit_edit_cancel = QAction("Exit edit mode && Cancel")
#         self.a_exit_edit_cancel.triggered.connect(lambda: self.exit_edit_mode(save=False))
#
#         self.a_show_obstacle = QAction("Show obstacle")
#         self.a_show_obstacle.triggered.connect(lambda: self.setCheckState(0, Qt.CheckState.Checked))
#
#         self.a_hide_obstacle = QAction("Hide obstacle")
#         self.a_hide_obstacle.triggered.connect(lambda: self.setCheckState(0, Qt.CheckState.Unchecked))
#
#         self.a_add_obstacle = QAction("Add obstacle")
#         self.a_add_obstacle.triggered.connect(lambda: self.parent().add_obstacle(self.area.k))
#
#         self.a_delete_obstacle = QAction("Delete obstacle")
#         self.a_delete_obstacle.triggered.connect(lambda: self.parent().delete_obstacle(self.area.k))
#
#     def setBold(self, value):
#         f = self.font(0)
#         f.setBold(value)
#         self.setFont(0, f)
#
#     def update(self):
#         name = self.context_menu_name
#         if self._edit is True:
#             self.setBold(True)
#             name += " ... editing ..."
#             self.editable_polygon.update()
#             self.setCheckState(0, Qt.CheckState.Checked)
#         else:
#             self.setBold(False)
#             self.fixed_polygon.update()
#         self.setText(0, name)
#
#     def common_action_list(self, scene_position: QPointF = QPointF()) -> list[QAction]:
#         rop = []
#         if self._edit:
#             rop.append(self.a_delete_obstacle)
#             rop.append(self.a_exit_edit_save)
#             rop.append(self.a_exit_edit_cancel)
#         else:
#             if self.item_visibility():
#                 rop.append(self.a_hide_obstacle)
#             else:
#                 rop.append(self.a_show_obstacle)
#             rop.append(self.a_enter_edit)
#             rop.append(self.a_add_obstacle)
#         return rop
#
#     def item_visibility(self):
#         return self.checkState(0) == Qt.CheckState.Checked
#
#     def remove_graphics(self):
#         if self.fixed_polygon is not None:
#             self.scene.removeItem(self.fixed_polygon)
#             self.fixed_polygon = None
#         if self.editable_polygon is not None:
#             self.scene.removeItem(self.editable_polygon)
#             self.editable_polygon = None
#
#     def enter_edit_mode(self):
#         self.take_focus()
#         if self._edit is False:
#             self._edit = True
#
#             self.scene.removeItem(self.fixed_polygon)
#             self.fixed_polygon = None
#
#             self.editable_polygon = QCGEditablePolygon(self, self.area.poly)
#             self.scene.addItem(self.editable_polygon)
#
#             self.setCheckState(0, Qt.CheckState.Checked)
#             self.update()
#
#     def exit_edit_mode(self, save: bool):
#         if self._edit is True:
#             self._edit = False
#             if save is True:
#                 self.area.poly = QPolygonF([p.pos().truncated() for p in self.editable_polygon])
#
#             self.scene.removeItem(self.editable_polygon)
#             self.editable_polygon = None
#
#             self.fixed_polygon = QCGHighlightablePolygon(self, self.area.poly)
#             self.scene.addItem(self.fixed_polygon)
#
#             self.update()
#
#     def contextMenuEvent(self, event):
#         menu = QMenu()
#         menu.addAction(self.a_localise)
#         menu.addActions(self.common_action_list())
#         menu.exec(QCursor.pos())
#
#     def localise(self):
#         self.setCheckState(0, Qt.CheckState.Checked)
#         if self._edit:
#             self.scene.move_to_item(self.editable_polygon)
#         else:
#             self.scene.move_to_item(self.fixed_polygon)
#
#
# class QControlSublayer(QTreeWidgetItem):
#     def __init__(self, parent, scene, sublayer):
#         super().__init__(parent)
#         self.scene = scene
#         self.sublayer = sublayer
#         self.setCheckState(0, Qt.CheckState.Unchecked)
#         self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate)
#         self.setExpanded(True)
#
#         for area in sublayer:
#             QControlArea(self, self.scene, area)
#
#         self.update()
#
#     def add_obstacle(self, k):
#         r: QRectF = self.scene.viewport().current_visible_scene_rect()
#         p1 = (0.7 * r.topLeft() + 0.3 * r.bottomRight()).truncated()
#         p2 = (0.7 * r.topRight() + 0.3 * r.bottomLeft()).truncated()
#         p3 = (0.7 * r.bottomRight() + 0.3 * r.topLeft()).truncated()
#         p4 = (0.7 * r.bottomLeft() + 0.3 * r.topRight()).truncated()
#         new_poly = QPolygonF([p1, p2, p3, p4])
#         new_obstacle = self.sublayer.add_obstacle(new_poly, k + 1)
#         new_child_item = QControlArea(None, self.scene, new_obstacle)
#         self.insertChild(k + 1, new_child_item)
#         new_child_item.setCheckState(0, Qt.CheckState.Checked)
#         new_child_item.enter_edit_mode()
#         for index in range(k + 1, self.childCount()):
#             self.child(index).update()
#         self.treeWidget().update_height()
#
#     def delete_obstacle(self, k):
#         self.sublayer.delete_obstacle(k)
#         item = self.child(k)
#         item.remove_graphics()
#         self.removeChild(item)
#         for index in range(k, self.childCount()):
#             self.child(index).update()
#         self.treeWidget().update_height()
#
#     def update(self):
#         self.setText(0, f"Sublayer {self.sublayer.j}")
#
#
# class QControlLayer(QTreeWidgetItem):
#     def __init__(self, parent, scene, layer):
#         super().__init__(parent)
#         self.scene = scene
#         self.layer = layer
#         self.setCheckState(0, Qt.CheckState.Unchecked)
#         self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate)
#         self.setExpanded(True)
#
#         for sublayer in layer:
#             QControlSublayer(self, self.scene, sublayer)
#
#         self.update()
#
#     def update(self):
#         self.setText(0, f"Layer {self.layer.i}")
#
#
# class QAreaTreeWidget(QTreeWidget):
#     def __init__(self, parent, scene, move):
#         super().__init__(parent)
#         self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#         self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#         self.setColumnCount(1)
#         self.setHeaderHidden(True)
#
#         self.scene = scene
#         self.move = move
#
#         for layer in move:
#             QControlLayer(self, self.scene, layer)
#
#         self.itemChanged.connect(self.item_changed)
#         self.itemExpanded.connect(self.update_height)
#         self.itemCollapsed.connect(self.update_height)
#
#     def update_height(self):
#         h = self.header().height() + 18 * self._count_visible_item() + 2
#         self.setMinimumHeight(h)
#         self.setMaximumHeight(h)
#         # self.setColumnWidth(0, 200)
#         # self.resizeColumnToContents(0)
#         # self.resizeColumnToContents(1)
#
#     def update(self):
#         super().update()
#         self.update_height()
#
#     def _count_visible_item(self):
#         count = 0
#         index = self.model().index(0, 0)
#         while index.isValid():
#             count += 1
#             index = self.indexBelow(index)
#         return count
#
#     def item_changed(self, item, column):
#         item.update()
#
#     def contextMenuEvent(self, event: QContextMenuEvent):
#         item = self.itemAt(event.pos())
#         if isinstance(item, QControlArea | QControlSublayer | QControlLayer):
#             item.contextMenuEvent(event)
#
#
# class QMotionControl(QTabControl):
#     def __init__(self, parent, scene, move):
#         super().__init__(parent, scene)
#         self.highlight_widget = None
#         self.move = move
#         self.layer_item = []
#
#         content = QWidget()
#         layout = QVBoxLayout(content)
#
#         # sub_content = QWidget()
#         # sub_layout = QHBoxLayout(sub_content)
#         # self.check_box = QCheckBox()
#         # self.check_box.setCheckState(Qt.CheckState.Checked)
#         # self.check_box.clicked.connect(self.set_highlight_mode)
#         # sub_layout.addWidget(self.check_box)
#         # self.label = QLabel("Highlight on layer")
#         # self.label.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
#         # sub_layout.addWidget(self.label)
#         # self.spin = QSpinBox()
#         # self.spin.setMinimum(0)
#         # self.spin.setMaximum(len(self.motion) - 1)
#         # self.spin.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
#         # self.spin.valueChanged.connect(self.set_highlight_mode)
#         # sub_layout.addWidget(self.spin)
#         # sub_layout.addStretch(255)
#         # layout.addWidget(sub_content)
#
#         self.tree_widget_label = QLabel("Areas Definition")
#         layout.addWidget(self.tree_widget_label)
#
#         self.tree_widget = QAreaTreeWidget(self, scene, move)
#         layout.addWidget(self.tree_widget)
#
#         layout.addStretch(255)
#         self.setWidget(content)
#
#     def update(self):
#         super().update()
#         self.tree_widget.update()
#
#     # def set_highlight_mode(self):
#     #     state = self.check_box.isChecked()
#     #     self.label.setEnabled(state)
#     #     self.spin.setEnabled(state)
#     #     for i, layer_item in enumerate(self):
#     #         for sublayer_item in layer_item:
#     #             for area_item in sublayer_item[1:]:
#     #                 area_item.graphic_item.setHighlight(state and self.spin.value() == i)
#     #             sublayer_item[0].graphic_item.setHighlight(False)
#
#     # def __iter__(self):
#     #     return iter(self.layer_item)
#     #
#     # def __len__(self):
#     #     return len(self.layer_item)
#     #
#     # def __getitem__(self, index):
#     #     return self.layer_item[index]
