import random
from config import HAZ_TYPES
import config

def gengrid():
    random.seed(config.RANDOM_SEED)
    M, N=config.M, config.N
    grid=[['L' for _ in range(N)] for _ in range(M)]
    anchor1, anchor2=select_anchors(M, N)
    path = []
    path += random_path(config.START_POS, anchor1)
    path += random_path(anchor1, anchor2)[1:]
    path += random_path(anchor2, config.GOAL_POS)[1:]
    path = remove_duplicates(path)
    assign_path_hazards(grid, path)
    fill_remaining(grid, path)

    return grid, path, anchor1, anchor2
    
    
    

def select_anchors(M, N):
    while True:
        a1 = (random.randint(1, M-2), random.randint(1, N-2))
        a2 = (random.randint(1, M-2), random.randint(1, N-2))

        if a1 == a2:
            continue
        if a1 == config.START_POS or a1 == config.GOAL_POS:
            continue
        if a2 == config.START_POS or a2 == config.GOAL_POS:
            continue

  
        if abs(a1[0]-a2[0]) + abs(a1[1]-a2[1]) == 1:
            continue

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
def fill_remaining(grid, path):
    path_set = set(path)
    for r in range(config.M):
        for c in range(config.N):
            if (r, c) in path_set:
                continue

            p = random.random()
            if p < config.NON_PATH_BRICK_RATIO:
                grid[r][c] = 'B'
            elif p < config.NON_PATH_BRICK_RATIO + config.NON_PATH_LAND_RATIO:
                grid[r][c] = 'L'
            else:
                grid[r][c] = random.choice(['V', 'W'])