from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class InfoSubInspector(QWidget):

    def __init__(self, inspector, accessor):
        # assert isinstance(inspector, Inspector)
        super().__init__()
        self._inspector = inspector
        self._accessor = accessor

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.info = QLabel()
        main_layout.addWidget(self.info)
        self.setLayout(main_layout)

    def update(self):
        self.info.setText(str(self._accessor()))
