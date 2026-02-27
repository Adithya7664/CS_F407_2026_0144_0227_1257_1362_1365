import random
import config
import heapq
import itertools
counter = itertools.count()

class State:
    def __init__(self, row, col, lives, time, turns, parent=None, action=None, heat=False, vibration=False):
        self.row = row
        self.col = col
        self.lives = lives
        self.time = time
        self.turns = turns
        self.parent = parent
        self.action = action
        self.heat=heat
        self.vibration=vibration
    def cost(self):
        return self.time + self.turns

    def score(self):
        if self.lives <= 0:
            return float('inf')
        return self.cost() / self.lives
    
def heuristic(r, c):
    goal_r, goal_c = config.GOAL_POS
    manhattan = abs(goal_r - r) + abs(goal_c - c)
    return manhattan * (config.WALK_TIME_COST + config.TURN_COST)

def valid_cell(r, c, grid):
    if r < 0 or r >= config.M:
        return False
    if c < 0 or c >= config.N:
        return False
    if grid[r][c] == 'B':
        return False
    return True

def reconstruct_path(state):
    
    path = []

    while state:
        path.append((state.row, state.col, state.action, state.lives))
        state = state.parent

    return path[::-1]

def search(grid):
    M, N=config.M, config.N
    start = State(
        config.START_POS[0],
        config.START_POS[1],
        config.INITIAL_LIVES,
        0,
        0, 
        None, 
        None,
        False, 
        False
    )

    pq = []
    heapq.heappush(pq, ((0, 0), next(counter), start))
    visited=dict()
    best_goal = None

    while pq:

        (_, _), _, current = heapq.heappop(pq)

        key = (current.row, current.col, current.lives)

        if key in visited:
            continue
        visited[key] = True

        if (current.row, current.col) == config.GOAL_POS:

            if best_goal is None or current.score() > best_goal.score():
                best_goal = current
            continue
        for next_state, next_risk in expand(current, grid):
            priority = (
                -next_state.lives,
                next_state.cost()+next_risk
            )
            heapq.heappush(pq, (priority, next(counter), next_state))

    if best_goal:
        return reconstruct_path(best_goal)

    return None

def thermal_sensor(r, c, grid):
    for dr, dc in config.ORTHOGONAL_MOVES:
        nr, nc = r + dr, c + dc
        if 0 <= nr < config.M and 0 <= nc < config.N:
            if grid[nr][nc] == 'V':
                return True
    return False

def seismic_sensor(r, c, grid):
    for dr, dc in config.ORTHOGONAL_MOVES:
        nr, nc = r + dr, c + dc
        if 0 <= nr < config.M and 0 <= nc < config.N:
            if grid[nr][nc] == 'W':
                return True
    return False

def expand(curstate, grid):
    
    result=[]
    for dr, dc in config.ORTHOGONAL_MOVES:

        # ---- WALK ----
        nr = curstate.row + dr
        nc = curstate.col + dc
        heat = thermal_sensor(nr, nc, grid)
        vibration = seismic_sensor(nr, nc, grid)
        risk_penalty=0
        if thermal_sensor(nr, nc, grid):
            risk_penalty += 0.5
        if seismic_sensor(nr, nc, grid):
            risk_penalty += 0.5
        if valid_cell(nr, nc, grid):
            lives = curstate.lives
            cell = grid[nr][nc]

            if cell in ['W', 'V']:
                lives -= config.HAZARD_LIFE_COST

            if lives > 0:
                successors=State(
                        nr, nc,
                        lives,
                        curstate.time + config.WALK_TIME_COST,
                        curstate.turns + config.TURN_COST,
                        parent=curstate,
                        action='walk', 
                        heat=heat, 
                        vibration=vibration
                    )
                result.append((successors, risk_penalty))

        # ---- JUMP ----
        nr2 = curstate.row + 2 * dr
        nc2 = curstate.col + 2 * dc

        mid_r = curstate.row + dr
        mid_c = curstate.col + dc

        if valid_cell(nr2, nc2, grid) and grid[mid_r][mid_c] != 'B':

            lives = curstate.lives
            cell = grid[nr2][nc2]

            if cell in ['W', 'V']:
                lives -= config.HAZARD_LIFE_COST

            if lives > 0:
                successors=State(
                        nr2, nc2,
                        lives,
                        curstate.time + config.JUMP_TIME_COST,
                        curstate.turns + config.TURN_COST,
                        parent=curstate,
                        action='jump', 
                        heat=heat, 
                        vibration=vibration
                    )
                result.append((successors, risk_penalty))

    return result