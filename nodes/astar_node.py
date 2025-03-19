# nodes/astar_node.py

from .greedy_node import GreedyNode

class AStarNode(GreedyNode):
    """
    A* requires:
    - g(n): cost_so_far
    - h(n): heuristic
    - f(n) = g(n) + h(n)
    """
    def __init__(self, state, parent=None, action=None, cost_so_far=0.0, heuristic=0.0):
        super().__init__(state, parent, action, heuristic)
        self.cost_so_far = cost_so_far  # g(n)
        self.f = self.cost_so_far + heuristic  # f(n) = g(n) + h(n)

    def __repr__(self):
        return (f"AStarNode(state={self.state}, g={self.cost_so_far}, "
                f"h={self.heuristic}, f={self.f}, action={self.action})")
