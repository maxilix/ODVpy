from math import floor

from PyQt6.QtCore import QRectF, Qt, QEvent
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent, QGraphicsItem, QMenu, QGraphicsEllipseItem, \
    QApplication

from qt.graphics.base import OdvGraphic, OdvShadow, OdvEditZone, OdvEditGraphic, GraphicState
from qt.scene_tool_bar import QSceneToolBar


class QScene(QGraphicsScene):
    tool_bar: QSceneToolBar

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pointer = QGraphicsEllipseItem()
        size = 2.2
        self.pointer.setRect(-size / 2, -size / 2, size, size)
        self.pointer.setZValue(100)
        self.pointer.setVisible(False)
        super().addItem(self.pointer)
        self.pointer_item = None

        # install itself as an EventFilter to watch all click
        QApplication.instance().installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if type(obj) != type(self):
                # print(f"Click on object {obj}")
                pass
        return super().eventFilter(obj, event)

    def center_view(self, zoom=1.5):
        r = self.sceneRect().center()
        x = r.x()
        y = r.y()
        self.viewport().zoom = zoom
        self.viewport().x = x
        self.viewport().y = y

    def viewport(self):
        return self.views()[0]

    def move_to_item(self, item: QGraphicsItem):
        self.viewport().move_to_rect(item.sceneBoundingRect())

    def move_to_rect(self, rect: QRectF):
        self.viewport().move_to_rect(rect)

    def move_to(self, x, y, zoom=20, blink_pixel=False):
        self.viewport().move_to(x, y, zoom)
        # if blink_pixel is True:  # TODO
        #     self.pointer.setPos(x + 0.5, y + 0.5)
        #     self.pointer.setVisible(True)
        #     anim = QVariantAnimation(self)
        #     anim.setDuration(2200)
        #     anim.setStartValue(1.0)
        #     anim.setEndValue(0.0)
        #     anim.valueChanged.connect(lambda o: self.pointer.setOpacity(o))
        #     anim.setEasingCurve(QEasingCurve.Type.InCubic)
        #     anim.start()
        #     anim.finished.connect(lambda: self.pointer.setVisible(False))
        #     anim.finished.connect(lambda: self.pointer.setOpacity(1))

    #TODO review adding/removing shadow mechanics
    #TODO review accept/ignore of event in the whole graphic item chain (and propagation)

    def addItem(self, item):
        assert isinstance(item, OdvGraphic)
        super().addItem(item)
        if item.shadow:
            super().addItem(item.shadow)

    def removeItem(self, item):
        if isinstance(item, OdvGraphic) and item.shadow is not None:
            super().removeItem(item.shadow)
        super().removeItem(item)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        shadow_list = [g.tree_item for g in self.items(event.scenePos()) if isinstance(g, OdvShadow) and g.tree_item.hover_detection()]
        self.viewport().info_bar.set_tree_items(shadow_list)
        if self.pointer_item is not None:
            if (ga:=self.pointer_item.grid_alignment) is not None:
                position =  event.scenePos().truncated() + ga
            else:
                position = event.scenePos()
            self.pointer.setPos(position)
            self.pointer_item.point_moved(self.pointer)
        else:
            super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        edit_zone_list = [g for g in self.items(event.scenePos()) if isinstance(g, OdvEditZone)]
        if len(edit_zone_list) == 0:
            for editable in [g for g in self.items() if isinstance(g, OdvEditGraphic)]:
                if editable.state == GraphicState.Unlock:
                    editable.lock()

        if self.pointer_item is not None:
            super().mousePressEvent(event)
        else:
            if event.button() == Qt.MouseButton.RightButton:# and not event.isAccepted():
                menu = QMenu()
                x = floor(event.scenePos().x())
                y = floor(event.scenePos().y())
                save_pos = QAction(f"({x}, {y})")
                save_pos.triggered.connect(lambda state: self.tool_bar.set_xy_localize(x, y))
                menu.addAction(save_pos)
                menu.addSeparator()
                actions = []
                for tree_item in [g.tree_item for g in self.items(event.scenePos()) if isinstance(g, OdvShadow) and g.tree_item.hover_detection()]:
                    actions.append(QAction(tree_item.name))
                    actions[-1].triggered.connect(lambda state, inner_item=tree_item: self.focus_on(inner_item))
                menu.addActions(actions)
                menu.exec(QCursor.pos())
            elif event.button() == Qt.MouseButton.LeftButton and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                editables = [g for g in self.items(event.scenePos()) if isinstance(g, OdvEditGraphic)]
                unlocked = 0
                for editable in editables:
                    if editable.isVisible() and editable.state == GraphicState.Lock:
                        editable.unlock()
                        unlocked += 1
                if unlocked == 0:
                    super().mousePressEvent(event)
            else:
                super().mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        if self.pointer_item is not None:
            if event.button() == Qt.MouseButton.LeftButton:
                self.pointer_item.add_point(self.pointer.pos())
        else:
            super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.pointer_item is not None:
            self.pointer_item.exit_creation_mode()
        super().mouseDoubleClickEvent(event)

    def claim_pointer(self, item):
        if self.pointer_item is None:
            self.pointer_item = item
            self.pointer_item.setVisible(True)
            self.pointer.setPen(self.pointer_item.thin_pen)
            self.pointer.setBrush(self.pointer_item.high_brush)
            self.pointer.setVisible(True)
            return True
        else:
            print(f"WARNING: pointer already exists for {self.pointer_item}")
            return False

    def release_pointer(self, item):
        if self.pointer_item is None:
            print(f"WARNING: no pointer to release")
            return False
        else:
            if self.pointer_item == item:
                self.pointer_item = None
                self.pointer.setVisible(False)
                return True
            else:
                print(f"WARNING: pointer is owned by {self.pointer_item}, not {item}")
                return False

    @staticmethod
    def focus_on(tree_item):
        tree_item.focus()
        tree_item.show_graphics()
        tree_item.localize_graphics()
