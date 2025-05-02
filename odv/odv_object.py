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
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.iterable = []

    @abstractmethod
    def __iter__(self) -> Iterator[OdvObject]:
        pass

    def __getitem__(self, index: int) -> OdvObject:
        for i,e in enumerate(self):
            if i == index:
                return e
        raise IndexError
        # return list(self)[index]

    def __len__(self) -> int:
        i=0
        for i,e in enumerate(self):
            pass
        return i + 1
        # return len(list(self))

    # def add_child(self, child: Any):
    #     self._odv_children.append(child)
    #
    # def remove_child(self, child: Any):
    #     self._odv_children.remove(child)
    #
    # def index(self, odv_child) -> int:
    #     return self._odv_children.index(odv_child)

    # @property
    # def iterable(self):
    #     print("WARNING OdvObjectIterable.iterable shouldn't be used ! Use __iter__ instead")
    #     return self._iterable
    #
    # @iterable.setter
    # def iterable(self, iterable):
    #     assert all([isinstance(e, OdvObject) for e in iterable])
    #     self._iterable = iterable




class OdvRoot(OdvObject, ABC):
    pass
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self._odv_children = []
    #
    # def __iter__(self) -> Iterator[Any]:
    #     return iter(self._odv_children)
    #
    # def __getitem__(self, index: int) -> Any:
    #     return self._odv_children[index]
    #
    # def __len__(self) -> int:
    #     return len(self._odv_children)
    #
    # def add_child(self, child: Any):
    #     self._odv_children.append(child)
    #
    # def remove_child(self, child: Any):
    #     self._odv_children.remove(child)
    #
    # def index(self, odv_child) -> int:
    #     return self._odv_children.index(odv_child)


class OdvLeaf(OdvObject, ABC):
    pass
    # def __init__(self, parent, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self._odv_parent = parent
    #
    # def __str__(self):
    #     indexes = ""
    #     odv_leaf = self
    #     while isinstance(odv_leaf, OdvLeaf):
    #         indexes = f"{odv_leaf.i} {indexes}"
    #         odv_leaf = odv_leaf.parent
    #     return f"{self.__class__.__name__} {indexes}"
    #
    # @property
    # def parent(self):
    #     return self._odv_parent
    #
    # @property
    # def i(self):
    #     if self._odv_parent is None:
    #         raise Exception("ODV_Root as no parent")
    #     else:
    #         return self._odv_parent.index(self)


# class OdvObject(OdvRoot, OdvLeaf, ABC):
#     pass
