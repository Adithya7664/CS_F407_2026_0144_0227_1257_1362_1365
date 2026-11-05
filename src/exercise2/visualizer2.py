import matplotlib.pyplot as plt
import config2
import matplotlib.patches as patches
from config2 import *
from config2 import HAZ_TYPES
from config2 import TEXT_COLORS
from config2 import CELL_COLORS2
from matplotlib.patches import FancyArrowPatch
haz_types=HAZ_TYPES

def drawG(grid, belief_g=None, scan_info=None, agent_pos=None, turns=None, time=None, lives=None, path=None, save_path=None):
    
    M = len(grid)
    N = len(grid[0])

    fig, (ax_bel, ax_gr) = plt.subplots(1, 2, figsize=(20, 9.5))
    fig.patch.set_facecolor('white')

    drawGrT(ax_gr, grid, M, N)
    drawBelG(ax_bel, belief_g, scan_info, M, N)

    if path:
        drawP(ax_bel, path, M)
        drawP(ax_gr, path, M)

    if agent_pos:
        ar, ac = agent_pos
        for ax in (ax_bel, ax_gr):
            ax.add_patch(patches.Circle((ac + 0.5, M - ar - 0.5), 0.22, facecolor='gold',
                                        edgecolor='black', linewidth=1.5, zorder=20))
            ax.text(ac + 0.5, M - ar - 0.5, "A", ha="center", va="center",
                    fontsize=14, weight="bold", zorder=21)

    if lives is not None:
        score = (time + turns) / lives if lives > 0 else float('inf')
        fig.suptitle(f"Lives: {lives} | Time: {time} | Turns: {turns} | Score: {score:.2f}", fontsize=18)

    fig.text(0.5, 0.02, "black arrow = walk    purple curve = jump    red dashed + X = life lost    "
                        "yellow border = scanned    gold circle = agent", ha="center", fontsize=12)
    fig.tight_layout(rect=[0, 0.05, 1, 0.93])
    if save_path is not None:
        plt.savefig(save_path, dpi=110)
        plt.close(fig)
    else:
        plt.show()
    
def drawP(ax, path, M):
    for i in range(len(path) - 1):
        r1, c1 = path[i][0], path[i][1]
        r2, c2 = path[i+1][0], path[i+1][1]
        if (r1, c1) == (r2, c2):      # scans and bumps don't move the agent
            continue
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
                r2, c2 = path[i+1][0], path[i+1][1]
                ax.text(
                c2 + 0.5,
                M - r2 - 0.5,
                "X",
                ha="center",
                va="center",
                fontsize=16,
                color='red', 
                fontweight='bold', 
                zorder=10
            )
                

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


def drawGrT(ax, grid, M, N):
    ax.set_facecolor('white')
    for r in range(M):
        for c in range(N):
            cell = grid[r][c]

            rect = patches.Rectangle(
                (c, M - r - 1),
                1, 1,
                linewidth=1,
                edgecolor='black',
                facecolor=CELL_COLORS2[cell]
            )
            ax.add_patch(rect)

            ax.text(
                c + 0.5,
                M - r - 0.5,
                cell,
                ha="center",
                va="center",
                fontsize=16,
                color=TEXT_COLORS[cell]
            )
            
    ax.set_xlim(0, N)
    ax.set_ylim(0, M)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Ground Truth Map')
    
def belief_color(belief):
    if belief["B"] > 0.5:
        return config2.BELIEF_COLORS['WALL']
    if belief["V"] > config2.THRESHOLD_VOLCANO:
        return config2.BELIEF_COLORS['V']
    if belief["W"] > config2.THRESHOLD_WATER:
        return config2.BELIEF_COLORS['W']
    if belief["L"] > config2.THRESHOLD_LAND:
        return config2.BELIEF_COLORS['L']
    return config2.BELIEF_COLORS['UNKNOWN']
    
def drawBelG(ax, bel_grid, scan_info, M, N):
    ax.set_facecolor('white')
    for r in range(M):
        for c in range(N):
            belief=bel_grid[r][c]
            risk=belief["V"]+belief["W"]
            rect = patches.Rectangle(
                (c, M - r - 1),
                1, 1,
                linewidth=1,
                edgecolor='black',
                facecolor=belief_color(belief=belief)
            )
            ax.add_patch(rect)
            ax.text(
                c + 0.5,
                M - r - 0.5,
                f"B {round(belief['B']*100)}%\n⚠{round(risk*100)}%" if belief["B"] > 0.5 else f"{round(risk*100)}%",
                ha="center",
                va="center",
                fontsize=14, weight="bold",
            )
            if scan_info[r][c]["scanned"]:
                highlight = patches.Rectangle(
                    (c, M - r - 1),
                    1, 1,
                    edgecolor='yellow',
                    linewidth=2,
                    fill=False
                )
                ax.add_patch(highlight)
                ax.text(
                    c + 0.5,
                    M - r - 0.15,
                    f"T:{1 if scan_info[r][c]['T'] else 0}",
                    fontsize=11,
                    ha="center", 
                    va="top"
                )
                ax.text(
                    c + 0.5,
                    M - r - 0.85,
                    f"S:{1 if scan_info[r][c]['S'] else 0}",
                    fontsize=11,
                    ha="center", 
                    va="bottom"
                )
    ax.set_xlim(0, N)
    ax.set_ylim(0, M)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Agent's belief map")