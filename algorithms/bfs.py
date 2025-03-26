from collections import deque

def bfs_search(initial_state, goal_test, actions_fn, level_data):
    """
    :param initial_state: The starting state
    :param goal_test: A function goal_test(state) -> bool
    :param actions_fn: A function actions_fn(state) -> list of (action, next_state)
    :return: list of actions from initial_state to goal, or None if no solution
    """
    from nodes.bfs_node import BFSNode

    root_node = BFSNode(state=initial_state, parent=None, action=None, depth=0)
    
    if goal_test(root_node.state):
        return reconstruct_path(root_node), 1, 1 #immediate success

    frontier = deque([root_node])   # FIFO queue
    visited = set([root_node.state])  # track visited states to avoid repeats

    expanded_nodes = 0  # Tracks how many nodes we expand
    max_frontier_size = 1  # Tracks peak size of the frontier

    while frontier:
        current_node = frontier.popleft()
        expanded_nodes += 1  

        # Expand children
        for action, next_state in actions_fn(current_node.state, level_data):
            if next_state not in visited:
                visited.add(next_state)
                child_node = BFSNode(
                    state=next_state, 
                    parent=current_node, 
                    action=action, 
                    depth=current_node.depth + 1
                )
                if goal_test(child_node.state):
                    return reconstruct_path(child_node), expanded_nodes, len(frontier)
                frontier.append(child_node)
                max_frontier_size = max(max_frontier_size, len(frontier))
    # No solution found
    return None


def reconstruct_path(node):
    """
    Recovers the actions by walking parents up to the root.
    """
    actions = []
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    return list(reversed(actions))
