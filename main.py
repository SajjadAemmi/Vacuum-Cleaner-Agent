import argparse
from src.agent import Agent


parser = argparse.ArgumentParser("Vacuum Cleaner Agent", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--mode", type=str, default="one",
                    help="\none: The agent can sense Clean or dirty of his room" +
                    "\nthree: The agent can sense Clean or dirty of his room and neighbor rooms" + 
                    "\nall: The agent can sense Clean or dirty of all rooms")
parser.add_argument("--input", type=str, default="maps/map4.txt", help="Input file")
parser.add_argument("--show", action=argparse.BooleanOptionalAction, default=False, help="Whether to show the animation or not")
args = parser.parse_args()


if __name__ == "__main__":
    agent = Agent(args.mode, args.input, args.show)
    agent.solve()
    agent.run()
