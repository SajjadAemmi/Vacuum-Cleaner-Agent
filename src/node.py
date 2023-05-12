import numpy as np


class Node(object):
    def __init__(self,
                 pos=None,
                 rooms=np.zeros((10, 10), dtype=int),
                 known_rooms=np.ones((10, 10), dtype=int) * -1,
                 f=0,
                 h=0):
        self.pos = pos
        self.rooms = rooms
        self.known_rooms = known_rooms
        self.f = f
        self.h = h
        self.cost = 0
        self.operations = []
        self.performance = 0

    def is_goal(self) -> bool:
        return np.array_equal(self.known_rooms, np.zeros((10, 10)))

    def calc_heuristic(self):
        self.h = np.count_nonzero(self.known_rooms)

    def calc_f(self, method):
        self.calc_heuristic()
        if method == "GBFS":
            self.f = self.h
        elif method == "A*":
            self.f = self.cost + self.h

    def update_known_rooms(self, mode):
        row, col = self.pos
        if mode == "one":
            self.known_rooms[row, col] = self.rooms[row, col]
        elif mode == "nine":
            min_row = max(0, row-1)
            max_row = min(9, row+1)
            min_col = max(0, col-1)
            max_col = min(9, col+1)
            self.known_rooms[min_row:max_row+1, min_col:max_col+1] = self.rooms[min_row:max_row+1, min_col:max_col+1]
        elif mode == "all":
            self.known_rooms = self.rooms

    def do_operation(self, operation):
        if operation == "U":
            self.pos[0] -= 1
            self.cost += 10

        elif operation == "D":
            self.pos[0] += 1
            self.cost += 10

        elif operation == "L":
            self.pos[1] -= 1
            self.cost += 10

        elif operation == "R":
            self.pos[1] += 1
            self.cost += 10

        elif operation == "C":
            self.cost += 15
            row, col = self.pos
            if self.rooms[row, col] == 1:
                self.rooms[row, col] = 0
                self.cost -= 100

        self.operations.append(operation)

    def is_operation_possible(self, operation) -> bool:
        if operation == "C" or operation == "O":
            return True
        elif operation == "U" and self.pos[0] > 0:
            return True
        elif operation == "D" and self.pos[0] < 9:
            return True
        elif operation == "L" and self.pos[1] > 0:
            return True
        elif operation == "R" and self.pos[1] < 9:
            return True
        else:
            return False
