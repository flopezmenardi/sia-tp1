def reconstruct_path(node):
    path = []
    while node.parent is not None:
        path.append(node.action)
        node = node.parent
    path.reverse()  # reverse to get path from initial state to goal
    return path

def dfs_search(initial_state, goal_test, actions_fn, level_data):
    """
    :param initial_state: starting state
    :param goal_test: function to check if a state is goal
    :param actions_fn: function returning (action, next_state) from a state
    :param max_depth: if you want to limit the depth (optional)
    :return: list of actions or None if no solution
    """
    from nodes.dfs_node import DFSNode

    root_node = DFSNode(state=initial_state, parent=None, action=None, depth=0)
    
    if goal_test(root_node.state):
        return reconstruct_path(root_node)

    stack = [root_node]
    visited = set([root_node.state])

    while stack:
        current_node = stack.pop()
        # If we have a limit, skip expanding if we reached max_depth
        # if max_depth is not None and current_node.depth >= max_depth:
        #    continue
        
        for action, next_state in actions_fn(current_node.state, level_data):
            if next_state not in visited:
                visited.add(next_state)
                child_node = DFSNode(
                    state=next_state,
                    parent=current_node,
                    action=action,
                    depth=current_node.depth + 1
                )
                if goal_test(child_node.state):
                    return reconstruct_path(child_node)
                stack.append(child_node)
                
    return None
