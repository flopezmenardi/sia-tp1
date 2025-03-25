import heapq

def reconstruct_path(node):
    path = []
    while node.parent is not None:
        path.append(node.action)
        node = node.parent
    path.reverse()  # reverse to get path from initial state to goal
    return path

def greedy_search(initial_state, goal_test, actions_fn, level_data, heuristics_fn):
    """
    Greedy search that expands nodes in order of lowest composed heuristic.
    
    Parameters:
      - initial_state: The starting state.
      - goal_test: A function goal_test(state) -> bool.
      - actions_fn: A function actions_fn(state, level_data) -> list of (action, next_state).
      - level_data: Static data for the level (walls, goals, etc.).
      - heuristics_fn: A list of heuristic functions, each taking (state, level_data) and returning a float.
    
    Returns:
      - A list of actions from initial_state to goal, or None if no solution is found.
    """
    from nodes.greedy_node import GreedyNode

    # Calculate all heuristic values for the initial state.
    heuristic_values = [h(initial_state, level_data) for h in heuristics_fn]
    root_node = GreedyNode(state=initial_state, parent=None, action=None, heuristics=heuristic_values)
    
    if goal_test(root_node.state):
        return reconstruct_path(root_node)
    
    # Initialize a tie-breaker counter.
    counter = 0
    frontier = []
    heapq.heappush(frontier, (root_node.composed_heuristic, counter, root_node))
    counter += 1
    visited = set([root_node.state])
    
    while frontier:
        _, _, current_node = heapq.heappop(frontier)
        
        if goal_test(current_node.state):
            return reconstruct_path(current_node)
        
        # Expand children using actions_fn(state, level_data)
        for action, next_state in actions_fn(current_node.state, level_data):
            if next_state not in visited:
                visited.add(next_state)
                h_values = [h(next_state, level_data) for h in heuristics_fn]
                child_node = GreedyNode(state=next_state, parent=current_node, action=action, heuristics=h_values)
                heapq.heappush(frontier, (child_node.composed_heuristic, counter, child_node))
                counter += 1
                
    return None
