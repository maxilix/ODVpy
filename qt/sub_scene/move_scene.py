from PyQt6.QtGui import QPen, QBrush, QColor


class MoveScene(object):
    def __init__(self, scene, motion):
        self.scene = scene
        self.motion = motion
        # self.sublayer_color = QColor(0, 255, 0)
        # pen_color = self.sublayer_color
        # pen_color.setAlpha(32)
        self.sublayer_pen = QPen(QColor(0, 255, 0, 128))
        self.sublayer_brush = QBrush(QColor(0, 255, 0, 16))
        self.sublayer_highlight = True
        self.sublayer_draw = []
        for layer in self.motion:
            self.sublayer_draw.append([])
            for sublayer in layer:
                sublayer_draw = self.scene.addPath(sublayer.QPainterPath(),
                                                   self.sublayer_pen,
                                                   self.sublayer_brush)
                # sublayer_draw.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
                sublayer_draw.setVisible(False)
                self.sublayer_draw[-1].append(sublayer_draw)

        self.area_pen = QColor(255, 0, 0, 128)
        self.area_blush = QColor(255, 0, 0, 16)

    def refresh(self, mousse_position):
        if self.sublayer_highlight:
            for draw_list in self.sublayer_draw:
                for draw in draw_list:
                    if draw.isVisible():
                        color = self.sublayer_brush.color()
                        if draw.path().contains(mousse_position):
                            color.setAlpha(32)
                        else:
                            color.setAlpha(16)
                        draw.setBrush(QBrush(color))

    def show_sublayer(self, i, j):
        self.sublayer_draw[i][j].setVisible(True)

    def hide_sublayer(self, i, j):
        self.sublayer_draw[i][j].setVisible(False)

