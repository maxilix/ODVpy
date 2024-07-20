from typing import List, Callable

from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import QScrollArea, QTabWidget, QGraphicsScene, QMenu, QTreeWidgetItem, QGraphicsItem


class QTabControl(QScrollArea):
    def __init__(self, parent: QTabWidget, scene):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self._context_menu_priority = 2  # Nornal
        self.scene = scene

    def is_current_control(self):
        return self.parent().indexOf(self) == self.parent().currentIndex()

    def context_menu_enabled(self):
        return self._context_menu_priority > 0

    @property
    def context_menu_priority(self):
        return self._context_menu_priority + 0.5 * self.is_current_control()

    @context_menu_priority.setter
    def context_menu_priority(self, priority):
        self._context_menu_priority = priority

    def exec_context_menu(self):
        menu = QMenu()
        priority_submenu = menu.addMenu("Priority")
        a_priority = [QAction("Disable"), QAction("Low"), QAction("Normal"), QAction("High")]
        for p, a in enumerate(a_priority):
            a.setCheckable(True)
            a.setChecked(self._context_menu_priority == p)
            a.triggered.connect(lambda state, priority=p: self._set_context_menu_priority(priority))
        priority_submenu.addActions(a_priority)

        menu.exec(QCursor.pos())

    def _set_context_menu_priority(self, priority: int):
        self.context_menu_priority = priority

    def tab_control(self):
        return self

    def take_focus(self):
        self.parent().parent().setCurrentWidget(self)


class QSubControl(object):
    def tab_control(self):
        tab_control = self
        while not isinstance(tab_control, QTabControl):
            if isinstance(tab_control, QTreeWidgetItem):
                tab_control = tab_control.treeWidget()
            else:
                tab_control = tab_control.parent()
        return tab_control

    def take_focus(self):
        self.tab_control().take_focus()



class QSharedMenuSection(object):
    def __init__(self, graphics_item: QGraphicsItem, event) -> None:
        scene_position = graphics_item.mapToScene(event.pos())

        self.name = graphics_item.control.context_menu_name()
        self.exclusive = graphics_item.control.context_menu_exclusive()

        self.action_list = []
        for action in graphics_item.local_action_list(scene_position):
            self.action_list.append(action)
        for action in graphics_item.control.common_action_list(scene_position):
            self.action_list.append(action)

        # print(graphics_item)
        tab_control = graphics_item.control.tab_control()

        self.enabled = tab_control.context_menu_enabled()
        self.priority = tab_control.context_menu_priority

    @property
    def priority(self) -> int | float:
        return self._priority

    @priority.setter
    def priority(self, priority: int | float) -> None:
        self._priority = max(min(3, priority), 1)  # priority is  1:Low, 2:Normal, 3:High

    def append(self, action: QAction) -> None:
        self.local_action_list.append(action)



class QSharedMenu(object):
    def __init__(self):
        # self._menu = QMenu()
        self._sections = []

    def add_section(self, section: QSharedMenuSection) -> None:
        if section.enabled is True:
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









