from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QCheckBox, QPushButton, QSlider

from odv.data_section.mask import Mask, MaskLayer, MaskEntry
from qt.common.utils import bounding_rect_of, mask_image_to_qimage
from qt.control.control_section import QSectionControl
from qt.control.generic_inspector import Inspector
from qt.control.generic_tree import QGenericTreeItem
from qt.graphics import GraphicMask


class MaskEntryInspector(Inspector):
    def __init__(self):
        super().__init__()

        ### Visibility Widget ###################################################
        visibility_layout = QHBoxLayout()
        visibility_layout.setContentsMargins(0, 0, 0, 0)

        visibility_layout.addWidget(QLabel("Visibility"))

        self.visibility_checkbox = QCheckBox()
        self.visibility_checkbox.setTristate(False)
        self.visibility_checkbox.clicked.connect(self.visibility_checkbox_clicked)
        visibility_layout.addWidget(self.visibility_checkbox)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self.opacity_slider_changed)
        visibility_layout.addWidget(self.opacity_slider)

        self.localise_button = QPushButton("Localise")
        self.localise_button.clicked.connect(self.localise_button_clicked)
        visibility_layout.addWidget(self.localise_button)

        self.main_layout.addLayout(visibility_layout)
        #########################################################################

        ### Geometry Edition Widget #############################################
        mask_edit_layout = QHBoxLayout()
        mask_edit_layout.setContentsMargins(0, 0, 0, 0)

        mask_edit_layout.addWidget(QLabel("Binary mask"))

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_button_clicked)
        mask_edit_layout.addWidget(self.edit_button)

        mask_edit_layout.addStretch()

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(lambda : self.save_cancel_button_clicked(save=True))
        mask_edit_layout.addWidget(self.save_button)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(lambda : self.save_cancel_button_clicked(save=False))
        mask_edit_layout.addWidget(self.cancel_button)

        self.main_layout.addLayout(mask_edit_layout)
        #########################################################################
        #
        # ### Infos Widget ########################################################
        # self.geometry_info_label = QLabel()
        #
        # self.main_layout.addWidget(self.geometry_info_label)
        # #########################################################################

        self.main_layout.addStretch()

    def visibility_checkbox_clicked(self):
        self.visibility_checkbox.setTristate(False)
        self.visibility_checkbox.update()
        for item in self.items:
            item.graphic_mask.setVisible(self.visibility_checkbox.isChecked())
            item.update()

    def opacity_slider_changed(self):
        for item in self.items:
            item.graphic_mask.setOpacity(self.opacity_slider.value() / 100)


    def edit_button_clicked(self):
        if self.visibility_checkbox.checkState() != Qt.CheckState.Checked:
            self.visibility_checkbox.click()
        [item.graphic_mask.enter_edit_mode() for item in self.items]
        self.edit_button.setDisabled(True)
        self.save_button.setEnabled(True)
        self.cancel_button.setEnabled(True)

    def save_cancel_button_clicked(self, save):
        [item.graphic_mask.exit_edit_mode(save=save) for item in self.items]
        self.edit_button.setEnabled(True)
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        # if save is True:
        #     for item in self.items:
        #         item.obstacle.poly = item.graphic_mask.polygon


    def connect_to(self, new_items):
        super().connect_to(new_items)
        if all([item.graphic_mask.isVisible() for item in self.items]):
            self.visibility_checkbox.setCheckState(Qt.CheckState.Checked)
        elif any([item.graphic_mask.isVisible() for item in self.items]):
            self.visibility_checkbox.setCheckState(Qt.CheckState.PartiallyChecked)
        else:
            self.visibility_checkbox.setCheckState(Qt.CheckState.Unchecked)

        min_opacity = min([int(100 * item.graphic_mask.opacity()) for item in self.items])
        self.opacity_slider.setValue(min_opacity)

        if len(self.items) == 1:
            self.edit_button.setText("Edit")
            self.edit_button.setDisabled(self.items[0].graphic_mask.edit)
            self.save_button.setText("Save")
            self.save_button.setEnabled(self.items[0].graphic_mask.edit)
            self.cancel_button.setText("Cancel")
            self.cancel_button.setEnabled(self.items[0].graphic_mask.edit)
        else:
            self.edit_button.setText("Edit All")
            self.edit_button.setDisabled(all([item.graphic_mask.edit for item in self.items]))
            self.save_button.setText("Save All")
            self.save_button.setEnabled(any([item.graphic_mask.edit for item in self.items]))
            self.cancel_button.setText("Cancel All")
            self.cancel_button.setEnabled(any([item.graphic_mask.edit for item in self.items]))

    def localise_button_clicked(self):
        if self.visibility_checkbox.checkState() != Qt.CheckState.Checked:
            self.visibility_checkbox.click()
        rect = bounding_rect_of([item.graphic_mask for item in self.items])
        self.items[0].graphic_mask.scene().move_to_rect(rect)



class MaskEntryItem(QGenericTreeItem):
    inspector_type = MaskEntryInspector
    draggable = True

    def __init__(self, section_control, mask_entry: MaskEntry):
        super().__init__(section_control, mask_entry)
        self.mask_entry = mask_entry

        # self.graphic_mask = GraphicMask(self, mask_image_to_qimage(self.mask_entry.mask_image, true_color=(0, 180, 255)), self.mask_entry.position)
        self.graphic_mask = GraphicMask(self, self.mask_entry.mask_image, self.mask_entry.position)
        self.graphic_mask.setOpacity(0.4)
        self.add_graphic(self.graphic_mask)

#########################################################################

class LayerInspector(Inspector):
    def __init__(self):
        super().__init__()
        self.main_layout.addStretch()

    def connect_to(self, new_items):
        super().connect_to(new_items)



class LayerItem(QGenericTreeItem):
    inspector_type = LayerInspector
    draggable = True

    def __init__(self, section_control, layer: MaskLayer):
        super().__init__(section_control, layer)
        self.layer = layer

#########################################################################

class MaskInspector(Inspector):
    def __init__(self):
        super().__init__()
        self.main_layout.addStretch()

    def connect_to(self, new_items):
        super().connect_to(new_items)



class MaskItem(QGenericTreeItem):
    inspector_type = MaskInspector
    draggable = False

    def __init__(self, section_control, mask:Mask):
        super().__init__(section_control, mask)
        self.mask = mask

#########################################################################

class QMaskControl(QSectionControl):
    item_types = {Mask: MaskItem,
                  MaskLayer: LayerItem,
                  MaskEntry: MaskEntryItem}
