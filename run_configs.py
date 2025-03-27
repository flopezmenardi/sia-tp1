import json
import pandas as pd
import matplotlib.pyplot as plt
from main_analysis import run_game

# Path to the JSON file containing configurations
config_file = "configs/analysis/configs.json"
results = []

# Load configurations from the JSON file
with open(config_file, "r") as f:
    configs = json.load(f)

# Run all configurations and collect results
for config in configs:
    print(f"Running with config: {config}")
    solution, expanded_nodes, frontier_size, processing_time = run_game(config, simulate=False)
    algo_name = config["algorithm"]
    condition = f"Level {config['level']}"  # Use level as the condition
    results.append({
        "Algorithm": algo_name,
        "Condition": condition,
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
    plt.figure(figsize=(10, 6))
    for algo in df["Algorithm"].unique():
        subset = df[df["Algorithm"] == algo]
        plt.plot(subset["Condition"], subset[metric], marker="o", label=algo)
    plt.title(title)
    plt.xlabel("Conditions")
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{metric.replace(' ', '_').lower()}_comparison.png")
    plt.show()

# Generate graphs for the specified metrics
generate_graph("Processing Time", "Comparison of Avg Time Across Algorithms and Conditions", "Avg Time (s)")
generate_graph("Expanded Nodes", "Comparison of Visited Nodes Across Algorithms and Conditions", "Visited Nodes")
generate_graph("Solution Length", "Comparison of Solution Length Across Algorithms and Conditions", "Solution Length")
generate_graph("Frontier Size", "Comparison of Frontier Size Across Algorithms and Conditions", "Frontier Size")