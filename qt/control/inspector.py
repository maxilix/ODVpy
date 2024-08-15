from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget, QPushButton, QStyle, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox


TITLE_SIZE = 22


class Inspector(QWidget):
    _deletable = True
    _child_addable = True

    def __init__(self, tab_control, odv_object):
        super().__init__()
        self._tab_control = tab_control
        self.odv_object = odv_object
        self.init_actions()
        self.prop = dict()
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
        for prop_label in self.prop:
            prop_box = QGroupBox(prop_label)
            prop_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            prop_box_layout = QVBoxLayout(prop_box)
            prop_box_layout.addWidget(self.prop[prop_label])
            sub_layout.addWidget(prop_box)
        self.main_layout.addLayout(sub_layout)
        self.main_layout.addStretch(1)


    @property
    def scene(self):
        return self._tab_control.scene

    @property
    def level(self):
        return self._tab_control.level

    @property
    def tree_item(self):
        return self._tab_control.tree_items[self.odv_object]

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

        self.a_add_child = QAction("Add child")
        # self.a_add_obstacle.triggered.connect()

        self.a_delete = QAction("Delete")
        # self.a_delete_obstacle.triggered.connect()

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
        if self._deletable:
            rop.append(self.a_delete)
        return rop

    def tree_menu_common_actions(self):
        rop = []
        rop.append(self.a_rename)
        if self._child_addable:
            rop.append(self.a_add_child)
        if self._deletable:
            rop.append(self.a_delete)
        return rop

    def has_focus(self):
        return self._tab_control.has_focus() and self._tab_control.tree.currentItem() == self.tree_item

    def take_focus(self):
        self._tab_control.take_focus()
        self._tab_control.tree.setCurrentItem(self.tree_item)


# class SectionInspector(Inspector):
#     def init_prop_section(self):
#         self.prop["Version"] = QLabel(str(self.odv_object.version))

