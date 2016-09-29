from state import State


class StartState(State):
    def __init__(self, globals):
        super(StartState, self).__init__(globals)

    def mouse_event(self, event, x, y):
        pass

    def keyboard_event(self, key):
        pass
