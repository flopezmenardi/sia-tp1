# TP1 SIA - Métodos de Búsqueda

[Enunciado](docs/SIA_TP1.pdf)

## Instalación

Parado en la carpeta del tp1 ejecutar

```sh
pip install -r requirements.txt
```

para instalar las dependencias necesarias en el ambiente virtual

## Ejecución

### Main
Al correr el archivo main, se visualizará la resolución hallada por dicho algoritmo utilizando Pygame, y se imprimirán métricas como nodos expandidos en terminal.
```
pipenv run python main.py configs/tests/[config_file]
```

Un archivo de configuración se vé así:
```
{
    "level": 1,
    "algorithm": "astar",
    "heuristics": ["manhattan", "deadlock"]
}
```

### Compare BFS with A*
```
pipenv run python compare_bfs_astar.py configs/compare_bfs_astar/[config_file]
```

### Compare BFS with DFS
```
pipenv run python compare_bfs_dfs.py configs/compare_bfs_dfs/[config_file]
```

### Compare heuristics
```
pipenv run python compare_heuristics.py configs/compare_heuristics/[config_file]
```

### Compare all algorithms
```
pipenv run python run_configs.py configs/analysis/config_euclidean.json
pipenv run python run_configs.py configs/analysis/config_manhattan.json
pipenv run python run_configs.py configs/analysis/config_hungarian.json
```

### Compare levels
```
pipenv run python compare_levels.py configs/compare_levels/greedy/[config_file]
pipenv run python compare_levels.py configs/compare_levels/astar/[config_file]
```