import time


class Maze:
    def __init__(self, filename, NodeClass):

        self.NodeClass = NodeClass

        with open(filename) as f:
            contents = f.read().strip().splitlines()
        grid_size = eval(contents[0])   # e.g. [5, 11]
        self.rows, self.cols = grid_size

        self.start = eval(contents[1])  # e.g. (0, 1)

        goals_line = contents[2]  # e.g. "(7, 0)|(10, 3)"
        goals_str = goals_line.split("|")
        self.goal = [eval(g) for g in goals_str]

        walls = []
        for line in contents[3:]:
            x, y, w, h = eval(line)
            for xx in range(x, x + w):
                for yy in range(y, y + h):
                    walls.append((xx, yy))
        self.walls = set(walls)

        # Prepare solution structures
        self.solution = None
        self.explored = set()
        self.num_explored = 0

    def neighbors(self, state):
        (x, y) = state
        candidates = [
            ("up",    (x,   y - 1)),
            ("left",  (x-1, y)),
            ("down",  (x,   y + 1)),
            ("right", (x+1, y))
        ]
        results = []
        for action, (nx, ny) in candidates:
            if 0 <= nx < self.cols and 0 <= ny < self.rows:
                if (nx, ny) not in self.walls:
                    results.append((action, (nx, ny)))
        return results

    def print(self):
        """
        Text-based debugging printout.
        We'll place:
          'A' = start,
          'B' = goal(s),
          '█' = walls,
          '*' = solution path,
          '.' = empty space
        """
        path = self.solution[1] if self.solution else None
        for row in range(self.rows):
            for col in range(self.cols):
                if (col, row) in self.walls:
                    print("█", end="")
                elif (col, row) == self.start:
                    print("A", end="")
                elif (col, row) in self.goal:
                    print("B", end="")
                elif path and (col, row) in self.solution:
                    print("*", end="")
                else:
                    print(".", end="")
            print()
        print()

    def _build_solution(self, goal_node, gui=None):
        """
        Reconstruct the path from goal_node to the start by climbing
        parent pointers. Also color path in green if GUI is present.
        """
        actions = []
        cells = []
        node = goal_node

        while node.parent is not None:
            actions.append(node.action)
            cells.append(node.state)
            if gui:
                gui.update_cell(node.state, "green")
                gui.window.update()
                time.sleep(0.1)
            node = node.parent

        actions.reverse()
        cells.reverse()
        self.solution = (actions, cells)

    def _get_frontier(self, method):
        """
        Return an instance of DFS, BFS, GBFS, AStar, or UCS based on 'method'.
        """
        from search import DFS, BFS, GBFS, AStar, UCS

        if method == "dfs":
            return DFS()
        elif method == "bfs":
            return BFS()
        elif method == "gbfs":
            # h: Manhattan distance to the nearest goal
            def h_func(state):
                x, y = state
                return min(abs(x - gx) + abs(y - gy) for (gx, gy) in self.goal)
            return GBFS(h_func)
        elif method == "astar":
            def g_cost(node):
                cost = 0
                cur = node
                while cur.parent is not None:
                    cost += 1
                    cur = cur.parent
                return cost

            def h_func(state):
                x, y = state
                return min(abs(x - gx) + abs(y - gy) for (gx, gy) in self.goal)
            return AStar(g_cost, h_func)
        elif method == "ucs":
            def g_cost(node):
                cost = 0
                cur = node
                while cur.parent is not None:
                    cost += 1
                    cur = cur.parent
                return cost
            return UCS(g_cost)
        else:
            raise ValueError(f"Unknown method: {method}")

    def solve(self, method="dfs", gui=None, max_depth=9999):

        if method == "iddfs":
            from iddfs import IDDFS
            solver = IDDFS(max_depth=max_depth)
            start_node = self.NodeClass(self.start, None, None)
            goal_node = solver.search(start_node, self, gui=gui)
            if goal_node is not None:
                self._build_solution(goal_node, gui)
            else:
                self.solution = None
            return

        # Otherwise, frontier-based approach
        frontier = self._get_frontier(method)
        start_node = self.NodeClass(self.start, None, None)
        frontier.add(start_node)

        self.explored = set()
        self.num_explored = 0

        while True:
            if frontier.empty():
                self.solution = None
                return

            node = frontier.remove()
            self.num_explored += 1

            # Debug print
            # print(f"Expanding: {node.state} via {node.action}")

            if gui:
                gui.update_cell(node.state, "yellow")
                gui.window.update()
                time.sleep(0.3)

            # Check if it's a goal
            if node.state in self.goal:
                self._build_solution(node, gui)
                return

            self.explored.add(node.state)

            # Add neighbors to frontier
            if method == "dfs":
                # Reverse the neighbor list so that the first in the list
                for (action, new_state) in reversed(self.neighbors(node.state)):
                    if (new_state not in self.explored) \
                       and not frontier.contains_state(new_state):
                        child = self.NodeClass(new_state, node, action)
                        frontier.add(child)
            else:
                for (action, new_state) in self.neighbors(node.state):
                    if (new_state not in self.explored) \
                       and not frontier.contains_state(new_state):
                        child = self.NodeClass(new_state, node, action)
                        frontier.add(child)
