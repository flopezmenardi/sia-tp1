class Node:
    """
    Nodo base que guarda:
    - state: un objeto de tipo SokobanState (o el que corresponda)
    - parent: referencia a otro nodo (el padre)
    - action: la acción que llevó de 'parent' a este
    - depth: profundidad en el árbol de búsqueda
    """
    def __init__(self, state, parent=None, action=None, cost_so_far=0.0, depth=0, heuristic=0.0):
        self.state = state              # (posJugador, posicionesCajas, etc.)
        self.parent = parent            # Nodo padre
        self.action = action            # Acción que llevó a este nodo
        self.cost_so_far = cost_so_far  # g(n)
        # self.depth = depth              # Profundidad en el árbol de búsqueda
        # self.heuristic = heuristic      # h(n), si hace falta
        # self.f = self.cost_so_far + self.heuristic  # f(n) = g(n) + h(n) (solo si usas A*)