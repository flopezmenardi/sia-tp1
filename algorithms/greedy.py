import heapq

def greedy_search(initial_state, goal_test, actions_fn, heuristic_fn):
    """
    Greedy search that expands nodes in order of lowest heuristic.
    :param initial_state: The starting state
    :param goal_test: A function goal_test(state) -> bool
    :param actions_fn: A function actions_fn(state) -> list of (action, next_state)
    :param heuristic_fn: h(n), returning a float for a given state
    :return: list of actions from initial_state to goal or None
    """
    from nodes.greedy_node import GreedyNode

    root_node = GreedyNode(
        state=initial_state,
        parent=None,
        action=None,
        heuristic=heuristic_fn(initial_state)
    )
    
    if goal_test(root_node.state):
        return reconstruct_path(root_node)

    # Priority queue, prioritizing by node.heuristic
    frontier = []
    heapq.heappush(frontier, (root_node.heuristic, root_node))
    
    visited = set([root_node.state])

    while frontier:
        _, current_node = heapq.heappop(frontier)

        # Check goal
        if goal_test(current_node.state):
            return reconstruct_path(current_node)
        
        # Expand children
        for action, next_state in actions_fn(current_node.state):
            if next_state not in visited:
                visited.add(next_state)
                h_value = heuristic_fn(next_state)
                child_node = GreedyNode(
                    state=next_state,
                    parent=current_node,
                    action=action,
                    heuristic=h_value
                )
                heapq.heappush(frontier, (child_node.heuristic, child_node))

    return None
