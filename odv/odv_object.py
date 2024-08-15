from abc import ABC, abstractmethod
from typing import Iterator, Self, Any

from common import RWStreamable


class OdvBase(RWStreamable, ABC):

    def __init__(self):
        # self._name cannot be initialized to self.__str__() because this function generally
        # uses the index of self in the list of children of the parent odv_object,
        # and this list does not yet exist when the child odv_object is created.
        self._odv_name = None

    def __str__(self):
        return f"{self.__class__.__name__}"

    @property
    def name(self):
        if self._odv_name is None:
            return self.__str__()
        return self._odv_name

    @name.setter
    def name(self, value):
        self._odv_name = value


class OdvRoot(OdvBase, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._odv_children = []

    def __iter__(self) -> Iterator[Any]:
        return iter(self._odv_children)

    def __getitem__(self, index: int) -> Any:
        return self._odv_children[index]

    def __len__(self) -> int:
        return len(self._odv_children)

    def add_child(self, child: Any):
        self._odv_children.append(child)

    def remove_child(self, child: Any):
        self._odv_children.remove(child)

    def index(self, odv_child) -> int:
        return self._odv_children.index(odv_child)


class OdvLeaf(OdvBase, ABC):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._odv_parent = parent

    def __str__(self):
        indexes = ""
        odv_leaf = self
        while isinstance(odv_leaf, OdvLeaf):
            indexes = f"{odv_leaf.i} {indexes}"
            odv_leaf = odv_leaf.parent
        return f"{self.__class__.__name__} {indexes}"

    @property
    def parent(self):
        return self._odv_parent

    @property
    def i(self):
        if self._odv_parent is None:
            raise Exception("ODV_Root as no parent")
        else:
            return self._odv_parent.index(self)


class OdvObject(OdvRoot, OdvLeaf, ABC):
    pass
