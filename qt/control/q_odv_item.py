from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QColor, QAction, QPen, QBrush

from qt.scene import QScene

class QODVItem(object):
    colors = []

    editable = True

    q_graphic_item_type = lambda *args: None
    q_inspector_item_type = lambda *args: None
    q_tree_item_type = lambda *args: None


    def __init__(self, q_tab_control, scene: QScene, odv_item):
        self.q_tab_control = q_tab_control
        self.scene = scene
        self.odv_item = odv_item

        self.name = str(odv_item)
        self._edit = False
        self._visible = False
        self._local_exclusive = False

        self.pens = []
        self.brushes = []
        self.init_graphic_tools()
        self.init_actions()

        self.q_graphic_item = self.q_graphic_item_type(self)
        self.q_inspector_item = self.q_inspector_item_type(self)
        self.q_tree_item = self.q_tree_item_type(self)

        if self.q_graphic_item is not None:
            self.scene.addItem(self.q_graphic_item)

        self.update()

    @property
    def visible(self):
        return self._visible
        # rop = self.q_dvd_inspector_item.visible
        # assert self.q_dvd_tree_item.visible == rop
        # return rop

    @visible.setter
    def visible(self, visible):
        self._visible = visible
        if self.q_tree_item is not None:
            self.q_tree_item.visible = visible
        if self.q_inspector_item is not None:
            self.q_inspector_item.visible = visible
        if self.q_graphic_item is not None:
            self.q_graphic_item.update()

    def update(self):
        if self.q_tree_item is not None:
            self.q_tree_item.update()
        if self.q_inspector_item is not None:
            self.q_inspector_item.update()
        if self.q_graphic_item is not None:
            self.q_graphic_item.update()

    def rename(self):
        pass

    def init_graphic_tools(self):

        for c in self.colors:
            temp_color = QColor(c)
            temp_color.setAlpha(255)
            pen = QPen(temp_color)
            pen.setWidthF(0.3)
            pen.setCapStyle(Qt.PenCapStyle.FlatCap)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            self.pens.append(pen)
            temp_color.setAlpha(32)
            brush = QBrush(temp_color)
            self.brushes.append(brush)

    @property
    def pen(self):
        return self.pens[0]

    @property
    def brush(self):
        return self.brushes[0]

    def init_actions(self):
        self.a_rename = QAction("Rename")
        self.a_rename.triggered.connect(self.rename)

        self.a_focus = QAction("Focus")
        self.a_focus.triggered.connect(self.take_focus)

        self.a_localise = QAction("Localise")
        self.a_localise.triggered.connect(self.localise)

        self.a_show = QAction("Show")
        self.a_show.triggered.connect(lambda: setattr(self, "visible", True))

        self.a_hide = QAction("Hide")
        self.a_hide.triggered.connect(lambda: setattr(self, "visible", False))

        self.a_edit = QAction("Edit")
        # self.a_hide.triggered.connect()

        self.a_save = QAction("Save")
        # self.a_hide.triggered.connect()

        self.a_cancel = QAction("Cancel")
        # self.a_hide.triggered.connect()

        self.a_add = QAction("Add")
        # self.a_add_obstacle.triggered.connect()

        self.a_delete = QAction("Delete")
        # self.a_delete_obstacle.triggered.connect()

    def scene_menu_name(self):
        return self.name

    def scene_menu_exclusive(self):
        return self.q_tab_control.scene_menu_exclusive() or self._local_exclusive

    def scene_menu_priority(self):
        return (self.q_tab_control.scene_menu_priority()
                + 0.5 * self.q_tab_control.has_focus()
                + 0.25 * self.q_tab_control.is_current_item(self))

    def scene_menu_enabled(self):
        return self.q_tab_control.scene_menu_enabled()

    def scene_menu_common_actions(self, scene_position: QPointF = QPointF()):
        rop = []

        if self.visible:
            rop.append(self.a_hide)
        else:
            rop.append(self.a_show)

        if scene_position:
            rop.append(self.a_focus)
        else:
            rop.append(self.a_localise)

        if self._edit:
            rop.append(self.a_save)
            rop.append(self.a_cancel)
        else:
            rop.append(self.a_edit)
        return rop

    def localise(self):
        self.visible = True
        self.scene.move_to_item(self.q_graphic_item)

    def take_focus(self):
        self.q_tab_control.take_focus()
        self.q_tab_control.set_current_item(self)
