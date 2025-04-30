from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStyle, QLabel

from common import Image
from dvm.dvm_parser import LevelMap, DvmParser
from qt.common.utils import image_to_qimage
from qt.control.subInspector import InfoQInspectorWidget, PixmapQInspectorWidget
from qt.control_old.tab__abstract import QTabControl

#
#
# class QMapTabControl(QTabControl):
#     def __init__(self, parent, dvm):
#         super().__init__(parent)
#         self.dvm = dvm
#         # self.bgnd = bgnd
#         # self.wf = self.dvm.level_map.size().width() / self.bgnd.minimap.size().width()
#         # self.hf = self.dvm.level_map.size().height() / self.bgnd.minimap.size().height()
#         # self.scene.viewport().view_changed.connect(self.refresh_minimap)
#
#         self.init_ui()
#         self.init_actions()
#
#         self.graphic = QCGMap(self, QPixmap(self.dvm.level_map))
#         self.scene.addItem(self.graphic)
#
#         self.update()
#
#     @property
#     def visible(self):
#         return self.check_box.isChecked()
#
#     @visible.setter
#     def visible(self, visible):
#         self.check_box.setChecked(visible)
#         self.graphic.update()
#
#     def init_ui(self):
#         content = QWidget()
#         layout = QVBoxLayout(content)
#
#         h1_layout = QHBoxLayout()
#         label = QLabel("Map visibility")
#         h1_layout.addWidget(label)
#         self.check_box = QCheckBox()
#         self.check_box.setCheckState(Qt.CheckState.Checked)
#         self.check_box.stateChanged.connect(self.update)
#         h1_layout.addWidget(self.check_box)
#
#         self.slider = QSlider(Qt.Orientation.Horizontal)
#         self.slider.setMinimum(0)
#         self.slider.setMaximum(255)
#         self.slider.setValue(255)
#         self.slider.valueChanged.connect(self.update)
#         h1_layout.addWidget(self.slider)
#         layout.addLayout(h1_layout)
#
#         h2_layout = QHBoxLayout()
#         self.size_label = QLabel()
#         h2_layout.addWidget(self.size_label)
#         h2_layout.addStretch(255)
#         change_dvm_button = QPushButton("Change DVM")
#         change_dvm_button.clicked.connect(self.change_dvm)
#         h2_layout.addWidget(change_dvm_button)
#         layout.addLayout(h2_layout)
#
#
#
#         layout.addStretch(1)
#
#         self.minimap_scene = QGraphicsScene()
#         mf = 0.3  # marge factor
#         self.minimap_scene.setSceneRect(- mf * self.bgnd.minimap.size().width(),
#                                         - mf * self.bgnd.minimap.size().height(),
#                                         (2 * mf + 1) * self.bgnd.minimap.size().width(),
#                                         (2 * mf + 1) * self.bgnd.minimap.size().height())
#         self.minimap_viewport = QGraphicsView(self.minimap_scene)
#         self.minimap_viewport.scale(2, 2)
#         self.minimap_viewport.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#         self.minimap_viewport.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#
#         self.minimap_item = QGraphicsPixmapItem(QPixmap.fromImage(self.bgnd.minimap))
#         self.minimap_scene.addItem(self.minimap_item)
#         self.minimap_rect_item = QGraphicsRectItem()
#         self.minimap_scene.addItem(self.minimap_rect_item)
#         layout.addWidget(self.minimap_viewport)
#
#         self.setWidget(content)
#
#
#     def init_actions(self):
#         self.a_show = QAction("Show")
#         self.a_show.triggered.connect(lambda: self.check_box.setCheckState(Qt.CheckState.Checked))
#         self.a_hide = QAction("Hide")
#         self.a_hide.triggered.connect(lambda: self.check_box.setCheckState(Qt.CheckState.Unchecked))
#
#     def scene_menu_name(self):
#         return "Map"
#
#     def scene_menu_exclusive(self):
#         return super().scene_menu_exclusive()
#
#     def scene_menu_priority(self):
#         return (super().scene_menu_priority()
#                 + 0.5 * self.has_focus())
#
#     def scene_menu_enabled(self):
#         return super().scene_menu_enabled()
#
#     def scene_menu_common_actions(self, scene_position: QPointF = QPointF()):
#         if self.visible:
#             return [self.a_hide]
#         else:
#             return [self.a_show]
#
#     def update(self):
#         # r = self.scene.viewport().current_visible_scene_rect()
#         # self.minimap_rect_item.setRect(r.x()/self.wf, r.y()/self.hf, r.width()/self.wf, r.height()/self.wf)
#         self.size_label.setText(f"Size {self.dvm.width}x{self.dvm.height}")
#         self.graphic.setOpacity(self.slider.value() / 255)
#         self.graphic.update()
#         super().update()
#
#     def refresh_minimap(self, rect_view: QRectF):
#         r = rect_view
#         self.minimap_rect_item.setRect(r.x() / self.wf, r.y() / self.hf, r.width() / self.wf, r.height() / self.wf)
#         self.minimap_viewport.centerOn(self.minimap_item.boundingRect().center())
#
#     def change_dvm(self):
#         dialog = QFileDialog(self)
#         dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
#         filters = ["BMP Image (*.bmp)",
#                    "PNG Image (*.png)",]
#         dialog.setNameFilters(filters)
#         # dialog.setViewMode(QFileDialog.ViewMode.List)
#         if dialog.exec():
#             filenames = dialog.selectedFiles()
#             if len(filenames) == 1:
#                 self.dvm.change_level_map_image(filenames[0])
#                 self.scene.removeItem(self.graphic)
#                 self.graphic = QCGMap(self, QPixmap(self.dvm.level_map_image))
#                 self.scene.addItem(self.graphic)
#                 self.update()





TITLE_SIZE = 22

class QLevelMapInspector(QWidget):

    def __init__(self, control, level_map):
        super().__init__()
        self._control = control

        self.level_map = level_map
        # self.sub_inspector_group = dict()
        main_layout = QVBoxLayout(self)

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
        self.title.setText("Map")
        f = self.title.font()
        f.setPointSizeF(TITLE_SIZE)
        self.title.setFont(f)
        header_layout.addWidget(self.title)

        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # info_box = QGroupBox()
        # info_box.setTitle("Info")
        # info_box.setStyleSheet("""
        #     QGroupBox::title {
        #         subcontrol-position: top left;
        #         padding: 0 30px;
        #     }
        #     """)

        self.infoQIW = InfoQInspectorWidget(self, self.get_info)
        main_layout.addWidget(self.infoQIW)

        self.pixmapQIW = PixmapQInspectorWidget(self, self.get_map, self.set_map)
        main_layout.addWidget(self.pixmapQIW)

        main_layout.addStretch()

        # self.sub_inspector_group["Info"] = [InfoSubInspector(self, "info")]
        # self.sub_inspector_group["Map"] = [(psi:=PixmapSubInspector(self, "qimage"))]
        # psi.visibility_checkbox.setChecked(True)
        #
        #
        # for group_name in self.sub_inspector_group:
        #     box = QGroupBox(group_name)
        #     box.setStyleSheet("""
        #         QGroupBox::title {
        #             subcontrol-position: top left;
        #             padding: 0 30px;
        #         }
        #         """)
        #     sub_inspector_name_list = [si.inspector_name for si in self.sub_inspector_group[group_name]]
        #     if all([name == "" for name in sub_inspector_name_list]):
        #         box_layout = QVBoxLayout(box)
        #         for sub_inspector in self.sub_inspector_group[group_name]:
        #             box_layout.addWidget(sub_inspector)
        #     else:
        #         box_layout = QFormLayout(box)
        #         for sub_inspector in self.sub_inspector_group[group_name]:
        #             box_layout.addRow(sub_inspector.inspector_name, sub_inspector)
        #     self.main_layout.addWidget(box)
        # # self.main_layout.addLayout(sub_layout)
        # self.main_layout.addStretch(1)
        # # self.update()

        self.update()

    def update(self):
        self.infoQIW.update()
        self.pixmapQIW.update()


    def get_info(self):
        return f"size: {self.level_map.width} x {self.level_map.height}"

    def get_map(self):
        return image_to_qimage(self.level_map.image)

    def set_map(self, new_map_filename):
        if new_map_filename.endswith(".dvm"):
            dvm = DvmParser(new_map_filename)
            self.level_map.image = dvm.level_map.image
        else:
            self.level_map.image = Image.from_file(new_map_filename)
        return self.get_map()


    @property
    def scene(self):
        return self._control.scene
    #
    # @property
    # def level(self):
    #     return self._tab_control.level
    #
    # @property
    # def tree_item(self) -> QODVTreeItem:
    #     return self._tab_control.tree_items[self.odv_object]
    #
    # @property
    # def sub_inspector_list(self):
    #     rop = []
    #     for group_name in self.sub_inspector_group:
    #         for sub_inspector in self.sub_inspector_group[group_name]:
    #             rop.append(sub_inspector)
    #     return rop
    #
    # @property
    # def valid_state(self):
    #     return all([sub_inspector.valid_state for sub_inspector in self.sub_inspector_list])
    #
    # @property
    # def graphic_list(self):
    #     return [sub_inspector.graphic for sub_inspector in self.sub_inspector_list if
    #             hasattr(sub_inspector, 'graphic')]
    #
    # @property
    # def inspector_child_list(self):
    #     rop = []
    #     count = self.tree_item.childCount()
    #     for i in range(count):
    #         rop.append(self.tree_item.child(i).inspector)
    #     return rop

    # def init_sub_inspector(self):
    #     # must define self.sub_inspector_group = {group_name : list[SubInspector]}
    #     pass

    # def get_odv_prop(self, prop_name):
    #     if hasattr(self, prop_name):
    #         return getattr(self, prop_name)
    #     elif hasattr(self.odv_object, prop_name):
    #         return getattr(self.odv_object, prop_name)
    #     else:
    #         raise AttributeError(
    #             f"Neither {self.__class__.__name__} nor {self.odv_object.__class__.__name__} have property {prop_name}")
    #
    # def set_odv_prop(self, prop_name, value):
    #     if hasattr(self, prop_name):
    #         setattr(self, prop_name, value)
    #     elif hasattr(self.odv_object, prop_name):
    #         setattr(self.odv_object, prop_name, value)
    #     else:
    #         raise AttributeError(
    #             f"Neither {self.__class__.__name__} nor {self.odv_object.__class__.__name__} have property {prop_name}")

    # def init_actions(self):
    #     self.a_rename = QAction("Rename")
    #     # self.a_rename.triggered.connect(self.rename)
    #
    #     self.a_focus = QAction("Focus")
    #     self.a_focus.triggered.connect(self.take_focus)
    #
    #     self.a_add_child = QAction(f"Add {self.child_name}")
    #     self.a_add_child.triggered.connect(self.add_child)
    #
    #     self.a_delete = QAction("Delete")
    #     self.a_delete.triggered.connect(self.delete_and_update)
    #
    #     self.a_children_show = QAction(f"Show all")
    #     self.a_children_show.triggered.connect(self.show_children)
    #
    #     self.a_children_hide = QAction(f"Hide all")
    #     self.a_children_hide.triggered.connect(self.hide_children)
    #
    #     self.a_children_delete = QAction("Delete all")
    #     self.a_children_delete.triggered.connect(self.delete_children)

    # def add_child(self):
    #     odv_child = self.new_odv_child()
    #     self.odv_object.add_child(odv_child)
    #
    #     self._tab_control.tree_items[odv_child] = QODVTreeItem(self._tab_control, odv_child)
    #     self.tree_item.addChild(self._tab_control.tree_items[odv_child])
    #
    #     self._tab_control.inspectors[odv_child] = self._tab_control.inspector_types.get(type(odv_child), Inspector)(
    #         self._tab_control, odv_child)
    #     self._tab_control.inspector_stack_layout.addWidget(self._tab_control.inspectors[odv_child])
    #
    #     self._tab_control.inspectors[odv_child].take_focus()  # take_focus finish with a global update

    # def new_odv_child(self):
    #     raise NotImplementedError
    #
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
    #
    # def delete_and_update(self):
    #     self._inner_delete()
    #     self._tab_control.inspectors[self.odv_object.parent].take_focus()  # take_focus finish with a global update
    #
    # def show_children(self):
    #     for ic in self.inspector_child_list:
    #         for si in ic.sub_inspector_list:
    #             if hasattr(si, 'visibility_checkbox'):
    #                 si.visibility_checkbox.setChecked(True)
    #         ic.update()
    #
    # def hide_children(self):
    #     for ic in self.inspector_child_list:
    #         for si in ic.sub_inspector_list:
    #             if hasattr(si, 'visibility_checkbox'):
    #                 si.visibility_checkbox.setChecked(False)
    #         ic.update()
    #
    # def delete_children(self):
    #     for ic in self.inspector_child_list:
    #         assert ic.deletable
    #         ic._inner_delete()
    #     self.update()
    #
    # def scene_menu_name(self):
    #     return self.odv_object.name
    #
    # def scene_menu_exclusive(self):
    #     return self._tab_control.scene_menu_exclusive()
    #
    # def scene_menu_enabled(self):
    #     return self._tab_control.scene_menu_enabled()
    #
    # def scene_menu_priority(self):
    #     return self._tab_control.scene_menu_priority() + 0.25 * self.has_focus()
    #
    # def scene_menu_common_actions(self, scene_position):
    #     rop = []
    #     rop.append(self.a_focus)
    #     return rop
    #
    # def tree_menu_common_actions(self):
    #     rop = []
    #     rop.append(self.a_rename)
    #     if self.child_name != "":
    #         rop.append(self.a_add_child)
    #     if self.deletable is True:
    #         rop.append(self.a_delete)
    #     if self.child_name != "":
    #         rop.append(["On Children", self.a_children_show, self.a_children_hide, self.a_children_delete])
    #
    #     return rop
    #
    # def has_focus(self):
    #     return self._tab_control.has_focus() and self._tab_control.tree.currentItem() == self.tree_item
    #
    # def take_focus(self):
    #     self._tab_control.take_focus()
    #     self._tab_control.tree.setCurrentItem(self.tree_item)
    #     self.update()


    # @property
    # def info(self):
    #     return f"size: {self.odv_object.width} x {self.odv_object.height}"
    #
    # @property
    # def qimage(self):
    #     # getter return a QImage
    #     return image_to_qimage(self.odv_object.image)
    #
    # @qimage.setter
    # def qimage(self, image_path):
    #     # setter need an image path string
    #     self.odv_object.image = Image.from_file(image_path)


class QMapTabControl(QTabControl):

    def __init__(self, main_control, level_map: LevelMap):
        super().__init__(main_control)

        self.level_map = level_map

        content = QWidget()
        layout = QVBoxLayout(content)

        print("parent")
        print(self.scene)

        level_map_widget = QLevelMapInspector(self, self.level_map)

        layout.addWidget(level_map_widget)
        layout.addStretch()

        self.setWidget(content)

