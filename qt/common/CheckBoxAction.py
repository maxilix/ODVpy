from PyQt6.QtWidgets import QWidgetAction, QWidget, QHBoxLayout, QLabel, QCheckBox, QGraphicsSceneMouseEvent

class QCheckBoxAction(QWidgetAction):

    def __init__(self, action_name):
        super().__init__(None)
        self.main_widget = QWidget()
        # self.main_widget.setMouseTracking(True)
        main_layout = QHBoxLayout(self.main_widget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
        self.checkbox = QCheckBox()
        self.checkbox.setStyleSheet("""
            QCheckBox {
                padding-left: 8px;
                padding-right: 0px;
                padding-top: 8px;
                padding-bottom: 8px;
            }
        """)
        self.label = QLabel("BGND S")
        self.label.mousePressEvent = self.labelMousePressEvent
        main_layout.addWidget(self.checkbox)
        main_layout.addWidget(self.label)
        self.main_widget.setStyleSheet("""
            QWidget:hover {
                background-color: #3584e4;
                color: white;
            }
        """)
        main_layout.addStretch()

        self.setDefaultWidget(self.main_widget)

    def labelMousePressEvent(self, event: QGraphicsSceneMouseEvent):
        self.releaseWidget(self.main_widget)
        self.trigger()
