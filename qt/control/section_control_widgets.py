from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import QCheckBox, QMenu, QWidgetAction, QLabel, QToolButton, QHBoxLayout, QWidget


class QHoverDetectionCheckboxesWidget(QWidget):
    def __init__(self, odv_types):
        super().__init__()
        self.odv_types = odv_types

        layout = QHBoxLayout(self)

        self.button = QToolButton()
        self.button.setFixedHeight(20)
        self.button.setFixedWidth(20)
        self.button.setArrowType(Qt.ArrowType.DownArrow)
        self.button.setEnabled(True)  # ------------------- #
        self.button.clicked.connect(self.show_menu)         #
        if len(odv_types) > 1:                              #
            layout.addWidget(self.button)                   #
        else:                                               #
            layout.addSpacing(26)                           #
                                                            #
        self.checkboxes = [QCheckBox()]                     #
                                                            #
        self.checkboxes[0].setChecked(True)  # ------------ #
        self.checkboxes[0].stateChanged.connect(lambda: self.button.setEnabled(self.checkboxes[0].isChecked()))
        layout.addWidget(self.checkboxes[0])

        layout.addWidget(QLabel(odv_types[0].__name__))

        if len(odv_types) > 1:
            self.menu = QMenu()

            for item_type in odv_types[1:]:
                cb = QCheckBox(item_type.__name__)
                cb.setChecked(True)
                cb.setStyleSheet("""
                    QCheckBox {
                        padding: 6px 8px 6px 8px;  /* réduit vertical, garde espace gauche */
                        margin: 0px;
                    }
                """)
                action = QWidgetAction(self.menu)
                action.setDefaultWidget(cb)
                self.menu.addAction(action)
                self.checkboxes.append(cb)

    def show_menu(self):
        self.menu.exec(self.button.mapToGlobal(self.checkboxes[0].rect().bottomLeft() + QPoint(18,12)))

    def isChecked(self, t):
        i = self.odv_types.index(t)
        return self.checkboxes[0].isChecked() and self.checkboxes[i].isChecked()
