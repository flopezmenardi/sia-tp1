# map_loader.py
import re

def load_sokoban_map(file_path):
    """
    Reads a Sokoban level text file and returns:
      - level_data: a LevelData object holding static info (walls, goals, etc.)
      - initial_state: a State object for the player's starting position and box positions

    Characters in the file:
      '#' : Wall
      '.' : Goal
      '$' : Box
      '@' : Player
      (any other character, including space): Floor / empty space

    This function supports non-rectangular maps by:
      1. Replacing leading spaces with '#' (filling left gaps),
      2. Padding each line on the right with '#' to reach the maximum line length,
      3. Ensuring that the first and last rows are completely filled with walls.
    """

    walls = set()
    goals = set()
    boxes = set()
    player_pos = None

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Remove newline characters.
    stripped_lines = [line.rstrip('\n') for line in lines]
    # Determine the maximum line length.
    max_length = max(len(line) for line in stripped_lines)

    padded_lines = []
    for line in stripped_lines:
        # Replace any leading whitespace with '#' characters.
        # This uses a regex to substitute the leading whitespace (if any) with an equal number of '#' characters.
        new_line = re.sub(r'^\s+', lambda m: '#' * len(m.group()), line)
        # Right-pad the line with '#' to reach max_length.
        padded_line = new_line.ljust(max_length, '#')
        padded_lines.append(padded_line)

    # Ensure the first and last rows are full walls.
    border_row = '#' * max_length
    if any(ch != '#' for ch in padded_lines[0]):
        padded_lines.insert(0, border_row)
    if any(ch != '#' for ch in padded_lines[-1]):
        padded_lines.append(border_row)

    # Log the final padded map.
    print("Loaded map:")
    for line in padded_lines:
        print(line)

    # Build the level information.
    for y, line in enumerate(padded_lines):
        for x, char in enumerate(line):
            if char == '#':
                walls.add((x, y))
            elif char == '.':
                goals.add((x, y))
            elif char == '$':
                boxes.add((x, y))
            elif char == '*': 
                goals.add((x, y)) 
                boxes.add((x, y))  
            elif char == '@':
                player_pos = (x, y)
            # All other characters are considered floor.

    # Import your LevelData and State classes.
    from states.level_data import LevelData
    from states.sokoban_state import State

    level_data = LevelData(walls, goals)
    initial_state = State(player_pos, boxes)

    return level_data, initial_state