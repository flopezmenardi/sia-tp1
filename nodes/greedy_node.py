from .base_node import BaseNode

def default_composition(heuristics):
    """
    Función de composición por defecto: suma todos los valores heurísticos.
    Puedes modificarla para usar max(heuristics) u otra combinación.
    """
    return sum(heuristics)

class GreedyNode(BaseNode):
    """
    Nodo para búsqueda Greedy que ahora acepta múltiples heurísticas.
    
    Parámetros:
      - heuristics: una lista (o iterable) de valores heurísticos (números).
      - composition_func: función que recibe la lista de heurísticos y devuelve un único valor.
        Por defecto se utiliza la suma.
    """
    def __init__(self, state, parent=None, action=None, heuristics=None, composition_func=None):
        super().__init__(state, parent, action)
        # Si no se especifica, usamos una lista vacía (equivalente a 0).
        if heuristics is None:
            heuristics = []
        self.heuristics = list(heuristics)
        
        # Si no se proporciona función de composición, usamos la función por defecto.
        if composition_func is None:
            composition_func = default_composition
        self.composition_func = composition_func
        
        # Calculamos el valor compuesto de la heurística.
        self.composed_heuristic = self.composition_func(self.heuristics)
        self.heuristic = self.composed_heuristic  # Se utiliza para ordenar en la cola de prioridad.
    
    def __repr__(self):
        return (f"GreedyNode(state={self.state}, heuristics={self.heuristics}, "
                f"composed_h={self.composed_heuristic}, action={self.action})")
