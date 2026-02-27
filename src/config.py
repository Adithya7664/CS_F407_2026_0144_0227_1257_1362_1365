# =========================
# CONFIGURATION FILE
# =========================

# ---------- GRID SETTINGS ----------
M = 8                      # Rows (8 <= M <= 10)
N = 10                     # Columns (8 <= N <= 10)

START_POS = (0, 0)
GOAL_POS = (M - 1, N - 1)

RANDOM_SEED = 42           # For reproducibility


# ---------- CELL DISTRIBUTION ----------
NON_PATH_HAZARD_RATIO = 0.50
NON_PATH_LAND_RATIO   = 0.40
NON_PATH_BRICK_RATIO  = 0.10

PATH_VOLCANO_COUNT = 2
PATH_WATER_COUNT   = 2


# ---------- AGENT SETTINGS ----------
INITIAL_LIVES = 4


# ---------- ACTION COSTS ----------
WALK_TIME_COST = 2
JUMP_TIME_COST = 3
TURN_COST      = 1

HAZARD_LIFE_COST = 1


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
GIF_NAME = "simulation.gif"
FPS = 2


# ---------- COLOR MAP ----------

TEXT_COLORS = {
    'L': 'black',
    'W': 'blue',
    'V': 'red',
    'B': 'black'
}

# ---------- Hazard Types --------
HAZ_TYPES = {
    'L', 'V', 'B', 'W'
}

CELL_COLORS = {'L': 'white',
    'W': '#87CEFA',   # light blue
    'V': '#FFB6C1',   # light red
    'B': '#A9A9A9'    # gray
}