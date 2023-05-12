from src.agent import Agent


def test():
    agent = Agent("one", "GBFS", "maps/map1.txt")
    solution = agent.think()
    assert solution == ['R', 'R', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'R', 'R', 'U', 'R', 'R', 'R', 'U', 'U', 'U', 'U', 'U', 'U', 'R', 'R', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'L', 'C', 'L', 'L', 'L', 'L', 'L', 'C', 'L', 'U', 'L', 'L', 'U', 'U', 'R', 'U', 'U', 'L', 'U', 'U', 'R', 'U', 'C', 'L', 'C', 'D', 'D', 'C', 'R', 'C', 'U', 'R', 'R', 'R', 'U', 'R', 'R', 'U', 'C', 'R', 'R', 'C', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'C', 'L', 'L', 'C', 'L', 'C', 'U', 'U', 'U', 'L', 'U', 'U', 'R', 'U', 'R', 'C', 'D', 'D', 'C', 'D', 'D', 'C', 'U', 'L', 'C', 'U', 'C', 'L', 'L', 'U', 'C', 'U', 'U', 'U', 'R', 'R', 'C', 'D', 'L', 'L', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'C', 'U', 'R', 'C', 'U', 'L', 'L', 'L', 'C', 'L', 'C', 'D', 'D', 'C', 'D', 'D', 'R', 'C', 'U', 'U', 'C', 'U', 'U', 'U', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'C', 'U', 'U', 'U', 'U', 'R']
