import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

from loaders.map_loader import load_sokoban_map
from states.sokoban_state import get_possible_moves
from algorithms.bfs import bfs_search
from algorithms.astar import a_star_search
from heuristics.manhattan import manhattan_heuristic
from heuristics.deadlock import deadlock_heuristic
from heuristics.hungarian import hungarian_heuristic

# Algorithm selection function
def select_algorithm(name):
    return {
        "bfs": bfs_search,
        "astar": a_star_search
    }.get(name.lower())

# Heuristic selection function
def select_heuristic(name):
    return {
        "manhattan": manhattan_heuristic,
        "deadlock": deadlock_heuristic,
        "hungarian": hungarian_heuristic
    }.get(name.lower())

def run_trials(algorithm_name, algorithm, level_data, initial_state, heuristics, num_trials=100):
    execution_times = []
    
    # Run multiple trials for execution time measurement
    for _ in range(num_trials):
        start_time = time.time()
        
        if algorithm_name == "astar":
            solution, expanded_nodes, _ = algorithm(initial_state, lambda s: s.is_goal(level_data), get_possible_moves, level_data, heuristics)
        else:  # BFS does not use heuristics
            solution, expanded_nodes, _ = algorithm(initial_state, lambda s: s.is_goal(level_data), get_possible_moves, level_data)

        end_time = time.time()
        execution_times.append(end_time - start_time)

    # Run a single execution to measure node expansion (since BFS is deterministic)
    if algorithm_name == "astar":
        _, expanded_nodes, _ = algorithm(initial_state, lambda s: s.is_goal(level_data), get_possible_moves, level_data, heuristics)
    else:
        _, expanded_nodes, _ = algorithm(initial_state, lambda s: s.is_goal(level_data), get_possible_moves, level_data)

    return np.mean(execution_times), np.std(execution_times), expanded_nodes

def main(config_file):
    with open(config_file, "r") as file:
        config = json.load(file)

    level_number = config["level"]
    algorithms_list = config["algorithms"]
    heuristics_list = config["heuristics"]

    level_data, initial_state = load_sokoban_map(f"maps/level{level_number}.txt")

    # Convert heuristic names to functions
    heuristic_funcs = [select_heuristic(h) for h in heuristics_list]
    if not all(heuristic_funcs):
        print(f"Invalid heuristic(s) found in: {heuristics_list}")
        return

    results = []
    for algorithm_name in algorithms_list:
        algorithm = select_algorithm(algorithm_name)
        if not algorithm:
            print(f"Skipping unknown algorithm: {algorithm_name}")
            continue

        avg_time, std_time, expanded_nodes = run_trials(algorithm_name, algorithm, level_data, initial_state, heuristic_funcs)

        results.append({
            "algorithm": algorithm_name, 
            "avg_time": avg_time, 
            "std_time": std_time, 
            "nodes_expanded": expanded_nodes
        })

    df = pd.DataFrame(results)

    # Print Execution Summary
    print("\n=== Execution Summary ===")
    print(df.to_string(index=False))

    # Plot Execution Time with Error Bars
    plt.figure(figsize=(10, 6))
    plt.bar(df["algorithm"], df["avg_time"], yerr=df["std_time"], capsize=5, color="lightblue")
    plt.xlabel("Algorithm")
    plt.ylabel("Average Execution Time (s)")
    heuristics_text = ", ".join(heuristics_list).upper()
    plt.title(f"Execution Time Comparison (Level {level_number}, Heuristics: {heuristics_text})")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plot Nodes Expanded
    plt.figure(figsize=(10, 6))
    plt.bar(df["algorithm"], df["nodes_expanded"], color="lightcoral")
    plt.xlabel("Algorithm")
    plt.ylabel("Nodes Expanded")
    plt.title(f"Memory Comparison (Nodes Expanded) for Level {level_number}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compare_bfs_astar.py <config_file>")
        sys.exit(1)

    main(sys.argv[1])