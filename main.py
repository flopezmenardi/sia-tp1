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
def draw_level(screen, state, level_data, wall_img, box_img, goal_img, player_img):
    screen.fill((255, 255, 255))  # Clear the screen

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
def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sokoban - BFS Solver")
    clock = pygame.time.Clock()

    wall_img = pygame.image.load("assets/wall.png")
    wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))

    box_img = pygame.image.load("assets/box.png")
    box_img = pygame.transform.scale(box_img, (TILE_SIZE, TILE_SIZE))

    goal_img = pygame.image.load("assets/goal.png")
    goal_img = pygame.transform.scale(goal_img, (TILE_SIZE, TILE_SIZE))

    player_img = pygame.image.load("assets/player.png")
    player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))

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
            draw_level(screen, current_state, level_data, wall_img, box_img, goal_img, player_img)
            pygame.time.delay(500)  # Delay for visualization
            step += 1
        else:
            pygame.time.delay(2000)  # Pause at the end
            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()