from typing import Self

from common import *
from odv.odv_object import OdvObject
from .section import Section


class Script(OdvObject):
    p: QPointF | QPolygonF
    layer_id: UShort
    main_area: UShort
    classname: str = ""

    def __str__(self):
        if self.classname == "":
            return super().__str__()
        else:
            return f"{super().__str__()} - {self.classname}"


    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent) -> Self:
        rop = cls(parent)
        n = stream.read(UShort)
        assert n not in [0, 2]
        if n == 1:
            rop.p = stream.read(QPointF)
        else:
            rop.p = QPolygonF([stream.read(QPointF) for _ in range(n)])


        rop.layer_id = stream.read(UShort)
        rop.main_area = stream.read(UShort)

        if stream.read(UChar):
            classname_length = stream.read(UShort)
            rop.classname = stream.read(String, classname_length)

        return rop

    def to_stream(self, stream: WriteStream) -> None:
        # TODO write script
        pass



class Scrp(Section):
    _section_name = "SCRP"
    _section_version = 1

    def _load(self, substream: ReadStream) -> None:
        nb_script = substream.read(UShort)
        for _ in range(nb_script):
            self.add_child(substream.read(Script, parent=self))

    def _save(self, substream: WriteStream) -> None:
        pass
