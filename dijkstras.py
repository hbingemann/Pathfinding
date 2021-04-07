
INFINITY = 999999


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.distance = INFINITY  # distance is min distance from start
        self.parent = None  # node from which we got the shortest distance
