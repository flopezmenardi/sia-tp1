class State:
    def __init__(self, player_pos, box_positions, goal_positions, walls):
        self.player_pos = player_pos  # (x, y)
        self.box_positions = frozenset(box_positions)  # Immutable for hashing
        self.goal_positions = frozenset(goal_positions)  # Immutable for quick lookup
        self.walls = frozenset(walls)  # Immutable for efficiency

    def is_goal(self):
        """Returns True if all boxes are on goal positions."""
        return self.box_positions == self.goal_positions

    def __eq__(self, other):
        """States are equal if the player and all boxes are in the same position."""
        return (self.player_pos == other.player_pos and 
                self.box_positions == other.box_positions)

    def __hash__(self):
        """Hash state for use in sets/dictionaries (important for BFS, A*)."""
        return hash((self.player_pos, self.box_positions))

    def __repr__(self):
        """Return a string representation of the state (for debugging)."""
        return f"Player: {self.player_pos}, Boxes: {self.box_positions}"