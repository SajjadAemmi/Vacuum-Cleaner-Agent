class Node(object):
    position = []
    world = [[None for x in range(10)] for y in range(10)]
    know_world = [[2 for x in range(10)] for y in range(10)]
    f = 0
    h = 0
    deep = 0
    operations = []
