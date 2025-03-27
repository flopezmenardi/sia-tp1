# euclidean.py

import math

def euclidean_heuristic(state, level_data):
    """
    Euclidean heuristic function for Sokoban.

    h(n) = [ Sum of (each box's Euclidean distance to its closest goal)
         + Euclidean distance from the player to the nearest box ] / 2
    
    This heuristic is admissible because dividing by 2 prevents overestimation.
    For example, in a case where the last box is adjacent to the last goal with the player 
    behind it, the raw Euclidean distance might be 2, but the real cost is 1.

    Parameters:
      - state: An instance of the State class, which has:
          - state.player_pos: tuple (x, y)
          - state.box_positions: an iterable (e.g., frozenset) of (x, y) positions
      - level_data: An instance of LevelData, which has:
          - level_data.goals: an iterable (e.g., frozenset) of (x, y) positions

    Returns:
      - float: The computed heuristic cost.
    """
    total_box_distance = 0.0
    for box in state.box_positions:
        # Compute Euclidean distance from the box to the closest goal.
        closest_goal_distance = min(
            math.hypot(box[0] - goal[0], box[1] - goal[1])
            for goal in level_data.goals
        )
        total_box_distance += closest_goal_distance

    # Compute the Euclidean distance from the player to the nearest box.
    if state.box_positions:
        player_to_box_distance = min(
            math.hypot(state.player_pos[0] - box[0], state.player_pos[1] - box[1])
            for box in state.box_positions
        )
    else:
        player_to_box_distance = 0.0

    return (total_box_distance + player_to_box_distance) / 2.0