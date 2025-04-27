from typing import Any

from common import *
from odv.odv_object import OdvObject
from odv.pathfinder import PathFinder
from .section import Section


class Obstacle(OdvObject):
    poly: QPolygonF


    # @property  # TODO del-it
    # def poly(self) -> QPolygonF:
    #     return self._poly
    #
    # @poly.setter
    # def poly(self, poly: QPolygonF):
    #     # check if poly is clockwise
    #     if poly.signed_area() <= 0:
    #         # clockwise
    #         self._poly = poly
    #     else:
    #         # counter-clockwise
    #         self._poly = QPolygonF(poly[::-1])

    @classmethod
    def from_stream(cls, stream: ReadStream, **kwargs):
        rop = cls()
        rop.poly = stream.read(QPolygonF)
        return rop

    def to_stream(self, stream: WriteStream):
        stream.write(self.poly)


class MainArea(OdvObject):
    area: QPolygonF
    obstacle_list: list[Obstacle]
    segment_list: list[QLineF]




    # @property  # TODO del-it
    # def main_area_id(self):
    #     rop = 0
    #     for layer_index in range(self.parent.i):
    #         rop += self.parent.parent[layer_index].total_area()
    #     for mainArea_index in range(self.i):
    #         rop += 1 + len(self.parent[mainArea_index])
    #     return rop

    # @property  # TODO del-it
    # def poly(self) -> QPolygonF:
    #     return self._poly
    #
    # @poly.setter
    # def poly(self, poly: QPolygonF):
    #     # check if poly is clockwise
    #     if poly.signed_area() <= 0:
    #         # clockwise
    #         self._poly = poly
    #     else:
    #         # counter-clockwise
    #         self._poly = QPolygonF(poly[::-1])

    @classmethod
    def from_stream(cls, stream: ReadStream, **kwargs) -> 'MainArea':
        rop = cls()
        rop.area = stream.read(QPolygonF)
        nb_segment = stream.read(UShort)
        rop.segment_list = [stream.read(QLineF) for _ in range(nb_segment)]
        nb_obstacle = stream.read(UShort)
        # for _ in range(nb_obstacle):
        #     rop.add_child(stream.read(Obstacle, parent=rop))
        rop.obstacle_list = [stream.read(Obstacle) for _ in range(nb_obstacle)]
        return rop

    def to_stream(self, substream: WriteStream) -> None:
        substream.write(self.area)

        substream.write(UShort(0))  # always write zero segments
        # nb_segment = len(self.segment_list)
        # substream.write(UShort(nb_segment))
        # for segment in self.segment_list:
        #     substream.write(segment)

        nb_obstacle = len(self.obstacle_list)
        substream.write(UShort(nb_obstacle))
        for obstacle in self.obstacle_list:
            substream.write(obstacle)

    # @property  # TODO del-it
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

    # @timeit
    # def contains(self, poly: QPolygonF) -> bool:
    #     poly_area = poly.area()
    #     inter = self.poly.intersected(poly)
    #     inter_area = inter.area()
    #     if (poly_area - inter_area) > 0.1:
    #         # poly not in main
    #         return False
    #     for obstacle in self :
    #         inter = obstacle.poly.intersected(poly)
    #         # if inter.isEmpty():
    #         #     continue
    #         inter_area = inter.area()
    #         if inter_area > 0.1:
    #             # obstacle intersects poly
    #             return False
    #     return True



class Layer(OdvObject):

    main_area_list: list[MainArea]
    parent: Any  # Must be Move

    def total_area(self) -> int:
        return sum([(len(main_area.obstacle_list) + 1) for main_area in self.main_area_list])

    @classmethod
    def from_stream(cls, stream: ReadStream, **kwargs) -> 'Layer':
        rop = cls()
        # total_area is rebuilt on demand
        total_area = stream.read(UShort)
        nb_main_area = stream.read(UShort)
        # for _ in range(nb_main_area):
        #     rop.add_child(stream.read(MainArea, parent=rop))
        rop.main_area_list = [stream.read(MainArea, parent=rop) for _ in range(nb_main_area)]
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        stream.write(UShort(self.total_area()))
        nb_main_area = len(self.main_area_list)
        stream.write(UShort(nb_main_area))
        for main_area in self.main_area_list:
            stream.write(main_area)


class Move(Section):
    _section_name = "MOVE"
    _section_version = 1

    layer_list: list[Layer]
    pathfinder: PathFinder

    def main_area(self, index: int):
        i = 0
        while (ta_i := self.layer_list[i].total_area()) <= index:
            i += 1
            index -= ta_i
        j = 0
        while (ta_j := (1 + len(self.layer_list[i].main_area_list[j].obstacle_list))) <= index:
            j += 1
            index -= ta_j
        assert index == 0
        rop = self.layer_list[i].main_area_list[j]
        return rop

    def main_area_iterator(self, *, include_None):
        class MAI:
            def __iter__(subself):
                if include_None:
                    rop = [None]
                else:
                    rop = []
                return iter(rop + [ma for layer in self.layer_list for ma in layer.main_area_list])
            def __getitem__(subself, index):
                return list(iter(subself))[index]
            def __len__(subself):
                return len(list(iter(subself)))
        return MAI()

    def _load(self, substream: ReadStream, **kwargs) -> None:
        nb_layer = substream.read(UShort)
        # for _ in range(nb_layer):
        #     self.add_child(substream.read(Layer, parent=self))
        self.layer_list = [substream.read(Layer, parent=self) for _ in range(nb_layer)]
        # substream.read_raw()
        self.pathfinder = substream.read(PathFinder)

    def _save(self, substream: WriteStream) -> None:
        nb_layer = len(self.layer_list)
        substream.write(UShort(nb_layer))
        for layer in self.layer_list:
            substream.write(layer)

        # self.pathfinder.rebuild()
        substream.write(self.pathfinder)
