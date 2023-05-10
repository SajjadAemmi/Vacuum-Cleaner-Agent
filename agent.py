import copy
from queue import Queue
from operator import attrgetter
import numpy as np
import matplotlib.pyplot as plt
from node import Node


class Agent:
    def __init__(self, mode, input_file, show):
        self.mode = mode
        self.show = show
        self.queue = []
        self.visited_states = []
        self.operations = ["U", "D", "R", "L", "C", "O"]
        self.Moves = []
        self.performance = 0

        self.root = Node()

        f = open(input_file, "r", encoding="utf-8")
        lines = f.read().split('\n')
        for i in range(10):
            cells = lines[i].split(' ')
            for j in range(10):
                self.root.world[i, j] = int(cells[j])

        assert mode in ["one", "three", "all"], "Invalid mode, must be one, three or all"
        if mode == "one":
            self.root.know_world[0, 0] = self.root.world[0, 0]
        elif mode == "three":
            self.root.know_world[0][0] = self.root.world[0][0]
            self.root.know_world[0][1] = self.root.world[0][1]
            self.root.know_world[1][0] = self.root.world[1][0]
            self.root.know_world[1][1] = self.root.world[1][1]
        elif mode == "all":
            self.root.know_world = self.root.world

        self.root.pos = [0, 0]
        self.root.f = self.heuristic(self.root)
        self.queue.append(self.root)
        visited_state = Node(world=self.root.world, pos=self.root.pos)
        self.visited_states.append(visited_state)

    def is_goal(self, state):
        if np.array_equal(state.know_world, np.ones((10, 10), dtype=int)):
            return True
        else:
            return False

    def do_operation(self, state, operation):
        next_state = copy.deepcopy(state)
        
        if operation == "U":
            next_state.pos[0] -= 1

        elif operation == "D":
            next_state.pos[0] += 1

        elif operation == "L":
            next_state.pos[1] -= 1

        elif operation == "R":
            next_state.pos[1] += 1

        elif operation == "C":
            row = next_state.pos[0]
            col = next_state.pos[1]
            next_state.world[row][col] = 1

        row = next_state.pos[0]
        col = next_state.pos[1]

        next_state.know_world[row][col] = next_state.world[row][col]

        return next_state.world, next_state.know_world, next_state.pos

    def heuristic(self, state):
        counter = 0
        for i in range(10):
            for j in range(10):
                if state.know_world[i][j] == 2 or state.know_world[i][j] == 0:
                    counter += 1

        return counter

    def make_child(self, parent_state, operation):
        child_state = copy.deepcopy(parent_state)
        child_state.world, child_state.know_world, child_state.pos = self.do_operation(
            parent_state, operation)

        state = Node(world=child_state.world, pos=child_state.pos)

        if state not in self.visited_states:
            child_state.deep = parent_state.deep + 1
            child_state.h = self.heuristic(child_state)
            child_state.f = child_state.h
            child_state.operations = parent_state.operations[:]
            child_state.operations.append(operation)
            self.queue.append(child_state)
            visited_state = Node(world=child_state.world, pos=child_state.pos)
            self.visited_states.append(visited_state)
        else:
            for state in self.queue:
                if state.world == child_state.world and state.know_world == child_state.know_world and state.pos == child_state.pos and state.f > child_state.f:
                    state.f = child_state.f + 0
                    state.deep = child_state.deep + 0
                    break

    def is_operation_possible(self, state, operation):
        if operation == "U":
            if state.pos[0] > 0:
                return True
            else:
                return False

        elif operation == "D":
            if state.pos[0] < 9:
                return True
            else:
                return False

        elif operation == "L":
            if state.pos[1] > 0:
                return True
            else:
                return False

        elif operation == "R":
            if state.pos[1] < 9:
                return True
            else:
                return False

        return True

    def GBFSTree(self):
        this_state = min(self.queue, key=attrgetter('f'))
        if self.show:
            fig, ax = plt.subplots()
            ax.imshow(this_state.world, extent=[0, 1, 0, 1])

        while self.is_goal(this_state) != True:
            for operation in self.operations:
                if self.is_operation_possible(this_state, operation):
                    self.make_child(this_state, operation)

            self.queue.remove(this_state)
            this_state = min(self.queue, key=attrgetter('f'))
            if self.show:
                ax.imshow(this_state.world)
                ax.scatter(this_state.pos[1], this_state.pos[0], s=100)
                plt.pause(0.01)
                ax.clear()

        print(this_state.operations)
        self.root.operations = this_state.operations

    def run(self):
        state = self.root
        for operation in state.operations:
            for i in range(10):
                for j in range(10):
                    if state.world[i][j] == 0:
                        self.performance -= 1

            if operation == "U":
                state.pos[0] -= 1
                self.performance -= 10

            elif operation == "D":
                state.pos[0] += 1
                self.performance -= 10

            elif operation == "R":
                state.pos[1] += 1
                self.performance -= 10

            elif operation == "L":
                state.pos[1] -= 1
                self.performance -= 10

            elif operation == "C":
                self.performance -= 15
                row = state.pos[0]
                col = state.pos[1]
                if state.world[row][col] == 0:
                    self.performance += 100
                state.world[row][col] = 1

        print("performance:", self.performance)
