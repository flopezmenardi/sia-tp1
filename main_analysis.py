import pygame
import sys
import json
import time

# Example placeholders for BFS, DFS, etc. 
# (Replace with your actual imports if needed)
from algorithms.bfs import bfs_search
from algorithms.dfs import dfs_search
from algorithms.greedy import greedy_search
from algorithms.astar import a_star_search

from loaders.map_loader import load_sokoban_map
from states.sokoban_state import apply_move, get_possible_moves
from heuristics.manhattan import manhattan_heuristic
from heuristics.deadlock import deadlock_heuristic
from heuristics.hungarian import hungarian_heuristic

# Height (in pixels) reserved at the top for stats
STATS_BAR_HEIGHT = 60  
FPS = 60
WHITE = (255, 255, 255)
BROWN = (164, 116, 73)

def select_algorithm(name):
    algorithms = {
        "bfs": bfs_search,
        "dfs": dfs_search,
        "greedy": greedy_search,
        "astar": a_star_search
    }
    return algorithms.get(name.lower())

def select_heuristic(name):
    heuristics = {
        "manhattan": manhattan_heuristic,
        "deadlock": deadlock_heuristic,
        "hungarian": hungarian_heuristic
    }
    return heuristics.get(name.lower())

def load_config(config_file):
    with open(config_file, "r") as file:
        return json.load(file)

def draw_stats(screen, font, line1_text, line2_text):
    """
    Draws two lines of stats at the top of the screen.
    line1_text, line2_text are strings to display.
    """
    # Clear the top bar (optional: fill a rectangle)
    pygame.draw.rect(screen, BROWN, (0, 0, screen.get_width(), STATS_BAR_HEIGHT))

    text_surface1 = font.render(line1_text, True, (0, 0, 0))
    text_surface2 = font.render(line2_text, True, (0, 0, 0))
    screen.blit(text_surface1, (10, 10))  # First line
    screen.blit(text_surface2, (10, 30))  # Second line

def draw_level(screen, state, level_data, images, tile_size, font, moves, pushes, algo_name, heur_names):
    """
    Draw the level below the stats bar. 
    Also draws the two lines of stats at the top.
    """
    # Fill entire screen
    screen.fill(WHITE)

    # Prepare stats lines
    boxes_on_goals = sum(1 for b in state.box_positions if b in level_data.goals)
    total_goals = len(level_data.goals)
    line1 = f"Moves: {moves}  Pushes: {pushes}  Boxes: {boxes_on_goals}/{total_goals}"
    if heur_names:
        heur_text = ", ".join(h.upper() for h in heur_names)
    else:
        heur_text = "None"
    line2 = f"Algorithm: {algo_name.upper()}  |  Heuristics: {heur_text}"

    # Draw the two lines at top
    draw_stats(screen, font, line1, line2)

    # Now draw the map offset by STATS_BAR_HEIGHT
    offset_y = STATS_BAR_HEIGHT

    # Draw walls
    for x, y in level_data.walls:
        screen.blit(images["wall"], (x * tile_size, y * tile_size + offset_y))

    # Draw goals
    for x, y in level_data.goals:
        screen.blit(images["goal"], (x * tile_size, y * tile_size + offset_y))

    # Draw boxes
    for x, y in state.box_positions:
        screen.blit(images["box"], (x * tile_size, y * tile_size + offset_y))

    # Draw player
    px, py = state.player_pos
    screen.blit(images["player"], (px * tile_size, py * tile_size + offset_y))

    pygame.display.update()

def run_game(config, simulate=False):
    """
    Runs the Sokoban solver based on the provided configuration.

    Args:
        config (dict): Configuration dictionary with keys:
            - level (int): The level number to load.
            - algorithm (str): The algorithm to use (e.g., "astar", "bfs").
            - heuristics (list of str): List of heuristic names (optional).
        simulate (bool): Whether to run the graphical simulation.

    Returns:
        tuple: (solution, expanded_nodes, frontier_size, processing_time)
    """
    # Extract configuration values
    level_number = config["level"]
    algo_name = config["algorithm"]
    heuristics = config.get("heuristics", [])  # Default to an empty list if not provided

    # Load the level file
    level_file = f"maps/level{level_number}.txt"
    level_data, initial_state = load_sokoban_map(level_file)

    # Select algorithm
    algorithm = select_algorithm(algo_name)
    if not algorithm:
        print(f"Unknown algorithm '{algo_name}'")
        return None, None, None, None

    # Prepare heuristics
    heuristic_functions = [select_heuristic(h) for h in heuristics if select_heuristic(h)]

    # Track execution time
    start_time = time.time()
    if heuristic_functions:
        solution, expanded_nodes, frontier_size = algorithm(
            initial_state, lambda s: s.is_goal(level_data), get_possible_moves, level_data, heuristic_functions
        )
    else:
        solution, expanded_nodes, frontier_size = algorithm(
            initial_state, lambda s: s.is_goal(level_data), get_possible_moves, level_data
        )
    end_time = time.time()
    processing_time = end_time - start_time

    if solution is None:
        print("❌ No solution found!")
        return None, expanded_nodes, frontier_size, processing_time
    else:
        print("✅ Solution found!")
        print(f"🔹 Cost of Solution: {len(solution)} steps")
        print(f"🔹 Nodes Expanded: {expanded_nodes}")
        print(f"🔹 Nodes in Frontier: {frontier_size}")
        print(f"🔹 Processing Time: {processing_time:.4f} seconds")
        print(f"🔹 Solution Path: {solution}")

    # Skip graphical simulation if simulate=False
    if not simulate:
        return solution, expanded_nodes, frontier_size, processing_time

    # Graphical simulation setup
    pygame.init()
    pygame.font.init()

    tile_size = 40
    map_pixel_width = level_data.width * tile_size
    map_pixel_height = level_data.height * tile_size
    window_width = map_pixel_width
    window_height = map_pixel_height + STATS_BAR_HEIGHT

    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Sokoban Solver (Dynamic)")

    # Load images
    wall_img = pygame.image.load("assets/wall.png").convert_alpha()
    wall_img = pygame.transform.scale(wall_img, (tile_size, tile_size))
    box_img = pygame.image.load("assets/box.png").convert_alpha()
    box_img = pygame.transform.scale(box_img, (tile_size, tile_size))
    goal_img = pygame.image.load("assets/goal.png").convert_alpha()
    goal_img = pygame.transform.scale(goal_img, (tile_size, tile_size))
    player_img = pygame.image.load("assets/player.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (tile_size, tile_size))

    images = {
        "wall": wall_img,
        "box": box_img,
        "goal": goal_img,
        "player": player_img
    }

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)

    moves = 0
    pushes = 0
    current_state = initial_state
    step = 0
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if step < len(solution):
            action = solution[step]
            # Check if push
            old_boxes = current_state.box_positions
            new_state = apply_move(current_state, action, level_data)
            if new_state.box_positions != old_boxes:
                pushes += 1
            moves += 1

            current_state = new_state
            draw_level(screen, current_state, level_data, images, tile_size, font, moves, pushes, algo_name, heuristics)
            pygame.time.delay(500)
            step += 1
        else:
            pygame.time.delay(2000)
            running = False

    pygame.quit()
    return solution, expanded_nodes, frontier_size, processing_time

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <config_file>")
        sys.exit(1)

    config_path = sys.argv[1]
    run_game(config_path)
