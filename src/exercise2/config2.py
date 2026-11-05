# =========================
# CONFIGURATION FILE (EXERCISE 2)
# =========================

# ---------- GRID SETTINGS ----------
M = 8                      # Rows (8 <= M <= 10)
N = 10                     # Columns (8 <= N <= 10)

START_POS = (0, 0)
GOAL_POS = (M - 1, N - 1)

RANDOM_SEED = 42           # For reproducibility
MATCHED_PRIOR = False

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
    "V": {"T": 0.85, "S": 0.60},
    "W": {"T": 0.01, "S": 0.85},
    "L": {"T": 0.10, "S": 0.05},
    "B": {"T": 0.05, "S": 0.01}
}
WALL_BLOCK = True

# ---------- DEATH-AWARE PLANNING (last life) ----------
DEATH_AWARE = True               # on the last life, avoid steps that are likely to be fatal
DEATH_RISK_THRESHOLD = 0.3       # last life: refuse a cell whose P(volcano or water) is at least this
DEATH_SCAN_BAND = (0.05, 0.95)   # last life: scan whenever risk is inside this wider band
DEATH_MAX_AVOID = 2              # last life: after refusing this many cells, stop detouring

# ---------- PROBING ALTERNATIVES ----------
PROBE_ALTERNATIVES = True        # before a likely-hazard step, scan other cells that might be safe land
PROBE_RISK = 0.7                 # "likely hazard" = P(volcano or water) at least this
PROBE_MAX_SCANS = 2              # at most this many probe scans per alternative cell
MAX_TURNS = 400                  # safety net: stop the run if it ever exceeds this many turns

# ---------- AGENT & SENSOR SETTINGS ----------
INITIAL_LIVES = 4
K_SCAN_LIMIT = 4      # Maximum sensor scans allowed per cell 


# ---------- ACTION COSTS ----------
WALK_TIME_COST = 2
JUMP_TIME_COST = 3
TURN_COST      = 1
HAZARD_LIFE_COST = 1
SCAN_TURN_COST = 1
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
FRAME_SAVE_DIR = "frames2/"
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
    'L': "#27ee41",         # Land high probability
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

CELL_COLORS2 = {'L': "#6bf77d",
    'W': '#87CEF5',   # light blue
    'V': '#FFB6C1',   # light red
    'B': '#A9A9A9'    # gray
}

NON_PATH_HAZARD_RATIO = 0.50
NON_PATH_LAND_RATIO   = 0.40
NON_PATH_BRICK_RATIO  = 0.10

PATH_VOLCANO_COUNT = 2
PATH_WATER_COUNT   = 2