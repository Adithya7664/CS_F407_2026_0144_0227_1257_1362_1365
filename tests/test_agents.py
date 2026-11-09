"""Sanity tests for both exercises.  Run from the repo root:  python -m unittest discover -s tests -v"""
import contextlib
import io
import os
import random
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src", "exercise1"))
sys.path.insert(0, os.path.join(ROOT, "src", "exercise2"))
sys.dont_write_bytecode = True

import agent          # noqa: E402  (exercise 1)
import agent2         # noqa: E402  (exercise 2)
import config         # noqa: E402
import config2        # noqa: E402
import grid_gen       # noqa: E402
import grid_gen2      # noqa: E402

SEEDS = range(1, 16)


def make_ex1(seed):
    random.seed(seed)
    return grid_gen.gengrid()


def make_ex2(seed):
    random.seed(seed)
    return grid_gen2.gengrid()


def run_ex2(seed):
    config2.RANDOM_SEED = seed
    grid, *_ = make_ex2(seed)
    bel = grid_gen2.belief_grid(config2.M, config2.N)
    scan = grid_gen2.scan_infor(config2.M, config2.N)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        path, _ = agent2.runagent(grid, bel, scan)
    return grid, path, out.getvalue()


class TestGenerators(unittest.TestCase):
    def check_path(self, path, start, goal):
        self.assertEqual(tuple(path[0]), tuple(start))
        self.assertEqual(tuple(path[-1]), tuple(goal))
        for (r1, c1), (r2, c2) in zip(path, path[1:]):
            self.assertEqual(abs(r1 - r2) + abs(c1 - c2), 1, f"gap between {(r1, c1)} and {(r2, c2)}")
        self.assertEqual(len(set(map(tuple, path))), len(path), "path revisits a cell")

    def test_exercise1_ground_truth_path_is_connected(self):
        for s in range(1, 41):
            _, path, _, _ = make_ex1(s)
            self.check_path(path, config.START_POS, config.GOAL_POS)

    def test_exercise2_ground_truth_path_is_connected(self):
        for s in range(1, 41):
            _, path, _, _ = make_ex2(s)
            self.check_path(path, config2.START_POS, config2.GOAL_POS)


class TestExercise1(unittest.TestCase):
    def test_optimal_path_respects_walls(self):
        for s in SEEDS:
            grid, *_ = make_ex1(s)
            path = agent.search(grid)
            self.assertIsNotNone(path, f"seed {s}: no path")
            self.assertEqual((path[-1][0], path[-1][1]), tuple(config.GOAL_POS))
            self.assertGreater(path[-1][3], 0)
            for (pr, pc, *_), (r, c, action, _) in zip(path, path[1:]):
                self.assertNotEqual(grid[r][c], "B", f"seed {s}: stepped on a wall")
                if action == "jump":
                    self.assertNotEqual(grid[(pr + r) // 2][(pc + c) // 2], "B", f"seed {s}: jumped over a wall")


class TestBayes(unittest.TestCase):
    def test_posterior_is_a_distribution(self):
        prior = {"V": 0.24, "W": 0.24, "L": 0.16, "B": 0.36}
        for T in (True, False):
            for S in (True, False):
                post = agent2.updatebelf(prior, T, S)
                self.assertAlmostEqual(sum(post.values()), 1.0)
                self.assertTrue(all(v >= 0 for v in post.values()))

    def test_readings_move_belief_the_right_way(self):
        prior = {"V": 0.25, "W": 0.25, "L": 0.25, "B": 0.25}
        self.assertEqual(max(agent2.updatebelf(prior, True, False).items(), key=lambda kv: kv[1])[0], "V")
        self.assertEqual(max(agent2.updatebelf(prior, False, True).items(), key=lambda kv: kv[1])[0], "W")

    def test_collapse_sets_certainty(self):
        bel = grid_gen2.belief_grid(config2.M, config2.N)
        agent2.collapse(2, 3, "W", bel)
        self.assertEqual(bel[2][3], {"L": 0, "V": 0, "W": 1, "B": 0})


class TestExercise2Agent(unittest.TestCase):
    def test_moves_obey_the_rules(self):
        for s in SEEDS:
            grid, path, _ = run_ex2(s)
            self.assertLess(len(path), config2.MAX_TURNS, f"seed {s}: run did not terminate")
            for (pr, pc, *_), (r, c, action, _) in zip(path, path[1:]):
                if action in ("scan", "bump"):
                    self.assertEqual((pr, pc), (r, c), f"seed {s}: {action} moved the agent")
                if action == "walk":
                    self.assertEqual(abs(pr - r) + abs(pc - c), 1)
                    self.assertNotEqual(grid[r][c], "B", f"seed {s}: walked into a wall")
                if action == "jump":
                    self.assertEqual(abs(pr - r) + abs(pc - c), 2)
                    self.assertNotEqual(grid[r][c], "B", f"seed {s}: jumped onto a wall")
                    self.assertNotEqual(grid[(pr + r) // 2][(pc + c) // 2], "B", f"seed {s}: jumped over a wall")

    def test_runs_are_reproducible(self):
        a = run_ex2(3)[1]
        b = run_ex2(3)[1]
        self.assertEqual(a, b)

    def test_agent_usually_reaches_the_goal(self):
        reached = sum(1 for s in SEEDS if "Goal Reached" in run_ex2(s)[2])
        self.assertGreaterEqual(reached, int(0.8 * len(SEEDS)), f"only {reached}/{len(SEEDS)} runs reached the goal")


if __name__ == "__main__":
    unittest.main()
