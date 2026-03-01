import random
from config import HAZ_TYPES
import config

def gengrid():
    random.seed(config.RANDOM_SEED)
    M, N = config.M, config.N
    # Initialize the grid with 'L'
    grid = [['L' for _ in range(N)] for _ in range(M)]
    
    anchor1, anchor2 = select_anchors(M, N)
    path = []
    
    # Generate random path through anchors
    path += random_path(config.START_POS, anchor1)
    path += random_path(anchor1, anchor2)[1:]
    path += random_path(anchor2, config.GOAL_POS)[1:]
    path = remove_duplicates(path)
    
    # Assign specific hazards to the path
    assign_path_hazards(grid, path)
    
    # Fill the rest of the grid using probabilistic priors
    fill_remaining(grid, path)

    return grid, path, anchor1, anchor2
    

def select_anchors(M, N):
    while True:
        a1 = (random.randint(1, M-2), random.randint(1, N-2))
        a2 = (random.randint(1, M-2), random.randint(1, N-2))

        # Anchors cannot be same, start, or goal
        if a1 == a2:
            continue
        if a1 == config.START_POS or a1 == config.GOAL_POS:
            continue
        if a2 == config.START_POS or a2 == config.GOAL_POS:
            continue

        # Anchors must not be adjacent
        if abs(a1[0]-a2[0]) + abs(a1[1]-a2[1]) == 1:
            continue

        # Anchors must not share the same row or column (non-linear)
        if a1[0] == a2[0] or a1[1] == a2[1]:
            continue

        return a1, a2
    
def random_path(start, end):
    path = [start]
    r, c = start
    while (r, c) != end:
        dr = end[0] - r
        dc = end[1] - c

        moves = []
        if dr != 0:
            moves.append((1 if dr > 0 else -1, 0))
        if dc != 0:
            moves.append((0, 1 if dc > 0 else -1))

        move = random.choice(moves)
        r += move[0]
        c += move[1]

        path.append((r, c))

    return path

def remove_duplicates(path):
    seen = set()
    new_path = []
    for p in path:
        if p not in seen:
            new_path.append(p)
            seen.add(p)
    return new_path

def assign_path_hazards(grid, path):
    valid_cells = path[1:-1] 
    while True:
        hazard_positions = random.sample(valid_cells, 4)
        types = ['V', 'V', 'W', 'W']
        random.shuffle(types)
        temp_assignment = dict(zip(hazard_positions, types))
        if not has_adjacent_same_type(temp_assignment):
            break  # valid assignment

    for pos, t in zip(hazard_positions, types):
        r, c = pos
        grid[r][c] = t
        
def has_adjacent_same_type(hazard_dict):
    positions = list(hazard_dict.keys())

    for i in range(len(positions)):
        r1, c1 = positions[i]
        t1 = hazard_dict[(r1, c1)]

        for j in range(i + 1, len(positions)):
            r2, c2 = positions[j]
            t2 = hazard_dict[(r2, c2)]

            # Check adjacency (Manhattan distance 1)
            if abs(r1 - r2) + abs(c1 - c2) == 1:
                if t1 == t2:
                    return True

    return False

# ==========================================
# EXERCISE 2 MODIFICATION: PROBABILISTIC FILL
# ==========================================
def fill_remaining(grid, path):
    path_set = set(path)
    for r in range(config.M):
        for c in range(config.N):
            # Skip cells that are part of the main path
            if (r, c) in path_set:
                continue

            # Assign cell terrain based on Exercise 2 Prior Probabilities
            p = random.random()
            
            # Cumulative probabilities to determine the terrain type
            if p < config.P_WALL:                                   # 0.00 to 0.36
                grid[r][c] = 'B'
            elif p < config.P_WALL + config.P_LAND:                 # 0.36 to 0.52 (0.36 + 0.16)
                grid[r][c] = 'L'
            elif p < config.P_WALL + config.P_LAND + config.P_LAVA: # 0.52 to 0.76 (0.52 + 0.24)
                grid[r][c] = 'V'
            else:                                                   # 0.76 to 1.00 (0.24)
                grid[r][c] = 'W'
