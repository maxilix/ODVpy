from abc import ABC, abstractmethod


class Control(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view = None

    def add_view(self, view):
        self.view = view

    # @abstractmethod
    def update(self):
        pass


class HierarchicalControl(Control):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.control_list = []

    def __iter__(self):
        return iter(self.control_list)

    def __len__(self):
        return len(self.control_list)

    def __getitem__(self, index):
        return self.control_list[index]

    def add_view(self, view):
        assert len(view) == len(self)
        super().add_view(view)
        for i in range(len(self)):
            self.control_list[i].add_view(view[i])


