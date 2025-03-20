import pygame
import sys
from algorithms.bfs import bfs_search
from loaders.map_loader import load_sokoban_map
from states.level_data import LevelData
from states.sokoban_state import State, apply_move, get_possible_moves

# Pygame setup
TILE_SIZE = 40  
WIDTH, HEIGHT = 800, 600  
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (165, 42, 42)

# Function to visualize the level
def draw_level(screen, level_data, state):
    """Draws the Sokoban level in Pygame."""
    screen.fill(WHITE)

    # Draw walls from level_data
    for x, y in level_data.walls:
        pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw goal positions from level_data
    for x, y in level_data.goals:
        pygame.draw.rect(screen, BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw boxes from the current state
    for x, y in state.box_positions:
        pygame.draw.rect(screen, BROWN, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw player
    px, py = state.player_pos
    pygame.draw.circle(screen, GREEN, (px * TILE_SIZE + TILE_SIZE // 2, py * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)

    pygame.display.flip()

# Game loop
def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sokoban - BFS Solver")
    clock = pygame.time.Clock()

    # Load the level and initial state
    level_data, initial_state = load_sokoban_map("maps/level1.txt")

    # Run BFS
    solution = bfs_search(initial_state, lambda s: s.is_goal(level_data), get_possible_moves, level_data)

    if solution is None:
        print("No solution found!")
        return

    print(f"Solution found in {len(solution)} steps: {solution}")

    # Game loop
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
            current_state = apply_move(current_state, action, level_data)  # Pass level_data
            draw_level(screen, level_data, current_state)
            pygame.time.delay(500)  # Delay for visualization
            step += 1
        else:
            pygame.time.delay(2000)  # Pause at the end
            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()