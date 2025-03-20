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
        # e.g. if we want EXACT match:
        return self.box_positions == level_data.goals
        # or if you'd want a subset logic, 
        # you'd do self.box_positions.issubset(level_data.goals)

    def __eq__(self, other):
        """Two states are equal if they share player/boxes."""
        return (self.player_pos == other.player_pos and 
                self.box_positions == other.box_positions)

    def __hash__(self):
        """Hash for BFS/A* expansions."""
        return hash((self.player_pos, self.box_positions))

    def __repr__(self):
        return f"Player: {self.player_pos}, Boxes: {sorted(self.box_positions)}"
