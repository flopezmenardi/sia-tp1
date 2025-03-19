# nodes/bfs_node.py

from .base_node import BaseNode

class BFSNode(BaseNode):
    """
    BFS can track the 'depth' of a node if you want
    to know which 'level' you're on in the search tree.
    """
    def __init__(self, state, parent=None, action=None, depth=0):
        super().__init__(state, parent, action)
        self.depth = depth

    def __repr__(self):
        return (f"BFSNode(state={self.state}, depth={self.depth}, "
                f"action={self.action})")
