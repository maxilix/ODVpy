from PyQt6.QtCore import Qt, QLineF, QPointF
from PyQt6.QtGui import QContextMenuEvent, QAction, QCursor, QPen, QColor, QBrush, QTransform
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QMenu, \
    QGraphicsScene, QLineEdit, QAbstractItemView, QGridLayout, QTreeWidget, QStackedLayout, QTreeWidgetItem

from qt.common.inspector import QInspector
from qt.control.common import QTabControl, QSubControl
from qt.graphics.line import QCGLine


class QBondItem(QSubControl, QTreeWidgetItem):
    def __init__(self, parent, scene: QGraphicsScene, bond_link):
        super().__init__(parent)
        self.scene = scene
        self.bond_link = bond_link
        self.setCheckState(0, Qt.CheckState.Checked)

        main_color = QColor(0, 180, 255)

        self.pen_color = main_color
        self.pen_color.setAlpha(255)
        self.pen = QPen(self.pen_color)
        self.pen.setWidthF(0.3)
        self.pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        self.pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

        self.brush_color = main_color
        self.brush_color.setAlpha(32)
        self.brush = QBrush(self.brush_color)
        self.low_brush = QBrush(self.brush_color)
        self.brush_color.setAlpha(96)
        self.high_brush = QBrush(self.brush_color)

        line = QLineF(bond_link.p1, bond_link.p2)

        self.line = QCGLine(self, line)
        self.scene.addItem(self.line)

        length = line.length()
        rotate = QTransform(0, 1, -1, 0, 0, 0)

        left_point = rotate.map(bond_link.p2 - bond_link.p1) / length * 10 + (bond_link.p1 + bond_link.p2) / 2
        right_point = rotate.map(bond_link.p1 - bond_link.p2) / length * 10 + (bond_link.p1 + bond_link.p2) / 2
        # self.line2 = QCGLine(self, QLineF(left_point, right_point))
        # self.scene.addItem(self.line2)

        self.init_actions()
        self.update()

    @property
    def context_menu_name(self):
        return f"Bond {self.bond_link.i}"

    def init_actions(self):
        self.a_localise = QAction("Localise")
        self.a_localise.triggered.connect(self.localise)

        self.a_show = QAction("Show bond")
        self.a_show.triggered.connect(lambda: self.setCheckState(0, Qt.CheckState.Checked))

        self.a_hide = QAction("Hide bond")
        self.a_hide.triggered.connect(lambda: self.setCheckState(0, Qt.CheckState.Unchecked))

        self.a_add = QAction("Add bond")
        # self.a_add_obstacle.triggered.connect(lambda: self.parent().add_obstacle(self.area.k))

        self.a_delete = QAction("Delete bond")
        # self.a_delete_obstacle.triggered.connect(lambda: self.parent().delete_obstacle(self.area.k))

    def setBold(self, value):
        f = self.font(0)
        f.setBold(value)
        self.setFont(0, f)

    def update(self):
        self.setText(0, self.context_menu_name)
        self.line.update()

    def item_visibility(self):
        return self.checkState(0) == Qt.CheckState.Checked


    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.addAction(self.a_localise)
        menu.addActions(self.common_action_list())
        menu.exec(QCursor.pos())

    def common_action_list(self, scene_position: QPointF = QPointF()) -> list[QAction]:
        rop = []
        if self.item_visibility():
            rop.append(self.a_hide)
        else:
            rop.append(self.a_show)
        rop.append(self.a_add)
        rop.append(self.a_delete)
        return rop

    def localise(self):
        self.setCheckState(0, Qt.CheckState.Checked)
        self.scene.move_to_item(self.line)


class QBondTreeWidget(QTreeWidget):
    def __init__(self, parent, inspector_stack):
        super().__init__(parent)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.inspector_stack = inspector_stack
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # self.itemChanged.connect(self.item_changed)
        self.itemSelectionChanged.connect(self.item_selection_changed)

    # def update_height(self):
    #
    #     h = 18 * self.count() + 2
    #     self.setMinimumHeight(h)
    #     self.setMaximumHeight(h)
    #
    # def update(self):
    #     # self.update_height()
    #     super().update()

    # def _count_visible_item(self):
    #     count = 0
    #     index = self.model().index(0, 0)
    #     while index.isValid():
    #         count += 1
    #         index = self.indexBelow(index)
    #     return count

    # def item_changed(self, item):
    #     item.update()

    def contextMenuEvent(self, event: QContextMenuEvent):
        item = self.itemAt(event.pos())
        item.contextMenuEvent(event)

    def item_selection_changed(self):
        self.inspector_stack.setCurrentIndex(self.selectedItems()[0].bond_link.i)


# class QBondInspector(QInspector):
#     def __init__(self, parent):
#         super().__init__(parent, has_location=True)
#
#         grid = QGridLayout()
#
#         label = QLabel("Layer Id")
#         grid.addWidget(label, 0, 0)
#         self.layer_id = QLineEdit()
#         grid.addWidget(self.layer_id, 0, 1)
#
#         label = QLabel("Left Area Id")
#         grid.addWidget(label, 1, 0)
#         self.left_id = QLineEdit()
#         grid.addWidget(self.left_id, 1, 1)
#
#         label = QLabel("Right Area Id")
#         grid.addWidget(label, 2, 0)
#         self.right_id = QLineEdit()
#         grid.addWidget(self.right_id, 2, 1)
#
#         self.main_layout.addLayout(grid)
#     def update(self):
#         if self.item is not None:
#             self.localise.clicked.connect(self.item.localise)
#             self.title.setText(self.item.context_menu_name)
#             self.layer_id.setText(str(self.item.bond_link.layer.i))
#             self.left_id.setText(str(self.item.bond_link.left_id))
#             self.right_id.setText(str(self.item.bond_link.right_id))
#
#     @property
#     def item(self):
#         return self._item
#
#     @item.setter
#     def item(self, item):
#         self._item = item
#         self.update()


class QBondControl(QTabControl):
    def __init__(self, parent, scene, bond):
        super().__init__(parent, scene)
        self.bond = bond

        content = QWidget()
        layout = QVBoxLayout(content)

        inspector_stack_widget = QWidget(self)
        self.inspector_stack_layout = QStackedLayout(inspector_stack_widget)
        self.tree = QBondTreeWidget(self, self.inspector_stack_layout)
        # self.tree.setColumnCount(1)
        # self.tree.setHeaderHidden(True)
        # self.tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # self.tree.itemSelectionChanged.connect(self.item_selection_changed)


        for bond_link in bond:
            tree_item = QBondItem(self.tree, scene, bond_link)
            self.inspector_stack_layout.addWidget(QInspector(parent=self, dvd_item=bond_link))

        # self.inspector_stack_layout.setCurrentIndex(self.tree.selectedItems()[0])
        self.tree.topLevelItem(0).setSelected(True)


        # # self.list_widget_label = QLabel("Bonds Definition")
        # # layout.addWidget(self.list_widget_label)
        #
        #
        # self.inspector = QBondInspector(self)
        # self.list_widget = QBondTreeWidget(self, scene, bond)
        # # self.list_widget.setSizePolicy()
        # # self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # # self.list_widget.itemSelectionChanged.connect(self.item_selection_changed)
        # try:
        #     self.list_widget.item(0).setSelected(True)
        #     selected_item = self.list_widget.item(0)
        # except AttributeError:
        #     selected_item = None


        layout.addWidget(inspector_stack_widget)
        layout.addSpacing(50)
        layout.addWidget(self.tree)

        self.setWidget(content)




