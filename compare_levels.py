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
        if new_state.box_positions != old_boxes:
            pushes += 1
        moves += 1
        current_state = new_state

    # Note: We're not including the actual solution in the results.
    return {
        "exec_time": exec_time,
        "expanded_nodes": expanded_nodes,
        "frontier_size": frontier_size,
        "moves": moves,
        "pushes": pushes,
        "solution_length": len(solution)
    }

def main(config_file):
    with open(config_file, "r") as file:
        config = json.load(file)

    level_numbers = config["levels"]
    algorithm_name = config["algorithm"]
    heuristics_list = config["heuristics"]  # Expects an array of heuristic names

    # Build the list of heuristic functions (same for all levels)
    heuristic_funcs = [select_heuristic(h) for h in heuristics_list]
    heuristic_display = ", ".join(heuristics_list)

    algorithm = select_algorithm(algorithm_name)
    if not algorithm:
        print(f"Invalid algorithm: {algorithm_name}")
        sys.exit(1)

    results = []
    for level in level_numbers:
        map_file = f"maps/level{level}.txt"
        print(f"Running level {level} using {algorithm_name.upper()} with heuristics [{heuristic_display}]...")
        level_data, initial_state = load_sokoban_map(map_file)
        metrics = run_trial(algorithm, level_data, initial_state, heuristic_funcs)
        metrics["level"] = level
        results.append(metrics)

    df = pd.DataFrame(results)
    # Remove the solution column if it exists (we don't need to compare the actual path)
    if "solution" in df.columns:
        df.drop(columns=["solution"], inplace=True)

    print("\n=== Execution Summary ===")
    print(df.to_string(index=False))

    # Define which metrics to plot (separate figures for each)
    metrics_to_plot = {
        "Execution Time (s)": "exec_time",
        "Nodes Expanded": "expanded_nodes",
        "Frontier Size": "frontier_size",
        "Solution Length": "solution_length",
        "Moves": "moves",
        "Pushes": "pushes"
    }

    # For each metric, create a separate figure window.
    for title, col in metrics_to_plot.items():
        plt.figure(figsize=(8, 6))
        plt.bar(df["level"].astype(str), df[col], color="skyblue")
        plt.xlabel("Level")
        plt.ylabel(title)
        plt.title(f"{title} per Level")
        # Adjust y-axis to 110% of the maximum value.
        max_val = df[col].max()
        plt.ylim(0, max_val * 1.1)
        plt.tight_layout()
        plt.show()
        plt.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compare_levels.py <config_file>")
        sys.exit(1)
    main(sys.argv[1])