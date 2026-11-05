"""Upgrades the Exercise 2 agent with:
  1. a death-aware "last life" guard           (skipped if patch_death.py was already applied)
  2. probing of alternative cells before a likely-hazard step
  3. a fix for a ping-pong livelock + a hard turn limit

Usage:
    python patch_agent_upgrade.py "<path to your src/exercise2 folder>"

Edits agent2.py and config2.py in place and preserves line endings (CRLF/LF).
Every edit must match exactly once; if anything fails, NOTHING is written.
Tip: commit your work first, so `git diff` shows exactly what this changed.
Switch features off any time in config2.py: DEATH_AWARE, PROBE_ALTERNATIVES.
"""
import os
import sys

if len(sys.argv) != 2:
    sys.exit(__doc__)
BASE = sys.argv[1]


def load(path):
    text = open(path, newline="").read()
    return text, ("\r\n" if "\r\n" in text else "\n")


def edit(text, nl, old, new, name):
    old, new = old.replace("\n", nl), new.replace("\n", nl)
    n = text.count(old)
    if n != 1:
        sys.exit(f"{name}: expected 1 match, found {n} for:\n{old[:90]!r}\nNothing was written.")
    return text.replace(old, new)


agent_path = os.path.join(BASE, "agent2.py")
config_path = os.path.join(BASE, "config2.py")
a, nl = load(agent_path)
c, nlc = load(config_path)

# ------------------------------------------------ stage 1: death-aware guard
if "DEATH_AWARE" not in a and "DEATH_AWARE" not in c:
    n = "agent2.py"
    a = edit(a, nl, "def search(current, belief_grid):\n", "def search(current, belief_grid, avoid=()):\n", n)
    a = edit(a, nl, "        for next_state, next_risk in expand(current, belief_grid):\n",
                    "        for next_state, next_risk in expand(current, belief_grid, avoid):\n", n)
    a = edit(a, nl, "def expand(curstate, belief_grid):\n", "def expand(curstate, belief_grid, avoid=()):\n", n)
    a = edit(a, nl, "        if newlives > 0:\n", "        if newlives > 0 and (nr, nc) not in avoid:\n", n)
    a = edit(a, nl, "        if newlivesj > 0:\n", "        if newlivesj > 0 and (nr2, nc2) not in avoid:\n", n)
    a = edit(a, nl, "    scans=4\n", "    scans=4\n    avoid = set()      # cells refused on the last life\n", n)
    a = edit(a, nl, "        nextS=search(curS, belief_grid)\n        if nextS is None:\n",
                    "        forced = False\n"
                    "        nextS = search(curS, belief_grid, avoid)\n"
                    "        if avoid and (nextS is None or len(avoid) > config2.DEATH_MAX_AVOID):\n"
                    "            avoid.clear()          # nothing safer exists (or too many detours): accept the risk\n"
                    "            forced = True\n"
                    "            nextS = search(curS, belief_grid)\n"
                    "        if nextS is None:\n", n)
    a = edit(a, nl, '        if 0.2< risk < 0.7 and scan_infor[r][c]["count"] < scans:\n',
                    "        last_life = config2.DEATH_AWARE and curS.lives <= config2.HAZARD_LIFE_COST\n"
                    "        lo, hi = config2.DEATH_SCAN_BAND if last_life else (0.2, 0.7)\n"
                    '        if lo < risk < hi and scan_infor[r][c]["count"] < scans:\n', n)
    a = edit(a, nl, "        true_cell = grid[r][c]\n",
                    "        if last_life and not forced and risk >= config2.DEATH_RISK_THRESHOLD:\n"
                    "            avoid.add((r, c))      # one hazard would end the run: look for another route\n"
                    "            continue\n"
                    "        true_cell = grid[r][c]\n", n)
    n = "config2.py"
    c = edit(c, nlc, "WALL_BLOCK = True\n",
                     "WALL_BLOCK = True\n"
                     "\n"
                     "# ---------- DEATH-AWARE PLANNING (last life) ----------\n"
                     "DEATH_AWARE = True               # on the last life, avoid steps that are likely to be fatal\n"
                     "DEATH_RISK_THRESHOLD = 0.3       # last life: refuse a cell whose P(volcano or water) is at least this\n"
                     "DEATH_SCAN_BAND = (0.05, 0.95)   # last life: scan whenever risk is inside this wider band\n"
                     "DEATH_MAX_AVOID = 2              # last life: after refusing this many cells, stop detouring\n", n)
    print("stage 1 (death-aware guard): applied")
else:
    print("stage 1 (death-aware guard): already present, skipped")

# ------------------------------------------------ stage 2: probing + livelock fix
if "PROBE_ALTERNATIVES" in a or "PROBE_ALTERNATIVES" in c:
    sys.exit("This upgrade is already applied. Nothing was written.")

n = "agent2.py"
a = edit(a, nl, "    avoid = set()      # cells refused on the last life\n",
                "    avoid = set()      # cells refused on the last life\n"
                "    visited = {config2.START_POS}   # cells the agent has stood on\n", n)
a = edit(a, nl, "    while (curS.row, curS.col) !=config2.GOAL_POS:\n",
                "    while (curS.row, curS.col) !=config2.GOAL_POS:\n"
                "        if curS.turns > config2.MAX_TURNS:      # safety net: never loop forever\n"
                '            print("Turn limit reached.")\n'
                "            return fullpath, snaps\n", n)
a = edit(a, nl, "        if avoid and (nextS is None or len(avoid) > config2.DEATH_MAX_AVOID):\n",
                "        if avoid and (nextS is None or len(avoid) > config2.DEATH_MAX_AVOID\n"
                "                      or (nextS.row, nextS.col) in visited):   # a detour must not step back\n", n)
a = edit(a, nl, "        collapse(r, c, true_cell, belief_grid)\n",
                "        collapse(r, c, true_cell, belief_grid)\n"
                "        visited.add((r, c))\n", n)
a = edit(a, nl, "        last_life = config2.DEATH_AWARE and curS.lives <= config2.HAZARD_LIFE_COST\n",
"""        if config2.PROBE_ALTERNATIVES and risk >= config2.PROBE_RISK:
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
""", n)
n = "config2.py"
c = edit(c, nlc, "DEATH_MAX_AVOID = 2              # last life: after refusing this many cells, stop detouring\n",
"""DEATH_MAX_AVOID = 2              # last life: after refusing this many cells, stop detouring

# ---------- PROBING ALTERNATIVES ----------
PROBE_ALTERNATIVES = True        # before a likely-hazard step, scan other cells that might be safe land
PROBE_RISK = 0.7                 # "likely hazard" = P(volcano or water) at least this
PROBE_MAX_SCANS = 2              # at most this many probe scans per alternative cell
MAX_TURNS = 400                  # safety net: stop the run if it ever exceeds this many turns
""", n)
print("stage 2 (probing + livelock fix + turn limit): applied")

open(agent_path, "w", newline="").write(a)
open(config_path, "w", newline="").write(c)
print("Done: agent2.py and config2.py updated.")