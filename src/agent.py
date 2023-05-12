import copy
from operator import attrgetter
import numpy as np
import matplotlib.pyplot as plt
from src.node import Node


class Agent:
    def __init__(self, mode, method, input_file, show=False):
        assert mode in ["one", "nine", "all"], "Invalid value, mode must be one, nine or all"
        self.mode = mode
        print("Mode:", self.mode)
        assert method in ["GBFS", "A*"], "Invalid value, method must be GBFS or A*"
        self.method = method
        print("Method:", self.method)
        self.show = show
        self.queue = []
        self.visited_states = []
        self.operations = ["U", "D", "R", "L", "C", "O"]

        self.root = Node()
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.read().split('\n')
            for i in range(10):
                cells = lines[i].split(' ')
                for j in range(10):
                    self.root.rooms[i, j] = int(cells[j])

    def make_child(self, parent_node, operation):
        child_node = copy.deepcopy(parent_node)
        child_node.do_operation(operation)
        child_node.update_known_rooms(self.mode)

        state = {"rooms": child_node.rooms.tolist(), "pos": child_node.pos}
        if state not in self.visited_states:
            child_node.calc_f(self.method)
            self.queue.append(child_node)
            self.visited_states.append(state)
        else:
            for node in self.queue:
                if node.rooms.tolist() == child_node.rooms.tolist() and node.pos == child_node.pos and node.f > child_node.f:
                    node.f = child_node.f

    def think(self):
        self.root.pos = [0, 0]
        self.root.update_known_rooms(self.mode)
        self.root.calc_f(self.method)
        self.queue.append(self.root)
        visited_state = {"rooms": self.root.rooms.tolist(), "pos": self.root.pos}
        self.visited_states.append(visited_state)

        if self.show:
            _, (ax1, ax2) = plt.subplots(1, 2)
   
        while True:
            node = min(self.queue, key=attrgetter('f'))
            if node.is_goal():
                break

            if self.show:
                self.show_rooms(node, ax1, ax2)

            for operation in self.operations:
                if node.is_operation_possible(operation):
                    self.make_child(node, operation)

            self.queue.remove(node)
        
        self.root.operations = node.operations
        return self.root.operations

    def run(self):
        for operation in self.root.operations:
            self.root.performance -= np.count_nonzero(self.root.rooms)

            if operation == "U":
                self.root.pos[0] -= 1
                self.root.performance -= 10

            elif operation == "D":
                self.root.pos[0] += 1
                self.root.performance -= 10

            elif operation == "R":
                self.root.pos[1] += 1
                self.root.performance -= 10

            elif operation == "L":
                self.root.pos[1] -= 1
                self.root.performance -= 10

            elif operation == "C":
                self.root.performance -= 15
                row, col = self.root.pos
                if self.root.rooms[row, col] == 1:
                    self.root.rooms[row, col] = 0
                    self.root.performance += 100

        print("performance:", self.root.performance)

    def show_rooms(self, node, ax1, ax2):
        ax1.imshow(node.rooms)
        ax1.scatter(node.pos[1], node.pos[0], s=100)
        ax2.imshow(node.known_rooms)
        ax2.scatter(node.pos[1], node.pos[0], s=100)
        plt.pause(0.01)
        ax1.clear()
        ax2.clear()
