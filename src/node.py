import numpy as np


class Node(object):
    def __init__(self,
                 pos=None,
                 world=np.zeros((10, 10), dtype=int),
                 known_world=np.ones((10, 10), dtype=int) * -1,
                 f=0,
                 h=0):
        self.pos = pos
        self.world = world
        self.known_world = known_world
        self.f = f
        self.h = h
        self.operations = []

    def is_goal(self) -> bool:
        return np.array_equal(self.known_world, np.zeros((10, 10)))

    def heuristic(self):
        return np.count_nonzero(self.known_world)
