from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget, QPushButton, QStyle, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox

import qt.control._generic_tree as generic_tree

TITLE_SIZE = 22

class SubInspector(QWidget):
    valid_state = True

    def __init__(self, inspector, prop_name):
        assert isinstance(inspector, Inspector)
        super().__init__()
        self._inspector = inspector
        self._prop_name = prop_name
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def global_update(self):
        self._inspector.update()

    @property
    def current(self):
        return self._inspector.get_odv_prop(self._prop_name)

    @current.setter
    def current(self, value):
        self._inspector.set_odv_prop(self._prop_name, value)


class Inspector(QWidget):
    deletable = True
    child_name = ""

    def __init__(self, tab_control, odv_object):
        super().__init__()
        self._tab_control = tab_control
        self.odv_object = odv_object
        self.init_actions()
        self.sub_inspector_group = dict()
        self.main_layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()
        self.settings_button = QPushButton(self)
        self.settings_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarUnshadeButton))
        self.settings_button.setIconSize(QSize(TITLE_SIZE, TITLE_SIZE))
        self.settings_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                padding: 0;
            }
            QPushButton:hover {
                background: #f0f0f0;
            }
        """)
        header_layout.addWidget(self.settings_button)

        self.title = QLabel(self)
        self.title.setText(self.odv_object.name)
        f = self.title.font()
        f.setPointSizeF(TITLE_SIZE)
        self.title.setFont(f)
        header_layout.addWidget(self.title)

        header_layout.addStretch(1)

        self.main_layout.addLayout(header_layout)

        sub_layout = QVBoxLayout()
        sub_layout.setSpacing(10)
        self.init_odv_prop()
        for group_name in self.sub_inspector_group:
            box = QGroupBox(group_name)
            box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            box_layout = QVBoxLayout(box)
            for sub_inspector in self.sub_inspector_group[group_name]:
                box_layout.addWidget(sub_inspector)
            self.main_layout.addWidget(box)
        # self.main_layout.addLayout(sub_layout)
        self.main_layout.addStretch(1)
        # self.update()

    def update(self):
        for sub_inspector in self.sub_inspector_list:
            sub_inspector.update()
        super().update()
        self.tree_item.update()

    @property
    def scene(self):
        return self._tab_control.scene

    @property
    def level(self):
        return self._tab_control.level

    @property
    def tree_item(self):
        return self._tab_control.tree_items[self.odv_object]

    @property
    def sub_inspector_list(self):
        rop = []
        for group_name in self.sub_inspector_group:
            for sub_inspector in self.sub_inspector_group[group_name]:
                rop.append(sub_inspector)
        return rop

    @property
    def valid_state(self):
        return all([sub_inspector.valid_state for sub_inspector in self.sub_inspector_list])

    @property
    def graphic_list(self):
        return [sub_inspector.graphic for sub_inspector in self.sub_inspector_list if hasattr(sub_inspector, 'graphic')]

    @property
    def inspector_child_list(self):
        rop = []
        count = self.tree_item.childCount()
        for i in range(count):
            rop.append(self.tree_item.child(i).inspector)
        return rop

    def init_odv_prop(self):
        # must define self.prop = {property_label : property_widget, ...}
        # must connect property_widget.changed signal to the right edition of self.odv_object
        #
        # note: for graphical properties, don't forget to add graphic item to self.scene
        pass

    def get_odv_prop(self, prop_name):
        if hasattr(self, prop_name):
            return getattr(self, prop_name)
        elif hasattr(self.odv_object, prop_name):
            return getattr(self.odv_object, prop_name)
        else:
            raise AttributeError(f"Neither {self.__class__.__name__} nor {self.odv_object.__class__.__name__} have property {prop_name}")

    def set_odv_prop(self, prop_name, value):
        if hasattr(self, prop_name):
            setattr(self, prop_name, value)
        elif hasattr(self.odv_object, prop_name):
            setattr(self.odv_object, prop_name, value)
        else:
            raise AttributeError(f"Neither {self.__class__.__name__} nor {self.odv_object.__class__.__name__} have property {prop_name}")

    def init_actions(self):
        self.a_rename = QAction("Rename")
        # self.a_rename.triggered.connect(self.rename)

        self.a_focus = QAction("Focus")
        self.a_focus.triggered.connect(self.take_focus)

        self.a_add_child = QAction(f"Add {self.child_name}")
        self.a_add_child.triggered.connect(self.add_child)

        self.a_delete = QAction("Delete")
        self.a_delete.triggered.connect(self.delete)


    def add_child(self):
        odv_child = self.new_odv_child()
        self.odv_object.add_child(odv_child)

        self._tab_control.tree_items[odv_child] = generic_tree.QODVTreeItem(self._tab_control, odv_child)
        self.tree_item.addChild(self._tab_control.tree_items[odv_child])

        self._tab_control.inspectors[odv_child] = self._tab_control.inspector_types.get(type(odv_child), Inspector)(self._tab_control, odv_child)
        self._tab_control.inspector_stack_layout.addWidget(self._tab_control.inspectors[odv_child])

        self._tab_control.inspectors[odv_child].take_focus()  # take_focus finish with a global update

    def new_odv_child(self):
        raise NotImplementedError

    def delete(self):
        for inspector_child in self.inspector_child_list:
            inspector_child.delete()
        self.tree_item.parent().removeChild(self.tree_item)
        self._tab_control.tree_items.pop(self.odv_object)

        self._tab_control.inspector_stack_layout.removeWidget(self)
        self._tab_control.inspectors.pop(self.odv_object)
        for g in self.graphic_list:
            self.scene.removeItem(g)
        self.deleteLater()

        self._tab_control.inspectors[self.odv_object.parent].take_focus()  # take_focus finish with a global update
        self.odv_object.parent.remove_child(self.odv_object)

        self._tab_control.update()

    def scene_menu_name(self):
        return self.odv_object.name

    def scene_menu_exclusive(self):
        return self._tab_control.scene_menu_exclusive()

    def scene_menu_enabled(self):
        return self._tab_control.scene_menu_enabled()

    def scene_menu_priority(self):
        return self._tab_control.scene_menu_priority() + 0.25 * self.has_focus()

    def scene_menu_common_actions(self, scene_position):
        rop = []
        rop.append(self.a_focus)
        if self.deletable:
            rop.append(self.a_delete)
        return rop

    def tree_menu_common_actions(self):
        rop = []
        rop.append(self.a_rename)
        if self.child_name != "":
            rop.append(self.a_add_child)
        if self.deletable is True:
            rop.append(self.a_delete)
        return rop

    def has_focus(self):
        return self._tab_control.has_focus() and self._tab_control.tree.currentItem() == self.tree_item

    def take_focus(self):
        self._tab_control.take_focus()
        self._tab_control.tree.setCurrentItem(self.tree_item)
        self.update()



# class SectionInspector(Inspector):
#     def init_prop_section(self):
#         self.prop["Version"] = QLabel(str(self.odv_object.version))

