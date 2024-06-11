from PyQt6.QtCore import Qt, QPointF, QEvent
from PyQt6.QtGui import QColor, QPen, QBrush
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QTabWidget, QLabel, QVBoxLayout, QCheckBox, QWidget, \
    QScrollArea, QTreeWidgetItemIterator, QPushButton, QHBoxLayout, QSpinBox, QGraphicsPolygonItem, QGraphicsScene, \
    QGraphicsItem

# from q_tests import scene
from .abstract_controller import Control, HierarchicalControl


class QGraphicsArea(QGraphicsPolygonItem):
    def __init__(self, area):
        super().__init__(area.QPolygonF())

        if area.main:
            self.main_color = QColor(160, 200, 40)
        else:
            self.main_color = QColor(255, 90, 40)

        pen_color = self.main_color
        pen_color.setAlpha(128)
        pen = QPen(pen_color)
        pen.setWidth(1)
        self.setPen(pen)

        brush_color = self.main_color
        brush_color.setAlpha(32)
        brush = QBrush(brush_color)
        self.setBrush(brush)

    # def refresh(self, mousse_position):
    #     if self.control.area.main:
    #         pass
    #     else:
    #         brush_color = self.main_color
    #         if self.polygon().containsPoint(mousse_position, Qt.FillRule.OddEvenFill):
    #             self.control.setSelected(True)
    #             brush_color.setAlpha(64)
    #             self.setBrush(QBrush(brush_color))
    #             self.setVisible(True)
    #         else:
    #             self.control.setSelected(False)
    #             brush_color.setAlpha(32)
    #             self.setBrush(QBrush(brush_color))
    #             if self.control.checkState(0) == Qt.CheckState.Checked:
    #                 self.setVisible(True)
    #             else:
    #                 self.setVisible(False)


class QControlArea(QTreeWidgetItem):
    def __init__(self, parent, scene: QGraphicsScene, area, index):
        super().__init__(parent)
        self.scene = scene
        self.area = area
        self.index = index

        self.graphic_area_item = QGraphicsArea(area)
        self.scene.addItem(self.graphic_area_item)
        # self.graphic_area_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        # self.graphic_area_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        if area.main is True:
            self.setText(0, f"Main Area")
        else:
            self.setText(0, f"Obstacle {self.index}")

        self.setCheckState(0, Qt.CheckState.Unchecked)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate)

    def update(self):
        self.graphic_area_item.setVisible(self.checkState(0) == Qt.CheckState.Checked)

    def mousse_event(self, scene_position: QPointF, event: QEvent):
        if self.area.main is False:
            if scene_position is not None and self.area.QPolygonF().containsPoint(scene_position, Qt.FillRule.OddEvenFill):
                self.setSelected(True)
                self.graphic_area_item.setVisible(True)
            else:
                self.setSelected(False)
                self.graphic_area_item.setVisible(self.checkState(0) == Qt.CheckState.Checked)


class QControlSublayer(QTreeWidgetItem):
    def __init__(self, parent, scene, sublayer, index):
        super().__init__(parent)
        self.scene = scene
        self.sublayer = sublayer
        self.index = index
        self.setText(0, f"Sublayer {self.index}")
        self.setCheckState(0, Qt.CheckState.Unchecked)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate)

        self.area_item = [QControlArea(self, self.scene, area, k) for k, area in enumerate(sublayer)]

    def __iter__(self):
        return iter(self.area_item)

    def __len__(self):
        return len(self.area_item)

    def __getitem__(self, index):
        return self.area_item[index]

    def mousse_event(self, scene_position: QPointF, event: QEvent):
        for area_item in self:
            area_item.mousse_event(scene_position, event)

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

    def mousse_event(self, scene_position: QPointF, event: QEvent):
        for sublayer_item in self:
            sublayer_item.mousse_event(scene_position, event)




class QHighlightWidget(QWidget):
    def __init__(self, parent, nb_layer):
        super().__init__(parent)
        layout = QHBoxLayout(self)

        self.check_box = QCheckBox()
        self.check_box.setCheckState(Qt.CheckState.Checked)
        self.check_box.clicked.connect(self.update)
        layout.addWidget(self.check_box)

        self.label = QLabel("Highlight on layer")
        self.label.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
        layout.addWidget(self.label)

        layout.addStretch(255)

        self.spin = QSpinBox()
        self.spin.setMinimum(0)
        self.spin.setMaximum(nb_layer)
        self.spin.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
        layout.addWidget(self.spin)
        self.update()

    def update(self):
        if self.check_box.isChecked() is True:
            self.label.setEnabled(True)
            self.spin.setEnabled(True)
        else:
            self.label.setEnabled(False)
            self.spin.setEnabled(False)

    def value(self):
        if self.check_box.isChecked() is False:
            return -1
        else:
            return self.spin.value()


class QAreaTreeWidget(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setHeaderLabels(["Layer", "Sublayer", "Area"])
        self.setHeaderHidden(True)

        self.itemDoubleClicked.connect(self.item_double_clicked)
        self.itemChanged.connect(self.item_changed)
        self.itemExpanded.connect(self.update_height)
        self.itemCollapsed.connect(self.update_height)

    def item_changed(self, item, column):
        if column == 0 and isinstance(item, QControlArea):
            item.update()

    def item_double_clicked(self, item, column):
        pass

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
            self.highlight_widget = QHighlightWidget(self, len(self.motion))
            layout.addWidget(self.highlight_widget)
            tree_widget = QAreaTreeWidget(self)
            self.layer_item = [QControlLayer(tree_widget, self.scene, layer, i) for i, layer in enumerate(self.motion)]

            tree_widget.update_height()
            layout.addWidget(tree_widget)

        layout.addStretch(255)
        self.setWidgetResizable(True)
        self.setWidget(content)

    def __iter__(self):
        return iter(self.layer_item)

    def __len__(self):
        return len(self.layer_item)

    def __getitem__(self, index):
        return self.layer_item[index]

    def mousse_event(self, scene_position: QPointF, event: QEvent):
        if self.highlight_widget is not None and (i := self.highlight_widget.value()) != -1:
            self[i].mousse_event(scene_position, event)


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

    def mousse_event(self, scene_position: QPointF, event: QEvent):
        self.control_areas.mousse_event(scene_position, event)
