import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

from loaders.map_loader import load_sokoban_map
from states.sokoban_state import apply_move, get_possible_moves
from algorithms.bfs import bfs_search
from algorithms.dfs import dfs_search
from algorithms.greedy import greedy_search
from algorithms.astar import a_star_search
from heuristics.manhattan import manhattan_heuristic
from heuristics.deadlock import deadlock_heuristic
from heuristics.hungarian import hungarian_heuristic

def select_algorithm(name):
    return {
        "bfs": bfs_search,
        "dfs": dfs_search,
        "greedy": greedy_search,
        "astar": a_star_search
    }.get(name.lower())

def select_heuristic(name):
    return {
        "manhattan": manhattan_heuristic,
        "deadlock": deadlock_heuristic,
        "hungarian": hungarian_heuristic
    }.get(name.lower())

def run_trial(algorithm, level_data, initial_state, heuristics):
    start_time = time.time()
    if heuristics:
        solution, expanded_nodes, frontier_size = algorithm(
            initial_state,
            lambda s: s.is_goal(level_data),
            get_possible_moves,
            level_data,
            heuristics
        )
    else:
        solution, expanded_nodes, frontier_size = algorithm(
            initial_state,
            lambda s: s.is_goal(level_data),
            get_possible_moves,
            level_data
        )
    end_time = time.time()
    exec_time = end_time - start_time

    # Simulate the solution to count moves and pushes.
    moves = 0
    pushes = 0
    current_state = initial_state
    for action in solution:
        old_boxes = current_state.box_positions
        new_state = apply_move(current_state, action, level_data)
        # If the box positions have changed, it was a push.
        if new_state.box_positions != old_boxes:
            pushes += 1
        moves += 1
        current_state = new_state

    return solution, exec_time, expanded_nodes, frontier_size, moves, pushes

def main(config_file):
    with open(config_file, "r") as file:
        config = json.load(file)

    level_number = config["level"]
    algorithm_name = config["algorithm"]
    heuristics_list = config["heuristics"]

    # Load level (map_data and initial state)
    level_data, initial_state = load_sokoban_map(f"maps/level{level_number}.txt")
    algorithm = select_algorithm(algorithm_name)
    if not algorithm:
        print(f"Invalid algorithm: {algorithm_name}")
        sys.exit(1)

    results = []
    for heuristics in heuristics_list:
        # Build a list of heuristic functions and a display name.
        heuristic_funcs = [select_heuristic(h) for h in heuristics]
        heuristic_names = ", ".join(heuristics)

        # Run a single trial for this heuristic configuration.
        solution, exec_time, expanded_nodes, frontier_size, moves, pushes = run_trial(
            algorithm, level_data, initial_state, heuristic_funcs
        )

        results.append({
            "heuristic": heuristic_names,
            "exec_time": exec_time,
            "expanded_nodes": expanded_nodes,
            "frontier_size": frontier_size,
            "moves": moves,
            "pushes": pushes,
            "solution_length": len(solution)
        })

    df = pd.DataFrame(results)

    # Print Execution Summary
    print("\n=== Execution Summary ===")
    print(df.to_string(index=False))

    # Generate Execution Time Chart
    plt.figure(figsize=(10, 6))
    plt.bar(df["heuristic"], df["exec_time"], color="skyblue")
    plt.xlabel("Heuristic")
    plt.ylabel("Execution Time (s)")
    plt.title(f"Execution Time of {algorithm_name.upper()} with Different Heuristics (Level {level_number})")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    plt.close()

    # Generate Moves and Pushes Chart
    bar_width = 0.35
    x = np.arange(len(df))
    plt.figure(figsize=(10, 6))
    plt.bar(x, df["moves"], width=bar_width, label="Moves", color="lightgreen")
    plt.bar(x + bar_width, df["pushes"], width=bar_width, label="Pushes", color="salmon")
    plt.xlabel("Heuristic")
    plt.ylabel("Count")
    plt.title(f"Moves and Pushes for {algorithm_name.upper()} with Different Heuristics (Level {level_number})")
    plt.xticks(x + bar_width / 2, df["heuristic"], rotation=45)
    plt.legend()
    max_val = max(df["moves"].max(), df["pushes"].max())
    plt.ylim(0, max_val * 1.1)
    plt.tight_layout()
    plt.show()
    plt.close()

    # Generate Expanded Nodes Chart
    plt.figure(figsize=(10, 6))
    plt.bar(df["heuristic"], df["expanded_nodes"], color="mediumpurple")
    plt.xlabel("Heuristic")
    plt.ylabel("Expanded Nodes")
    plt.title(f"Expanded Nodes for {algorithm_name.upper()} with Different Heuristics (Level {level_number})")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    plt.close()

    # Generate Frontier Size Chart
    plt.figure(figsize=(10, 6))
    plt.bar(df["heuristic"], df["frontier_size"], color="tomato")
    plt.xlabel("Heuristic")
    plt.ylabel("Frontier Size")
    plt.title(f"Frontier Size for {algorithm_name.upper()} with Different Heuristics (Level {level_number})")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compare_heuristics.py <config_file>")
        sys.exit(1)
    main(sys.argv[1])