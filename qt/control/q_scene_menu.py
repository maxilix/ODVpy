from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import QMenu


class QSceneMenuSection(object):
    def __init__(self, graphics_item, event) -> None:
        scene_position = graphics_item.mapToScene(event.pos())

        self.name = graphics_item.odv_object.scene_menu_name()
        self.exclusive = graphics_item.odv_object.scene_menu_exclusive()
        self.enabled = graphics_item.odv_object.scene_menu_enabled()
        self.priority = graphics_item.odv_object.scene_menu_priority()

        self.action_list = []
        if graphics_item.visible:
            for action in graphics_item.scene_menu_local_actions(scene_position):
                self.action_list.append(action)
        for action in graphics_item.odv_object.scene_menu_common_actions(scene_position):
            self.action_list.append(action)

    @property
    def priority(self) -> int | float:
        return self._priority

    @priority.setter
    def priority(self, priority: int | float) -> None:
        self._priority = max(min(3, priority), 1)  # priority is  1:Low, 2:Normal, 3:High

    def append(self, action: QAction) -> None:
        self.local_action_list.append(action)


class QSceneMenu(object):
    def __init__(self):
        # self._menu = QMenu()
        self._sections = []

    def add_section(self, section: QSceneMenuSection) -> None:
        if section.enabled is True and section.name not in [s.name for s in self._sections]:
            self._sections.append(section)

    def exec(self):
        menu = QMenu()
        menu.setStyleSheet(":enabled {color: black} :disabled {color: gray}")
        filter_sections = [s for s in self._sections if s.exclusive]
        if filter_sections == []:
            filter_sections = sorted(self._sections, key=lambda s: s.priority, reverse=True)
        else:
            filter_sections.sort(key=lambda s: s.priority, reverse=True)

        for section in filter_sections:
            menu.addSection(section.name)
            for action in section.action_list:
                menu.addAction(action)

        if filter_sections != []:
            menu.exec(QCursor.pos())
