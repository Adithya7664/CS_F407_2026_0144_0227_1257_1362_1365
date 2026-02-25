import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import random

haz_types=['L', 'V', 'B', 'W']
TEXT_COLORS=['black', 'red', 'grey', 'blue']

def drawG(grid, agentp, title, path):
    M=len(grid)
    N=len(grid[0])
    cell_size=0.7
    line_w=0.9
    fig, ax=plt.subplots(figsize=(M*cell_size, N*cell_size))

    for X in range(N):
        for Y in range(M):
            cell=grid[X][Y]
            pat=patches.Rectangle(Y, cell_size, cell_size, line_w)
            ax.add_patch(pat)
            ax.text(Y+0.5, M-X-0.5, cell, ha="center", va="center", fontsize=12, color=TEXT_COLORS[cell])
    if agentp:
        r, c=agentp
        ax.text(c+0.5, M-r-0.5, "A", ha="center", va="center", fontsize=13, color="black", weight="bold")
            
            
    ax.set_xlim(0, N)
    ax.set_ylim(0, M)
    ax.set_aspect('equal')
    ax.axis('off')
    if title:
        plt.title(title)
        
    if path:
        plt.savefig(path, bbox_inches='tight')
    plt.show()