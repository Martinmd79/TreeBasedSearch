import sys
from node import Node
from mazee import Maze
from gui import MazeGUI

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <filename> <method>")
        sys.exit(0)

    filename = sys.argv[1]
    method = sys.argv[2].lower()
    max_depth = 9999
    if len(sys.argv) == 4:
        max_depth = int(sys.argv[3])

    maze = Maze(filename, NodeClass=Node)

    # Create the GUI
    gui = MazeGUI(maze)

    def solve_and_print():

        maze.solve(method=method, gui=gui, max_depth=max_depth)

        print("\n=== Maze Text Output ===")
        maze.print()

        if maze.solution:
            actions, cells = maze.solution
            print("Actions:", actions)
            print("Goal reached:", cells[-1])  # last cell = goal

    gui.window.after(100, solve_and_print)
    gui.window.mainloop()
