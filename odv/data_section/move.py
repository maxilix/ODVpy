from typing import Self

from common import *
from debug import timeit
from odv.odv_object import OdvObjectIterable, OdvObject
from odv.data_section.move_pathfinder import PathFinder
from odv.section import Section


class Obstacle(OdvObject):
    _poly: QPolygonF

    def __str__(self):
        return f"Obstacle {self.parent.sector_id + self.i + 1}"

    # @property
    # def global_id(self):
    #     return self.parent.sector_id + self.i + 1

    @property
    def poly(self) -> QPolygonF:
        return self._poly

    @poly.setter
    def poly(self, poly: QPolygonF):
        # check if poly is clockwise
        if poly.signed_area() <= 0:
            # clockwise
            self._poly = poly
        else:
            # counter-clockwise
            self._poly = QPolygonF(poly[::-1])

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent):
        rop = cls(parent)
        rop.poly = stream.read(QPolygonF)
        return rop

    def to_stream(self, stream: WriteStream):
        stream.write(self.poly)


class Sector(OdvObjectIterable):
    _poly: QPolygonF
    obstacle_list: list[Obstacle]

    def __str__(self):
        return f"Sector {self.sector_id}"

    def __iter__(self):
        return iter(self.obstacle_list)

    @property
    def sector_id(self):
        rop = 0
        for layer_index in range(self.parent.i):
            rop += self.parent.parent[layer_index].total_polygon()
        for sector_index in range(self.i):
            rop += 1 + len(self.parent[sector_index])
        return rop

    @property
    def poly(self) -> QPolygonF:
        return self._poly

    @poly.setter
    def poly(self, poly: QPolygonF):
        # check if poly is clockwise
        if poly.signed_area() <= 0:
            # clockwise
            self._poly = poly
        else:
            # counter-clockwise
            self._poly = QPolygonF(poly[::-1])

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent) -> Self:
        rop = cls(parent)
        rop.poly = stream.read(QPolygonF)
        nb_segment = stream.read(UShort)
        segment_list = [stream.read(QLineF) for _ in range(nb_segment)]
        nb_obstacle = stream.read(UShort)
        # for _ in range(nb_obstacle):
        #     rop.add_child(stream.read(Obstacle, parent=rop))
        rop.obstacle_list = [stream.read(Obstacle, parent=rop) for _ in range(nb_obstacle)]
        return rop

    def to_stream(self, substream: WriteStream) -> None:
        substream.write(self.poly)

        substream.write(UShort(0))  # always write zero segments
        # nb_segment = len(self.segment_list)
        # substream.write(UShort(nb_segment))
        # for segment in self.segment_list:
        #     substream.write(segment)

        nb_obstacle = len(self)
        substream.write(UShort(nb_obstacle))
        for obstacle in self.obstacle_list:
            substream.write(obstacle)

    # @property
    # def path(self):
    #     if self._path is None:
    #         self._path = QPainterPath()
    #         self._path.addPolygon(self.main.poly)
    #         self._path.closeSubpath()
    #         for obstacle in self.obstacles:
    #             negative = QPainterPath()
    #             negative.addPolygon(obstacle.poly)
    #             negative.closeSubpath()
    #             self._path -= negative
    #     return self._path

    @timeit
    def contains(self, poly: QPolygonF) -> bool:
        poly_area = poly.area()
        inter = self.poly.intersected(poly)
        inter_area = inter.area()
        if (poly_area - inter_area) > 0.1:
            # poly not in main
            return False
        for obstacle in self :
            inter = obstacle.poly.intersected(poly)
            # if inter.isEmpty():
            #     continue
            inter_area = inter.area()
            if inter_area > 0.1:
                # obstacle intersects poly
                return False
        return True



class Layer(OdvObjectIterable):
    sector_list: list[Sector]

    def __iter__(self):
        return iter(self.sector_list)

    def total_polygon(self) -> int:
        return sum([(len(sector) + 1) for sector in self])

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent) -> Self:
        rop = cls(parent)
        # total_polygon is rebuilt on demand
        total_polygon = stream.read(UShort)
        nb_sector = stream.read(UShort)
        # for _ in range(nb_sector):
        #     rop.add_child(stream.read(Sector, parent=rop))
        rop.sector_list = [stream.read(Sector, parent=rop) for _ in range(nb_sector)]
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(UShort(self.total_polygon()))
        nb_sector = len(self)
        stream.write(UShort(nb_sector))
        for sector in self.sector_list:
            stream.write(sector)


class Move(Section, OdvObjectIterable):
    _section_name = "MOVE"
    _section_version = 1

    layer_list: list[Layer]
    path_finder: PathFinder

    def __iter__(self):
        return iter(self.layer_list)

    def sector(self, index: int):
        i = 0
        while (ta_i := self[i].total_polygon()) <= index:
            i += 1
            index -= ta_i
        j = 0
        while (ta_j := (1 + len(self[i][j]))) <= index:
            j += 1
            index -= ta_j
        assert index == 0
        rop = self[i][j]
        return rop

    def sector_iterator(self, *, include_None):
        class SI:
            def __iter__(subself):
                if include_None:
                    return iter([None] + [s for layer in self for s in layer])
                else:
                    return iter(s for layer in self for s in layer)
            def __getitem__(self, item):
                return list(iter(self))[item]
            def __len__(self):
                return len(list(iter(self)))
        return SI()

    def _load(self, substream: ReadStream) -> None:
        nb_layer = substream.read(UShort)
        # for _ in range(nb_layer):
        #     self.add_child(substream.read(Layer, parent=self))
        self.layer_list = [substream.read(Layer, parent=self) for _ in range(nb_layer)]
        self.pathfinder = substream.read(PathFinder)

    def _save(self, substream: WriteStream) -> None:
        nb_layer = len(self)
        substream.write(UShort(nb_layer))
        for layer in self.layer_list:
            substream.write(layer)

        self.pathfinder.rebuild(self)
        substream.write(self.pathfinder)
