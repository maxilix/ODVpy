from abc import ABC, abstractmethod


class View(object):
    def __init__(self, control, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.control = control

    # @abstractmethod
    def refresh(self, *args, **kwargs):
        pass


class HierarchicalView(View):
    def __init__(self, control, *args, **kwargs):
        super().__init__(control, *args, **kwargs)
        self.view_list = []

    def __iter__(self):
        return iter(self.view_list)

    def __len__(self):
        return len(self.view_list)

    def __getitem__(self, index):
        return self.view_list[index]



