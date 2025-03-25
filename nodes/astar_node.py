from .greedy_node import GreedyNode

class AStarNode(GreedyNode):
    """
    Nodo para A* que utiliza la composición de múltiples heurísticas.
    
    Además de lo que aporta GreedyNode (el valor compuesto de h(n)),
    almacena:
      - cost_so_far (g(n))
      - f(n) = g(n) + composed_heuristic (h(n))
    """
    def __init__(self, state, parent=None, action=None, cost_so_far=0.0, heuristics=None, composition_func=None):
        super().__init__(state, parent, action, heuristics, composition_func)
        self.cost_so_far = cost_so_far  # g(n)
        self.f = self.cost_so_far + self.composed_heuristic  # f(n) = g(n) + h(n)
    
    def __repr__(self):
        return (f"AStarNode(state={self.state}, g={self.cost_so_far}, "
                f"heuristics={self.heuristics}, composed_h={self.composed_heuristic}, "
                f"f={self.f}, action={self.action})")
