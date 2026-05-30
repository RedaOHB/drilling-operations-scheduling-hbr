# Drilling Time Optimization -HBR-
 
This repository contains the formulation, methodology, implementation, and experimental analysis for the drilling rig scheduling problem arising from the **Hassi Bir Rekaiz development phase** (Algeria).
 
The problem involves scheduling **2 drilling rigs** across **25 wells**, minimizing the total project completion time (makespan) while accounting for well drilling durations and rig travel times between wells.

## Problem Overview
 
Since the discovery of oil in 1956 in the Algerian Sahara, Algeria has been developing new oil and gas fields to grow its economy. The Hassi Bir Rekaiz project is one such development, operated by **SONATRACH** and its partners.
 
The scheduling problem is modeled as an **uncapacitated Vehicle Routing Problem (VRP)**: each rig follows a route through a subset of wells, and the goal is to minimize the time at which the last rig completes its last well. The formal mathematical formulation and methodology are documented in `docs/`.

```
drilling-time-optimization-hbr/
├── data/
│   └── data.xlsx              # Devices travel time matrix and  well drilling times
├── docs/
│   ├── mathematical_formulation.md  # ILP formulation and linearization
│   ├── methodology.md         # Exact and approximate solution methods
│   └── problem.md             # Problem description
├── notebooks/
│   └── experiments.ipynb      # Experiments, comparisons, and analysis
├── src/
│   ├── heuristics.py          # Nearest Neighbor and Insertion heuristics
│   ├── metaheuristics.py      # Variable Neighborhood Search (VNS)
│   ├── utils.py               # Neighbourhood, local search and Time functions
│   └── main.py                # Main execution script
├── LICENSE
└── README.md
```

## Methodology
 
The problem is solved using three approaches:
 
**Heuristics** (constructive):
- **Nearest Neighbor (NN)**: builds routes successively, assigning the closest undrilled well at each step.
- **Insertion (IN)**: builds routes by inserting the nearest unvisited well into the position that minimizes added travel cost.

**Metaheuristic** (improvement-based):
- **Variable Neighborhood Search (VNS)**: takes a heuristic solution as input and iteratively explores structured neighborhoods to escape local optima.

## Instance
 
| Parameter | Value |
|-----------|-------|
| `Number of wells ($n$)` | 25 |
| `Number of rigs ($m$)` | 2 |
| `Travel times` | Asymmetric matrix (days) |
| `Drilling times` | Per-well duration (days) |
| `Data source` | Hassi Bir Rekaiz exploration phase (Feb. 2018) |

## Getting Started
 
### 1. Clone the repository
 
```bash
git clone https://github.com/RedaOHB/drilling-time-optimization-hbr.git
cd drilling-time-optinization-hbr
```

### 2. Install dependencies
 
```bash
pip install numpy pandas matplotlib openpyxl jupyter
```
 
### 3. Run the main script
 
```bash
python src/main.py
```

### 4. Run the notebook
 
Launch Jupyter from the **project root**:
 
```bash
jupyter notebook
```
 
Then open `notebooks/experiments.ipynb`.

## Documentation
 
| File | Description |
|------|-------------|
| `docs/problem.md` | Real-world context and problem statement |
| `docs/mathematical_formulation.md` | ILP model, linearization, and model size analysis |
| `docs/methodology.md` | Solution methods: exact (Gurobi), heuristics, metaheuristic |
| `notebooks/experiments.ipynb` | Full experimental analysis with plots and comparisons |

## Results
 
Results and interpretation are available in `notebooks/experiments.ipynb`. The notebook covers:
 
- Comparison of NN, Insertion, and VNS on the real instance
- VNS improvement over each heuristic starting point
- Sensitivity analysis with respect to the number of rigs
- Solution quality and runtime trade-offs

## License
 
This project is licensed under the [MIT License](LICENSE).

## Author
 
Developed as part of a master's thesis in Operations Research.
 
 
