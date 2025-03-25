def manhattan_heuristic(state, level_data):
    """
    A* heuristic function for Sokoban

    h(n) = Sum of (each box's distance to its closest goal)
         + Distance from player to the nearest box.
    
    :param state: The current Sokoban state (player position, box positions)
    :param level_data: Static level data (walls, goals, precomputed distances)
    :return: Heuristic cost 
    """

    #calculate box-to-goal distance (sum over all boxes) 
    total_box_distance = 0
    
    for box in state.box_positions:
        # Find closest goal using precomputed distances
        closest_goal = min(level_data.goals, key=lambda goal: level_data.get_manhattan_distance(box, goal))
        total_box_distance += level_data.get_manhattan_distance(box, closest_goal)

    #calculate player-to-closest-box distance 
    if state.box_positions:
        closest_box = min(state.box_positions, key=lambda box: level_data.get_manhattan_distance(state.player_pos, box))
        player_to_box_distance = level_data.get_manhattan_distance(state.player_pos, closest_box)
    else:
        player_to_box_distance = 0  #case no boxes left

    #return the total heuristic sum
    return total_box_distance + player_to_box_distance