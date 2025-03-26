import heapq

def cost_fn(state, action):
    return 1  #uniform cost for every move

def reconstruct_path(node):
    path = []
    while node.parent is not None:
        path.append(node.action)
        node = node.parent
    path.reverse()  # reverse to get path from initial state to goal
    return path

def a_star_search(initial_state, goal_test, actions_fn, level_data, heuristics_fn):
    """
    :param initial_state: The starting state
    :param goal_test: goal_test(state) -> bool
    :param actions_fn: returns (action, next_state) list
    :param cost_fn: cost_fn(state, action) -> float
    :param heuristics_fn: list of heuristic_fn(state) -> float
    :return: list of actions from initial_state to goal or None
    """
    from nodes.astar_node import AStarNode

    #sum of all heuristic functions' results
    heuristic_values = [h(initial_state, level_data) for h in heuristics_fn]

    #construct initial node
    root_node = AStarNode(
        state=initial_state,
        parent=None,
        action=None,
        cost_so_far=0.0,
        heuristics=heuristic_values
    )
    
    if goal_test(root_node.state):
        return reconstruct_path(root_node)
    
    #priority queue ordered by f(n) = g(n) + h(n) -- comparison by f(n) defined in AStarNode
    frontier = []
    heapq.heappush(frontier, (root_node.f, root_node))
    
    visited = dict()  
    visited[root_node.state] = root_node.cost_so_far

    expanded_nodes = 0
    max_frontier_size = 1

    while frontier:
        _, current_node = heapq.heappop(frontier)
        expanded_nodes += 1

        if goal_test(current_node.state):
            return reconstruct_path(current_node), expanded_nodes, max_frontier_size

        #expand children
        for action, next_state in actions_fn(current_node.state, level_data):
            new_g = current_node.cost_so_far + cost_fn(current_node.state, action)
            #if next_state is new or can be reached cheaper, then push new child
            if (next_state not in visited) or (new_g < visited[next_state]):
                visited[next_state] = new_g
                h_values = [h(next_state, level_data) for h in heuristics_fn]  #apply all heuristics
                child_node = AStarNode(
                    state=next_state,
                    parent=current_node,
                    action=action,
                    cost_so_far=new_g,
                    heuristics=h_values
                )
                heapq.heappush(frontier, (child_node.f, child_node))
        max_frontier_size = max(max_frontier_size, len(frontier))

    return None, expanded_nodes, max_frontier_size
