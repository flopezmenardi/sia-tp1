import pygame
import sys
import json
from algorithms.bfs import bfs_search
from algorithms.dfs import dfs_search
from algorithms.greedy import greedy_search
from algorithms.astar import a_star_search
from loaders.map_loader import load_sokoban_map
from states.level_data import LevelData
from states.sokoban_state import State, apply_move, get_possible_moves
from heuristics.manhattan import manhattan_heuristic

# Pygame setup
TILE_SIZE = 40  
WIDTH, HEIGHT = 800, 600  
FPS = 60

# White color for screen
WHITE = (255, 255, 255)

# Load configuration from JSON
def load_config(config_file):
    with open(config_file, "r") as file:
        return json.load(file)

# Select the search algorithm dynamically
def select_algorithm(name):
    algorithms = {
        "bfs": bfs_search,
        "dfs": dfs_search,
        "greedy": greedy_search,
        "astar": a_star_search
    }
    return algorithms.get(name.lower())

# Select heuristic function dynamically (if needed)
def select_heuristic(name):
    heuristics = {
        "manhattan": manhattan_heuristic
        # ,
        # "deadlocks": deadlocks_heuristic
    }
    return heuristics.get(name.lower())

# Function to visualize the level
def draw_level(screen, state, level_data, wall_img, box_img, goal_img, player_img):
    screen.fill(WHITE)  # Clear screen

    # Draw walls
    for x, y in level_data.walls:
        screen.blit(wall_img, (x * TILE_SIZE, y * TILE_SIZE))

    # Draw goals
    for x, y in level_data.goals:
        screen.blit(goal_img, (x * TILE_SIZE, y * TILE_SIZE))

    # Draw boxes
    for x, y in state.box_positions:
        screen.blit(box_img, (x * TILE_SIZE, y * TILE_SIZE))

    # Draw player
    px, py = state.player_pos
    screen.blit(player_img, (px * TILE_SIZE, py * TILE_SIZE))

    pygame.display.flip()  # Update screen

# Game loop
def run_game(config_path="config.json"):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sokoban Solver")
    clock = pygame.time.Clock()

    # Load assets
    wall_img = pygame.image.load("assets/wall.png").convert_alpha()
    wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))
    box_img = pygame.image.load("assets/box.png").convert_alpha()
    box_img = pygame.transform.scale(box_img, (TILE_SIZE, TILE_SIZE))
    goal_img = pygame.image.load("assets/goal.png").convert_alpha()
    goal_img = pygame.transform.scale(goal_img, (TILE_SIZE, TILE_SIZE))
    player_img = pygame.image.load("assets/player.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))

    # Load configuration
    config = load_config(config_path)
    level_number = config.get("level", 1)  #default to level 1 if not provided
    level_file = f"maps/level{level_number}.txt"
    algorithm_name = config.get("algorithm", "bfs") #default to BFS if not provided
    heuristic_name = config.get("heuristic", None)

    # Load level
    level_data, initial_state = load_sokoban_map(level_file)

    # Select search algorithm
    algorithm = select_algorithm(algorithm_name)
    if not algorithm:
        print(f"Error: Unknown algorithm '{algorithm_name}'")
        return

    # Select heuristic (if applicable)
    heuristic = select_heuristic(heuristic_name) if heuristic_name else None

    # Run selected algorithm
    if heuristic:
        # Ensure heuristic is always a list, even if only one is selected
        heuristics = heuristic if isinstance(heuristic, list) else [heuristic]
        solution = algorithm(initial_state, lambda s: s.is_goal(level_data), get_possible_moves, level_data, heuristics)
    else:
        solution = algorithm(initial_state, lambda s: s.is_goal(level_data), get_possible_moves, level_data)

    if solution is None:
        print("No solution found!")
        return

    print(f"Solution found in {len(solution)} steps: {solution}")

    # Game loop visualization
    current_state = initial_state
    running = True
    step = 0

    while running:
        clock.tick(FPS)  

        # Event handling 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if step < len(solution):
            action = solution[step]
            current_state = apply_move(current_state, action, level_data)
            draw_level(screen, current_state, level_data, wall_img, box_img, goal_img, player_img)
            pygame.time.delay(500)  # Delay for visualization
            step += 1
        else:
            pygame.time.delay(2000)  # Pause at the end
            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Must include config json file: python main.py <config_file>")
        sys.exit(1)

    config_path = sys.argv[1]  
    run_game(config_path)