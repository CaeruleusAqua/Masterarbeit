from objects import *
from objects import color


class Scenario:
    def __init__(self, handler):
        handler.graph.drawables.append(Circle((0, 0), 10, color.RED, filled=True))
        handler.graph.drawables.append(Circle((0, 0), 30, color.RED, filled=False))
        handler.graph.drawables.append(Arc((20, 0), 10, color.BLUE, startAngle=0, endAngle=180, filled=True))
        handler.graph.drawables.append(Car((0, 0), color.GREEN))
