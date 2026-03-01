# =========================
# CONFIGURATION FILE (EXERCISE 2)
# =========================

# ---------- GRID SETTINGS ----------
M = 8                      # Rows (8 <= M <= 10)
N = 10                     # Columns (8 <= N <= 10)

START_POS = (0, 0)
GOAL_POS = (M - 1, N - 1)

RANDOM_SEED = 42           # For reproducibility


# ---------- PROBABILISTIC SETTINGS (NEW FOR EXERCISE-2) ----------
# Independent prior probabilities 
P_VOLCANO_BASE = 0.4
P_WATER_BASE = 0.4

# Derived Prior probabilities for filling the grid 
P_LAVA = P_VOLCANO_BASE * (1 - P_WATER_BASE)         # 0.24
P_WATER = (1 - P_VOLCANO_BASE) * P_WATER_BASE        # 0.24
P_LAND = P_VOLCANO_BASE * P_WATER_BASE               # 0.16
P_WALL = (1 - P_VOLCANO_BASE) * (1 - P_WATER_BASE)   # 0.36

# Conditional Probability Table (CPT) 
# Format: 'Terrain_Type': (P(Thermal=True | Terrain), P(Seismic=True | Terrain))
CPT = {
    'V': (0.85, 0.60),  # LAVA / VOLCANO
    'W': (0.01, 0.85),  # WATER
    'L': (0.10, 0.05),  # SAFE / LAND
    'B': (0.05, 0.01)   # WALL / BRICK
}


# ---------- AGENT & SENSOR SETTINGS ----------
INITIAL_LIVES = 4
K_SCAN_LIMIT = 4      # Maximum sensor scans allowed per cell 


# ---------- ACTION COSTS ----------
WALK_TIME_COST = 2
JUMP_TIME_COST = 3
TURN_COST      = 1
HAZARD_LIFE_COST = 1
# Note: Scanning a cell costs 0 time units but advances the turn counter by 1.


# ---------- SCORING ----------
# Final score = (turns + time) / lives
LIFE_PRIORITY_WEIGHT = 1000   # For search weighting


# ---------- MOVEMENT ----------
ORTHOGONAL_MOVES = [
    (-1, 0),  # up
    (1, 0),   # down
    (0, -1),  # left
    (0, 1)    # right
]


# ---------- VISUAL SETTINGS ----------
CELL_SIZE = 1
FRAME_SAVE_DIR = "frames/"
GIF_NAME = "simulation_ex2.gif"
FPS = 2

# ---------- BELIEF MAP COLOR THRESHOLDS ----------
# Used for coloring the Agent's Belief Map in the left panel 
THRESHOLD_VOLCANO = 0.4  # If P(Volcano) > 0.4 -> Red 
THRESHOLD_WATER = 0.4    # If P(Water) > 0.4 -> Blue 
THRESHOLD_LAND = 0.5     # If P(Land) > 0.5 -> Green 

BELIEF_COLORS = {
    'V': 'red',             # Volcano high probability
    'W': '#3498db',         # Water high probability
    'L': '#2ecc71',         # Land high probability
    'UNKNOWN': 'lightgrey', # Below thresholds 
    'WALL': 'grey',         # Wall
    'SCAN_BORDER': 'yellow' # Scanned cells border 
}

TEXT_COLORS = {
    'L': 'black',
    'W': 'blue',
    'V': 'red',
    'B': 'black'
}

# ---------- HAZARD TYPES --------
HAZ_TYPES = {
    'L', 'V', 'B', 'W'
}

CELL_COLORS2 = {'L': 'green',
    'W': '#87CEF5',   # light blue
    'V': '#FFB6C1',   # light red
    'B': '#A9A9A9'    # gray
}