# level_data.py (just an example filename)

class LevelData:
    """
    Contains static data about the Sokoban level:
      - walls: set/frozenset of (x, y) for walls
      - goals: set/frozenset of (x, y) for goal positions
      - deadlocks: frozenset of positions where a box cannot be moved to a goal
      - manhattan distances: dict for quick distance lookup
    Possibly other attributes like width, height, etc.
    """
    def __init__(self, walls, goals):
        self.walls = frozenset(walls)
        self.goals = frozenset(goals)
        self.width = max(x for x, y in walls) + 1
        self.height = max(y for x, y in walls) + 1

        #precompute useful data
        self.deadlocks = self._compute_deadlocks()
        self.manhattan_distances = self._precompute_manhattan_distances()

    def is_wall(self, x, y):
        return (x, y) in self.walls

    def is_goal(self, x, y):
        return (x, y) in self.goals

    def is_deadlock(self, x, y):
        return (x, y) in self.deadlocks

    def get_manhattan_distance(self, pos1, pos2):
        return self.manhattan_distances.get((pos1, pos2), float('inf'))

    
    # --- PRECOMPUTATION FUNCTIONS ---
    def _compute_deadlocks(self):
        """
        Find positions where a box can never reach a goal
        Examples: in a corner that isn't a goal, against two walls with no opening on other side, or in a U-shaped wall (no matter how wide)
        """
        deadlocks = set()

        for x, y in product(range(self.width), range(self.height)):
            if self.is_wall(x, y) or self.is_goal(x, y):
                continue  #ignore walls and goals

            ####### CASE 1: Corner Deadlocks #######
            if ((self.is_wall(x - 1, y) and self.is_wall(x, y - 1)) or
                (self.is_wall(x + 1, y) and self.is_wall(x, y - 1)) or
                (self.is_wall(x - 1, y) and self.is_wall(x, y + 1)) or
                (self.is_wall(x + 1, y) and self.is_wall(x, y + 1))):
                deadlocks.add((x, y))
                continue  #skip to next position

            ####### CASE 2: U-Shaped Deadlocks (trapped against a wall between 2 others) #######
            #check left/right (horizontal U-shape)
            if (self.is_wall(x - 1, y) and self.is_wall(x + 1, y)):  
                #check if goal is in this row
                if not any(self.is_goal(gx, y) for gx in range(self.width)):
                    deadlocks.add((x, y))
            
            #check up/down (vertical U-shape)
            elif (self.is_wall(x, y - 1) and self.is_wall(x, y + 1)):  
                #check if goal is in this column
                if not any(self.is_goal(x, gy) for gy in range(self.height)):
                    deadlocks.add((x, y))

        return frozenset(deadlocks)

    def _precompute_manhattan_distances(self):
        """
        Precompute Manhattan distances for all pairs of (x, y) positions.
        This speeds up heuristic calculations.
        """
        distances = {}
        all_positions = product(range(self.width), range(self.height))

        for (x1, y1), (x2, y2) in product(all_positions, repeat=2):
            distances[((x1, y1), (x2, y2))] = abs(x1 - x2) + abs(y1 - y2)

        return distances
