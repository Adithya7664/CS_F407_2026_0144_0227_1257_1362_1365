# CS_F407_2026_0144_0227_1257_1362_1365
Intelligent Agent Navigation – Deterministic & Probabilistic
📌 Overview:

This project implements an intelligent grid-based navigation system in two stages:

-Exercise 1 – Deterministic Optimal Agent

-Exercise 2 – Probabilistic Bayesian Agent with Noisy Sensors

The agent must navigate from a start cell (0,0) to the goal (M-1,N-1) while:

1.Minimizing score = (Time + Turns) / Lives

2.Avoiding hazards (Volcano & Water)

3.Handling movement constraints (Walk & Jump)

4.Managing limited lives.

Each cell in the grid can be:
| Label | Meaning    | Color |
| ----- | ---------- | ----- |
| L     | Land       | Green |
| V     | Volcano    | Red   |
| W     | Water      | Blue  |
| B     | Brick Wall | Gray  |  


**Exercise 1 – Deterministic Agent**:
✔ Features

Unique safe path generation using anchor cells

Exactly:

2 Volcano cells

2 Water cells on ground-truth path

A*-like search optimizing:

Score = (Time + Turns) / Lives
✔ Movement Types

-Walk (distance 1) → Black straight arrow

-Jump (distance 2) → Purple curved arrow

-Damage → Red dashed arrow + Red ❌  

✔ Output

-Initial grid visualization

-Optimal path

-Step-by-step animation saved as GIF




**Exercise 2 – Probabilistic Bayesian Agent**:

In this version:

1. Agent does NOT know true terrain

Uses noisy sensors:

-Thermal (Volcano detection)

-Seismic (Water detection)

-Maintains belief over each cell

-Updates belief using Bayesian inference

📡 *Sensor Model (CPT)*

Terrain	  P(Thermal=True)	  P(Seismic=True)
Volcano	  0.85	              0.60
Water	    0.01	              0.85
Land	    0.10	              0.05
Wall	    0.05	              0.01  

Bayesian Update:

Posterior computed using:

`P(Terrain | T, S)` ∝ P(T | Terrain) × P(S | Terrain) × Prior

Normalized over all terrain types.



🔍 **Scan Logic**

Agent scans when:

0.2 < Risk < 0.7

Each scan:

-Costs 1 turn

-Does not move agent

-Maximum scans per cell: 4

-After 4 scans → cell marked BLOCKED.

*Visualization (Exercise 2)*:

Two synchronized panels:

`Left Panel – Belief Map`

-Cell color based on posterior probabilities

-Displays risk percentage

-Yellow border for scanned cells

-Shows sensor readings: T: True/False, S: True/False

-Red ❌ when life lost

`Right Panel – Ground Truth`

-True terrain coloring

-Same path overlay

-Damage markers

-Life/time/turns/score displayed

**How to Run**:
🔹 Exercise 1
python main.py in excercise1 folder

Outputs:

-Grid visualization

-Optimal path

-Animation saved as GIF

🔹 Exercise 2
python main2.py in excersize2 folder

Outputs:

-Belief map vs Ground truth

-Bayesian updates

-Scan visualization

-Risk-aware navigation animation

*Example results*:
Ex1: <img width="466" height="62" alt="image" src="https://github.com/user-attachments/assets/d44a9d64-f8de-4a17-add1-7253ad389757" />

Ex2: <img width="410" height="33" alt="image" src="https://github.com/user-attachments/assets/2f6913a7-36aa-4963-8cf4-01de9327e6d6" />

	Key Concepts Demonstrated`:

-A* search with multi-objective scoring

-Risk-aware planning

-Bayesian inference

-Belief space planning

-Noisy sensor integration

-Probabilistic decision making

-Visualization engineering

**Requirements**

-Python 3.x

-matplotlib

-numpy

-imageio

`Conclusion`:

This project demonstrates the transition from:

Deterministic optimal planning
→ Probabilistic belief-based intelligent navigation

The second agent operates under uncertainty and dynamically adapts through Bayesian reasoning, successfully navigating the environment while managing risk and limited resources.

