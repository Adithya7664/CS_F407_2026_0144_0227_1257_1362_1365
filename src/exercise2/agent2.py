import copy
import random
import config2
import heapq
import itertools
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
    goal_r, goal_c = config2.GOAL_POS
    manhattan = abs(goal_r - r) + abs(goal_c - c)
    return manhattan * (config2.WALK_TIME_COST + config2.TURN_COST)

def search(current, belief_grid, avoid=()):
    M, N=config2.M, config2.N
    start = current

    pq = []
    heapq.heappush(pq, ((0, 0), next(counter), start))
    visited=dict()
    best_goal = None

    while pq:

        (_, _), _, current = heapq.heappop(pq)

        key = (current.row, current.col, round(current.lives, 2))

        if key in visited:
            continue
        visited[key] = True

        if (current.row, current.col) == config2.GOAL_POS:
            while current.parent and current.parent.parent:
                current=current.parent
            return current
        for next_state, next_risk in expand(current, belief_grid, avoid):
            priority = (
                -next_state.lives,
                next_state.cost()+next_risk
            )
            heapq.heappush(pq, (priority, next(counter), next_state))

    if best_goal:
        return best_goal

    return None

def expand(curstate, belief_grid, avoid=()):
    
    result=[]
    for dr, dc in config2.ORTHOGONAL_MOVES:

        # ---- WALK ----
        nr = curstate.row + dr
        nc = curstate.col + dc
        if not (0 <= nr < config2.M and 0 <= nc < config2.N):
            continue
        belf=belief_grid[nr][nc]
        if belf["B"]>0.8:
            continue
        risk_penalty=belf["V"]+belf["W"]
        expected_liveloss=risk_penalty*config2.HAZARD_LIFE_COST
        
        lives = curstate.lives
        newlives=max(lives-expected_liveloss, 0.05)

        if newlives > 0 and (nr, nc) not in avoid:
            successors=State(
                    nr, nc,
                    newlives,
                    curstate.time + config2.WALK_TIME_COST,
                    curstate.turns + config2.TURN_COST,
                    parent=curstate,
                    action='walk'
                )
            result.append((successors, risk_penalty))

        # ---- JUMP ----
        nr2 = curstate.row + 2 * dr
        nc2 = curstate.col + 2 * dc
        if not (0 <= nr2 < config2.M and 0 <= nc2 < config2.N):
            continue
        
        belf=belief_grid[nr2][nc2]
        if belf["B"]>0.8 or belief_grid[curstate.row + dr][curstate.col + dc]["B"]>0.8:
            continue                       # cannot land on, or jump over, a wall
        risk_penalty=belf["V"]+belf["W"]
        expected_liveloss=risk_penalty*config2.HAZARD_LIFE_COST

        lives = curstate.lives
        newlivesj=max(lives-expected_liveloss, 0.05)

        if newlivesj > 0 and (nr2, nc2) not in avoid:
            successors=State(
                    nr2, nc2,
                    newlivesj,
                    curstate.time + config2.JUMP_TIME_COST,
                    curstate.turns + config2.TURN_COST,
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

def collapse(r, c, truet, belief_grid):
    for x in ["L", "V", "W", "B"]:
        belief_grid[r][c][x]=0
    belief_grid[r][c][truet]=1
    
def runagent(grid, belief_grid, scan_infor):
    curS=State(config2.START_POS[0], config2.START_POS[1], config2.INITIAL_LIVES, 0, 0)
    fullpath=[(curS.row, curS.col, None, curS.lives)]
    snaps=[(copy.deepcopy(belief_grid), copy.deepcopy(scan_infor))]
    scans=4
    avoid = set()      # cells refused on the last life
    visited = {config2.START_POS}   # cells the agent has stood on
    while (curS.row, curS.col) !=config2.GOAL_POS:
        if curS.turns > config2.MAX_TURNS:      # safety net: never loop forever
            print("Turn limit reached.")
            return fullpath, snaps
        forced = False
        nextS = search(curS, belief_grid, avoid)
        if avoid and (nextS is None or len(avoid) > config2.DEATH_MAX_AVOID
                      or (nextS.row, nextS.col) in visited):   # a detour must not step back
            avoid.clear()          # nothing safer exists (or too many detours): accept the risk
            forced = True
            nextS = search(curS, belief_grid)
        if nextS is None:
            print("No safe path found.")
            return fullpath, snaps
        r, c = nextS.row, nextS.col

        belief = belief_grid[r][c]
        risk = belief["V"] + belief["W"]
        if config2.PROBE_ALTERNATIVES and risk >= config2.PROBE_RISK:
            # the planned step is very likely a hazard: scan other cells that could be safer land
            gr, gc = config2.GOAL_POS
            here = abs(curS.row - gr) + abs(curS.col - gc)
            alts = []
            for s2, _ in expand(curS, belief_grid, ()):
                a2, b2 = s2.row, s2.col
                bf = belief_grid[a2][b2]
                ar = bf["V"] + bf["W"]
                if (a2, b2) == (r, c) or (a2, b2) in visited:
                    continue
                if scan_infor[a2][b2]["count"] >= config2.PROBE_MAX_SCANS or not (0.05 < ar < 0.95):
                    continue
                d = abs(a2 - gr) + abs(b2 - gc)
                if d <= here:
                    alts.append((d, ar, a2, b2))
            if alts:
                alts.sort()
                _, _, a2, b2 = alts[0]
                T = Tsim(grid, a2, b2)
                S = Ssim(grid, a2, b2)
                belief_grid[a2][b2] = updatebelf(belief_grid[a2][b2], T, S)
                scan_infor[a2][b2]["count"] += 1
                scan_infor[a2][b2]["T"] = T
                scan_infor[a2][b2]["S"] = S
                scan_infor[a2][b2]["scanned"] = True
                curS = State(curS.row, curS.col, curS.lives, curS.time, curS.turns + config2.SCAN_TURN_COST, None, 'scan')
                fullpath.append((curS.row, curS.col, 'scan', curS.lives))
                snaps.append((copy.deepcopy(belief_grid), copy.deepcopy(scan_infor)))
                continue
        last_life = config2.DEATH_AWARE and curS.lives <= config2.HAZARD_LIFE_COST
        lo, hi = config2.DEATH_SCAN_BAND if last_life else (0.2, 0.7)
        if lo < risk < hi and scan_infor[r][c]["count"] < scans:
            T = Tsim(grid, r, c)
            S = Ssim(grid, r, c)

            belief_grid[r][c] = updatebelf(belief, T, S)
            scan_infor[r][c]["count"] += 1
            scan_infor[r][c]["T"] = T
            scan_infor[r][c]["S"] = S
            scan_infor[r][c]["scanned"] = True 
            curS=State(curS.row, curS.col, curS.lives, curS.time, curS.turns+config2.SCAN_TURN_COST, None, 'scan')
            fullpath.append((curS.row, curS.col, 'scan', curS.lives))
            snaps.append((copy.deepcopy(belief_grid), copy.deepcopy(scan_infor)))
            continue
        if scan_infor[r][c]["count"] >= scans and 0.2 < risk < 0.7:
            belief_grid[r][c] = {"L":0, "V":0, "W":0, "B":1}
            continue
        if last_life and not forced and risk >= config2.DEATH_RISK_THRESHOLD:
            avoid.add((r, c))      # one hazard would end the run: look for another route
            continue
        true_cell = grid[r][c]
        if config2.WALL_BLOCK and nextS.action == 'jump':
            mr, mc = (curS.row + r) // 2, (curS.col + c) // 2
            if grid[mr][mc] == "B":        # a jump cannot pass over a wall
                collapse(mr, mc, "B", belief_grid)
                curS = State(curS.row, curS.col, curS.lives, curS.time,
                             curS.turns + config2.TURN_COST, None, 'bump')
                fullpath.append((curS.row, curS.col, 'bump', curS.lives))
                snaps.append((copy.deepcopy(belief_grid), copy.deepcopy(scan_infor)))
                continue
        if config2.WALL_BLOCK and true_cell == "B":
            collapse(r, c, "B", belief_grid)
            curS = State(curS.row, curS.col, curS.lives, curS.time,
                         curS.turns + config2.TURN_COST, None, 'bump')
            fullpath.append((curS.row, curS.col, 'bump', curS.lives))
            snaps.append((copy.deepcopy(belief_grid), copy.deepcopy(scan_infor)))
            continue

        new_lives = curS.lives
        if true_cell in ["V", "W"]:
            new_lives -= config2.HAZARD_LIFE_COST

        if new_lives <= 0:
            print("Agent died.")
            collapse(r, c, true_cell, belief_grid)
            fullpath.append((r, c, nextS.action, 0))
            snaps.append((copy.deepcopy(belief_grid), copy.deepcopy(scan_infor)))
            return fullpath, snaps
        collapse(r, c, true_cell, belief_grid)
        visited.add((r, c))
        step_time = config2.WALK_TIME_COST if nextS.action == 'walk' else config2.JUMP_TIME_COST
        curS = State(r, c, new_lives, curS.time + step_time, curS.turns + config2.TURN_COST)
        fullpath.append((r, c, nextS.action, curS.lives))
        snaps.append((copy.deepcopy(belief_grid), copy.deepcopy(scan_infor)))
        
    print("Goal Reached")
    return fullpath, snaps
