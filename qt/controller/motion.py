from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QPen, QBrush, QPainter, QPainterPath, QAction, QCursor
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QTabWidget, QLabel, QVBoxLayout, QCheckBox, QWidget, \
    QScrollArea, QPushButton, QHBoxLayout, QSpinBox, QGraphicsScene, \
    QGraphicsItem, QMenu

from dvd.move import Obstacle, MainArea
from qt.view.main_view import QScene


class QGraphicsArea(QGraphicsItem):

    def __init__(self, main_color: QColor,  area: Obstacle, scene: QGraphicsScene, control):
        super().__init__()
        self.area = area
        self.control = control
        self.main_color = main_color

        self.poly_pen_color = self.main_color
        self.poly_pen_color.setAlpha(255)
        self.poly_pen = QPen(self.poly_pen_color)
        self.poly_pen.setWidthF(0.5)
        self.poly_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

        self.poly_brush_color = self.main_color
        self.poly_brush_color.setAlpha(32)
        self.poly_brush = QBrush(self.poly_brush_color)

        self._highlight_visibility = True
        self._highlight = False
        self._normal_visibility = True

        scene.addItem(self)
        self.setAcceptHoverEvents(True)

    def setVisible(self, normal_visibility: bool) -> None:
        self._normal_visibility = normal_visibility
        super().setVisible(self._normal_visibility or self._highlight_visibility)
        self.update()

    def setHighlight(self, highlight_visibility: bool) -> None:
        self._highlight_visibility = highlight_visibility
        super().setVisible(self._normal_visibility or self._highlight_visibility)
        self.update()

    def boundingRect(self) -> QRectF:
        r = self.area.qpf.boundingRect()
        r.setX(r.x() - self.poly_pen.widthF() / 2)
        r.setY(r.y() - self.poly_pen.widthF() / 2)
        r.setWidth(r.width() + self.poly_pen.widthF())
        r.setHeight(r.height() + self.poly_pen.widthF())
        return r

    def paint(self, painter: QPainter, option, widget=None):
        if self._highlight and self._highlight_visibility:
            self.poly_brush_color.setAlpha(64)
        else:
            if self._normal_visibility is True:
                self.poly_brush_color.setAlpha(32)
            else:
                # no drawing
                return

        self.poly_brush = QBrush(self.poly_brush_color)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen(self.poly_pen)
        painter.setBrush(self.poly_brush)

        painter.drawPolygon(self.area.qpf, Qt.FillRule.OddEvenFill)

    def shape(self):
        path = QPainterPath()
        path.addPolygon(self.area.qpf)
        return path

    def hoverEnterEvent(self, event):
        # print("enter")
        self._highlight = True
        self.control.setSelected(True)
        self.update()

    def hoverLeaveEvent(self, event):
        # print("leave")
        self._highlight = False
        self.control.setSelected(False)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self._highlight = True
            self.control.setSelected(True)
            menu = QMenu()
            # header = QAction(f"{self.control.text(0)}")
            # f = header.font()
            # f.setBold(True)
            # header.setFont(f)
            # header.setEnabled(False)
            action_show = QAction("Show")
            action_hide = QAction("Hide")
            action_edit = QAction("Edit")
            action_delete = QAction("Delete")

            # menu.addAction(header)
            menu.addSection(f"{self.control.text(0)}")
            menu.addAction(action_show)
            menu.addAction(action_hide)
            menu.addSeparator()
            menu.addAction(action_edit)
            menu.addAction(action_delete)

            action = menu.exec(QCursor.pos())

            if action == action_show:
                self.control.setCheckState(0, Qt.CheckState.Checked)
            elif action == action_hide:
                self.control.setCheckState(0, Qt.CheckState.Unchecked)
            elif action == action_edit:
                print("EDIT")
            elif action == action_delete:
                print("DELETE")




class QControlArea(QTreeWidgetItem):
    def __init__(self, parent, scene: QGraphicsScene, area, index):
        super().__init__(parent)
        self.scene = scene
        self.area = area
        self.index = index

        if index == 0:
            self.graphic_item = QGraphicsArea(QColor(160, 200, 40), area, scene, self)
            self.setText(0, f"Main Area")
        else:
            self.graphic_item = QGraphicsArea(QColor(255, 90, 40), area, scene, self)
            self.setText(0, f"Obstacle {self.index}")

        self.setCheckState(0, Qt.CheckState.Unchecked)
        # self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate)

    def update(self):
        self.graphic_item.setVisible(self.checkState(0) == Qt.CheckState.Checked)


class QControlSublayer(QTreeWidgetItem):
    def __init__(self, parent, scene, sublayer, index):
        super().__init__(parent)
        self.scene = scene
        self.sublayer = sublayer
        self.index = index
        self.setText(0, f"Sublayer {self.index}")
        self.setCheckState(0, Qt.CheckState.Unchecked)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate)

        # self.main_area_item = QControlArea(self, self.scene, sublayer.main, -1)
        self.area_item = [QControlArea(self, self.scene, area, k) for k, area in enumerate(sublayer)]



    def __iter__(self):
        return iter(self.area_item)

    def __len__(self):
        return len(self.area_item)

    def __getitem__(self, index):
        return self.area_item[index]



class QControlLayer(QTreeWidgetItem):
    def __init__(self, parent, scene, layer, index):
        super().__init__(parent)
        self.scene = scene
        self.layer = layer
        self.index = index
        self.setText(0, f"Layer {self.index}")
        self.setCheckState(0, Qt.CheckState.Unchecked)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate)

        self.sublayer_item = [QControlSublayer(self, self.scene, sublayer, j) for j, sublayer in enumerate(layer)]

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

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.setHeaderLabels(["Layer", "Sublayer", "Area"])
        self.setHeaderHidden(True)

        # self.itemDoubleClicked.connect(self.item_double_clicked)
        self.itemChanged.connect(self.item_changed)
        self.itemExpanded.connect(self.update_height)
        self.itemCollapsed.connect(self.update_height)
        self.customContextMenuRequested.connect(self.context_menu_requested)

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

    def context_menu_requested(self, pos):
        item = self.itemAt(pos)
        if isinstance(item, QControlArea):
            menu = QMenu(self)
            menu.setTitle(f"{item.text(0)}")
            action_localise = QAction("Localise", self)
            action_edit = QAction("Edit", self)
            action_delete = QAction("Delete", self)

            menu.addAction(action_localise)
            menu.addAction(action_edit)
            menu.addAction(action_delete)

            action = menu.exec(self.mapToGlobal(pos))

            if action == action_localise:
                self.scene.move_to_item(item.graphic_item)
                item.setCheckState(0, Qt.CheckState.Checked)
            elif action == action_delete:
                print("Delete action triggered")
                # Implement your delete action here


class QControlAreas(QScrollArea):
    def __init__(self, parent, scene, motion):
        super().__init__(parent)
        self.highlight_widget = None
        self.scene = scene
        self.motion = motion
        self.layer_item = []
        self.init_ui()

    def init_ui(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        if self.motion.loaded_areas is False:
            label = QLabel("No loaded areas")
            layout.addWidget(label)
        else:
            ####
            sub_content = QWidget()
            sub_layout = QHBoxLayout(sub_content)
            self.check_box = QCheckBox()
            self.check_box.setCheckState(Qt.CheckState.Checked)
            self.check_box.clicked.connect(self.set_highlight_mode)
            sub_layout.addWidget(self.check_box)
            self.label = QLabel("Highlight on layer")
            self.label.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
            sub_layout.addWidget(self.label)
            sub_layout.addStretch(255)
            self.spin = QSpinBox()
            self.spin.setMinimum(0)
            self.spin.setMaximum(len(self.motion))
            self.spin.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
            self.spin.valueChanged.connect(self.set_highlight_mode)
            sub_layout.addWidget(self.spin)
            ###

            layout.addWidget(sub_content)
            tree_widget = QAreaTreeWidget(self, self.scene)
            self.layer_item = [QControlLayer(tree_widget, self.scene, layer, i) for i, layer in enumerate(self.motion)]

            tree_widget.update_height()
            self.set_highlight_mode()
            layout.addWidget(tree_widget)

        layout.addStretch(255)
        self.setWidgetResizable(True)
        self.setWidget(content)

    def set_highlight_mode(self):
        state = self.check_box.isChecked()
        self.label.setEnabled(state)
        self.spin.setEnabled(state)
        for i, layer_item in enumerate(self):
            for sublayer_item in layer_item:
                for area_item in sublayer_item[1:]:
                    area_item.graphic_item.setHighlight(state and self.spin.value() == i)
                sublayer_item[0].graphic_item.setHighlight(False)

    def __iter__(self):
        return iter(self.layer_item)

    def __len__(self):
        return len(self.layer_item)

    def __getitem__(self, index):
        return self.layer_item[index]


class QControlMotion(QWidget):
    def __init__(self, parent, scene, motion):
        super().__init__(parent)
        self.scene = scene
        self.motion = motion

        self.init_ui()

    def init_ui(self):
        # content = QWidget()
        layout = QVBoxLayout(self)

        load_areas_button = QPushButton("(re)Load areas only")
        load_areas_button.clicked.connect(self.load_areas_click)
        layout.addWidget(load_areas_button)

        load_all_button = QPushButton("(re)Load areas and pathfinder")
        load_all_button.clicked.connect(self.load_all_click)
        layout.addWidget(load_all_button)

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(False)
        self.control_areas = QControlAreas(self, self.scene, self.motion)
        tabs.addTab(self.control_areas, f"Areas")
        self.control_pathfinder = QWidget(self)
        tabs.addTab(self.control_pathfinder, f"PathFinder")
        layout.addWidget(tabs)

    def load_areas_click(self):
        self.motion.load(only_areas=True)
        self.control_areas.init_ui()

    def load_all_click(self):
        self.motion.load(only_areas=False)
        self.control_areas.init_ui()
        # self.control_pathfinder.init_ui()
