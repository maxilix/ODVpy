from abc import ABC, abstractmethod
from typing import Iterator, Self, Any

from common import RWStreamable, auto_id


class OdvObject(RWStreamable, ABC):

    def __init__(self):
        self.name = f"{self.__class__.__name__}_{auto_id(self.__class__.__name__)}"

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<{self.__class__.__name__} : {self.name}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name


class OdvObjectIterable(OdvObject, ABC):

    @abstractmethod
    def __iter__(self) -> Iterator[OdvObject]:
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





class OdvRoot(OdvObject, ABC):
    pass



class OdvLeaf(OdvObject, ABC):
    pass
