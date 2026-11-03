import config2, grid_gen2, random

bad = 0
for seed in range(1, 501):
    config2.RANDOM_SEED = seed
    g, path, a1, a2 = grid_gen2.gengrid()
    contiguous = all(abs(path[i][0]-path[i+1][0]) + abs(path[i][1]-path[i+1][1]) == 1
                     for i in range(len(path) - 1))
    hz = sorted(g[r][c] for r, c in path if g[r][c] in "VW")
    if not contiguous or hz != ["V", "V", "W", "W"]:
        bad += 1
print("bad paths:", bad, "(want 0)")

b = grid_gen2.belief_grid(2, 2)
b[0][0]["V"] = 0.99
print("cells independent:", b[1][1]["V"] != 0.99)