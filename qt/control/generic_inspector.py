from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QCheckBox, QSlider, QStyle, \
    QPushButton

from qt.common.utils import bounding_rect_of



class QSubInspectorWidget(QWidget):
    update_required = pyqtSignal()
    value_changed = pyqtSignal()



class QVisibilitySIW(QSubInspectorWidget):

    def __init__(self, *, title:str="Visilibity", opacity_slider:bool=False, edit_buttons:bool=False):
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

    def visibility_checkbox_clicked(self):
        self.visibility_checkbox.setTristate(False)
        self.visibility_checkbox.update()
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
        self.update_required.emit()
        rect = bounding_rect_of(self.graphics)
        # access the scene using the first graphic
        self.graphics[0].scene().move_to_rect(rect)

    def edit_button_clicked(self):
        [graphic.enter_edit_mode() for graphic in self.graphics]
        [graphic.setVisible(True) for graphic in self.graphics]
        self.update_required.emit()
        self.edit_button.setDisabled(True)
        self.save_button.setEnabled(True)
        self.cancel_button.setEnabled(True)

    def save_cancel_button_clicked(self, save):
        [graphic.exit_edit_mode(save=save) for graphic in self.graphics]
        self.update_required.emit()
        self.edit_button.setEnabled(True)
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        if save is True:
            self.value_changed.emit()

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

        if self.opacity_slider is not None:
            min_opacity = min([int(100 * graphic.opacity()) for graphic in self.graphics])
            self.opacity_slider.setValue(min_opacity)

        if self.edit_button is not None:
            if len(self.graphics) == 1:
                self.edit_button.setText("Edit")
                self.edit_button.setDisabled(self.graphics[0].edit)
                self.save_button.setText("Save")
                self.save_button.setEnabled(self.graphics[0].edit)
                self.cancel_button.setText("Cancel")
                self.cancel_button.setEnabled(self.graphics[0].edit)
            else:
                self.edit_button.setText("Edit All")
                self.edit_button.setDisabled(all([graphic.edit for graphic in self.graphics]))
                self.save_button.setText("Save All")
                self.save_button.setEnabled(any([graphic.edit for graphic in self.graphics]))
                self.cancel_button.setText("Cancel All")
                self.cancel_button.setEnabled(any([graphic.edit for graphic in self.graphics]))



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
            self.title.setText(f"Linked to {n} {new_items[0]._odv_object.__class__.__name__}{"s" if n != 1 else ""}")
            self.title.setToolTip("\n".join([e.name for e in new_items]))

    def update(self):
        self.connect_to(self.items)
        for item in self.items:
            item.update()
        super().update()
