from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QToolButton


class SubInspector(QWidget):
    valid_state = True

    def __init__(self, inspector, prop_name, inspector_name="", **kwargs):
        assert isinstance(inspector, Inspector)
        super().__init__()
        self._inspector = inspector
        self.inspector_name = inspector_name
        self._prop_name = prop_name
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.sub_init(**kwargs)

    def sub_init(self, **kwargs):
        pass

    def global_update(self):
        self._inspector.update()

    @property
    def current(self):
        return self._inspector.get_odv_prop(self._prop_name)

    @current.setter
    def current(self, value):
        self._inspector.set_odv_prop(self._prop_name, value)


class Inspector(QWidget):

    def __init__(self):
        super().__init__()
        self._item_list = []
        self.sub_inspector_list = []
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
        self.main_layout.addStretch()

    @property
    def item_list(self):
        return self._item_list

    @item_list.setter
    def item_list(self, new_list):
        assert len(new_list) == 0 or all([type(new_list[0]) == type(e) for e in new_list])
        self._item_list = new_list
        self.update()

    def update(self):
        super().update()
        if self._item_list == []:
            self.title.setText("Inspector unlinked")
            self.title.setToolTip(None)
        elif (n:=len(self._item_list)) == 1:
            self.title.setText(self._item_list[0].name)
            self.title.setToolTip(None)
        else:
            assert all([type(self._item_list[0]) == type(e) for e in self._item_list])
            self.title.setText(f"Linked to {n} {self._item_list[0].odv_object.__class__.__name__}{"s" if n != 1 else ""}")
            self.title.setToolTip("\n".join([e.name for e in self._item_list]))
        for si in self.sub_inspector_list:
            si.update()




    def add_sub_inspector(self, sub_inspector):
        self.sub_inspector_list.append(sub_inspector)
        n = self.main_layout.count()
        self.main_layout.insertWidget(n - 1, sub_inspector)
        # self.update()