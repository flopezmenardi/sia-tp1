# test.py

def print_map(level_data, state):
    """
    Print the Sokoban level to the console.

    Priority rules (simple):
      - If there's a wall (#), we display '#'
      - Else if it's the player's position, display '@'
      - Else if it's one of the box positions, display '$'
      - Else if it's a goal, display '.'
      - Else display ' ' (floor)

    NOTE: This does not visually distinguish a box or player on top of a goal.
    If you need that, you'll have to add checks for overlaps.
    """
    xs, ys = [], []
    
    # Collect all x,y coords from walls, goals, boxes, and the player
    for (wx, wy) in level_data.walls:
        xs.append(wx)
        ys.append(wy)
    for (gx, gy) in level_data.goals:
        xs.append(gx)
        ys.append(gy)
    for (bx, by) in state.box_positions:
        xs.append(bx)
        ys.append(by)
    px, py = state.player_pos
    xs.append(px)
    ys.append(py)

    # Determine bounding box
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    print()
    for y in range(min_y, max_y + 1):
        row_chars = []
        for x in range(min_x, max_x + 1):
            if (x, y) in level_data.walls:
                row_chars.append('#')
            elif (x, y) == state.player_pos:
                row_chars.append('@')
            elif (x, y) in state.box_positions:
                row_chars.append('$')
            elif (x, y) in level_data.goals:
                row_chars.append('.')
            else:
                row_chars.append(' ')
        print("".join(row_chars))
    print()

def main():
    print("=== Testing map_loader, sokoban_state, and level_data ===")

    # 1) Load the level and the initial state:
    from loaders.map_loader import load_sokoban_map
    level_data, initial_state = load_sokoban_map("maps/level1.txt")

    # 2) Print counts of walls, goals, and boxes:
    print("Number of walls:", len(level_data.walls))
    print("Number of goals:", len(level_data.goals))
    print("Number of boxes:", len(initial_state.box_positions))

    # 3) Print actual sets if desired:
    print("Walls loaded:", level_data.walls)
    print("Goals loaded:", level_data.goals)

    # 4) Display the initial state (player + boxes)
    print("Initial State:", initial_state)

    # 5) Check if the initial state is a goal:
    if initial_state.is_goal(level_data):
        print("The initial state is already at the goal.")
    else:
        print("Initial state is NOT a goal.")

    # 6) Print the map to visually confirm layout
    print("Here's the map with the initial state rendered:")
    print_map(level_data, initial_state)

    print("=== Test completed ===")

if __name__ == "__main__":
    main()
