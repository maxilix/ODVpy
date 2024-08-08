from abc import ABC, abstractmethod

from common import RWStreamable


class OdvObject(RWStreamable, ABC):

    def __init__(self, parent):
        self.parent = parent
        self._name = None

    @property
    def name(self):
        if self._name is None:
            self._name = self.__str__()
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
