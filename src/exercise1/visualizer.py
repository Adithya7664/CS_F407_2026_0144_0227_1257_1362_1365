import matplotlib.pyplot as plt
import matplotlib.patches as patches
import arrow
import numpy as np
import pandas as pd
import random
from config import HAZ_TYPES
from config import TEXT_COLORS
from config import CELL_COLORS
from matplotlib.patches import FancyArrowPatch

haz_types=HAZ_TYPES

def drawG(grid, agent_pos=None, turns=None, time=None, lives=None, path=None, save_path=None):
    
    M = len(grid)
    N = len(grid[0])

    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    for r in range(M):
        for c in range(N):
            cell = grid[r][c]

            rect = patches.Rectangle(
                (c, M - r - 1),
                1, 1,
                linewidth=1,
                edgecolor='black',
                facecolor=CELL_COLORS[cell]
            )
            ax.add_patch(rect)

            ax.text(
                c + 0.5,
                M - r - 0.5,
                cell,
                ha="center",
                va="center",
                fontsize=12,
                color=TEXT_COLORS[cell]
            )

    if agent_pos:
        r, c = agent_pos
        ax.text(
            c + 0.5,
            M - r - 0.5,
            "A",
            ha="center",
            va="center",
            fontsize=14,
            weight="bold"
        )

    if path:
        drawP(ax, path, M)

    if lives is not None:
        score = (time + turns) / lives if lives > 0 else float('inf')
        plt.title(
            f"Lives: {lives} | Time: {time} | Turns: {turns} | Score: {score:.2f}",
            fontsize=14
        )

    ax.set_xlim(0, N)
    ax.set_ylim(0, M)
    ax.set_aspect('equal')
    ax.axis('off')

    if save_path is not None:
        plt.savefig(save_path)
        plt.close(fig)
    else:
        plt.show()
    
def drawP(ax, path, M):
    
    for i in range(len(path) - 1):

        r1, c1 = path[i][0], path[i][1]
        r2, c2 = path[i+1][0], path[i+1][1]

        start_x = c1 + 0.5
        start_y = M - r1 - 0.5

        end_x = c2 + 0.5
        end_y = M - r2 - 0.5

        dx = end_x - start_x
        dy = end_y - start_y

        is_jump = abs(r2 - r1) == 2 or abs(c2 - c1) == 2

        life1 = path[i][3] if len(path[i]) > 3 else None
        life2 = path[i+1][3] if len(path[i+1]) > 3 else None

        color = 'black'
        linestyle = '-'

        if is_jump:
            color = 'purple'

        if life1 is not None and life2 is not None:
            if life2 < life1:
                color = 'red'
                linestyle = '--'

        if is_jump:
            arrow = FancyArrowPatch(
                (start_x, start_y),
                (end_x, end_y),
                connectionstyle="arc3,rad=0.3",
                arrowstyle='->',
                color=color,
                linewidth=2,
                linestyle=linestyle
            )
            ax.add_patch(arrow)
        else:
            ax.arrow(
                start_x,
                start_y,
                dx,
                dy,
                head_width=0.2,
                length_includes_head=True,
                color=color,
                linestyle=linestyle
            )

