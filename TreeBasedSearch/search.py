import heapq


class DFS:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(n.state == state for n in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        return self.frontier.pop()


class BFS(DFS):
    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node


class PriorityFrontier:
    """
    A generic priority queue (min-heap) Frontier.
    We store items as (priority, count, node).
    'count' is a tie-breaker so that the earliest added node with the same
    priority is expanded first.
    """

    def __init__(self, priority_func):
        self.priority_func = priority_func
        self.frontier = []
        self.count = 0  # tie-breaker counter

    def add(self, node):
        self.count += 1
        priority = self.priority_func(node)
        heapq.heappush(self.frontier, (priority, self.count, node))

    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        _, _, node = heapq.heappop(self.frontier)
        return node

    def contains_state(self, state):
        return any(item[2].state == state for item in self.frontier)

    def empty(self):
        return len(self.frontier) == 0


class GBFS(PriorityFrontier):
    def __init__(self, h_func):
        super().__init__(lambda node: h_func(node.state))


class AStar(PriorityFrontier):
    def __init__(self, g_func, h_func):
        super().__init__(lambda node: g_func(node) + h_func(node.state))


class UCS(AStar):
    def __init__(self, g_func):
        super().__init__(g_func, lambda s: 0)
