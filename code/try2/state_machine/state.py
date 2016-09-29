from abc import ABCMeta, abstractmethod


class State:
    __metaclass__ = ABCMeta

    def __init__(self, globals):
        self.globals = globals

    @abstractmethod
    def mouse_event(self, event, x, y):
        pass

    @abstractmethod
    def keyboard_event(self, key):
        pass
