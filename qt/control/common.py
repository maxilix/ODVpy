from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import QScrollArea, QTabWidget, QGraphicsScene, QMenu


class QControl(QScrollArea):
    def __init__(self, parent: QTabWidget, scene: QGraphicsScene):
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
        self._context_menu_priority = priority



