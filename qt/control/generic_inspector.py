from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QToolButton


# class SubInspector(QWidget):
#     valid_state = True
#
#     def __init__(self, inspector, prop_name, inspector_name="", **kwargs):
#         assert isinstance(inspector, Inspector)
#         super().__init__()
#         self._inspector = inspector
#         self.inspector_name = inspector_name
#         self._prop_name = prop_name
#         self.main_layout = QVBoxLayout()
#         self.main_layout.setContentsMargins(0, 0, 0, 0)
#         self.sub_init(**kwargs)
#
#     def sub_init(self, **kwargs):
#         pass
#
#     def global_update(self):
#         self._inspector.update()
#
#     @property
#     def current(self):
#         return self._inspector.get_odv_prop(self._prop_name)
#
#     @current.setter
#     def current(self, value):
#         self._inspector.set_odv_prop(self._prop_name, value)


class Inspector(QWidget):

    def __init__(self):
        super().__init__()
        self.items = []
        self.main_layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()
        self.settings_button = QToolButton(self)
        self.settings_button.setArrowType(Qt.ArrowType.DownArrow)
        header_layout.addWidget(self.settings_button)
        self.title = QLabel(self)
        f = self.title.font()
        f.setPointSizeF(18)
        self.title.setFont(f)
        header_layout.addWidget(self.title)
        header_layout.addStretch()

        self.main_layout.addLayout(header_layout)
        self.main_layout.addSpacing(20)
        # self.main_layout design is left up to the child

    def connect_to(self, new_items):
        self.items = new_items

        if (n:=len(new_items)) == 1:
            self.title.setText(new_items[0].name)
            self.title.setToolTip(None)
        else:
            assert all([type(new_items[0]) == type(e) for e in new_items])
            self.title.setText(f"Linked to {n} {new_items[0]._odv_object.__class__.__name__}{"s" if n != 1 else ""}")
            self.title.setToolTip("\n".join([e.name for e in new_items]))

    @property
    def item(self):
        assert len(self.items) == 1
        return self.items[0]

    def update(self):
        self.connect_to(self.items)
        super().update()

    # def set_title(self, items: QGenericTreeItem|list[QGenericTreeItem]) -> None:
    #     if isinstance(items, QGenericTreeItem):
    #         items = [items]
    #     if (n:=len(items)) == 1:
    #         self.title.setText(items[0].name)
    #         self.title.setToolTip(None)
    #     else:
    #         assert all([type(items[0]) == type(e) for e in items])
    #         self.title.setText(f"Linked to {n} {items[0].odv_object.__class__.__name__}{"s" if n != 1 else ""}")
    #         self.title.setToolTip("\n".join([e.name for e in items]))

    def add_widget(self, widget):
        n = self.main_layout.count()
        self.main_layout.insertWidget(n - 1, widget)
