# test_maze.py

import unittest
import tempfile
import os

from node import Node
from mazee import Maze


class TestMazeSearch(unittest.TestCase):
    def setUp(self):

        self.maze_text = """[2, 2]
(0, 0)
(1, 1)
"""

        fd, self.temp_file = tempfile.mkstemp()
        with os.fdopen(fd, 'w') as f:
            f.write(self.maze_text)

        self.maze = Maze(self.temp_file, NodeClass=Node)

    def tearDown(self):
        os.remove(self.temp_file)

    def test_dfs(self):
        self.maze.solve(method="dfs")
        # We expect solution is not None
        self.assertIsNotNone(self.maze.solution, "DFS should find a path")
        actions, cells = self.maze.solution
        self.assertIn((1, 1), cells, "Goal should be included in DFS path")

    def test_bfs(self):
        self.maze.solve(method="bfs")
        self.assertIsNotNone(self.maze.solution, "BFS should find a path")
        actions, cells = self.maze.solution
        self.assertIn((1, 1), cells, "Goal should be in BFS path")

    def test_iddfs(self):
        self.maze.solve(method="iddfs")
        self.assertIsNotNone(self.maze.solution, "IDDFS should find a path")
        actions, cells = self.maze.solution
        self.assertIn((1, 1), cells, "Goal should be in IDDFS path")


if __name__ == "__main__":
    unittest.main()
