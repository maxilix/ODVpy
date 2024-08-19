from PyQt6.QtCore import QPointF

from common import RWStreamable


class Gateway(RWStreamable):
    def __init__(self, p1:QPointF, p2:QPointF, p3:QPointF):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __iter__(self):
        return iter([self.p1, self.p2, self.p3])

    def truncated(self):
        return Gateway(self.p1.truncated(), self.p2.truncated(), self.p3.truncated())

    @classmethod
    def from_stream(cls, stream):
        p1 = stream.read(QPointF)
        p2 = stream.read(QPointF)
        p3 = stream.read(QPointF)
        return cls(p1, p2, p3)

    def to_stream(self, stream):
        stream.write(self.p1)
        stream.write(self.p2)
        stream.write(self.p3)