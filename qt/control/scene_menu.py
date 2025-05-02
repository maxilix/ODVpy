from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import QMenu


# class QSceneMenuSection(object):
#
#     def __init__(self, graphics_item, event) -> None:
#         scene_position = graphics_item.mapToScene(event.pos())
#
#         self.name = graphics_item.sub_inspector.scene_menu_name()
#         self.exclusive = graphics_item.sub_inspector.scene_menu_exclusive()
#         self.enabled = graphics_item.sub_inspector.scene_menu_enabled()
#         self.priority = graphics_item.sub_inspector.scene_menu_priority()
#         # print(self.name, self.priority)
#
#         self.action_list = []
#         if graphics_item.visible:
#             for action in graphics_item.scene_menu_local_actions(scene_position):
#                 self.action_list.append(action)
#         for action in graphics_item.sub_inspector.scene_menu_common_actions(scene_position):
#             self.action_list.append(action)


# class QSceneMenu(object):
#     def __init__(self):
#         # self._menu = QMenu()
#         self._sections = []
#
#     def add_section(self, section: QSceneMenuSection) -> None:
#         if section.enabled is True and section.name not in [s.name for s in self._sections]:
#             self._sections.append(section)
#
#     def exec(self):
#         if self._sections == []:
#             return
#
#         menu = QMenu()
#         menu.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
#         filter_sections = [s for s in self._sections if s.exclusive]
#         if filter_sections == []:
#             filter_sections = self._sections
#
#         filter_sections.sort(key=lambda s: s.priority, reverse=True)
#
#         for section in filter_sections:
#             menu.addSection(section.name)
#             for action in section.action_list:
#                 menu.addAction(action)
#         menu.exec(QCursor.pos())
