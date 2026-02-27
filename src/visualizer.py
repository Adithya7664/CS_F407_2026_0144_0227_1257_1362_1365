import matplotlib.pyplot as plt
import matplotlib.patches as patches
import arrow
import numpy as np
import pandas as pd
import random
from config import HAZ_TYPES
from config import TEXT_COLORS

haz_types=HAZ_TYPES

def drawG(grid, agent_pos=None, turns=None, time=None, lives=None, path=None):
    
    M = len(grid)
    N = len(grid[0])

    fig, ax = plt.subplots(figsize=(N, M))

    for r in range(M):
        for c in range(N):
            cell = grid[r][c]

            rect = patches.Rectangle(
                (c, M - r - 1),
                1, 1,
                linewidth=1,
                edgecolor='black',
            )
            ax.add_patch(rect)

            ax.text(
                c + 0.5,
                M - r - 0.5,
                cell,
                ha="center",
                va="center",
                fontsize=12
            )

    if agent_pos:
        r, c = agent_pos
        ax.text(
            c + 0.5,
            M - r - 0.5,
            "A",
            ha="center",
            va="center",
            fontsize=13,
            weight="bold"
        )

    if path:
        drawP(ax, path, M)

    if lives is not None:
        score = (time + turns) / lives if lives > 0 else float('inf')
        plt.title(f"Lives: {lives} | Time: {time} | Turns: {turns} | Score: {score}")

    ax.set_xlim(0, N)
    ax.set_ylim(0, M)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.show()
    
def drawP(ax, path, M):
    for i in range(len(path)-1):
        x1, y1=path[i]
        x2, y2=path[i+1]
        x=x2-x1
        y=y1-y2
        ifjump=x==2 or y==2
        color='black'
        linestyle='-'
        if ifjump:
            color='purple'
        if hasattr(path[i+1], 'damage') and path[i+1].damage:
            color='red'
            linestyle='--'
            
        ax.arrow(y1+0.5, M-x1-0.5, x, y, head_width=0.15, length_includes_head=True, fc=color, ec=color, linestyle=linestyle)

