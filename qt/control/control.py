from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QCursor, QAction
from PyQt6.QtWidgets import QTabWidget, QMenu, QWidget

from game_data import SECTION_FLAG

from app_context import AppContext as AC
from qt.control.control_section import QSectionControl


class QControl(QTabWidget):
    sendStatus = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()

        self.setTabPosition(QTabWidget.TabPosition.East)
        self.setMovable(False)

        for i in range(3):
            try:
                self.addTab(QSectionControl(i), SECTION_FLAG[i])
            except Exception as e:
                print(f"[Section tab {SECTION_FLAG[i]}] Widget Error '{e}'.")
                self.addTab(QWidget(), SECTION_FLAG[i])

        # adjust the width to fit the children
        self.setFixedWidth(self.minimumSizeHint().width())

    # def mousePressEvent(self, event: QMouseEvent):
    #     # TODO make the click detectable only on the TabBar rect
    #     if event.button() == Qt.MouseButton.RightButton:
    #         tab_index = self.tabBar().tabAt(self.tabBar().mapFromParent(event.pos()))
    #         menu = QMenu()
    #         if tab_index != -1:
    #             section_name = self.tabText(tab_index)
    #             close_action = QAction(f"Close {section_name}")
    #             close_action.triggered.connect(lambda state, name=section_name: self.close_tab(name))
    #             menu.addAction(close_action)
    #             menu.addSeparator()
    #
    #         add_actions = []
    #         for section_name in self.tab:
    #             if self.tab[section_name] is not None and section_name not in [self.tabText(i) for i in range(self.count())]:
    #                 add_actions.append(QAction(f"Add {section_name}"))
    #                 add_actions[-1].triggered.connect(lambda state, name=section_name: self.add_tab(name))
    #         menu.addActions(add_actions)
    #         menu.exec(QCursor.pos())
    #     super().mousePressEvent(event)

    def close_tab(self, name):
        if name == "BGND":
            print("BGND cannot be closed")
        else:
            print(f"close {name}")

    def update(self):
        super().update()
        for i in range(3):
            self.widget(i).update()