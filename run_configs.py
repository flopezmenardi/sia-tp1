import json
import pandas as pd
import matplotlib.pyplot as plt
from itertools import product
from main_analysis import run_game
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run Sokoban configurations and generate comparisons.")
parser.add_argument("config_file", type=str, help="Path to the JSON file containing configurations.")
args = parser.parse_args()

# Load configurations from the JSON file
with open(args.config_file, "r") as f:
    config_data = json.load(f)

# Extract levels, algorithms, and heuristics
levels = config_data["levels"]
algorithms = config_data["algorithms"]
heuristics_list = config_data["heuristics"]

# Generate all permutations of levels, algorithms, and heuristics
configurations = list(product(levels, algorithms, heuristics_list))

# Run all configurations and collect results
results = []
for level, algorithm, heuristics in configurations:
    config = {
        "level": level,
        "algorithm": algorithm,
        "heuristics": heuristics
    }
    print(f"Running with config: {config}")
    solution, expanded_nodes, frontier_size, processing_time = run_game(config, simulate=False)
    condition = f"Level {level}"  # Use level as the condition
    results.append({
        "Algorithm": algorithm,
        "Condition": condition,
        "Heuristics": ", ".join(heuristics) if heuristics else "None",
        "Solution Length": len(solution) if solution else None,
        "Expanded Nodes": expanded_nodes,
        "Frontier Size": frontier_size,
        "Processing Time": processing_time
    })

# Convert results to a DataFrame for easier analysis
df = pd.DataFrame(results)

# Save results to a CSV file for future reference
df.to_csv("results.csv", index=False)

# Generate graphs for comparisons
def generate_graph(metric, title, ylabel):
    plt.figure(figsize=(12, 8))
    algorithms = df["Algorithm"].unique()
    x_labels = df["Condition"].unique()
    x = range(len(x_labels))  # X-axis positions for the bars

    # Bar width and offsets for each algorithm
    bar_width = 0.2
    offsets = [(i - len(algorithms) / 2) * bar_width for i in range(len(algorithms))]

    for i, algo in enumerate(algorithms):
        subset = df[df["Algorithm"] == algo]
        y_values = [subset[subset["Condition"] == condition][metric].mean() for condition in x_labels]

        # Include heuristics in the label only for informed searches
        if algo in ["astar", "greedy"]:
            label = f"{algo} ({subset['Heuristics'].iloc[0]})"
        else:
            label = algo

        plt.bar(
            [pos + offsets[i] for pos in x],  # Adjust bar positions for each algorithm
            y_values,
            bar_width,
            label=label
        )

    plt.title(title)
    plt.xlabel("Conditions")
    plt.ylabel(ylabel)
    plt.xticks(x, x_labels, rotation=45)
    plt.legend()
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(f"{metric.replace(' ', '_').lower()}_comparison.png")
    plt.show()

# Generate graphs for the specified metrics
generate_graph("Processing Time", "Comparison of Avg Time Across Algorithms and Conditions", "Avg Time (s)")
generate_graph("Expanded Nodes", "Comparison of Visited Nodes Across Algorithms and Conditions", "Visited Nodes")
generate_graph("Solution Length", "Comparison of Solution Length Across Algorithms and Conditions", "Solution Length")
generate_graph("Frontier Size", "Comparison of Frontier Size Across Algorithms and Conditions", "Frontier Size")