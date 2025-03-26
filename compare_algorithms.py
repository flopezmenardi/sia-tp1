import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

from loaders.map_loader import load_sokoban_map
from states.sokoban_state import get_possible_moves
from algorithms.bfs import bfs_search
from algorithms.dfs import dfs_search
from algorithms.greedy import greedy_search
from algorithms.astar import a_star_search
from heuristics.manhattan import manhattan_heuristic
from heuristics.deadlock import deadlock_heuristic
from heuristics.hungarian import hungarian_heuristic

# Algorithm and heuristic selection functions
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

def run_trials(algorithm, level_data, initial_state, heuristics, num_trials=100):
    execution_times = []
    nodes_expanded = []

    for _ in range(num_trials):
        start_time = time.time()

        if heuristics:
            solution, expanded_nodes, _ = algorithm(initial_state, lambda s: s.is_goal(level_data), get_possible_moves, level_data, heuristics)
        else:
            solution, expanded_nodes, _ = algorithm(initial_state, lambda s: s.is_goal(level_data), get_possible_moves, level_data)

        end_time = time.time()
        execution_times.append(end_time - start_time)
        nodes_expanded.append(expanded_nodes)

    return np.mean(execution_times), np.std(execution_times), np.mean(nodes_expanded)

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

        avg_time, std_time, avg_nodes = run_trials(algorithm, level_data, initial_state, heuristic_funcs)

        results.append({"algorithm": algorithm_name, "avg_time": avg_time, "std_time": std_time, "nodes_expanded": avg_nodes})

    df = pd.DataFrame(results)

    # Print Execution Summary
    print("\n=== Execution Summary ===")
    print(df.to_string(index=False))

    # Generate bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(df["algorithm"], df["avg_time"], yerr=df["std_time"], capsize=5, color="lightcoral")
    plt.xlabel("Algorithm")
    plt.ylabel("Average Execution Time (s)")
    heuristics_text = ", ".join(heuristics_list).upper()
    plt.title(f"Execution Time Comparison for Different Algorithms\n(Level {level_number}, Heuristics: {heuristics_text})")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.show()
    plt.close()  # Ensure script terminates after displaying the graph

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compare_algorithms.py <config_file>")
        sys.exit(1)

    main(sys.argv[1])