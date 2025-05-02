from abc import ABC, abstractmethod
from typing import Iterator, Self, Any

from common import RWStreamable


class OdvObject(RWStreamable, ABC):
    _odv_name: str
    _odv_parent: Self | None

    def __init__(self, odv_parent: Self | None = None):
        # _odv_name is initialized to empty string,
        # name property return _odv_name if it was overwritten, else return __str__
        self._odv_name = ""

        # parent must be an OdvObject or None
        assert isinstance(odv_parent, OdvObject) or odv_parent is None
        # parent type cannot be changed after initialization (see parent setter)
        self._odv_parent = odv_parent

    def __str__(self):
        indexes = ""
        odv_child = self
        while isinstance(odv_child.parent, OdvObjectIterable):
            indexes = f" {odv_child.i}{indexes}"
            odv_child = odv_child.parent
        return f"{self.__class__.__name__}{indexes}"

    @property
    def parent(self):
        return self._odv_parent

    @parent.setter
    def parent(self, new_odv_parent):
        assert type(self._odv_parent) == type(new_odv_parent)
        self._odv_parent = new_odv_parent

    @property
    def name(self):
        if self._odv_name == "":
            return self.__str__()
        return self._odv_name

    @name.setter
    def name(self, new_name):
        self._odv_name = new_name

    @property
    def i(self):
        if self.parent is None:
            raise Exception(f"{self.name} as no parent")
        elif not isinstance(self.parent, OdvObjectIterable):
            raise Exception(f"{self.name} is not an OdvObjectIterable")
        else:
            return list(iter(self.parent)).index(self)


class OdvObjectIterable(OdvObject, ABC):

    @abstractmethod
    def __iter__(self) -> Iterator[Any]:
        pass

    def __getitem__(self, index: int) -> OdvObject:
        for i,e in enumerate(self):
            if i == index:
                return e
        raise IndexError

    def __len__(self) -> int:
        i=0
        for i,e in enumerate(self):
            pass
        return i + 1

    # def index(self, odv_child) -> int:
    #     return list(iter(self)).index(odv_child)

