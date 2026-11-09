"""Entry point used by the browser's live mode (Pyodide). Also handy from a normal shell:
    python -c "import live; print(live.run_live(7)[:80])"
"""
import json

import config2
from export_replay import run_seed


def run_live(seed, rows=8, cols=10, probing=True, last_life=True):
    rows = max(8, min(10, int(rows)))
    cols = max(8, min(10, int(cols)))
    config2.M, config2.N = rows, cols
    config2.GOAL_POS = (rows - 1, cols - 1)
    config2.PROBE_ALTERNATIVES = bool(probing)
    config2.DEATH_AWARE = bool(last_life)
    return json.dumps(run_seed(int(seed)), separators=(",", ":"))
