from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QCheckBox, QSlider, QStyle, \
    QPushButton, QSpinBox, QGridLayout, QMessageBox, QMenu

from qt.common.utils import bounding_rect_of
from qt.graphics.base import GraphicState


class QSubInspectorWidget(QWidget):
    update_required = pyqtSignal()
    value_changed = pyqtSignal()

class VISILAYOUT1(QSubInspectorWidget):
    def __init__(self, *, title: str = "Visilibity", opacity_slider: bool = False, position: bool = False,
                 edit_buttons: bool = False):
        super().__init__(None)
        self.graphics = []
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # if title != "":
        #     title_layout = QHBoxLayout()
        #     title_layout.setContentsMargins(0, 0, 0, 0)
        #
        #     title_layout.addSpacing(50)
        #     title_layout.addWidget(QLabel(title))
        #     title_layout.addStretch()
        #
        #     main_layout.addLayout(title_layout)

        visibility_layout = QHBoxLayout()
        visibility_layout.setContentsMargins(0, 0, 0, 0)

        visibility_layout.addWidget(QLabel(title))

        self.visibility_checkbox = QCheckBox()
        self.visibility_checkbox.setTristate(False)
        self.visibility_checkbox.clicked.connect(self.visibility_checkbox_clicked)
        visibility_layout.addWidget(self.visibility_checkbox)

        if opacity_slider is True:
            self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
            self.opacity_slider.setMinimum(0)
            self.opacity_slider.setMaximum(100)
            self.opacity_slider.valueChanged.connect(self.opacity_slider_changed)
            visibility_layout.addWidget(self.opacity_slider)

            self.opacity_reset_button = QToolButton()
            icon = self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)  # SP_DialogResetButton
            self.opacity_reset_button.setIcon(icon)
            self.opacity_reset_button.clicked.connect(self.opacity_reset_button_clicked)

            visibility_layout.addWidget(self.opacity_reset_button)

            visibility_layout.addSpacing(120)
        else:
            self.opacity_slider = None
            self.opacity_reset_button = None

            visibility_layout.addStretch()

        self.localise_button = QPushButton("Localise")
        self.localise_button.clicked.connect(self.localise_button_clicked)
        visibility_layout.addWidget(self.localise_button)

        main_layout.addLayout(visibility_layout)

        if edit_buttons is True:
            edit_layout = QHBoxLayout()
            edit_layout.setContentsMargins(0, 0, 0, 0)

            self.edit_button = QPushButton("Edit")
            self.edit_button.clicked.connect(self.edit_button_clicked)
            edit_layout.addWidget(self.edit_button)

            edit_layout.addStretch()

            self.save_button = QPushButton("Save")
            self.save_button.clicked.connect(lambda: self.save_cancel_button_clicked(save=True))
            edit_layout.addWidget(self.save_button)
            self.cancel_button = QPushButton("Cancel")
            self.cancel_button.clicked.connect(lambda: self.save_cancel_button_clicked(save=False))
            edit_layout.addWidget(self.cancel_button)

            main_layout.addLayout(edit_layout)
        else:
            self.edit_button = None
            self.save_button = None
            self.cancel_button = None

class VISILAYOUT2(QSubInspectorWidget):
    def __init__(self, *, title:str="Visilibity", opacity_slider:bool=False, position:bool=False, edit_buttons:bool=False):
        super().__init__(None)
        self.graphics = []
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        c1_layout = QVBoxLayout()
        c1_layout.setContentsMargins(0, 0, 0, 0)

        visibility_layout = QHBoxLayout()
        visibility_layout.setContentsMargins(0, 0, 0, 0)
        self.visibility_checkbox = QCheckBox()
        self.visibility_checkbox.setTristate(False)
        self.visibility_checkbox.clicked.connect(self.visibility_checkbox_clicked)
        visibility_layout.addWidget(self.visibility_checkbox)
        visibility_layout.addWidget(QLabel(title))
        visibility_layout.addStretch()
        c1_layout.addLayout(visibility_layout)

        opacity_layout = QHBoxLayout()
        opacity_layout.setContentsMargins(0, 0, 0, 0)
        if opacity_slider is True:
            self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
            self.opacity_slider.setMinimum(0)
            self.opacity_slider.setMaximum(100)
            self.opacity_slider.valueChanged.connect(self.opacity_slider_changed)
            opacity_layout.addWidget(self.opacity_slider)

            self.opacity_reset_button = QToolButton()
            icon = self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)  # SP_DialogResetButton
            self.opacity_reset_button.setIcon(icon)
            self.opacity_reset_button.clicked.connect(self.opacity_reset_button_clicked)
            opacity_layout.addWidget(self.opacity_reset_button)
        else:
            self.opacity_slider = None
            self.opacity_reset_button = None
            opacity_layout.addStretch()
        c1_layout.addLayout(opacity_layout)

        position_layout = QHBoxLayout()
        position_layout.setContentsMargins(0, 0, 0, 0)
        if position is True:
            position_layout.addStretch()

            self.position_x = QSpinBox()
            self.position_x.setPrefix("x ")
            self.position_x.setValue(1234)
            # self.position_x.valueChanged.connect()
            position_layout.addWidget(self.position_x)

            self.position_y = QSpinBox()
            self.position_y.setPrefix("y ")
            self.position_y.setValue(5678)
            # self.position_y.valueChanged.connect()
            position_layout.addWidget(self.position_y)
        else:
            self.position_x = None
            self.position_y = None
            position_layout.addStretch()
        c1_layout.addLayout(position_layout)

        main_layout.addLayout(c1_layout)
        main_layout.addSpacing(15)

        c2_layout = QGridLayout()
        c2_layout.setContentsMargins(0, 0, 0, 0)
        if position is True:
            position_N_button = QToolButton()
            position_N_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp))
            # position_N_button.clicked.connect()
            c2_layout.addWidget(position_N_button, 0, 1)
            position_E_button = QToolButton()
            position_E_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowRight))
            # position_E_button.clicked.connect()
            c2_layout.addWidget(position_E_button, 1, 2)
            position_W_button = QToolButton()
            position_W_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowLeft))
            # position_W_button.clicked.connect()
            c2_layout.addWidget(position_W_button, 1, 0)
            position_S_button = QToolButton()
            position_S_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown))
            # position_S_button.clicked.connect()
            c2_layout.addWidget(position_S_button, 2, 1)

        main_layout.addLayout(c2_layout)
        main_layout.addSpacing(15)

        c3_layout = QVBoxLayout()
        c3_layout.setContentsMargins(0, 0, 0, 0)

        localise_layout = QHBoxLayout()

        self.localise_button = QPushButton("Localise")
        self.localise_button.clicked.connect(self.localise_button_clicked)
        localise_layout.addWidget(self.localise_button)
        localise_layout.addStretch()
        delete_button = QToolButton()
        delete_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TabCloseButton))
        # delete_button.clicked.connect()
        localise_layout.addWidget(delete_button)

        c3_layout.addLayout(localise_layout)

        if edit_buttons is True:
            self.edit_button = QPushButton("Edit")
            self.edit_button.clicked.connect(self.edit_button_clicked)
            c3_layout.addWidget(self.edit_button)

            edit_layout = QHBoxLayout()
            edit_layout.setContentsMargins(0, 0, 0, 0)
            self.save_button = QPushButton("Save")
            self.save_button.clicked.connect(lambda: self.save_cancel_button_clicked(save=True))
            edit_layout.addWidget(self.save_button)
            edit_layout.addStretch()
            self.cancel_button = QPushButton("Cancel")
            self.cancel_button.clicked.connect(lambda: self.save_cancel_button_clicked(save=False))
            edit_layout.addWidget(self.cancel_button)

            c3_layout.addLayout(edit_layout)
        else:
            self.edit_button = None
            self.save_button = None
            self.cancel_button = None
            c3_layout.addStretch()
        main_layout.addLayout(c3_layout)

class VISILAYOUT3(QSubInspectorWidget):
    def __init__(self, *, title: str = "Visilibity", opacity_slider: bool = False, position: bool = False,
                 edit_buttons: bool = False):
        super().__init__(None)
        self.graphics = []
        main_layout = QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.visibility_checkbox = QCheckBox()
        self.visibility_checkbox.setTristate(False)
        self.visibility_checkbox.clicked.connect(self.visibility_checkbox_clicked)
        main_layout.addWidget(self.visibility_checkbox, 0, 0)

        name_layout = QHBoxLayout()
        name_layout.setContentsMargins(0, 0, 0, 0)
        self.title_label = QLabel(title)
        name_layout.addWidget(self.title_label)
        name_layout.addStretch()
        name_layout.addWidget(QToolButton())
        name_layout.addWidget(QToolButton())
        main_layout.addLayout(name_layout, 0, 1)

        main_layout.setColumnMinimumWidth(3, 20)

        position_N_button = QToolButton()
        position_N_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp))
        # position_N_button.clicked.connect()
        main_layout.addWidget(position_N_button, 0, 5)

        pos_layout = QHBoxLayout()
        pos_layout.setContentsMargins(0, 0, 0, 0)
        pos_layout.addSpacing(10)
        self.position_x = QSpinBox()
        # self.position_x.setPrefix("x")
        self.position_x.setMaximum(9999)
        self.position_x.setValue(1234)
        # self.position_x.valueChanged.connect()
        pos_layout.addWidget(self.position_x)
        self.position_y = QSpinBox()
        # self.position_y.setPrefix("y")
        self.position_y.setMaximum(9999)
        self.position_y.setValue(2345)
        # self.position_y.valueChanged.connect()
        pos_layout.addWidget(self.position_y)

        main_layout.addLayout(pos_layout, 0, 6)

        main_layout.setColumnMinimumWidth(7, 20)


        edit_layout = QHBoxLayout()
        edit_layout.setContentsMargins(0, 0, 0, 0)
        if edit_buttons is True:
            self.edit_button = QPushButton("Edit")
            self.edit_button.clicked.connect(self.edit_button_clicked)
            edit_layout.addWidget(self.edit_button)
            edit_layout.addSpacing(20)
        else:
            self.edit_button = None
            edit_layout.addStretch()
        self.delete_button = QToolButton()
        self.delete_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TabCloseButton))
        self.delete_button.clicked.connect(self.delete_button_clicked)
        edit_layout.addWidget(self.delete_button)
        main_layout.addLayout(edit_layout, 0, 8)

        self.opacity_reset_button = QToolButton()
        self.opacity_reset_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        self.opacity_reset_button.clicked.connect(self.opacity_reset_button_clicked)
        main_layout.addWidget(self.opacity_reset_button, 1, 0)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.valueChanged.connect(self.opacity_slider_changed)
        main_layout.addWidget(self.opacity_slider, 1, 1)

        position_W_button = QToolButton()
        position_W_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowLeft))
        # position_W_button.clicked.connect()
        main_layout.addWidget(position_W_button, 1, 4)

        position_S_button = QToolButton()
        position_S_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown))
        # position_S_button.clicked.connect()
        main_layout.addWidget(position_S_button, 1, 5)

        localise_layout = QHBoxLayout()
        localise_layout.setContentsMargins(0, 0, 0, 0)
        position_E_button = QToolButton()
        position_E_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowRight))
        # position_E_button.clicked.connect()
        localise_layout.addWidget(position_E_button)
        localise_layout.addStretch(0)
        self.localise_button = QPushButton("Localise")
        self.localise_button.clicked.connect(self.localise_button_clicked)
        localise_layout.addWidget(self.localise_button)
        main_layout.addLayout(localise_layout, 1, 6)

        if edit_buttons is True:
            save_cancel_layout = QHBoxLayout()
            save_cancel_layout.setContentsMargins(0, 0, 0, 0)
            self.save_button = QPushButton("Save")
            self.save_button.setMinimumWidth(100)
            self.save_button.clicked.connect(lambda: self.save_cancel_button_clicked(save=True))
            save_cancel_layout.addWidget(self.save_button)
            self.cancel_button = QPushButton("Cancel")
            self.cancel_button.setMinimumWidth(100)
            self.cancel_button.clicked.connect(lambda: self.save_cancel_button_clicked(save=False))
            save_cancel_layout.addWidget(self.cancel_button)
            main_layout.addLayout(save_cancel_layout, 1, 8)
        else:
            self.save_button = None
            self.cancel_button = None

class VISILAYOUT4(QSubInspectorWidget):
    def __init__(self, *, title: str = "Visilibity"):
        super().__init__(None)
        self.graphics = []

        l1_layout = QHBoxLayout()
        l1_layout.setContentsMargins(0, 0, 0, 0)

        self.visibility_checkbox = QCheckBox()
        self.visibility_checkbox.setTristate(False)
        self.visibility_checkbox.clicked.connect(self.visibility_checkbox_clicked)
        l1_layout.addWidget(self.visibility_checkbox)

        self.title_label = QLabel(title)
        l1_layout.addWidget(self.title_label)

        l1_layout.addStretch()

        self.localise_button = QPushButton("Localise")
        self.localise_button.clicked.connect(self.localise_button_clicked)
        l1_layout.addWidget(self.localise_button)

        self.settings_button = QToolButton(self)
        self.settings_button.setArrowType(Qt.ArrowType.DownArrow)
        self.settings_button.clicked.connect(self.open_option_menu)
        l1_layout.addWidget(self.settings_button)


        l2_layout = QHBoxLayout()
        l2_layout.setContentsMargins(0, 0, 0, 0)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.valueChanged.connect(self.opacity_slider_changed)
        l2_layout.addWidget(self.opacity_slider)

        self.opacity_reset_button = QToolButton()
        self.opacity_reset_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        self.opacity_reset_button.clicked.connect(self.opacity_reset_button_clicked)
        l2_layout.addWidget(self.opacity_reset_button)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(l1_layout)
        main_layout.addLayout(l2_layout)


    def open_option_menu(self):
        option_menu = QMenu()
        a_create = QAction("Create")
        a_edit = QAction("Edit")
        a_save = QAction("Save")
        a_cancel = QAction("Cancel")
        a_delete = QAction("Delete")
        # a_finalize.triggered.connect(lambda: self.pointer_item.exit_creation_mode(save=True))
        option_menu.addAction(a_create)
        option_menu.addAction(a_edit)
        option_menu.addAction(a_save)
        option_menu.addAction(a_cancel)
        option_menu.addAction(a_delete)
        option_menu.exec(QCursor.pos())





class QVisibilitySIW(VISILAYOUT4):

    def visibility_checkbox_clicked(self):
        self.visibility_checkbox.setTristate(False)
        # self.visibility_checkbox.update()
        for graphic in self.graphics:
            graphic.setVisible(self.visibility_checkbox.isChecked())
        self.update_required.emit()

    def opacity_slider_changed(self):
        for graphic in self.graphics:
            graphic.setOpacity(self.opacity_slider.value() / 100)

    def opacity_reset_button_clicked(self):
        io = [graphic.initial_opacity for graphic in self.graphics]
        assert all([io[0] == e for e in io[1:]])
        self.opacity_slider.setValue(int(100 * io[0]))

    def localise_button_clicked(self):
        [graphic.setVisible(True) for graphic in self.graphics]
        rect = bounding_rect_of(self.graphics)
        # access the scene using the first graphic
        self.graphics[0].scene().move_to_rect(rect)
        self.update_required.emit()

    def edit_button_clicked(self):
        if self.graphics[0].state == GraphicState.Fix:
            [graphic.enter_edit_mode() for graphic in self.graphics]
            [graphic.setVisible(True) for graphic in self.graphics]
        elif self.graphics[0].state == GraphicState.NoGraph:
            [graphic.enter_creation_mode() for graphic in self.graphics]
            [graphic.setVisible(True) for graphic in self.graphics]
        # self.edit_button.setDisabled(True)
        # self.save_button.setEnabled(True)
        # self.cancel_button.setEnabled(True)
        self.update_required.emit()

    def save_cancel_button_clicked(self, save):
        [graphic.exit_edit_mode(save=save) for graphic in self.graphics]
        # self.edit_button.setEnabled(True)
        # self.save_button.setDisabled(True)
        # self.cancel_button.setDisabled(True)
        self.update_required.emit()
        if save is True:
            self.value_changed.emit()

    def delete_button_clicked(self):
        if (n:=len(self.graphics)) == 1:
            msg = f"Do you really want to delete the \"{self.title_label.text()}\" graphic ?"
        else:
            msg = f"Do you really want to delete all {n} \"{self.title_label.text()}\" graphics ?"

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # self.save_button.setDisabled(True)
            # self.cancel_button.setDisabled(True)
            # self.edit_button.setEnabled(True)
            [graphic.setVisible(False) for graphic in self.graphics]
            [graphic.delete() for graphic in self.graphics]
            self.update_required.emit()
            # if self.opacity_slider is not None:
            #     self.opacity_reset_button_clicked()
            #     self.opacity_slider.setDisabled(True)
            #     self.opacity_reset_button.setDisabled(True)


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

        # if self.opacity_slider is not None:
        min_opacity = min([int(100 * graphic.opacity()) for graphic in self.graphics])
        self.opacity_slider.setValue(min_opacity)

        # if self.edit_button is not None:
        #     if len(self.graphics) == 1:
        #         match self.graphics[0].state:
        #             case GraphicState.Fix:
        #                 self.edit_button.setText("Edit")
        #                 self.edit_button.setEnabled(True)
        #                 self.save_button.setText("Save")
        #                 self.save_button.setDisabled(True)
        #                 self.cancel_button.setText("Cancel")
        #                 self.cancel_button.setDisabled(True)
        #             case GraphicState.Edit:
        #                 self.edit_button.setText("Edit")
        #                 self.edit_button.setDisabled(True)
        #                 self.save_button.setText("Save")
        #                 self.save_button.setEnabled(True)
        #                 self.cancel_button.setText("Cancel")
        #                 self.cancel_button.setEnabled(True)
        #             case GraphicState.NoGraph:
        #                 self.edit_button.setText("Create")
        #                 self.edit_button.setEnabled(True)
        #                 self.save_button.setText("Save")
        #                 self.save_button.setDisabled(True)
        #                 self.cancel_button.setText("Cancel")
        #                 self.cancel_button.setDisabled(True)
        #             case GraphicState.Create:
        #                 self.edit_button.setText("Create")
        #                 self.edit_button.setDisabled(True)
        #                 self.save_button.setText("Save")
        #                 self.save_button.setDisabled(True)
        #                 self.cancel_button.setText("Cancel")
        #                 self.cancel_button.setEnabled(True)
        #
        #
        #     else:
        #         pass
        #         # self.edit_button.setText("Edit All")
        #         # self.edit_button.setDisabled(all(graphic.edit for graphic in self.graphics))
        #         # self.save_button.setText("Save All")
        #         # self.save_button.setEnabled(any([graphic.edit for graphic in self.graphics]))
        #         # self.cancel_button.setText("Cancel All")
        #         # self.cancel_button.setEnabled(any([graphic.edit for graphic in self.graphics]))



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
