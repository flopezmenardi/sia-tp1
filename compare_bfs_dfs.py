import json
import time
import pandas as pd
import matplotlib.pyplot as plt
import sys

from loaders.map_loader import load_sokoban_map
from states.sokoban_state import get_possible_moves
from algorithms.bfs import bfs_search
from algorithms.dfs import dfs_search  # Import DFS

# Algorithm selection function
def select_algorithm(name):
    return {
        "bfs": bfs_search,
        "dfs": dfs_search  # Added DFS
    }.get(name.lower())

def run_algorithm(algorithm_name, algorithm, level_data, initial_state):
    # Measure execution time
    start_time = time.time()
    solution, expanded_nodes, _ = algorithm(initial_state, lambda s: s.is_goal(level_data), get_possible_moves, level_data)
    end_time = time.time()
    
    execution_time = end_time - start_time
    solution_cost = len(solution) if solution else float('inf')  # If no solution, set cost to infinity
    return execution_time, expanded_nodes, solution_cost

def main(config_file):
    with open(config_file, "r") as file:
        config = json.load(file)

    level_number = config["level"]
    algorithms_list = config["algorithms"]

    level_data, initial_state = load_sokoban_map(f"maps/level{level_number}.txt")

    results = []
    for algorithm_name in algorithms_list:
        algorithm = select_algorithm(algorithm_name)
        if not algorithm:
            print(f"Skipping unknown algorithm: {algorithm_name}")
            continue

        exec_time, expanded_nodes, solution_cost = run_algorithm(algorithm_name, algorithm, level_data, initial_state)

        results.append({
            "algorithm": algorithm_name, 
            "execution_time": exec_time, 
            "nodes_expanded": expanded_nodes,
            "solution_cost": solution_cost
        })

    df = pd.DataFrame(results)

    # Print Execution Summary
    print("\n=== Execution Summary ===")
    print(df.to_string(index=False))

    # Plot Execution Time
    plt.figure(figsize=(10, 6))
    bars = plt.bar(df["algorithm"], df["execution_time"], color="lightblue")
    plt.xlabel("Algorithm")
    plt.ylabel("Execution Time (s)")
    plt.title(f"Execution Time Comparison (Level {level_number})")
    
    # Add Solution Cost as text annotation
    for bar, cost in zip(bars, df["solution_cost"]):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"Cost: {cost}", ha="center", va="bottom", fontsize=10, fontweight="bold")

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plot Nodes Expanded
    plt.figure(figsize=(10, 6))
    bars = plt.bar(df["algorithm"], df["nodes_expanded"], color="lightcoral")
    plt.xlabel("Algorithm")
    plt.ylabel("Nodes Expanded")
    plt.title(f"Memory Comparison (Nodes Expanded) for Level {level_number}")

    # Add Solution Cost as text annotation
    for bar, cost in zip(bars, df["solution_cost"]):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"Cost: {cost}", ha="center", va="bottom", fontsize=10, fontweight="bold")

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compare_bfs_dfs.py <config_file>")
        sys.exit(1)

    main(sys.argv[1])