import copy
from operator import attrgetter
import matplotlib.pyplot as plt
from src.node import Node


class Agent:
    def __init__(self, mode, input_file, show):
        self.mode = mode
        self.show = show
        self.queue = []
        self.visited_states = []
        self.performance = 0
        self.operations = ["U", "D", "R", "L", "C", "O"]
        self.root = Node()

        f = open(input_file, "r", encoding="utf-8")
        lines = f.read().split('\n')
        for i in range(10):
            cells = lines[i].split(' ')
            for j in range(10):
                self.root.world[i, j] = int(cells[j])

        assert mode in ["one", "three", "all"], "Invalid value, mode must be one, three or all"
        if mode == "one":
            self.root.known_world[0, 0] = self.root.world[0, 0]
        elif mode == "three":
            self.root.known_world[0:2, 0:2] = self.root.world[0:2, 0:2]
        elif mode == "all":
            self.root.known_world = self.root.world

        self.root.pos = [0, 0]
        self.root.f = self.root.heuristic()
        self.queue.append(self.root)
        visited_state = {"world": self.root.world.tolist(), "pos": self.root.pos}
        self.visited_states.append(visited_state)

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
            next_state.world[row, col] = 0

        row = next_state.pos[0]
        col = next_state.pos[1]

        next_state.known_world[row, col] = next_state.world[row, col]
        return next_state.world, next_state.known_world, next_state.pos

    def make_child(self, parent_state, operation):
        child_state = copy.deepcopy(parent_state)
        child_state.world, child_state.known_world, child_state.pos = self.do_operation(
            parent_state, operation)

        state = {"world": child_state.world.tolist(), "pos": child_state.pos}

        if state not in self.visited_states:
            child_state.h = child_state.heuristic()
            child_state.f = child_state.h
            child_state.operations = parent_state.operations
            child_state.operations.append(operation)
            self.queue.append(child_state)
            visited_state = {
                "world": child_state.world.tolist(), "pos": child_state.pos}
            self.visited_states.append(visited_state)
        else:
            for state in self.queue:
                if state.world.tolist() == child_state.world.tolist() and state.known_world.tolist() == child_state.known_world.tolist() and state.pos == child_state.pos and state.f > child_state.f:
                    state.f = child_state.f

    def is_operation_possible(self, state, operation):
        if operation == "U" and state.pos[0] > 0:
            return True
        elif operation == "D" and state.pos[0] < 9:
            return True
        elif operation == "L" and state.pos[1] > 0:
            return True
        elif operation == "R" and state.pos[1] < 9:
            return True
        elif operation == "C" or operation == "O":
            return True
        else:
            return False

    def solve(self):
        # GBFS Algorithm
        this_state = min(self.queue, key=attrgetter('f'))
        if self.show:
            _, (ax1, ax2) = plt.subplots(1, 2)
            ax1.imshow(this_state.world)
            ax2.imshow(this_state.known_world)

        while not this_state.is_goal():
            for operation in self.operations:
                if self.is_operation_possible(this_state, operation):
                    self.make_child(this_state, operation)

            self.queue.remove(this_state)
            this_state = min(self.queue, key=attrgetter('f'))
            if self.show:
                ax1.imshow(this_state.world)
                ax1.scatter(this_state.pos[1], this_state.pos[0], s=100)
                ax2.imshow(this_state.known_world)
                ax2.scatter(this_state.pos[1], this_state.pos[0], s=100)
                plt.pause(0.01)
                ax1.clear()
                ax2.clear()

        self.root.operations = this_state.operations
        replacements = {"U": "⬆️", "D": "⬇️", "R": "➡️", "L": "⬅️", "C": "🧹"}
        replacer = replacements.get  # For faster gets.
        print([replacer(n, n) for n in self.root.operations])

    def run(self):
        for operation in self.root.operations:
            for i in range(10):
                for j in range(10):
                    if self.root.world[i, j] == 1:
                        self.performance -= 1

            if operation == "U":
                self.root.pos[0] -= 1
                self.performance -= 10

            elif operation == "D":
                self.root.pos[0] += 1
                self.performance -= 10

            elif operation == "R":
                self.root.pos[1] += 1
                self.performance -= 10

            elif operation == "L":
                self.root.pos[1] -= 1
                self.performance -= 10

            elif operation == "C":
                self.performance -= 15
                row = self.root.pos[0]
                col = self.root.pos[1]
                if self.root.world[row][col] == 1:
                    self.performance += 100
                self.root.world[row][col] = 0

        print("performance:", self.performance)
