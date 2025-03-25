import heapq

def cost_fn(state, action):
    return 1  #uniform cost for every move

def a_star_search(initial_state, goal_test, actions_fn, level_data, heuristic_fn):
    """
    :param initial_state: The starting state
    :param goal_test: goal_test(state) -> bool
    :param actions_fn: returns (action, next_state) list
    :param cost_fn: cost_fn(state, action) -> float
    :param heuristic_fn: heuristic_fn(state) -> float
    :return: list of actions from initial_state to goal or None
    """
    from nodes.astar_node import AStarNode

    # Construct initial node
    root_node = AStarNode(
        state=initial_state,
        parent=None,
        action=None,
        cost_so_far=0.0,
        heuristics=heuristic_fn(initial_state, level_data)
    )
    
    if goal_test(root_node.state):
        return reconstruct_path(root_node)
    
    # Priority queue ordered by f(n) = g(n) + h(n)
    frontier = []
    heapq.heappush(frontier, (root_node.f, root_node))
    
    visited = dict()  
    # Instead of a set, sometimes we keep a dict mapping:
    #   visited[state] = best_cost_so_far
    # So we can do "if next_state not in visited or new_g < visited[next_state]" checks.

    visited[root_node.state] = root_node.cost_so_far

    while frontier:
        _, current_node = heapq.heappop(frontier)

        if goal_test(current_node.state):
            return reconstruct_path(current_node)

        # Expand children
        for action, next_state in actions_fn(current_node.state):
            new_g = current_node.cost_so_far + cost_fn(current_node.state, action)
            # If next_state is new or can be reached cheaper, then push new child
            if (next_state not in visited) or (new_g < visited[next_state]):
                visited[next_state] = new_g
                h_value = heuristic_fn(next_state)
                child_node = AStarNode(
                    state=next_state,
                    parent=current_node,
                    action=action,
                    cost_so_far=new_g,
                    heuristic=h_value
                )
                heapq.heappush(frontier, (child_node.f, child_node))

    return None
