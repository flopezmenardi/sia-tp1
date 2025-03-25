import numpy as np
from scipy.optimize import linear_sum_assignment

def hungarian_player_heuristic(state, level_data):
    """
    Heurística compuesta para Sokoban:
      - Calcula el costo mínimo (suma de distancias Manhattan) para asignar 
        las cajas a las metas (usando el algoritmo Hungarian).
      - Suma la distancia Manhattan mínima desde el jugador a alguna caja que
        aún no se encuentre en una meta.
    
    Parámetros:
      - state: instancia de State, que tiene:
            state.player_pos: tupla (x, y)
            state.box_positions: frozenset de posiciones (x, y)
      - level_data: instancia de LevelData, que tiene:
            level_data.goals: frozenset de posiciones (x, y)
            level_data.get_manhattan_distance(pos1, pos2): retorna la distancia Manhattan entre pos1 y pos2.
    
    Retorna:
      - Un valor numérico (float) que es la suma del costo óptimo de asignación entre cajas y metas 
        y la distancia mínima del jugador a una caja que aún no esté en meta.
    """
    boxes = list(state.box_positions)
    goals = list(level_data.goals)
    
    # Si no hay cajas, la heurística es 0.
    if not boxes:
        return 0

    # Construir la matriz de costos:
    # Cada elemento (i, j) es la distancia Manhattan desde la caja i a la meta j.
    cost_matrix = np.zeros((len(boxes), len(goals)), dtype=float)
    for i, box in enumerate(boxes):
        for j, goal in enumerate(goals):
            cost_matrix[i, j] = level_data.get_manhattan_distance(box, goal)

    # Usar el algoritmo Hungarian para hallar la asignación óptima.
    # linear_sum_assignment funciona con matrices rectangulares; 
    # devuelve dos arrays: row_ind y col_ind.
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    assignment_cost = cost_matrix[row_ind, col_ind].sum()

    # Calcular la distancia mínima desde el jugador a alguna caja que aún no esté en meta.
    boxes_not_on_goal = [box for box in boxes if box not in level_data.goals]
    if boxes_not_on_goal:
        player_distance = min(level_data.get_manhattan_distance(state.player_pos, box)
                              for box in boxes_not_on_goal)
    else:
        player_distance = 0

    return assignment_cost + player_distance
