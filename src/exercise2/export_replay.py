"""Run the Exercise 2 agent on one or more seeds and save each run as JSON.

usage (from src/exercise2):  python export_replay.py 42            -> replays/seed_42.json
                             python export_replay.py 1 30          -> seeds 1..30 + replays/index.json
"""
import contextlib
import io
import json
import os
import random
import sys

import config2
import grid_gen2
from agent2 import runagent

OUT_DIR = "replays"


def run_seed(seed):
    config2.RANDOM_SEED = seed
    random.seed(seed)
    grid, gpath, a1, a2 = grid_gen2.gengrid()
    bel = grid_gen2.belief_grid(config2.M, config2.N)
    scan = grid_gen2.scan_infor(config2.M, config2.N)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        path, snaps = runagent(grid, bel, scan)
    msg = buf.getvalue().strip().splitlines()[-1] if buf.getvalue().strip() else ""
    outcome = "goal" if msg == "Goal Reached" else ("died" if "died" in msg else "stopped")

    steps, time_, turns = [], 0, 0
    for i, (r, c, action, lives) in enumerate(path):
        if i > 0:
            time_ += {"walk": config2.WALK_TIME_COST, "jump": config2.JUMP_TIME_COST}.get(action, 0)
            turns += config2.SCAN_TURN_COST if action == "scan" else config2.TURN_COST
        bel_i, scan_i = snaps[i]
        steps.append({
            "r": r, "c": c, "action": action, "lives": round(lives, 3),
            "time": time_, "turns": turns,
            # per cell: [V, W, L, B] probabilities
            "belief": [[[round(bel_i[y][x][k], 3) for k in "VWLB"] for x in range(config2.N)]
                       for y in range(config2.M)],
            # per cell: null if never scanned, else [T, S] of the latest scan
            "scan": [[[int(bool(scan_i[y][x]["T"])), int(bool(scan_i[y][x]["S"]))]
                      if scan_i[y][x]["scanned"] else None for x in range(config2.N)]
                     for y in range(config2.M)],
        })
    return {
        "seed": seed, "outcome": outcome,
        "meta": {"M": config2.M, "N": config2.N, "start": list(config2.START_POS),
                 "goal": list(config2.GOAL_POS), "initial_lives": config2.INITIAL_LIVES},
        "grid": grid, "steps": steps,
    }


def main():
    args = [int(a) for a in sys.argv[1:]]
    if not args:
        sys.exit(__doc__)
    seeds = range(args[0], args[-1] + 1)
    os.makedirs(OUT_DIR, exist_ok=True)
    index = []
    for s in seeds:
        data = run_seed(s)
        with open(os.path.join(OUT_DIR, f"seed_{s}.json"), "w") as f:
            json.dump(data, f, separators=(",", ":"))
        index.append({"seed": s, "outcome": data["outcome"], "steps": len(data["steps"]),
                      "lives": data["steps"][-1]["lives"]})
        print(s, data["outcome"], len(data["steps"]))
    with open(os.path.join(OUT_DIR, "index.json"), "w") as f:
        json.dump(index, f)


if __name__ == "__main__":
    main()
