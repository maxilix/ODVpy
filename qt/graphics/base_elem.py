from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter

# from qt.control.scene_menu import QSceneMenuSection


class OdvGraphicElement(object):

    def __init__(self, *args, **kwargs):
        self.force_visible = False
        super().__init__(*args, **kwargs)

    def paint(self, painter: QPainter, option, widget=None):
        if self.visible:
            painter.setRenderHints(QPainter.RenderHint.Antialiasing)
            super().paint(painter, option, widget)

    # @property
    # def visible(self):
    #     if self.parentItem() is None:
    #         return False
    #     else:
    #         return self.parentItem().visible or self.force_visible

    # @property
    # def sub_inspector(self):
    #     return self.parentItem().sub_inspector

    def mousePressEvent(self, event):
        # if event.button() == Qt.MouseButton.RightButton:
        #     section = QSceneMenuSection(self, event)
        #     event.shared_menu.add_section(section)
        #     event.accept()
        super().mousePressEvent(event)

    def scene_menu_local_actions(self, scene_position):
        return []
