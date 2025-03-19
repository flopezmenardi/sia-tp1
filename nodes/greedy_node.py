# nodes/greedy_node.py

from .base_node import BaseNode

class GreedyNode(BaseNode):
    """
    For Greedy search we store a heuristic h(n),
    used to prioritize expansion in a priority queue or sorted structure.
    """
    def __init__(self, state, parent=None, action=None, heuristic=0.0):
        super().__init__(state, parent, action)
        self.heuristic = heuristic  # h(n)

    def __repr__(self):
        return (f"GreedyNode(state={self.state}, h={self.heuristic}, "
                f"action={self.action})")
