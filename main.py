import argparse
from src.agent import Agent


parser = argparse.ArgumentParser("Vacuum Cleaner Agent", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--mode", type=str, default="one",
                    help="\none: The agent can sense Clean or dirty of his room" +
                    "\nnine: The agent can sense Clean or dirty of his room and neighbor rooms" + 
                    "\nall: The agent can sense Clean or dirty of all rooms")
parser.add_argument("--method", type=str, default="GBFS",
                    help="\nGBFS: Greedy Best-First Search. It always prioritizes the node with the lowest heuristic value without any consideration of the cost to get to that node." +
                    "\nA*: A* search. It always prioritizes the node with the lowest sum of heuristic value and cost to get to that node.")
parser.add_argument("--input", type=str, default="maps/map1.txt", help="Input file")
parser.add_argument("--show", action=argparse.BooleanOptionalAction, default=False, help="Whether to show the animation or not")
args = parser.parse_args()


if __name__ == "__main__":
    agent = Agent(args.mode, args.method, args.input, args.show)

    print("Agent thinks to find the best solution... 🤔")
    solution = agent.think()
    
    print("Agent found the best solution! 🤩")
    print(solution)
    
    print("Agent comes into action... 🧹")
    agent.run()
    
    print("All rooms are clean now 😌")
