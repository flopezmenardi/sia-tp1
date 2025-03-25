# heuristics.py

def deadlock_heuristic(state, level_data):
    """
    Heurística que penaliza estados deadlocked en Sokoban.
    
    Para cada caja en el estado, si la caja NO está en una meta y se encuentra
    en una posición que level_data considera deadlock, se retorna infinito, ya que
    en ese caso el estado es irresoluble.
    
    Si no se detecta ningún deadlock, se retorna 0, pues esta heurística no aporta
    costo adicional.
    
    Esta función es admisible, ya que nunca sobreestima el coste real:
      - En estados sin deadlock, el coste real (derivado de evitar deadlocks) es 0.
      - En estados deadlocked, el coste real es inalcanzable (teóricamente infinito).
    
    Parámetros:
      state: instancia de State (con state.box_positions, etc.).
      level_data: instancia de LevelData (que posee level_data.deadlocks y método is_deadlock).
    
    Retorna:
      float: 0 si no hay deadlock, o float('inf') si se detecta un deadlock.
    """
    for box in state.box_positions:
        # Si la caja ya está en meta, no la consideramos.
        if box in level_data.goals:
            continue
        # Si la posición de la caja está marcada como deadlock, penalizamos.
        if level_data.is_deadlock(box[0], box[1]):
            return float('inf')
    
    # Si ninguna caja problemática se detecta, no se añade costo extra.
    return 0
