import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

M=8
N=10
cell_size=0.7
line_w=0.9
haz_types=['L', 'V', 'B', 'W']
colors=['black', 'red', 'grey', 'blue']
fig, ax=plt.subplots(figsize=(M*cell_size, N*cell_size))

for x in range(N):
    ax.plot([x, x], [0, M], color='black', linewidth=line_w)
for y in range(M+1):
    ax.plot([0, N], [y, y], color='black', linewidth=line_w)

for row in range(M):
    for col in range(N):
        ind = random.randint(0, 3)
        ax.text(
            col + 0.5,
            M - row - 0.5,
            haz_types[ind],
            ha="center",
            va="center",
            color=colors[ind],
            fontsize=20
        )
        
ax.set_xlim(0, N)
ax.set_ylim(0, M)
ax.set_aspect('equal')
ax.axis('off')

plt.show()