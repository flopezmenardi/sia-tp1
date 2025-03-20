# state.py

class State:
    def __init__(self, player_pos, box_positions):
        """
        We no longer store walls/goals in the state.
        They remain in a global or external structure.
        """
        self.player_pos = player_pos  # (x, y)
        self.box_positions = frozenset(box_positions)  # Must be immutable for hashing

    def is_goal(self, level_data):
        """
        Check if all boxes are on goal positions, 
        referencing the external 'level_data' for the goals.
        """
        # if we want EXACT match:
        return self.box_positions == level_data.goals
        # if we want a subset logic do: self.box_positions.issubset(level_data.goals)

    def __eq__(self, other):
        """Two states are equal if they share player/boxes."""
        return (self.player_pos == other.player_pos and 
                self.box_positions == other.box_positions)

    def __hash__(self):
        """Hash for BFS/A* expansions."""
        return hash((self.player_pos, self.box_positions))

    def __repr__(self):
        return f"Player: {self.player_pos}, Boxes: {sorted(self.box_positions)}"

def apply_move(state, action, level_data):
    """Applies an action and returns a new state."""
    px, py = state.player_pos
    new_px, new_py = px, py

    if action == "UP":
        new_py -= 1
    elif action == "DOWN":
        new_py += 1
    elif action == "LEFT":
        new_px -= 1
    elif action == "RIGHT":
        new_px += 1

    # Check if the new position is a wall
    if (new_px, new_py) in level_data.walls:
        return state  # If it's a wall, cancel the move

    # Check if the player is pushing a box
    new_box_positions = set(state.box_positions)
    if (new_px, new_py) in state.box_positions:
        # Calculate new box position
        new_bx, new_by = new_px + (new_px - px), new_py + (new_py - py)

        # If the new box position is invalid, cancel the move
        if (new_bx, new_by) in level_data.walls or (new_bx, new_by) in state.box_positions:
            return state

        # Move the box
        new_box_positions.remove((new_px, new_py))
        new_box_positions.add((new_bx, new_by))

    return State((new_px, new_py), new_box_positions)

def get_possible_moves(state, level_data):
    """
    Generates all valid moves from the current state.
    Returns a list of (action, new_state) pairs.
    """
    possible_moves = []
    px, py = state.player_pos  # Current player position

    # Directions the player can move: (dx, dy, action)
    directions = [
        (0, -1, "UP"),
        (0, 1, "DOWN"),
        (-1, 0, "LEFT"),
        (1, 0, "RIGHT")
    ]

    for dx, dy, action in directions:
        new_px, new_py = px + dx, py + dy  # New player position

        # If the new position is a wall, skip it
        if (new_px, new_py) in level_data.walls:
            continue  

        # If there's a box at the new position, check if it can be pushed
        new_box_positions = set(state.box_positions)
        if (new_px, new_py) in state.box_positions:
            new_bx, new_by = new_px + dx, new_py + dy  # New box position

            # If the box would be pushed into a wall or another box, skip
            if (new_bx, new_by) in level_data.walls or (new_bx, new_by) in state.box_positions:
                continue

            # Move the box
            new_box_positions.remove((new_px, new_py))
            new_box_positions.add((new_bx, new_by))

        # If valid, add to possible moves
        new_state = State((new_px, new_py), new_box_positions)
        possible_moves.append((action, new_state))

    return possible_moves