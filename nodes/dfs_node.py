# nodes/dfs_node.py

from .base_node import BaseNode

class DFSNode(BaseNode):
    """
    DFS can also track depth to limit recursion (Depth-Limited Search)
    or for iterative deepening.
    """
    def __init__(self, state, parent=None, action=None, depth=0):
        super().__init__(state, parent, action)
        self.depth = depth

    def __repr__(self):
        return (f"DFSNode(state={self.state}, depth={self.depth}, "
                f"action={self.action})")
