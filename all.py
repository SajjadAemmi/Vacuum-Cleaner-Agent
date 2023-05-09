import copy
from operator import attrgetter

Queue = []
VisitedStates = []
Operations = ["U", "D", "R", "L", "C", "O"]
Moves = []
PerformanceMeasure = 0

def isGoal(state):

    if state.world ==[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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


class Node(object):

    position = []
    world = [[None for x in range(10)] for y in range(10)]
    f = 0
    h = 0
    deep = 0
    operations = []


def doOperation(state, Operation):

    nextState = copy.deepcopy(state)

    if Operation == "U":
        nextState.position[0] = nextState.position[0] - 1

    elif Operation == "D":
        nextState.position[0] = nextState.position[0] + 1

    elif Operation == "R":
        nextState.position[1] = nextState.position[1] + 1

    elif Operation == "L":
        nextState.position[1] = nextState.position[1] - 1

    elif Operation == "C":
        row = nextState.position[0]
        col = nextState.position[1]
        nextState.world[row][col] = 1

    return nextState.world, nextState.position


def heuristic(state):

    cntr = 0

    for i in range(10):
        for j in range(10):
            if state.world[i][j] == 0:
                cntr = cntr + 1

    return cntr


def makeChild(thisState, Operation):

    global Queue
    global VisitedStates

    childState = copy.deepcopy(thisState)
    childState.world, childState.position = doOperation(thisState, Operation)

    state = {"world": childState.world[:], "position": childState.position[:]}

    if state not in VisitedStates:
        childState.deep = thisState.deep + 1
        childState.h = heuristic(childState)
        childState.f = childState.h
        childState.operations = thisState.operations[:]
        childState.operations.append(Operation)
        Queue.append(childState)
        visited_state = {"world": childState.world[:], "position": childState.position[:]}
        VisitedStates.append(visited_state)
    else:
        for s in Queue:
            if s.world == childState.world and s.position == childState.position and s.f > childState.f:
                s.f = childState.f + 0
                s.deep = childState.deep + 0
                break


def isOperationPossible(state, Operation):

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

    elif Operation == "R":
        if state.position[1] < 9:
            return True
        else:
            return False

    elif Operation == "L":
        if state.position[1] > 0:
            return True
        else:
            return False

    return True

def GBFSTree():

    global Queue
    global Operations
    global VisitedStates

    thisState = min(Queue, key=attrgetter('f'))

    while isGoal(thisState) != True:

        for Operation in Operations:
            if isOperationPossible(thisState, Operation):
                makeChild(thisState, Operation)

        Queue.remove(thisState)
        thisState = min(Queue, key=attrgetter('f'))

    print(thisState.operations)
    return thisState.operations


def solve(state):

    global PerformanceMeasure

    for Operation in state.operations:

        for i in range(10):
            for j in range(10):
                if state.world[i][j] == 0:
                    PerformanceMeasure = PerformanceMeasure - 1

        if Operation == "U":
            state.position[0] = state.position[0] - 1
            PerformanceMeasure = PerformanceMeasure - 10

        elif Operation == "D":
            state.position[0] = state.position[0] + 1
            PerformanceMeasure = PerformanceMeasure - 10

        elif Operation == "R":
            state.position[1] = state.position[1] + 1
            PerformanceMeasure = PerformanceMeasure - 10

        elif Operation == "L":
            state.position[1] = state.position[1] - 1
            PerformanceMeasure = PerformanceMeasure - 10

        elif Operation == "C":
            PerformanceMeasure = PerformanceMeasure - 15

            row = state.position[0]
            col = state.position[1]

            if state.world[row][col] == 0:
                PerformanceMeasure = PerformanceMeasure + 100

            state.world[row][col] = 1

    print("PerformanceMeasure: ")
    print(PerformanceMeasure)


def startGame():

    root = Node()

    f = open("maps/map4.txt")
    lines = f.read().split('\n')
    for i in range(10):
        cells = lines[i].split(' ')
        for j in range(10):
            root.world[i][j] = int(cells[j])

    root.position = [0, 0]

    root.f = heuristic(root)
    Queue.append(root)
    visited_state = {"world": root.world[:], "position": root.position[:]}
    VisitedStates.append(visited_state)
    root.operations = GBFSTree()
    solve(root)


startGame()
