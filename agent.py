import copy
from operator import attrgetter
from node import Node


class Agent:
    def __init__(self, input, mode):
        self.Queue = []
        self.VisitedStates = []
        self.Operations = ["U", "D", "R", "L", "C", "O"]
        self.Moves = []
        self.PerformanceMeasure = 0

        self.root = Node()

        f = open(input)
        lines = f.read().split('\n')
        for i in range(10):
            cells = lines[i].split(' ')
            for j in range(10):
                self.root.world[i][j] = int(cells[j])

        self.root.know_world[0][0] = self.root.world[0][0]
        self.root.position = [0, 0]

        self.root.f = self.heuristic(self.root)
        self.Queue.append(self.root)
        visited_state = {"world": self.root.world[:], "position": self.root.position[:]}
        self.VisitedStates.append(visited_state)
        self.root.operations = self.GBFSTree()
        self.solve(self.root)

    def isGoal(self, state):
        if state.know_world == [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]:
            return True
        else:
            return False

    def doOperation(self, state, Operation):
        nextState = copy.deepcopy(state)

        if Operation == "U":
            nextState.position[0] -= 1

        elif Operation == "D":
            nextState.position[0] += 1

        elif Operation == "L":
            nextState.position[1] -= 1

        elif Operation == "R":
            nextState.position[1] += 1

        elif Operation == "C":
            row = nextState.position[0]
            col = nextState.position[1]
            nextState.world[row][col] = 1

        row = nextState.position[0]
        col = nextState.position[1]

        nextState.know_world[row][col] = nextState.world[row][col]

        return nextState.world, nextState.know_world, nextState.position

    def heuristic(self, state):
        counter = 0
        for i in range(10):
            for j in range(10):
                if state.know_world[i][j] == 2 or state.know_world[i][j] == 0:
                    counter += 1

        return counter

    def makeChild(self, parentState, Operation):
        childState = copy.deepcopy(parentState)
        childState.world, childState.know_world, childState.position = self.doOperation(
            parentState, Operation)

        state = {"world": childState.world[:], "position": childState.position[:]}

        if state not in self.VisitedStates:
            childState.deep = parentState.deep + 1
            childState.h = self.heuristic(childState)
            childState.f = childState.h
            childState.operations = parentState.operations[:]
            childState.operations.append(Operation)
            self.Queue.append(childState)
            visited_state = {
                "world": childState.world[:], "position": childState.position[:]}
            self.VisitedStates.append(visited_state)
        else:
            for state in self.Queue:
                if state.world == childState.world and state.know_world == childState.know_world and state.position == childState.position and state.f > childState.f:
                    state.f = childState.f + 0
                    state.deep = childState.deep + 0
                    break

    def isOperationPossible(self, state, Operation):
        if Operation == "U":
            if state.position[0] > 0:
                return True
            else:
                return False

        elif Operation == "D":
            if state.position[0] < 9:
                return True
            else:
                return False

        elif Operation == "L":
            if state.position[1] > 0:
                return True
            else:
                return False

        elif Operation == "R":
            if state.position[1] < 9:
                return True
            else:
                return False

        return True

    def GBFSTree(self):
        thisState = min(self.Queue, key=attrgetter('f'))

        while self.isGoal(thisState) != True:
            for Operation in self.Operations:
                if self.isOperationPossible(thisState, Operation):
                    self.makeChild(thisState, Operation)

            self.Queue.remove(thisState)
            thisState = min(self.Queue, key=attrgetter('f'))

        print(thisState.operations)
        return thisState.operations

    def solve(self, state):
        for Operation in state.operations:
            for i in range(10):
                for j in range(10):
                    if state.world[i][j] == 0:
                        PerformanceMeasure -= 1

            if Operation == "U":
                state.position[0] -= 1
                PerformanceMeasure -= 10

            elif Operation == "D":
                state.position[0] += 1
                PerformanceMeasure -= 10

            elif Operation == "R":
                state.position[1] += 1
                PerformanceMeasure -= 10

            elif Operation == "L":
                state.position[1] -= 1
                PerformanceMeasure -= 10

            elif Operation == "C":
                PerformanceMeasure -= 15

                row = state.position[0]
                col = state.position[1]

                if state.world[row][col] == 0:
                    PerformanceMeasure += 100

                state.world[row][col] = 1

        print("PerformanceMeasure:", PerformanceMeasure)
