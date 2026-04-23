from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QTabWidget

from app_context import AppContext as AC
from config import Config
from game_data import SECTION_FLAG
from qt.control.section_control import QSectionControl


class QControl(QTabWidget):
    sendStatus = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()

        self.setTabPosition(QTabWidget.TabPosition.East)
        self.setMovable(False)

        for i in range(4):
            self.addTab(QSectionControl(i), SECTION_FLAG[i])
            # try:
            #     pass
            # except Exception as e:
            #     print(f"[Section tab {SECTION_FLAG[i]}] Widget Error '{e}'.")
            #     self.addTab(QWidget(), SECTION_FLAG[i])

        # adjust the width to fit the children
        self.setFixedWidth(self.minimumSizeHint().width())

        self.currentChanged.connect(self.current_tab_changed)
        AC.level_changed.connect(self.level_changed)

    def current_tab_changed(self, index):
        self.widget(index).update()

    def level_changed(self):
        for i in range(self.count()):
            self.widget(i).unload()
        for i in range(self.count()):
            if SECTION_FLAG[i] in Config.loaded_section:
                self.widget(i).load()
        for i in range(self.count()):
            self.widget(i).update()
        AC.scene.center_view(zoom=0.75)
