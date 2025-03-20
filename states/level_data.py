# level_data.py (just an example filename)

class LevelData:
    """
    Contains static data about the Sokoban level:
      - walls: set/frozenset of (x, y) for walls
      - goals: set/frozenset of (x, y) for goal positions
    Possibly other attributes like width, height, etc.
    """
    def __init__(self, walls, goals):
        self.walls = frozenset(walls)
        self.goals = frozenset(goals)

    def is_wall(self, x, y):
        return (x, y) in self.walls

    def is_goal(self, x, y):
        return (x, y) in self.goals

    # if you like, you can add extra helper methods here
