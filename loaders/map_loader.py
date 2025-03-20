# map_loader.py

def load_sokoban_map(file_path):
    """
    Reads a Sokoban level text file and returns:
      - level_data: a LevelData object holding static info (walls, goals).
      - initial_state: a State object for the player's starting position and box positions.

    Characters in the file:
      # : Wall
      . : Goal
      $ : Box
      @ : Player
      ' ' or other chars: Floor / empty space
    """

    walls = set()
    goals = set()
    boxes = set()
    player_pos = None

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # We'll treat row=Y, column=X, with (x=0, y=0) at top-left
    for y, line in enumerate(lines):
        line = line.rstrip('\n')
        for x, char in enumerate(line):
            if char == '#':
                walls.add((x, y))
            elif char == '.':
                goals.add((x, y))
            elif char == '$':
                boxes.add((x, y))
            elif char == '@':
                player_pos = (x, y)
            # if char == ' ' or any other, consider it empty floor

    # Import your classes from their respective modules
    from states.level_data import LevelData
    from states.sokoban_state import State

    # Create the static level data object
    level_data = LevelData(walls, goals)

    # Create the initial state with dynamic info (player, boxes)
    initial_state = State(player_pos, boxes)

    return level_data, initial_state
