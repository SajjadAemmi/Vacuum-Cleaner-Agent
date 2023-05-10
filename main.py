import argparse
from agent import Agent


parser = argparse.ArgumentParser("Vacuum Cleaner Agent")
parser.add_argument("--mode", type=str, default="one", help='''
one: The agent can sense Clean or dirty of his room
three: The agent can sense Clean or dirty of his room and neighbor rooms
all: The agent can sense Clean or dirty of all rooms
''')
parser.add_argument("--input", type=str, default="maps/map4.txt", help="Input file")
parser.add_argument("--show", action=argparse.BooleanOptionalAction, help="Whether to show the animation or not")
args = parser.parse_args()


if __name__ == "__main__":
    agent = Agent(args.mode, args.input, args.show)
    agent.GBFSTree()
    agent.run()
