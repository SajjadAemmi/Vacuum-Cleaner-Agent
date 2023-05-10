import numpy as np


class Node(object):
    def __init__(self,
                 pos=[],
                 world=np.zeros((10, 10), dtype=int),
                 know_world=np.ones((10, 10), dtype=int) * 2,
                 f=0,
                 h=0,
                 deep=0,
                 operations=[]):
        self.pos = pos
        self.world = world
        self.know_world = know_world
        self.f = f
        self.h = h
        self.deep = deep
        self.operations = operations
