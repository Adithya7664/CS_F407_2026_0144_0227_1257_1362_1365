import random
import config
import heapq
import itertools
from grid_gen2 import belief_grid
from grid_gen2 import scan_infor
import config2
counter = itertools.count()

class State:
    def __init__(self, row, col, lives, time, turns, parent=None, action=None):
        self.row = row
        self.col = col
        self.lives = lives
        self.time = time
        self.turns = turns
        self.parent = parent
        self.action = action

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

def search(current):
    M, N=config.M, config.N
    start = current

    pq = []
    heapq.heappush(pq, ((0, 0), next(counter), start))
    visited=set()
    best_goal = None

    while pq:

        (_, _), _, current = heapq.heappop(pq)

        key = (current.row, current.col, round(current.lives, 2))

        if key in visited:
            continue
        visited[key] = True

        if (current.row, current.col) == config.GOAL_POS:
            while current.parent and current.parent.parent:
                current=current.parent
            return current
        for next_state, next_risk in expand(current):
            priority = (
                -next_state.lives,
                next_state.cost()+next_risk
            )
            heapq.heappush(pq, (priority, next(counter), next_state))

    if best_goal:
        return best_goal

    return None

def expand(curstate):
    
    result=[]
    for dr, dc in config.ORTHOGONAL_MOVES:

        # ---- WALK ----
        nr = curstate.row + dr
        nc = curstate.col + dc
        if not (0 <= nr < config.M and 0 <= nc < config.N):
            continue
        belf=belief_grid[nr][nc]
        if belf["B"]>0.8:
            continue
        risk_penalty=belf["V"]+belf["W"]
        expected_liveloss=risk_penalty*config.HAZARD_LIFE_COST
        
        lives = curstate.lives

        newlives=lives-expected_liveloss

        if newlives > 0:
            successors=State(
                    nr, nc,
                    newlives,
                    curstate.time + config.WALK_TIME_COST,
                    curstate.turns + config.TURN_COST,
                    parent=curstate,
                    action='walk'
                )
            result.append((successors, risk_penalty))

        # ---- JUMP ----
        nr2 = curstate.row + 2 * dr
        nc2 = curstate.col + 2 * dc
        if not (0 <= nr2 < config.M and 0 <= nc2 < config.N):
            continue
        
        belf=belief_grid[nr2][nc2]
        if belf["B"]>0.8:
            continue
        risk_penalty=belf["V"]+belf["W"]
        expected_liveloss=risk_penalty*config.HAZARD_LIFE_COST

        lives = curstate.lives

        newlivesj=lives-expected_liveloss

        if newlivesj > 0:
            successors=State(
                    nr2, nc2,
                    newlivesj,
                    curstate.time + config.JUMP_TIME_COST,
                    curstate.turns + config.TURN_COST,
                    parent=curstate,
                    action='jump', 
                )
            result.append((successors, risk_penalty))

    return result

def updatebelf(prior, T, S):
    posterior={}
    total=0
    for cell_type in ["L", "V", "W", "B"]:
        pprior=prior[cell_type]
        pt=config2.CPT[cell_type]["T"] if T else (1-config2.CPT[cell_type]["T"])
        ps=config2.CPT[cell_type]["S"] if S else (1-config2.CPT[cell_type]["S"])
        likelihood=pt*ps
        posterior[cell_type]=likelihood*pprior
        total+=posterior[cell_type]
    for k in posterior:
        if total == 0:
            return prior
        posterior[k]/=total
        
    return posterior

def Tsim(grid, r, c):
    true=grid[r][c]
    ps=config2.CPT[true]["T"]
    return random.random() < ps

def Ssim(grid, r, c):
    true=grid[r][c]
    ps=config2.CPT[true]["S"]
    return random.random() < ps

def collapse(r, c, truet):
    for x in ["L", "V", "W", "B"]:
        belief_grid[r][c][x]=0
    belief_grid[r][c][truet]=1
    
def runagent(grid):
    curS=State(config.START_POS[0], config.START_POS[1], config.INITIAL_LIVES, 0, 0)
    fullpath=[(curS.row, curS.col, None, curS.lives)]
    thres=0.38
    scans=4
    while (curS.row, curS.col) !=config.GOAL_POS:
        nextS=search(curS)
        if nextS is None:
            print("No safe path found.")
            return fullpath
        r, c = nextS.row, nextS.col

        belief = belief_grid[r][c]
        risk = belief["V"] + belief["W"]
        if 0.2< risk < 0.7 and scan_infor[r][c]["count"] < scans:
            T = Tsim(grid, r, c)
            S = Ssim(grid, r, c)

            belief_grid[r][c] = updatebelf(belief, T, S)
            scan_infor[r][c]["count"] += 1
            scan_infor[r][c]["T"] = T
            scan_infor[r][c]["S"] = S
            curS=State(curS.row, curS.col, curS.lives, curS.time, curS.turns+config2.SCAN_TURN_COST, None, 'scan')
            fullpath.append((curS.row, curS.col, 'scan', curS.lives))
            continue
        if scan_infor[r][c]["count"] >= scans:
            belief_grid[r][c] = {"L":0, "V":0, "W":0, "B":1}
            continue
        true_cell = grid[r][c]

        new_lives = curS.lives
        if true_cell in ["V", "W"]:
            new_lives -= config.HAZARD_LIFE_COST

        if new_lives <= 0:
            print("Agent died.")
            return fullpath
        collapse(r, c, true_cell)
        curS=State(r, c, new_lives, curS.time+(config.WALK_TIME_COST if abs(r-fullpath[-1][0])==2 or abs(r-fullpath[-1][1])==2 else config.JUMP_TIME_COST), curS.turns+config.TURN_COST)
        fullpath.append((r, c, nextS.action, curS.lives))
        
    print("Goal Reached")
    return fullpath
