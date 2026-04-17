from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QCheckBox, QSlider, QStyle, \
    QPushButton, QSpinBox, QGridLayout, QMessageBox, QMenu, QComboBox, QGraphicsScene, QWidgetAction

from qt.common.clickable_label import QClickableLabel
from qt.common.searchable_menu import SearchableMenu
from qt.common.separator_line import QHLine
from qt.common.utils import bounding_rect_of
from qt.graphics.base import GraphicState
from qt.scene import QScene


class QSubInspectorWidget(QWidget):
    update_required = pyqtSignal()
    value_changed = pyqtSignal()



#
# class VISILAYOUT1(QSubInspectorWidget):
#     def __init__(self, *, title: str = "Visilibity", opacity_slider: bool = False, position: bool = False,
#                  edit_buttons: bool = False):
#         super().__init__(None)
#         self.graphics = []
#         main_layout = QVBoxLayout(self)
#         main_layout.setContentsMargins(0, 0, 0, 0)
#
#         # if title != "":
#         #     title_layout = QHBoxLayout()
#         #     title_layout.setContentsMargins(0, 0, 0, 0)
#         #
#         #     title_layout.addSpacing(50)
#         #     title_layout.addWidget(QLabel(title))
#         #     title_layout.addStretch()
#         #
#         #     main_layout.addLayout(title_layout)
#
#         visibility_layout = QHBoxLayout()
#         visibility_layout.setContentsMargins(0, 0, 0, 0)
#
#         visibility_layout.addWidget(QLabel(title))
#
#         self.visibility_checkbox = QCheckBox()
#         self.visibility_checkbox.setTristate(False)
#         self.visibility_checkbox.clicked.connect(self.visibility_checkbox_clicked)
#         visibility_layout.addWidget(self.visibility_checkbox)
#
#         if opacity_slider is True:
#             self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
#             self.opacity_slider.setMinimum(0)
#             self.opacity_slider.setMaximum(100)
#             self.opacity_slider.valueChanged.connect(self.opacity_slider_changed)
#             visibility_layout.addWidget(self.opacity_slider)
#
#             self.opacity_reset_button = QToolButton()
#             icon = self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)  # SP_DialogResetButton
#             self.opacity_reset_button.setIcon(icon)
#             self.opacity_reset_button.clicked.connect(self.opacity_reset_button_clicked)
#
#             visibility_layout.addWidget(self.opacity_reset_button)
#
#             visibility_layout.addSpacing(120)
#         else:
#             self.opacity_slider = None
#             self.opacity_reset_button = None
#
#             visibility_layout.addStretch()
#
#         self.localize_button = QPushButton("Localize")
#         self.localize_button.clicked.connect(self.localize_button_clicked)
#         visibility_layout.addWidget(self.localize_button)
#
#         main_layout.addLayout(visibility_layout)
#
#         if edit_buttons is True:
#             edit_layout = QHBoxLayout()
#             edit_layout.setContentsMargins(0, 0, 0, 0)
#
#             self.edit_button = QPushButton("Edit")
#             self.edit_button.clicked.connect(self.edit_button_clicked)
#             edit_layout.addWidget(self.edit_button)
#
#             edit_layout.addStretch()
#
#             self.save_button = QPushButton("Save")
#             self.save_button.clicked.connect(lambda: self.save_cancel_button_clicked(save=True))
#             edit_layout.addWidget(self.save_button)
#             self.cancel_button = QPushButton("Cancel")
#             self.cancel_button.clicked.connect(lambda: self.save_cancel_button_clicked(save=False))
#             edit_layout.addWidget(self.cancel_button)
#
#             main_layout.addLayout(edit_layout)
#         else:
#             self.edit_button = None
#             self.save_button = None
#             self.cancel_button = None
#
# class VISILAYOUT2(QSubInspectorWidget):
#     def __init__(self, *, title:str="Visilibity", opacity_slider:bool=False, position:bool=False, edit_buttons:bool=False):
#         super().__init__(None)
#         self.graphics = []
#         main_layout = QHBoxLayout(self)
#         main_layout.setContentsMargins(0, 0, 0, 0)
#
#         c1_layout = QVBoxLayout()
#         c1_layout.setContentsMargins(0, 0, 0, 0)
#
#         visibility_layout = QHBoxLayout()
#         visibility_layout.setContentsMargins(0, 0, 0, 0)
#         self.visibility_checkbox = QCheckBox()
#         self.visibility_checkbox.setTristate(False)
#         self.visibility_checkbox.clicked.connect(self.visibility_checkbox_clicked)
#         visibility_layout.addWidget(self.visibility_checkbox)
#         visibility_layout.addWidget(QLabel(title))
#         visibility_layout.addStretch()
#         c1_layout.addLayout(visibility_layout)
#
#         opacity_layout = QHBoxLayout()
#         opacity_layout.setContentsMargins(0, 0, 0, 0)
#         if opacity_slider is True:
#             self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
#             self.opacity_slider.setMinimum(0)
#             self.opacity_slider.setMaximum(100)
#             self.opacity_slider.valueChanged.connect(self.opacity_slider_changed)
#             opacity_layout.addWidget(self.opacity_slider)
#
#             self.opacity_reset_button = QToolButton()
#             icon = self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)  # SP_DialogResetButton
#             self.opacity_reset_button.setIcon(icon)
#             self.opacity_reset_button.clicked.connect(self.opacity_reset_button_clicked)
#             opacity_layout.addWidget(self.opacity_reset_button)
#         else:
#             self.opacity_slider = None
#             self.opacity_reset_button = None
#             opacity_layout.addStretch()
#         c1_layout.addLayout(opacity_layout)
#
#         position_layout = QHBoxLayout()
#         position_layout.setContentsMargins(0, 0, 0, 0)
#         if position is True:
#             position_layout.addStretch()
#
#             self.position_x = QSpinBox()
#             self.position_x.setPrefix("x ")
#             self.position_x.setValue(1234)
#             # self.position_x.valueChanged.connect()
#             position_layout.addWidget(self.position_x)
#
#             self.position_y = QSpinBox()
#             self.position_y.setPrefix("y ")
#             self.position_y.setValue(5678)
#             # self.position_y.valueChanged.connect()
#             position_layout.addWidget(self.position_y)
#         else:
#             self.position_x = None
#             self.position_y = None
#             position_layout.addStretch()
#         c1_layout.addLayout(position_layout)
#
#         main_layout.addLayout(c1_layout)
#         main_layout.addSpacing(15)
#
#         c2_layout = QGridLayout()
#         c2_layout.setContentsMargins(0, 0, 0, 0)
#         if position is True:
#             position_N_button = QToolButton()
#             position_N_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp))
#             # position_N_button.clicked.connect()
#             c2_layout.addWidget(position_N_button, 0, 1)
#             position_E_button = QToolButton()
#             position_E_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowRight))
#             # position_E_button.clicked.connect()
#             c2_layout.addWidget(position_E_button, 1, 2)
#             position_W_button = QToolButton()
#             position_W_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowLeft))
#             # position_W_button.clicked.connect()
#             c2_layout.addWidget(position_W_button, 1, 0)
#             position_S_button = QToolButton()
#             position_S_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown))
#             # position_S_button.clicked.connect()
#             c2_layout.addWidget(position_S_button, 2, 1)
#
#         main_layout.addLayout(c2_layout)
#         main_layout.addSpacing(15)
#
#         c3_layout = QVBoxLayout()
#         c3_layout.setContentsMargins(0, 0, 0, 0)
#
#         localize_layout = QHBoxLayout()
#
#         self.localize_button = QPushButton("Localize")
#         self.localize_button.clicked.connect(self.localize_button_clicked)
#         localize_layout.addWidget(self.localize_button)
#         localize_layout.addStretch()
#         delete_button = QToolButton()
#         delete_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TabCloseButton))
#         # delete_button.clicked.connect()
#         localize_layout.addWidget(delete_button)
#
#         c3_layout.addLayout(localize_layout)
#
#         if edit_buttons is True:
#             self.edit_button = QPushButton("Edit")
#             self.edit_button.clicked.connect(self.edit_button_clicked)
#             c3_layout.addWidget(self.edit_button)
#
#             edit_layout = QHBoxLayout()
#             edit_layout.setContentsMargins(0, 0, 0, 0)
#             self.save_button = QPushButton("Save")
#             self.save_button.clicked.connect(lambda: self.save_cancel_button_clicked(save=True))
#             edit_layout.addWidget(self.save_button)
#             edit_layout.addStretch()
#             self.cancel_button = QPushButton("Cancel")
#             self.cancel_button.clicked.connect(lambda: self.save_cancel_button_clicked(save=False))
#             edit_layout.addWidget(self.cancel_button)
#
#             c3_layout.addLayout(edit_layout)
#         else:
#             self.edit_button = None
#             self.save_button = None
#             self.cancel_button = None
#             c3_layout.addStretch()
#         main_layout.addLayout(c3_layout)
#
# class VISILAYOUT3(QSubInspectorWidget):
#     def __init__(self, *, title: str = "Visilibity", opacity_slider: bool = False, position: bool = False,
#                  edit_buttons: bool = False):
#         super().__init__(None)
#         self.graphics = []
#         main_layout = QGridLayout(self)
#         main_layout.setContentsMargins(0, 0, 0, 0)
#
#         self.visibility_checkbox = QCheckBox()
#         self.visibility_checkbox.setTristate(False)
#         self.visibility_checkbox.clicked.connect(self.visibility_checkbox_clicked)
#         main_layout.addWidget(self.visibility_checkbox, 0, 0)
#
#         name_layout = QHBoxLayout()
#         name_layout.setContentsMargins(0, 0, 0, 0)
#         self.title_label = QLabel(title)
#         name_layout.addWidget(self.title_label)
#         name_layout.addStretch()
#         name_layout.addWidget(QToolButton())
#         name_layout.addWidget(QToolButton())
#         main_layout.addLayout(name_layout, 0, 1)
#
#         main_layout.setColumnMinimumWidth(3, 20)
#
#         position_N_button = QToolButton()
#         position_N_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp))
#         # position_N_button.clicked.connect()
#         main_layout.addWidget(position_N_button, 0, 5)
#
#         pos_layout = QHBoxLayout()
#         pos_layout.setContentsMargins(0, 0, 0, 0)
#         pos_layout.addSpacing(10)
#         self.position_x = QSpinBox()
#         # self.position_x.setPrefix("x")
#         self.position_x.setMaximum(9999)
#         self.position_x.setValue(1234)
#         # self.position_x.valueChanged.connect()
#         pos_layout.addWidget(self.position_x)
#         self.position_y = QSpinBox()
#         # self.position_y.setPrefix("y")
#         self.position_y.setMaximum(9999)
#         self.position_y.setValue(2345)
#         # self.position_y.valueChanged.connect()
#         pos_layout.addWidget(self.position_y)
#
#         main_layout.addLayout(pos_layout, 0, 6)
#
#         main_layout.setColumnMinimumWidth(7, 20)
#
#
#         edit_layout = QHBoxLayout()
#         edit_layout.setContentsMargins(0, 0, 0, 0)
#         if edit_buttons is True:
#             self.edit_button = QPushButton("Edit")
#             self.edit_button.clicked.connect(self.edit_button_clicked)
#             edit_layout.addWidget(self.edit_button)
#             edit_layout.addSpacing(20)
#         else:
#             self.edit_button = None
#             edit_layout.addStretch()
#         self.delete_button = QToolButton()
#         self.delete_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TabCloseButton))
#         self.delete_button.clicked.connect(self.delete_button_clicked)
#         edit_layout.addWidget(self.delete_button)
#         main_layout.addLayout(edit_layout, 0, 8)
#
#         self.opacity_reset_button = QToolButton()
#         self.opacity_reset_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
#         self.opacity_reset_button.clicked.connect(self.opacity_reset_button_clicked)
#         main_layout.addWidget(self.opacity_reset_button, 1, 0)
#
#         self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
#         self.opacity_slider.setMinimum(0)
#         self.opacity_slider.setMaximum(100)
#         self.opacity_slider.valueChanged.connect(self.opacity_slider_changed)
#         main_layout.addWidget(self.opacity_slider, 1, 1)
#
#         position_W_button = QToolButton()
#         position_W_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowLeft))
#         # position_W_button.clicked.connect()
#         main_layout.addWidget(position_W_button, 1, 4)
#
#         position_S_button = QToolButton()
#         position_S_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown))
#         # position_S_button.clicked.connect()
#         main_layout.addWidget(position_S_button, 1, 5)
#
#         localize_layout = QHBoxLayout()
#         localize_layout.setContentsMargins(0, 0, 0, 0)
#         position_E_button = QToolButton()
#         position_E_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowRight))
#         # position_E_button.clicked.connect()
#         localize_layout.addWidget(position_E_button)
#         localize_layout.addStretch(0)
#         self.localize_button = QPushButton("Localize")
#         self.localize_button.clicked.connect(self.localize_button_clicked)
#         localize_layout.addWidget(self.localize_button)
#         main_layout.addLayout(localize_layout, 1, 6)
#
#         if edit_buttons is True:
#             save_cancel_layout = QHBoxLayout()
#             save_cancel_layout.setContentsMargins(0, 0, 0, 0)
#             self.save_button = QPushButton("Save")
#             self.save_button.setMinimumWidth(100)
#             self.save_button.clicked.connect(lambda: self.save_cancel_button_clicked(save=True))
#             save_cancel_layout.addWidget(self.save_button)
#             self.cancel_button = QPushButton("Cancel")
#             self.cancel_button.setMinimumWidth(100)
#             self.cancel_button.clicked.connect(lambda: self.save_cancel_button_clicked(save=False))
#             save_cancel_layout.addWidget(self.cancel_button)
#             main_layout.addLayout(save_cancel_layout, 1, 8)
#         else:
#             self.save_button = None
#             self.cancel_button = None

class QGeometrySIW(QSubInspectorWidget):
    def __init__(self, *, geometry_name: str = "Visilibity", position_buttons=False):
        super().__init__(None)
        self.graphics = []
        self.geometry_name = geometry_name
        self.init_actions()
        self.init_ui(position_buttons)

    @property
    def scene(self) -> QScene:
        current = self.parent()
        while not hasattr(current, "scene"):
            current = current.parent()
        return current.scene


    def init_actions(self):
        self.a_localize = QAction("Localize", self)
        self.a_localize.triggered.connect(self.localize_triggered)
        self.a_create = QAction("Create", self)
        self.a_create.triggered.connect(self.create_triggered)
        self.m_copy_from = QMenu("Copy from")
        self.a_unlock = QAction("Unlock", self)
        self.a_unlock.triggered.connect(self.unlock_triggered)
        self.a_lock = QAction("Lock", self)
        self.a_lock.triggered.connect(self.lock_triggered)
        self.a_delete = QAction("Delete", self)
        self.a_delete.triggered.connect(self.delete_triggered)
        self.useless = QAction("", self)
        self.useless.setEnabled(False)


        self.option_menu = QMenu(self)
        self.option_menu.setToolTipsVisible(True)
        self.option_menu.addAction(self.a_localize)
        self.option_menu.addSeparator()
        self.option_menu.addAction(self.a_create)
        self.option_menu.addMenu(self.m_copy_from)
        self.option_menu.addAction(self.a_unlock)
        self.option_menu.addAction(self.a_lock)
        self.option_menu.addSeparator()
        self.option_menu.addAction(self.a_delete)
        self.option_menu.addAction(self.useless)


    def init_ui(self, position_buttons):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        l1_layout = QHBoxLayout()
        l1_layout.setContentsMargins(0, 0, 0, 0)

        self.visibility_checkbox = QCheckBox()
        self.visibility_checkbox.setTristate(False)
        self.visibility_checkbox.clicked.connect(self.visibility_checkbox_clicked)
        l1_layout.addWidget(self.visibility_checkbox)

        self.geometry_name_label = QClickableLabel(self.geometry_name)
        self.geometry_name_label.double_clicked.connect(self.a_localize.trigger)
        l1_layout.addWidget(self.geometry_name_label)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.sliderMoved.connect(self.opacity_slider_moved)  # Do not handle all move TODO
        l1_layout.addWidget(self.opacity_slider)

        self.opacity_reset_button = QToolButton()
        self.opacity_reset_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        self.opacity_reset_button.clicked.connect(self.opacity_reset_button_clicked)
        l1_layout.addWidget(self.opacity_reset_button)

        l1_layout.addSpacing(20)

        self.action_button = QPushButton()
        self.action_button.setCheckable(True)
        self.action_button.setFixedWidth(80)
        l1_layout.addWidget(self.action_button)

        # l1_layout.addSpacing(30)

        self.menu_button = QToolButton(self)
        self.menu_button.setArrowType(Qt.ArrowType.DownArrow)
        self.menu_button.clicked.connect(self.open_menu)
        l1_layout.addWidget(self.menu_button)

        main_layout.addLayout(l1_layout)

        if position_buttons:
            l2_layout = QHBoxLayout()
            l2_layout.setContentsMargins(0, 0, 0, 0)
            l2_layout.addSpacing(80)

            grid_layout = QGridLayout()
            grid_layout.setContentsMargins(0, 0, 0, 0)

            position_N_button = QToolButton()
            position_N_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp))
            # position_N_button.clicked.connect()
            grid_layout.addWidget(position_N_button, 0, 1)

            position_W_button = QToolButton()
            position_W_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowLeft))
            # position_W_button.clicked.connect()
            grid_layout.addWidget(position_W_button, 1, 0)

            position_S_button = QToolButton()
            position_S_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown))
            # position_S_button.clicked.connect()
            grid_layout.addWidget(position_S_button, 1, 1)

            position_E_button = QToolButton()
            position_E_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowRight))
            # position_E_button.clicked.connect()
            grid_layout.addWidget(position_E_button, 1, 2)

            l2_layout.addLayout(grid_layout)

            l2_layout.addSpacing(30)

            self.position_x = QSpinBox()
            # self.position_x.setPrefix("x")
            self.position_x.setMaximum(9999)
            self.position_x.setValue(1234)
            self.position_x.setFixedWidth(60)
            # self.position_x.valueChanged.connect()
            l2_layout.addWidget(self.position_x)

            self.position_y = QSpinBox()
            # self.position_y.setPrefix("y")
            self.position_y.setMaximum(9999)
            self.position_y.setValue(2345)
            self.position_y.setFixedWidth(60)
            # self.position_y.valueChanged.connect()
            l2_layout.addWidget(self.position_y)

            self.position_combo_box = QComboBox()
            self.position_combo_box.addItems(["position 1", "position 2", "position 3"])
            l2_layout.addWidget(self.position_combo_box)

            l2_layout.addSpacing(60)
            main_layout.addLayout(l2_layout)


    def open_menu(self):
        self.m_copy_from.clear()
        actions = []
        for scene_item in self.scene.items():
            if isinstance(scene_item, type(self.graphics[0])):
                action = QAction(f"{scene_item.item.name}", self)
                actions.append(action)
                action.triggered.connect(lambda state, item=scene_item: self.copy_from_triggered(item))

        widget = SearchableMenu(actions, self.option_menu)
        action_widget = QWidgetAction(self.m_copy_from)
        action_widget.setDefaultWidget(widget)
        self.m_copy_from.addAction(action_widget)

        self.option_menu.exec(QCursor.pos())

    def visibility_checkbox_clicked(self):
        self.visibility_checkbox.setTristate(False)
        for graphic in self.graphics:
            graphic.setVisible(self.visibility_checkbox.isChecked())
        self.update_required.emit()

    def opacity_slider_moved(self):
        for graphic in self.graphics:
            graphic.setOpacity(self.opacity_slider.value() / 100)

    def opacity_reset_button_clicked(self):
        io = [graphic.initial_opacity for graphic in self.graphics]
        assert all([io[0] == e for e in io[1:]])
        self.opacity_slider.setValue(int(100 * io[0]))

    def localize_triggered(self):
        [graphic.setVisible(True) for graphic in self.graphics]
        rect = bounding_rect_of(self.graphics)
        self.scene.move_to_rect(rect)
        self.update_required.emit()

    def create_triggered(self):
        g = [graphic for graphic in self.graphics if graphic.state == GraphicState.NoGraph]
        g[0].enter_creation_mode(followers=g[1:])
        self.update_required.emit()

    def exit_creation_triggered(self):
        g = [graphic for graphic in self.graphics if graphic.state == GraphicState.Create]
        assert len(g) == 1
        g[0].exit_creation_mode()
        self.update_required.emit()

    def copy_from_triggered(self, graphic_item):
        for graphic in self.graphics:
            graphic.copy_from(graphic_item)
        self.value_changed.emit()
        self.update_required.emit()

    def unlock_triggered(self):
        for graphic in self.graphics:
            if graphic.state == GraphicState.Lock:
                graphic.unlock()
        self.update_required.emit()

    def lock_triggered(self):
        for graphic in self.graphics:
            if graphic.state == GraphicState.Unlock:
                graphic.lock()
        self.value_changed.emit()
        self.update_required.emit()

    def delete_triggered(self):
        # TODO remove the confirmation dialog box once the “Undo/Redo” feature is implemented
        if (n:=len(self.graphics)) == 1:
            msg = f"Do you really want to delete the \"{self.geometry_name}\" graphic ?"
        else:
            msg = f"Do you really want to delete all {n} \"{self.geometry_name}\" graphics ?"

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            [graphic.setVisible(False) for graphic in self.graphics]
            [graphic.delete() for graphic in self.graphics]
            self.value_changed.emit()
            self.update_required.emit()

    def connect_to(self, new_graphics):
        if not isinstance(new_graphics, list):
            new_graphics = [new_graphics]
        self.graphics = new_graphics
        visibility = [graphic.isVisible() for graphic in self.graphics]
        if all(visibility):
            self.visibility_checkbox.setCheckState(Qt.CheckState.Checked)
        elif any(visibility):
            self.visibility_checkbox.setCheckState(Qt.CheckState.PartiallyChecked)
        else:
            self.visibility_checkbox.setCheckState(Qt.CheckState.Unchecked)

        s = self.graphics[0].state
        if all(s == g.state for g in self.graphics[1:]):
            self.action_button.setEnabled(True)
            try:
                # Qt raise a TypeError if the signal "button.clicked" is not connected
                self.action_button.clicked.disconnect()
            except TypeError:
                pass
            if s == GraphicState.NoGraph:
                self.action_button.setChecked(False)
                self.action_button.setText("Create")
                self.action_button.clicked.connect(self.create_triggered)
            elif s == GraphicState.Lock:
                self.action_button.setChecked(False)
                self.action_button.setText("Unlock")
                self.action_button.clicked.connect(self.unlock_triggered)
            elif s == GraphicState.Unlock:
                self.action_button.setChecked(True)
                self.action_button.setText("Unlocked")
                self.action_button.clicked.connect(self.lock_triggered)
            elif s == GraphicState.Create:
                self.action_button.setChecked(True)
                self.action_button.setText("Creating")
                self.action_button.clicked.connect(self.exit_creation_triggered)
            else:
                raise
        else:
            self.action_button.setEnabled(False)
            self.action_button.setText("multiple")


        # Localize Action
        if (n:=[graphic.state != GraphicState.NoGraph for graphic in self.graphics].count(True)) > 0:
            self.a_localize.setEnabled(True)
            localize_tool_tip = f"Localize the {n} existing {self.geometry_name}{"s" if n > 1 else ""}"
            for graphic in self.graphics:
                if graphic.state != GraphicState.NoGraph:
                    localize_tool_tip += f"\n - {graphic.item.name}"
            self.a_localize.setToolTip(localize_tool_tip)
        else:
            self.a_localize.setEnabled(False)

        # Create Action
        if (n:=[graphic.state == GraphicState.NoGraph for graphic in self.graphics].count(True)) > 0:
            self.a_create.setEnabled(True)
            create_tool_tip = f"Create the {n} missing {self.geometry_name}{"s" if n > 1 else ""}"
            for graphic in self.graphics:
                if graphic.state == GraphicState.NoGraph:
                    create_tool_tip += f"\n - {graphic.item.name}"
            self.a_create.setToolTip(create_tool_tip)
        else:
            self.a_create.setEnabled(False)

        # Edit Action
        if (n:=[graphic.state == GraphicState.Lock for graphic in self.graphics].count(True)) > 0:
            self.a_unlock.setEnabled(True)
            edit_tool_tip = f"Edit the {n} {self.geometry_name}{"s" if n > 1 else ""} currently in fix mode"
            for graphic in self.graphics:
                if graphic.state == GraphicState.Lock:
                    edit_tool_tip += f"\n - {graphic.item.name}"
            self.a_unlock.setToolTip(edit_tool_tip)
        else:
            self.a_unlock.setEnabled(False)

        # Save Action
        if (n:=[graphic.state == GraphicState.Unlock for graphic in self.graphics].count(True)) > 0:
            self.a_lock.setEnabled(True)
            save_tool_tip = f"Save the {n} {self.geometry_name}{"s" if n > 1 else ""} currently in edit mode"
            for graphic in self.graphics:
                if graphic.state == GraphicState.Unlock:
                    save_tool_tip += f"\n - {graphic.item.name}"
            self.a_lock.setToolTip(save_tool_tip)
        else:
            self.a_lock.setEnabled(False)

        # Delete Action
        if (n:=[graphic.state != GraphicState.NoGraph for graphic in self.graphics].count(True)) > 0:
            self.a_delete.setEnabled(True)
            delete_tool_tip = f"Delete the {n} exiting {self.geometry_name}{"s" if n > 1 else ""}"
            for graphic in self.graphics:
                if graphic.state != GraphicState.NoGraph:
                    delete_tool_tip += f"\n - {graphic.item.name}"
            self.a_delete.setToolTip(delete_tool_tip)
        else:
            self.a_delete.setEnabled(False)

        min_opacity = min([int(100 * graphic.opacity()) for graphic in self.graphics])
        self.opacity_slider.setValue(min_opacity)



class Inspector(QWidget):

    def __init__(self):
        super().__init__()
        self.items = []
        self.main_layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()
        self.settings_button = QToolButton(self)
        self.settings_button.setArrowType(Qt.ArrowType.DownArrow)
        header_layout.addWidget(self.settings_button)
        self.title = QLabel(self)
        f = self.title.font()
        f.setPointSizeF(18)
        self.title.setFont(f)
        header_layout.addWidget(self.title)
        header_layout.addStretch()

        self.main_layout.addLayout(header_layout)
        self.main_layout.addSpacing(20)
        # self.main_layout design is left up to the child

    def connect_to(self, new_items):
        self.items = new_items

        if (n:=len(new_items)) == 1:
            self.title.setText(new_items[0].name)
            self.title.setToolTip(None)
        else:
            assert all([type(new_items[0]) == type(e) for e in new_items])
            plural = f"{new_items[0]._odv_object.__class__.__name__}s"
            if plural.endswith("ys"):
                plural = plural.replace("ys", "ies")
            self.title.setText(f"Linked to {n} {plural}")
            self.title.setToolTip("\n".join([e.name for e in new_items]))

    def update(self):
        self.connect_to(self.items)
        super().update()

    def update_item(self):
        for item in self.items:
            item.update()

    def update_both(self):
        self.update_item()
        self.update()
