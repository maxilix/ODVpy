from PyQt6.QtCore import QPointF


class Gateway(object):
    def __init__(self, p1:QPointF, p2:QPointF, p3:QPointF):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __iter__(self):
        yield self.p1
        yield self.p2
        yield self.p3

    def truncated(self):
        return Gateway(self.p1.truncated(), self.p2.truncated(), self.p3.truncated())