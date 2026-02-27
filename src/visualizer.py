import matplotlib.pyplot as plt
import matplotlib.patches as patches
import arrow
import numpy as np
import pandas as pd
import random
from config import HAZ_TYPES
from config import TEXT_COLORS

haz_types=HAZ_TYPES

def drawG(grid, agentp=None, turns=None, time=None, lives=None, path=None):
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
        
    if path:
        drawP(ax, path, M)  
        
    if lives is not None:
        score=(time+turns)/lives if lives>0 else float('inf')
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

