# iddfs.py

import time


class IDDFS:
    """
    Iterative Deepening Depth-First Search.
    Rather than using a single frontier, it repeatedly does DFS
    with an increasing depth limit. If no solution is found up
    to max_depth, it returns None.
    """

    def __init__(self, max_depth=9999):
        self.max_depth = max_depth

    def search(self, start_node, maze, gui=None):
        for depth_limit in range(self.max_depth):
            visited_this_round = set()
            result = self._depth_limited_search(
                node=start_node,
                limit=depth_limit,
                maze=maze,
                visited=visited_this_round,
                gui=gui
            )
            if result is not None:
                return result
        return None

    def _depth_limited_search(self, node, limit, maze, visited, gui):
        # Check if we found a goal
        if node.state in maze.goal:
            return node

        if limit == 0:
            return None

        visited.add(node.state)

        # Explore neighbors in up-left-down-right order
        for action, new_state in maze.neighbors(node.state):
            if new_state not in visited:
                child = maze.NodeClass(new_state, node, action)
                if gui:
                    gui.update_cell(child.state, color="yellow")
                    gui.window.update()
                    time.sleep(0.05)

                result = self._depth_limited_search(
                    child, limit - 1, maze, visited, gui
                )
                if result is not None:
                    return result

        return None
