from PyQt6.QtCore import QRegularExpression
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog, \
    QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsRectItem

from common import ReadStream, Image
from odv.data_section import Bgnd
from qt.common.simple_messagebox import QErrorBox
from qt.common.utils import image_to_qimage
from qt.control.control_section import QSectionControl
from qt.control.generic_inspector import Inspector, QVisibilitySIW
from qt.control.generic_tree import QGenericTreeItem
from qt.graphics import GraphicMap


class BgndInspector(Inspector):

    def __init__(self):
        super().__init__()

        # BgndInspector can only be connected to a single item
        self.item = None

        self.visibility_siw = QVisibilitySIW(opacity_slider=True)
        self.visibility_siw.update_required.connect(self.update)
        self.main_layout.addWidget(self.visibility_siw)

        ### DVM filename Widget #################################################
        dvm_file_layout = QHBoxLayout()
        dvm_file_layout.setContentsMargins(0, 0, 0, 0)

        dvm_file_layout.addWidget(QLabel("DVM Filename"))

        self.dvm_line_edit = QLineEdit()
        self.dvm_line_edit.setMaxLength(32)
        self.dvm_line_edit.setValidator(QRegularExpressionValidator(QRegularExpression("[A-Za-z0-9_]+")))
        self.dvm_line_edit.textChanged.connect(self.dvm_line_edit_changed)
        dvm_file_layout.addWidget(self.dvm_line_edit)

        self.main_layout.addLayout(dvm_file_layout)
        #########################################################################

        ### DVM info Widget #####################################################
        dvm_info_layout = QHBoxLayout()
        dvm_info_layout.setContentsMargins(0, 0, 0, 0)

        self.dvm_size_label = QLabel()
        dvm_info_layout.addWidget(self.dvm_size_label)

        dvm_info_layout.addStretch()

        self.change_image_button = QPushButton("Change Image")
        self.change_image_button.clicked.connect(self.change_image_button_clicked)
        dvm_info_layout.addWidget(self.change_image_button)

        self.main_layout.addLayout(dvm_info_layout)
        #########################################################################

        self.main_layout.addStretch()

        ### Minimap Widget ######################################################
        self.minimap_scene = QGraphicsScene()
        self.minimap_viewport = QGraphicsView(self.minimap_scene)
        self.minimap_viewport.scale(1.5, 1.5)
        self.minimap_viewport.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.minimap_viewport.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.minimap_item = None
        self.minimap_rect_item = None
        self.factor_w = 1
        self.factor_h = 1

        self.main_layout.addWidget(self.minimap_viewport)
        #########################################################################

        ### Rebuild Minimap Widget ##############################################
        rebuild_minimap_layout = QHBoxLayout()
        rebuild_minimap_layout.setContentsMargins(0, 0, 0, 0)

        rebuild_minimap_layout.addStretch()

        self.change_image_button = QPushButton("Rebuild Minimap from the Map")
        self.change_image_button.clicked.connect(self.rebuild_minimap_clicked)
        rebuild_minimap_layout.addWidget(self.change_image_button)

        self.main_layout.addLayout(rebuild_minimap_layout)
        #########################################################################

    def change_image_button_clicked(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        filters = ["Image or DVM (*.png *.bmp *.dvm)",
                   "BMP Image (*.bmp)",
                   "PNG Image (*.png)",
                   "DVM File (*.dvm)",]
        dialog.setNameFilters(filters)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if len(filenames) == 1:
                if filenames[0].lower().endswith(".dvm"):
                    dvm_stream = ReadStream.from_file(filenames[0])
                    new_image = dvm_stream.read(Image)
                else:
                    new_image = Image.from_file(filenames[0])
                self.item.bgnd.map_image = new_image
                self.item.reset_graphic_map()
                self.update()

    def rebuild_minimap_clicked(self):
        QErrorBox("This tool rebuilds a minimap from the map,\nbut is not yet available.").exec()

    def dvm_line_edit_changed(self):
        self.item.bgnd.dvm_filename = self.dvm_line_edit.text()

    def refresh_minimap(self, rect_view: QRectF):
        r = rect_view
        self.minimap_rect_item.setRect(r.x() / self.factor_w, r.y() / self.factor_h, r.width() / self.factor_w, r.height() / self.factor_w)
        self.minimap_viewport.centerOn(self.minimap_item.boundingRect().center())

    def connect_to(self, new_items):
        # BgndInspector can only be connected to a single item
        assert len(new_items) == 1
        super().connect_to(new_items)
        self.item = self.items[0]

        minimap_w = self.item.bgnd.minimap_image.width
        minimap_h = self.item.bgnd.minimap_image.height
        map_w = self.item.bgnd.map_image.width
        map_h = self.item.bgnd.map_image.height
        self.factor_w = map_w / minimap_w
        self.factor_h = map_h / minimap_h

        self.visibility_siw.connect_to(self.item.graphic_map)

        self.dvm_line_edit.setText(self.item.bgnd.dvm_filename)
        self.dvm_size_label.setText(f"DVM Image Size: {map_w} x {map_h}")

        self.minimap_scene.clear()
        mf = 0.15  # marge factor
        self.minimap_scene.setSceneRect(- mf * minimap_w,
                                        - mf * minimap_h,
                                        (2 * mf + 1) * minimap_w,
                                        (2 * mf + 1) * minimap_h)
        self.minimap_item = QGraphicsPixmapItem(QPixmap(image_to_qimage(self.item.bgnd.minimap_image)))
        self.minimap_scene.addItem(self.minimap_item)
        self.minimap_rect_item = QGraphicsRectItem()
        self.minimap_scene.addItem(self.minimap_rect_item)
        self.item.section_control.scene.viewport().view_changed.connect(self.refresh_minimap)


class BgndItem(QGenericTreeItem):
    inspector_type = BgndInspector

    def __init__(self, section_control, bgnd:Bgnd):
        super().__init__(section_control, bgnd)
        self.bgnd = bgnd

        self.graphic_map = None
        self.reset_graphic_map()

    def reset_graphic_map(self):
        if self.graphic_map is not None:
            self.remove_graphic(self.graphic_map)
            del self.graphic_map
        self.graphic_map = GraphicMap(self, image_to_qimage(self.bgnd.map_image))
        self.add_graphic(self.graphic_map)
        self.graphic_map.setVisible(True)



class QBgndControl(QSectionControl):
    item_types = {Bgnd: BgndItem}
