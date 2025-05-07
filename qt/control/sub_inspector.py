from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class QSubInspectorWidget(QWidget):

    def __init__(self, inspector, prop):
        super().__init__()
        self.inspector = inspector
        self.prop = prop
        # self.get = getter
        # self.set = setter

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def get(self):
        rop = [getattr(item, self.prop) for item in self.inspector.item_list]
        if rop == []:
            return None
        elif all(rop[0] == e for e in rop):
            return rop[0]
        else:
            return rop







class InfoQSIW(QSubInspectorWidget):
    info: QLabel
    def __init__(self, inspector, prop):
        super().__init__(inspector, prop)

        self.info = QLabel()
        self.main_layout.addWidget(self.info)
        self.setLayout(self.main_layout)

    def update(self):
        self.info.setText(str(self.get()))