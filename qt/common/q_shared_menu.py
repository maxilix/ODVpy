from enum import Enum

from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import QMenu


# class MenuPriority(Enum):
#     DISABLE = 0
#     LOW = 1
#     NORMAL = 2
#     HIGH = 3


class QSharedMenuSection(object):
    def __init__(self, name: str, action_list: list[QAction], priority: int = 2, exclusive: bool = False) -> None:
        self.name = name
        self.action_list = action_list
        self.priority = priority
        self.exclusive = exclusive

    @property
    def priority(self) -> int | float:
        return self._priority

    @priority.setter
    def priority(self, priority: int | float) -> None:
        self._priority = max(min(3, priority), 1)  # priority is  1:Low, 2:Normal, 3:High

    def append(self, action: QAction) -> None:
        self.action_list.append(action)



class QSharedMenu(object):
    def __init__(self):
        # self._menu = QMenu()
        self._sections = []

    def add_section(self, section: QSharedMenuSection) -> None:
        self._sections.append(section)

    def exec(self):
        menu = QMenu()
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


