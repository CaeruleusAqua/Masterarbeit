class Lane:
    def __init__(self):
        self.id = 0
        self.anchor = None
        self.nodes = list()
        self.points = list()
        self.parents = list()

    def update(self):
        for parent in self.parents:
            parent.update()
