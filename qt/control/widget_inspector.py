from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget, QPushButton, QStyle, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox, QFormLayout, \
    QSizePolicy

from qt.control.widget_generic_tree import QGenericTreeItem

TITLE_SIZE = 22

class SubInspector(QWidget):
    valid_state = True

    def __init__(self, inspector, prop_name, inspector_name="", **kwargs):
        assert isinstance(inspector, QInspectorWidget)
        super().__init__()
        self._inspector = inspector
        self.inspector_name = inspector_name
        self._prop_name = prop_name
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.sub_init(**kwargs)

    def sub_init(self, **kwargs):
        pass

    def global_update(self):
        self._inspector.update()

    @property
    def current(self):
        return self._inspector.get_odv_prop(self._prop_name)

    @current.setter
    def current(self, value):
        self._inspector.set_odv_prop(self._prop_name, value)


class QInspectorWidget(QWidget):
    deletable = True
    draggable = False
    child_name = ""

    def __init__(self, tab, odv_object):
        super().__init__()
        self.tab = tab
        self.odv_object = odv_object
        self.sub_inspector_list = []

        self.main_layout = QVBoxLayout(self)

        # self.main_layout.insertWidget(0)

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
        self.title.setText(f"{self.odv_object.name}")
        f = self.title.font()
        f.setPointSizeF(TITLE_SIZE)
        self.title.setFont(f)
        header_layout.addWidget(self.title)
        header_layout.addStretch()

        self.main_layout.addLayout(header_layout)
        self.main_layout.addStretch()

    def update(self):
        for sub_inspector in self.sub_inspector_list:
            sub_inspector.update()
        super().update()
        # self.tree_item.update()

    def add_sub_inspector(self, sub_inspector):
        self.sub_inspector_list.append(sub_inspector)
        n = self.main_layout.count()
        self.main_layout.insertWidget(n - 1, sub_inspector)

    @property
    def scene(self):
        return self.tab.scene

    # @property
    # def level(self):
    #     return self._tab_control.level
    #
    # @property
    # def tree_item(self) -> QGenericTreeItem:
    #     return self._tab_control.tree_items[self.odv_object]

    # @property
    # def sub_inspector_list(self):
    #     rop = []
    #     for group_name in self.sub_inspector_group:
    #         for sub_inspector in self.sub_inspector_group[group_name]:
    #             rop.append(sub_inspector)
    #     return rop

    # @property
    # def valid_state(self):
    #     return all([sub_inspector.valid_state for sub_inspector in self.sub_inspector_list])

    # @property
    # def graphic_list(self):
    #     return [sub_inspector.graphic for sub_inspector in self.sub_inspector_list if hasattr(sub_inspector, 'graphic')]

    @property
    def inspector_child_list(self):
        rop = []
        count = self.tree_item.childCount()
        for i in range(count):
            rop.append(self.tree_item.child(i).inspector)
        return rop


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
        self.a_delete.triggered.connect(self.delete_and_update)

        self.a_children_show = QAction(f"Show all")
        self.a_children_show.triggered.connect(self.show_children)

        self.a_children_hide = QAction(f"Hide all")
        self.a_children_hide.triggered.connect(self.hide_children)

        self.a_children_delete = QAction("Delete all")
        self.a_children_delete.triggered.connect(self.delete_children)

    def add_child(self):
        odv_child = self.new_odv_child()
        self.odv_object.add_child(odv_child)

        self._tab_control.tree_items[odv_child] = QGenericTreeItem(self._tab_control, odv_child)
        self.tree_item.addChild(self._tab_control.tree_items[odv_child])

        self._tab_control.inspectors[odv_child] = self._tab_control.inspector_types.get(type(odv_child), QInspectorWidget)(self._tab_control, odv_child)
        self._tab_control.inspector_stack_layout.addWidget(self._tab_control.inspectors[odv_child])

        self._tab_control.inspectors[odv_child].take_focus()  # take_focus finish with a global update

    def new_odv_child(self):
        raise NotImplementedError

    # def _inner_delete(self):
    #     for inspector_child in self.inspector_child_list:
    #         inspector_child._inner_delete()
    #     self.tree_item.parent().removeChild(self.tree_item)
    #     self._tab_control.tree_items.pop(self.odv_object)
    #
    #     self._tab_control.inspector_stack_layout.removeWidget(self)
    #     self._tab_control.inspectors.pop(self.odv_object)
    #     for g in self.graphic_list:
    #         self.scene.removeItem(g)
    #     self.deleteLater()
    #     self.odv_object.parent.remove_child(self.odv_object)

    # def delete_and_update(self):
    #     self._inner_delete()
    #     self._tab_control.inspectors[self.odv_object.parent].take_focus()  # take_focus finish with a global update

    def show_children(self):
        for ic in self.inspector_child_list:
            for si in ic.sub_inspector_list:
                if hasattr(si, 'visibility_checkbox'):
                    si.visibility_checkbox.setChecked(True)
            ic.update()

    def hide_children(self):
        for ic in self.inspector_child_list:
            for si in ic.sub_inspector_list:
                if hasattr(si, 'visibility_checkbox'):
                    si.visibility_checkbox.setChecked(False)
            ic.update()

    def delete_children(self):
        for ic in self.inspector_child_list:
            assert ic.deletable
            ic._inner_delete()
        self.update()

    # def scene_menu_name(self):
    #     return self.odv_object.name

    # def scene_menu_exclusive(self):
    #     return self._tab_control.scene_menu_exclusive()

    # def scene_menu_enabled(self):
    #     return self._tab_control.scene_menu_enabled()

    # def scene_menu_priority(self):
    #     return self._tab_control.scene_menu_priority() + 0.25 * self.has_focus()

    # def scene_menu_common_actions(self, scene_position):
    #     rop = []
    #     rop.append(self.a_focus)
    #     return rop

    # def tree_menu_common_actions(self):
    #     rop = []
    #     rop.append(self.a_rename)
    #     if self.child_name != "":
    #         rop.append(self.a_add_child)
    #     if self.deletable is True:
    #         rop.append(self.a_delete)
    #     if self.child_name != "":
    #         rop.append(["On Children", self.a_children_show, self.a_children_hide, self.a_children_delete])
    #     return rop

    def has_focus(self):
        return self._tab_control.has_focus() and self._tab_control.tree.currentItem() == self.tree_item

    def take_focus(self):
        self._tab_control.take_focus()
        self._tab_control.tree.setCurrentItem(self.tree_item)
        self.update()



# class SectionInspector(Inspector):
#     def init_prop_section(self):
#         self.prop["Version"] = QLabel(str(self.odv_object.version))

